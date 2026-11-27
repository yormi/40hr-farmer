import Anthropic from "@anthropic-ai/sdk";
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { createServer } from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { z } from "zod";
import { isAuthorized, listConversations, loadConfig, receiveInbound, saveConfig } from "./manychat.ts";

const PORT = 8791;
const CHAT_MODEL = "claude-sonnet-5-5";
const TITLE_MODEL = "claude-haiku-5-5";
const here = path.dirname(fileURLToPath(import.meta.url));
const secretsFile = path.resolve(here, "../../../.secrets/anthropic.env");
const pageSource = readFileSync(path.join(here, "index.html"), "utf8");
const version = createHash("sha256").update(pageSource).update(String(Date.now())).digest("hex").slice(0, 12);
const page = pageSource.replace("__APP_VERSION__", version);

export type Block = {
  id: string;
  type: "step" | "condition";
  title: string;
  prompt: string;
  info: string[];
  quickReplies?: string[];
  linkButtons?: { caption: string; url: string }[];
  next: { target: string; condition: string }[];
};

const TurnSchema = z.object({
  replies: z.array(z.string()).describe("Messages sent one after another this turn"),
  quickReplies: z
    .array(z.string())
    .describe("Quick reply buttons under the last message, 20 characters max each. The step's default quick replies unless its instructions say otherwise. Empty for none"),
  linkButtons: z
    .array(z.object({ caption: z.string(), url: z.string() }))
    .describe("Buttons under the last message that open a URL, 3 max, 20 characters max per caption. The step's default link buttons unless its instructions say otherwise. Empty for none"),
  step: z.number().int().describe("Number of the plan step this turn's messages belong to, 0 when the plan is complete"),
  collected: z
    .array(z.object({ field: z.string(), value: z.string() }))
    .describe("Info learned or corrected this turn, using the labels exactly"),
});

if (existsSync(secretsFile)) process.loadEnvFile(secretsFile);
const manychatSecretsFile = path.resolve(here, "../../../.secrets/manychat.env");
if (existsSync(manychatSecretsFile)) process.loadEnvFile(manychatSecretsFile);
const client = new Anthropic();

function buildSystemPrompt(plan: Block[], collected: Record<string, string>, tone: string, instructions: string, startId?: string) {
  const stepNumber = (id: string) => plan.findIndex((block) => block.id === id) + 1;
  const start =
    plan.find((block) => block.id === startId) ??
    plan.find((block) => !plan.some((other) => other.next.some((edge) => edge.target === block.id))) ??
    plan[0];
  const steps = plan
    .map((block, index) => {
      if (block.type === "condition") {
        const branches = block.next
          .map((edge) => `  - when ${edge.condition || "otherwise"}: Step ${stepNumber(edge.target)}`)
          .join("\n");
        return `Step ${index + 1} (condition): ${block.title}\nPrecisions: ${block.prompt}\nBranches:\n${branches}\nSend no message for this step. Pick the branch that fits and continue with that step.`;
      }
      const info = block.info
        .map((label) => `  - ${label}: ${collected[label] ?? "not yet"}`)
        .join("\n");
      const quickReplies = block.quickReplies?.length
        ? `\nDefault quick replies: ${block.quickReplies.join(" | ")}`
        : "";
      const linkButtons = block.linkButtons?.length
        ? `\nDefault link buttons: ${block.linkButtons.map((button) => `${button.caption} (${button.url})`).join(" | ")}`
        : "";
      const leadsTo = block.next.length ? `Step ${stepNumber(block.next[0].target)}` : "end of the plan";
      return `Step ${index + 1}: ${block.title}\nInstructions: ${block.prompt}\nInfo to get:\n${info}${quickReplies}${linkButtons}\nLeads to: ${leadsTo}`;
    })
    .join("\n\n");
  const collectedLines = Object.entries(collected).map(([label, value]) => `- ${label}: ${value}`).join("\n");
  const collectedSection = collectedLines ? `Info collected so far, use it in computations:\n${collectedLines}\n\n` : "";
  const instructionsSection = instructions.trim() ? `Instructions:\n${instructions}\n\n` : "";
  return `${instructionsSection}Conversation plan, as a graph. Start at Step ${start ? stepNumber(start.id) : 1}.

${steps}

${collectedSection}When a step is done, continue in the same turn with the next step's messages. No filler like "Let's keep going".

Tone:
${tone}`;
}

async function chat(plan: Block[], messages: Anthropic.MessageParam[], collected: Record<string, string>, tone: string, instructions: string, startId?: string) {
  const response = await client.beta.messages.parse({
    model: CHAT_MODEL,
    max_tokens: 16000,
    system: buildSystemPrompt(plan, collected, tone, instructions, startId),
    messages,
    output_config: { effort: "low", format: zodOutputFormat(TurnSchema) },
    betas: ["server-side-fallback-2026-07-01"],
    fallbacks: "default",
  });
  if (response.stop_reason === "refusal") {
    return { replies: ["Sorry, I can't help with that one."], quickReplies: [], linkButtons: [], step: null, collected };
  }
  if (!response.parsed_output) throw new Error("Could not read Claude's answer");
  const learned = Object.fromEntries(response.parsed_output.collected.map((entry) => [entry.field, entry.value]));
  const quickReplies = response.parsed_output.quickReplies.map((caption) => caption.trim()).filter((caption) => caption && caption.length <= 20);
  const linkButtons = response.parsed_output.linkButtons
    .filter((button) => button.caption.trim() && button.caption.trim().length <= 20 && /^https?:\/\//.test(button.url))
    .slice(0, 3);
  return { replies: response.parsed_output.replies, quickReplies, linkButtons, step: response.parsed_output.step, collected: { ...collected, ...learned } };
}

const DummySchema = z.object({ values: z.array(z.object({ field: z.string(), value: z.string() })) });

async function makeDummyValues(labels: string[]) {
  const response = await client.messages.parse({
    model: TITLE_MODEL,
    max_tokens: 4000,
    system: "Invent a realistic answer for each field, as a small tomato grower would type it in a chat. A few words at most, like '120k USD' or '30,000'. Use the field names exactly.",
    messages: [{ role: "user", content: JSON.stringify(labels) }],
    output_config: { format: zodOutputFormat(DummySchema) },
  });
  const entries = response.parsed_output?.values ?? [];
  return { values: Object.fromEntries(entries.map((entry) => [entry.field, entry.value])) };
}

async function makeTitle(text: string, kind: string) {
  const response = await client.messages.create({
    model: TITLE_MODEL,
    max_tokens: 1000,
    system:
      kind === "condition"
        ? "Write a title of at most 4 words naming what these branch conditions check. Reply with the title only. No quotes. No period."
        : "Write a title of at most 4 words for this instruction to a chatbot. Reply with the title only. No quotes. No period.",
    messages: [{ role: "user", content: text }],
  });
  const title = response.content.flatMap((block) => (block.type === "text" ? [block.text] : [])).join("");
  return { title: title.trim() };
}

createServer(async (request, response) => {
  const sendJson = (status: number, payload: object) => {
    response.writeHead(status, { "Content-Type": "application/json" });
    response.end(JSON.stringify(payload));
  };

  if (request.url === "/ig-inbound" && request.method === "POST") {
    if (!isAuthorized(request.headers)) return sendJson(401, { error: "Unauthorized" });
    let body = "";
    for await (const chunk of request) body += chunk;
    console.log(" "); // journald drops empty lines, not a lone space
    console.log(`ig-inbound body: ${body}`);
    let inbound;
    try {
      inbound = JSON.parse(body);
    } catch {
      return sendJson(400, { error: "Bad JSON" });
    }
    response.writeHead(200).end();
    return void receiveInbound(inbound, (config, messages, collected) =>
      chat(config.plan, messages, collected, config.tone, config.instructions),
    );
  }
  if (request.url === "/test-ig" && request.method === "POST") {
    const username = (process.env.ALLOWED_USERNAMES ?? "").split(",")[0].trim();
    console.log(" ");
    console.log(`test-ig: simulating PROFIT for @${username}`);
    const status = await receiveInbound(
      { contact_id: process.env.TEST_CONTACT_ID, ig_username: username, trigger: "profit_comment" },
      (config, messages, collected) => chat(config.plan, messages, collected, config.tone, config.instructions),
    );
    return sendJson(200, { status: status ?? "Not sent, see the server log" });
  }
  if (request.method === "GET" && request.url === "/version") return sendJson(200, { version });
  if (request.method === "GET" && request.url === "/conversations") return sendJson(200, await listConversations());
  if (request.method === "GET" && request.url === "/config") {
    const config = loadConfig();
    return config ? sendJson(200, config) : sendJson(404, { error: "No config" });
  }
  if (request.method === "GET") {
    response.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    return response.end(page);
  }

  try {
    let body = "";
    for await (const chunk of request) body += chunk;
    const data = JSON.parse(body);
    if (request.url === "/config") return sendJson(200, saveConfig(data) ?? { saved: true });
    if (request.url === "/dummy") return sendJson(200, await makeDummyValues(data.labels));
    if (request.url === "/title") return sendJson(200, await makeTitle(data.text ?? data.prompt, data.kind));
    sendJson(200, await chat(data.plan, data.messages, data.collected, data.tone, data.instructions ?? "", data.startId));
  } catch (error) {
    sendJson(502, { error: error instanceof Error ? error.message : String(error) });
  }
}).listen(PORT, "127.0.0.1", () => console.log(`Open http://localhost:${PORT}`));
