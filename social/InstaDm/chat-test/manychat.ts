import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import type { IncomingHttpHeaders } from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";
import type { Block } from "./server.ts";

type Config = { plan: Block[]; tone: string; instructions: string };
type Message = { role: "user" | "assistant"; content: string };
type Collected = Record<string, string>;
type StoredMessage = Message & { at: string; step?: number | null };
type Conversation = { startedAt: string; completedAt?: string; messages: StoredMessage[]; collected: Collected };
type Grower = { username: string; firstName?: string; lastName?: string; conversations: Conversation[] };
type LegacyConversation = { messages: Message[]; collected: Collected };
type LinkButton = { caption: string; url: string };
type Turn = { replies: string[]; quickReplies: string[]; linkButtons: LinkButton[]; step: number | null; collected: Collected };
export type RunChat = (config: Config, messages: Message[], collected: Collected) => Promise<Turn>;
type Inbound = { contact_id?: string | number; ig_username?: string; name?: string; text?: string; trigger?: string };

const QUICK_REPLY_FLOW = "content20261125165345_480225";
const OPENING = "(The farmer just commented PROFIT.)";
const LEGACY_OPENING = "(The farmer just commented PROFIT. Start at the first step and send only that step's messages.)";
const FOLLOW_UP_WINDOW = 24 * 60 * 60 * 1000;
const here = path.dirname(fileURLToPath(import.meta.url));
const dataDirectory = path.join(here, "data");
const configFile = path.join(dataDirectory, "config.json");
const conversationsFile = path.join(dataDirectory, "conversations.json");
const latestRun = new Map<string, number>();

function readJson<T>(file: string, fallback: T): T {
  return existsSync(file) ? JSON.parse(readFileSync(file, "utf8")) : fallback;
}

function writeJson(file: string, value: unknown) {
  mkdirSync(dataDirectory, { recursive: true });
  writeFileSync(file, JSON.stringify(value, null, 2));
}

export function loadConfig() {
  return readJson<Config | null>(configFile, null);
}

export function saveConfig(config: Config) {
  writeJson(configFile, config);
}

function loadGrowers() {
  const stored = readJson<Record<string, Grower | LegacyConversation>>(conversationsFile, {});
  return Object.fromEntries(
    Object.entries(stored).map(([contactId, entry]) => [
      contactId,
      "conversations" in entry
        ? entry
        : { username: "", conversations: [{ startedAt: "", messages: entry.messages.map((message) => ({ ...message, at: "" })), collected: entry.collected }] },
    ]),
  ) as Record<string, Grower>;
}

async function fetchProfile(contactId: string) {
  const baseUrl = process.env.MANYCHAT_API_URL ?? "https://api.manychat.com";
  const response = await fetch(`${baseUrl}/fb/subscriber/getInfo?subscriber_id=${contactId}`, {
    headers: { Authorization: `Bearer ${process.env.MANYCHAT_API_KEY}` },
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const { data } = await response.json();
  return { firstName: data.first_name ?? "", lastName: data.last_name ?? "", username: data.ig_username ?? "" };
}

// Visible part: from the PROFIT comment until 24 hours after the turn that completed the plan.
export async function listConversations() {
  const growers = loadGrowers();
  const missing = Object.entries(growers).filter(([, grower]) => grower.firstName === undefined);
  for (const [contactId, grower] of missing) {
    try {
      const profile = await fetchProfile(contactId);
      Object.assign(grower, { firstName: profile.firstName, lastName: profile.lastName, username: grower.username || profile.username });
    } catch (error) {
      console.error(`profile ${contactId}: ${error instanceof Error ? error.message : error}`);
    }
  }
  if (missing.length) {
    const latest = loadGrowers();
    for (const [contactId, grower] of missing) if (latest[contactId]) Object.assign(latest[contactId], { firstName: grower.firstName, lastName: grower.lastName, username: grower.username });
    writeJson(conversationsFile, latest);
  }
  return Object.entries(growers)
    .map(([contactId, grower]) => {
      const conversations = grower.conversations
        .map((conversation) => {
          const endIndex = conversation.messages.findIndex((message) => message.role === "assistant" && message.step === 0);
          const completedAt = conversation.messages[endIndex]?.at;
          const cutoff = completedAt ? new Date(Date.parse(completedAt) + FOLLOW_UP_WINDOW).toISOString() : "";
          const visible =
            endIndex === -1
              ? conversation.messages
              : conversation.messages.filter((message, index) => index <= endIndex || (cutoff && message.at <= cutoff));
          return {
            startedAt: conversation.startedAt,
            completedAt,
            status: endIndex === -1 ? "in progress" : "completed",
            collected: conversation.collected,
            messages: visible.map((message) =>
              message.role === "user" && (message.content === OPENING || message.content === LEGACY_OPENING)
                ? { role: "profit", content: "", at: message.at }
                : { role: message.role, content: message.content, at: message.at },
            ),
          };
        })
        .reverse();
      const lastActivity = conversations.flatMap((conversation) => conversation.messages.map((message) => message.at)).sort().at(-1) ?? "";
      return { contactId, username: grower.username, firstName: grower.firstName ?? "", lastName: grower.lastName ?? "", lastActivity, conversations };
    })
    .sort((first, second) => second.lastActivity.localeCompare(first.lastActivity));
}

export function isAuthorized(headers: IncomingHttpHeaders) {
  const secret = process.env.MANYCHAT_REQUEST_SECRET;
  return Boolean(secret) && headers["x-orisha-secret"] === secret;
}

function delayBefore(previousMessage: string) {
  return Math.min(4000, Math.max(1200, 800 + 40 * previousMessage.length));
}

function buildContent(texts: string[], quickReplies: string[], linkButtons: LinkButton[]) {
  return {
    messages: texts.map((text) => ({ type: "text", text, buttons: linkButtons.map((button) => ({ type: "url", ...button })) })),
    actions: [],
    // The flow's External Request forwards the tapped caption to /ig-inbound.
    quick_replies: quickReplies.map((caption) => ({ type: "flow", caption, target: QUICK_REPLY_FLOW })),
  };
}

async function sendMessage(contactId: string, text: string, quickReplies: string[], linkButtons: LinkButton[]) {
  const baseUrl = process.env.MANYCHAT_API_URL ?? "https://api.manychat.com";
  const content = { type: "instagram", ...buildContent([text], quickReplies, linkButtons) };
  const response = await fetch(`${baseUrl}/fb/sending/sendContent`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${process.env.MANYCHAT_API_KEY}` },
    body: JSON.stringify({ subscriber_id: Number(contactId), data: { version: "v2", content } }),
  });
  if (response.ok) return;
  const body = await response.text();
  let reason = body;
  try {
    const parsed = JSON.parse(body);
    reason = `${parsed.message}${parsed.code ? ` (code ${parsed.code})` : ""}${parsed.details ? ` ${JSON.stringify(parsed.details)}` : ""}`;
  } catch {}
  throw new Error(`HTTP ${response.status}: ${reason}`);
}

function logTurn(username: string, text: string, before: Collected, turn: Turn, config: Config, quickReplies: string[], status: string) {
  const captured = Object.entries(turn.collected).filter(([field, value]) => before[field] !== value);
  const step = turn.step ? `${turn.step} (${config.plan[turn.step - 1]?.title})` : "complete";
  console.log(
    [
      `ig-turn @${username}`,
      `  in: ${text}`,
      `  captured: ${captured.map(([field, value]) => `${field} = ${value}`).join("; ") || "nothing new"}`,
      `  all captured: ${JSON.stringify(turn.collected)}`,
      `  step: ${step}`,
      ...turn.replies.map((reply, index) => `  out ${index + 1}: ${reply}`),
      `  quick replies: ${quickReplies.join(" | ") || "none"}`,
      `  manychat: ${status}`,
    ].join("\n"),
  );
}

// profit_comment arrives after the farmer taps the comment reply's button, so the DM window is open.
export async function receiveInbound(inbound: Inbound, runChat: RunChat) {
  if (inbound.contact_id === undefined) return console.log("ig-inbound: no contact_id");
  const contactId = String(inbound.contact_id);
  const username = (inbound.ig_username ?? "").replace(/^@/, "").toLowerCase();
  const allowed = (process.env.ALLOWED_USERNAMES ?? "").split(",").map((handle) => handle.trim().replace(/^@/, "").toLowerCase());
  if (!username || !allowed.includes(username)) return console.log(`ig-inbound: blocked ${contactId} @${username}`);
  const config = readJson<Config | null>(configFile, null);
  if (!config) return console.log("ig-inbound: no plan saved yet, press 'Use for ManyChat' in the app");

  const run = (latestRun.get(contactId) ?? 0) + 1;
  latestRun.set(contactId, run);
  const growers = loadGrowers();
  const opening = inbound.trigger === "profit_comment";
  const text = opening ? OPENING : inbound.text?.trim();
  if (!text) return;
  if (!opening && !growers[contactId]) return console.log(`ig-inbound: ignored ${contactId}, no conversation`);
  const now = new Date().toISOString();
  const grower = growers[contactId] ?? { username, conversations: [] };
  grower.username = username;
  if (opening) grower.conversations.push({ startedAt: now, messages: [], collected: {} });
  const conversation = grower.conversations[grower.conversations.length - 1];
  conversation.messages.push({ role: "user", content: text, at: now });
  growers[contactId] = grower;
  writeJson(conversationsFile, growers);

  const before = { ...conversation.collected };
  let turn: Turn;
  try {
    const messages = conversation.messages.map(({ role, content }) => ({ role, content }));
    turn = await runChat(config, messages, conversation.collected);
  } catch (error) {
    return console.error(`ig-inbound: @${username} Claude failed: ${error instanceof Error ? error.message : error}`);
  }
  if (latestRun.get(contactId) !== run) return;
  const latest = loadGrowers();
  const answeredAt = new Date().toISOString();
  const latestConversations = latest[contactId]?.conversations ?? grower.conversations;
  latestConversations[latestConversations.length - 1] = {
    ...conversation,
    completedAt: conversation.completedAt ?? (turn.step === 0 ? answeredAt : undefined),
    messages: [...conversation.messages, { role: "assistant", content: turn.replies.join("\n\n"), at: answeredAt, step: turn.step }],
    collected: turn.collected,
  };
  latest[contactId] = { username, conversations: latestConversations };
  writeJson(conversationsFile, latest);

  const quickReplies = turn.quickReplies;
  let sent = 0;
  let status = "";
  try {
    for (const [index, reply] of turn.replies.entries()) {
      if (index > 0) await new Promise((resolve) => setTimeout(resolve, delayBefore(turn.replies[index - 1])));
      if (latestRun.get(contactId) !== run) {
        status = `CANCELLED by a newer message, ${sent} sent`;
        break;
      }
      const isLast = index === turn.replies.length - 1;
      await sendMessage(contactId, reply, isLast ? quickReplies : [], isLast ? turn.linkButtons : []);
      sent++;
    }
    status ||= `SUCCEEDED, ${sent} sent`;
  } catch (error) {
    status = `FAILED after ${sent} sent: ${error instanceof Error ? error.message : error}`;
  }
  logTurn(username, text, before, turn, config, quickReplies, status);
  return status;
}
