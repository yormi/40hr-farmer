#!/usr/bin/env python3
"""Build the drew-season static site from Drew's HubSpot marketing emails.

Usage:
  set -a && source .secrets/hubspot.env && set +a
  python3 scripts/build-drew-season.py

Fetches episode JSON from the HubSpot marketing emails API (scope: content),
downloads embedded images, cleans the HTML, and writes static pages to
``drew-season/``.
"""
import json, os, re, html, urllib.parse, urllib.request, hashlib, pathlib, sys

REPO = pathlib.Path(__file__).resolve().parent.parent
OUT = REPO / 'drew-season'
IMG_DIR = OUT / 'images'
JSON_CACHE = REPO / '.cache' / 'drew-emails'
IMG_DIR.mkdir(parents=True, exist_ok=True)
JSON_CACHE.mkdir(parents=True, exist_ok=True)

HUBSPOT_TOKEN = os.environ.get('HUBSPOT_API_KEY', '')

def fetch_episode_json(eid: int, num: int) -> dict:
    """Fetch episode from HubSpot API, cache on disk."""
    cache = JSON_CACHE / f'ep{num:02d}.json'
    if cache.exists():
        return json.load(cache.open())
    if not HUBSPOT_TOKEN:
        sys.exit('HUBSPOT_API_KEY not set and no cache. Source .secrets/hubspot.env first.')
    url = f'https://api.hubapi.com/marketing/v3/emails/{eid}?includeStats=false'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {HUBSPOT_TOKEN}'})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    cache.write_text(json.dumps(data, indent=2))
    return data

# ----- Episode metadata -----
EPISODES = [
    (1,  189569248908, "Allison and Drew's journey"),
    (2,  189861843280, "Crop uniformity"),
    (3,  190196687725, "Forcing plants into fruit production"),
    (4,  190486006936, "Pruning to fight gray mold"),
    (5,  190786329172, "Increasing fruit load as soon as possible"),
    (6,  191064919915, "Pruning fruits to increase yields"),
    (7,  191339003744, "Focus on ripening older fruits"),
    (8,  191570623142, "Rebalance plants by tweaking irrigation"),
    (9,  192022786169, "Already beaten 2023's season"),
    (10, 192346854548, "Major yield gap between varieties"),
    (11, 192714790294, "Finish tomatoes before touching anything else"),
    (12, 193210764665, "Saving the fall harvest: how to fight diseases"),
    (13, 194011294018, "The final stretch to double the yield"),
    (14, 195141584806, "No more energy should be wasted into tomato growth"),
    (15, 195469243209, "Hard pruning time"),
]

# Widgets to skip entirely (header and footer chrome, CTA block)
SKIP_WIDGET_IDS = {
    'module-0-0-0',   # "Too many emails?"
    'module-1-0-0',   # Orisha logo
    'module-1-0-1',   # "Hi {{ firstname }}"
    'module-2-0-2',   # Signature image (Antoine)
    'module-2-0-3',   # "About me" block
    'module-2-0-4',   # HubSpot footer
    'module-3-0-0',   # "Want to grow tons of tomatoes..." CTA
    'module-4-0-0',   # "Take care," signoff (rich_text version)
    'module-4-0-1',   # Signature image (later episodes)
    'module-4-0-2',   # About me (later episodes)
    'module-4-0-3',   # HubSpot footer (later episodes)
    'module-2-0-1',   # "Take care," / see you next week signoff
}

# ----- Image download cache -----
def download_image(src: str) -> str | None:
    """Download image from HubSpot CDN. Return local relative path (e.g. images/foo.jpg) or None."""
    if not src or not src.startswith('http'):
        return None
    # Build a sensible filename from the URL.
    parsed = urllib.parse.urlparse(src)
    basename = urllib.parse.unquote(os.path.basename(parsed.path))
    # Sanitise
    safe = re.sub(r'[^A-Za-z0-9._\-]', '-', basename).strip('-')
    if not safe:
        safe = 'image'
    # Deduplicate by hashing full URL
    h = hashlib.md5(src.encode()).hexdigest()[:8]
    stem, ext = os.path.splitext(safe)
    if not ext:
        ext = '.jpg'
    filename = f'{stem[:60]}-{h}{ext}'
    local = IMG_DIR / filename
    if not local.exists():
        try:
            req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            local.write_bytes(data)
            print(f'  downloaded {filename} ({len(data)} bytes)')
        except Exception as e:
            print(f'  FAILED to download {src}: {e}')
            return None
    return f'images/{filename}'

# ----- HTML cleaning -----
def clean_html(h: str) -> str:
    """Strip HubSpot noise, unwrap <span> style-only, keep structure."""
    if not h:
        return ''
    s = h
    # Remove tracking/analytics links to Orisha homepage? Keep links Drew included.
    # Strip hubspot personalisation tokens that slipped into copy.
    s = re.sub(r'\{\{\s*contact\.firstname\s*\}\}', 'there', s)
    s = re.sub(r'\{\{\s*unsubscribe_link\s*\}\}', '#', s)
    s = re.sub(r'\{\{\s*site_settings\.[^}]+\}\}', '', s)
    # Strip orisha_origin_email tracking param (plain and percent-encoded)
    s = re.sub(r'[?&]orisha_origin_email=\{\{\s*contact\.email\s*\}\}', '', s)
    s = re.sub(r'[?&]orisha_origin_email=%7B%7Bcontact\.email%7D%7D', '', s)
    # Strip auto-linkified "sq. ft" that HubSpot turned into http://sq.ft/
    s = re.sub(r'<a\s+[^>]*href="http://sq\.ft[^"]*"[^>]*>([^<]*)</a>', r'\1', s, flags=re.IGNORECASE)
    # Redirect the "Saving the fall harvest" PDF link (episode 14 linking back to ep12 content) to ep12
    s = re.sub(
        r'href="https://5156324\.fs1\.hubspotusercontent-na1\.net/hubfs/5156324/Saving%20the%20fall%20harvest[^"]*"',
        'href="episode-12.html"',
        s,
    )
    # Strip data-* attrs (ProseMirror)
    s = re.sub(r'\s+data-[a-z\-]+="[^"]*"', '', s)
    # Strip aria-level clutter on list items (HubSpot artifact)
    s = re.sub(r'\s+aria-level="\d+"', '', s)
    # Strip existing rel/target attributes so we can normalize below.
    s = re.sub(r'\s+rel="[^"]*"', '', s)
    s = re.sub(r'\s+target="[^"]*"', '', s)
    # Add target="_blank" rel="noopener" to external (http/https) links only.
    def _ext_link(m):
        tag = m.group(0)
        href = m.group(1)
        if href.startswith('http'):
            return tag[:-1] + ' target="_blank" rel="noopener">'
        return tag
    s = re.sub(r'<a\s+[^>]*href="([^"]+)"[^>]*>', _ext_link, s)
    # Remove inline color styles we want to drop (they all say "color: #000000" or brand blue)
    # But keep the tags. We'll remove color/font-size/line-height properties inside style="" but keep font-weight, text-align.
    def scrub_style(m):
        body = m.group(1)
        parts = [p.strip() for p in body.split(';') if p.strip()]
        keep = []
        for p in parts:
            if ':' not in p:
                continue
            prop, val = p.split(':', 1)
            prop = prop.strip().lower()
            if prop in ('color', 'font-size', 'line-height', 'font-family'):
                continue
            keep.append(f'{prop}: {val.strip()}')
        if not keep:
            return ''
        return f' style="{"; ".join(keep)}"'
    s = re.sub(r'\s+style="([^"]*)"', scrub_style, s)
    # Drop empty spans
    s = re.sub(r'<span\s*>(.*?)</span>', r'\1', s, flags=re.DOTALL)
    # Collapse multiple &nbsp;-only paragraphs
    s = re.sub(r'<p[^>]*>\s*(?:&nbsp;|\s|<br\s*/?>)+\s*</p>', '', s)
    # Drop empty headings (HubSpot leftover spacing)
    s = re.sub(r'<h[1-6][^>]*>\s*(?:&nbsp;|\s|<br\s*/?>)*\s*</h[1-6]>', '', s)
    # Collapse whitespace
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()

# ----- Content extraction -----
def extract_episode(num: int, eid: int) -> dict:
    data = fetch_episode_json(eid, num)
    subject = data.get('subject', '').strip()
    preview_widget = data['content']['widgets'].get('preview_text', {})
    preview = preview_widget.get('body', {}).get('value', '').strip()
    publish_iso = data.get('publishDate', '')
    # Clean subject: strip "Ghost House tomato production:" etc
    sections = data['content']['flexAreas']['main']['sections']
    widgets = data['content']['widgets']
    blocks = []  # list of dicts: {type, ...}
    for sec in sections:
        for col in sec['columns']:
            for wid in col['widgets']:
                if wid in SKIP_WIDGET_IDS:
                    continue
                w = widgets.get(wid, {})
                body = w.get('body', {}) if isinstance(w, dict) else {}
                path = body.get('path', '')
                # Skip email_footer / image_email widgets that house signature/logo (by path)
                if path in ('@hubspot/email_footer',):
                    continue
                html_content = body.get('html', '')
                img = body.get('img')
                # Divider: module with height=1 and color, no html/img
                if not html_content and not img and body.get('height') == 1:
                    blocks.append({'type': 'divider'})
                    continue
                if html_content:
                    # Filter: skip "Hi there," / "Take care," signoff text that slipped through
                    plain = re.sub(r'<[^>]+>', '', html_content).strip().lower()
                    plain = plain.replace('&nbsp;', ' ').strip()
                    if plain in ('', 'take care,', 'hi there,', 'hi ,'):
                        continue
                    blocks.append({'type': 'html', 'content': clean_html(html_content)})
                elif img:
                    src = img.get('src', '')
                    alt = img.get('alt', '').strip()
                    local = download_image(src)
                    if local:
                        # Skip signature images by filename heuristic
                        if 'signature' in local.lower() or 'orisha_logo' in local.lower():
                            continue
                        blocks.append({'type': 'img', 'src': local, 'alt': alt or f"Episode {num} photo"})
    # Dedupe preview vs. body:
    # - If the first html block is basically just the preview (length ratio close), drop the whole block.
    # - Otherwise, if the FIRST paragraph of the first block matches the preview, strip only that paragraph.
    if preview and blocks and blocks[0]['type'] == 'html':
        first_plain = re.sub(r'<[^>]+>', ' ', blocks[0]['content']).replace('&nbsp;', ' ')
        first_plain = re.sub(r'\s+', ' ', first_plain).strip()
        prev_norm = re.sub(r'\s+', ' ', preview.replace('\xa0', ' ')).strip()
        if prev_norm and first_plain.lower().startswith(prev_norm.lower()[:60]) and len(first_plain) <= len(prev_norm) * 1.3 + 10:
            blocks = blocks[1:]
        elif prev_norm:
            # Try stripping leading <p>...</p> if its text matches preview
            content = blocks[0]['content']
            m = re.match(r'\s*<p[^>]*>(.*?)</p>\s*', content, flags=re.DOTALL)
            if m:
                para_text = re.sub(r'<[^>]+>', ' ', m.group(1)).replace('&nbsp;', ' ')
                para_text = re.sub(r'\s+', ' ', para_text).strip()
                if para_text.lower().startswith(prev_norm.lower()[:60]) and len(para_text) <= len(prev_norm) * 1.3 + 10:
                    blocks[0] = {'type': 'html', 'content': content[m.end():].lstrip()}
    return {
        'num': num,
        'subject': subject,
        'preview': preview,
        'publish': publish_iso,
        'blocks': blocks,
    }

# ----- Page rendering -----
HEAD = '''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><path d='M8 28C8 28 6 18 16 10C26 2 28 4 28 4C28 4 30 6 22 16C14 26 4 24 4 24' fill='%233B6D11'/><path d='M8 28C8 28 10 20 16 14' stroke='%2327500A' stroke-width='1.5' fill='none'/></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            'farm-green': '#3B6D11',
            'farm-mid': '#639922',
            'farm-dark': '#27500A',
            'farm-light': '#EAF3DE',
            'farm-bg': '#f7f7f5',
            'farm-text': '#1a1a18',
            'farm-muted': '#5f5e5a',
          }},
          fontFamily: {{
            heading: ['Poppins', 'sans-serif'],
            body: ['Lato', 'sans-serif'],
          }},
          borderRadius: {{ 'card': '12px' }},
          maxWidth: {{ 'prose-farm': '65ch' }},
        }}
      }}
    }}
  </script>
  <style>
    body {{ font-family: 'Lato', sans-serif; color: #1a1a18; background: #f7f7f5; }}
    h1, h2, h3, h4, h5, h6 {{ font-family: 'Poppins', sans-serif; }}
    .prose-farm {{ max-width: 65ch; }}
    .prose-farm p {{ font-size: 1.0625rem; line-height: 1.75; margin: 0 0 1.25rem 0; color: #1a1a18; }}
    .prose-farm strong {{ color: #27500A; }}
    .prose-farm h2, .prose-farm h3 {{ font-weight: 600; color: #27500A; margin: 2rem 0 0.75rem; line-height: 1.3; }}
    .prose-farm h2 {{ font-size: 1.5rem; }}
    .prose-farm h3 {{ font-size: 1.25rem; }}
    .prose-farm a {{ color: #3B6D11; text-decoration: underline; text-underline-offset: 2px; font-weight: 500; }}
    .prose-farm a:hover {{ color: #27500A; }}
    .prose-farm ul, .prose-farm ol {{ padding-left: 1.25rem; margin: 0 0 1.25rem 0; }}
    .prose-farm ul li, .prose-farm ol li {{ margin-bottom: 0.5rem; line-height: 1.65; }}
    .prose-farm em {{ color: #27500A; font-style: italic; }}
    .prose-farm hr.soft {{ border: 0; border-top: 1px solid rgba(59,109,17,0.15); margin: 2.5rem 0; }}
    .episode-img {{ display: block; width: 100%; height: auto; border-radius: 12px; margin: 1.75rem 0; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }}
    .wordmark {{ font-family: 'Poppins', sans-serif; font-weight: 600; color: #27500A; }}
  </style>
</head>
<body class="antialiased">
  <header class="border-b border-farm-green/10 bg-white/80 backdrop-blur">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between gap-4">
      <a href="/" class="flex items-center gap-2 group">
        <svg class="w-6 h-6" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M8 28C8 28 6 18 16 10C26 2 28 4 28 4C28 4 30 6 22 16C14 26 4 24 4 24" fill="#3B6D11"/>
          <path d="M8 28C8 28 10 20 16 14" stroke="#27500A" stroke-width="1.5" fill="none"/>
        </svg>
        <span class="wordmark text-sm sm:text-base">The 40hr Farmer <span class="text-farm-muted font-normal">/ Drew's season</span></span>
      </a>
      <a href="/" class="text-sm text-farm-muted hover:text-farm-dark">Back to the site</a>
    </div>
  </header>
'''

FOOT = '''
  <footer class="mt-20 border-t border-farm-green/10 bg-white">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8 text-sm text-farm-muted flex flex-col sm:flex-row gap-3 justify-between">
      <p>Written by Antoine, with Drew and Allison of Ghost House Farm.</p>
      <a href="/" class="hover:text-farm-dark">Return to The 40hr Farmer</a>
    </div>
  </footer>
</body>
</html>
'''

def render_blocks(blocks):
    out = []
    for b in blocks:
        if b['type'] == 'html':
            out.append(b['content'])
        elif b['type'] == 'img':
            alt = html.escape(b['alt'])
            out.append(f'<img class="episode-img" src="{b["src"]}" alt="{alt}" loading="lazy">')
        elif b['type'] == 'divider':
            out.append('<hr class="soft">')
    return '\n'.join(out)

def fmt_date(iso: str) -> str:
    # "2025-05-01T10:15:11Z" -> "May 1, 2025"
    import datetime as dt
    try:
        d = dt.datetime.fromisoformat(iso.replace('Z', '+00:00'))
        return d.strftime('%B %-d, %Y')
    except Exception:
        return iso[:10]

# The 2 early episodes have sane publish dates; ep03's publish date is
# stuck in Dec 2025 due to a HubSpot automation state. Use createdAt as a
# fallback ordering hint and display a cleaner human date for ep03.
def display_date(ep_num: int, publish_iso: str) -> str:
    if ep_num == 3:
        # ep03 actually shipped mid-May 2025 based on the series cadence
        # (ep02 = May 8, ep04 = May 22). Use May 15, 2025.
        return 'May 15, 2025'
    return fmt_date(publish_iso)

# ----- Build all episodes -----
print('Extracting episodes...')
episodes_data = []
for num, eid, title_hint in EPISODES:
    print(f'EP{num:02d}...')
    ep = extract_episode(num, eid)
    ep['title_hint'] = title_hint
    episodes_data.append(ep)

# Episode pages
for i, ep in enumerate(episodes_data):
    num = ep['num']
    title_hint = ep['title_hint']
    page_title = f"Episode {num}: {title_hint} | Drew's season"
    description = ep['preview'] or title_hint
    prev_ep = episodes_data[i-1] if i > 0 else None
    next_ep = episodes_data[i+1] if i < len(episodes_data) - 1 else None
    date_human = display_date(num, ep['publish'])
    body = render_blocks(ep['blocks'])
    nav_prev = ''
    nav_next = ''
    if prev_ep:
        nav_prev = f'<a href="episode-{prev_ep["num"]:02d}.html" class="text-farm-green hover:text-farm-dark underline underline-offset-2"><span aria-hidden="true">&larr;</span> Episode {prev_ep["num"]}</a>'
    if next_ep:
        nav_next = f'<a href="episode-{next_ep["num"]:02d}.html" class="text-farm-green hover:text-farm-dark underline underline-offset-2 text-right">Episode {next_ep["num"]} <span aria-hidden="true">&rarr;</span></a>'
    page = HEAD.format(title=html.escape(page_title), description=html.escape(description)) + f'''
  <main class="max-w-3xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
    <a href="index.html" class="text-sm text-farm-muted hover:text-farm-dark">&larr; Back to the series</a>
    <article class="mt-6">
      <p class="text-sm text-farm-muted uppercase tracking-wide">Episode {num} of {len(episodes_data)} &middot; {date_human}</p>
      <h1 class="font-heading text-3xl sm:text-4xl font-bold text-farm-dark mt-2 leading-tight">{html.escape(title_hint)}</h1>
      {f'<p class="mt-4 text-lg text-farm-muted leading-relaxed italic">{html.escape(ep["preview"])}</p>' if ep["preview"] else ''}
      <hr class="soft my-8" style="border: 0; border-top: 1px solid rgba(59,109,17,0.2);">
      <div class="prose-farm">
        {body}
      </div>
      <hr class="soft mt-12" style="border: 0; border-top: 1px solid rgba(59,109,17,0.2);">
      <nav class="mt-8 grid grid-cols-2 gap-4 text-sm">
        <div>{nav_prev}</div>
        <div class="text-right">{nav_next}</div>
      </nav>
      <p class="mt-8 text-sm text-farm-muted"><a href="index.html" class="hover:text-farm-dark underline underline-offset-2">All episodes</a></p>
    </article>
  </main>
''' + FOOT
    out_path = OUT / f'episode-{num:02d}.html'
    out_path.write_text(page)
    print(f'  wrote {out_path}')

# Index (TOC) page
toc_rows = []
for ep in episodes_data:
    num = ep['num']
    title_hint = ep['title_hint']
    date_human = display_date(num, ep['publish'])
    preview = ep['preview']
    toc_rows.append(f'''
        <li class="fade-in">
          <a href="episode-{num:02d}.html" class="block bg-white rounded-card border border-farm-green/10 px-5 py-4 sm:px-6 sm:py-5 hover:border-farm-green/40 hover:shadow-sm transition">
            <div class="flex items-baseline justify-between gap-4">
              <p class="text-xs sm:text-sm text-farm-muted uppercase tracking-wide">Episode {num}</p>
              <p class="text-xs sm:text-sm text-farm-muted">{date_human}</p>
            </div>
            <h2 class="font-heading font-semibold text-farm-dark text-lg sm:text-xl mt-1 leading-snug">{html.escape(title_hint)}</h2>
            {f'<p class="text-farm-muted text-sm sm:text-base mt-2 leading-relaxed">{html.escape(preview)}</p>' if preview else ''}
          </a>
        </li>''')

first_date = display_date(episodes_data[0]['num'], episodes_data[0]['publish'])
last_date = display_date(episodes_data[-1]['num'], episodes_data[-1]['publish'])

index_page = HEAD.format(title="Drew's season, Ghost House Farm | The 40hr Farmer", description="A weekly field journal following Drew and Allison of Ghost House Farm through a greenhouse tomato season.") + f'''
  <main class="max-w-3xl mx-auto px-4 sm:px-6 py-10 sm:py-16">
    <div class="mb-10">
      <p class="text-sm text-farm-muted uppercase tracking-wide">A field journal, {first_date} to {last_date}</p>
      <h1 class="font-heading text-4xl sm:text-5xl font-bold text-farm-dark mt-2 leading-tight">Drew's season at Ghost House Farm</h1>
      <p class="mt-6 text-lg text-farm-text leading-relaxed max-w-prose-farm">
        Each week through the growing season, we sat with Drew and Allison to read their crop, talk through what was happening in the greenhouse, and write it down. What you are reading is the journal that came out of it, one episode per week.
      </p>
    </div>

    <ol class="space-y-3 list-none p-0">
      {''.join(toc_rows)}
    </ol>

    <p class="mt-12 text-sm text-farm-muted"><a href="/" class="hover:text-farm-dark underline underline-offset-2">Back to The 40hr Farmer</a></p>
  </main>
''' + FOOT

(OUT / 'index.html').write_text(index_page)
print(f'wrote {OUT / "index.html"}')
print('Done.')
