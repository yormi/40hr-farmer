# Google Photos bulk download — Claude curates

Used 2026-04-15 to pull 66 farm/farmer shots from ~533 Aug-2025+ candidates in Guillaume's personal library.

Personal-library photos are authenticated — `wget` returns HTML error pages. All fetching must happen in-browser with session cookies, which means the Claude Chrome extension needs to be connected.

## Flow

1. **Open the library** in the MCP-controlled tab: `https://photos.google.com/u/1/?pageId=none`

2. **Install a MutationObserver** that captures each tile's `(id, date)` pair. Key DOM facts:
   - Tile anchor: `a.p137Zd` carries `aria-label="Photo - <orientation> - <DD mois. YYYY, HH:MM:SS>"` (French locale).
   - Inner div `div.RY3tic` has a `style="background-image: url(.../pw/AP1Gcz...)"` whose ID is the authenticated image ref.
   - Store results in `window._tiles = new Map()` keyed by id.

   ```js
   const FR = {'janv.':0,'févr.':1,'mars':2,'avr.':3,'mai':4,'juin':5,
               'juil.':6,'août':7,'sept.':8,'oct.':9,'nov.':10,'déc.':11};
   const parseAria = a => {
     const m = a?.match(/(\d{1,2})\s+([a-zéû.]+)\s+(\d{4})/i);
     return m && FR[m[2].toLowerCase()] !== undefined
       ? {d:+m[1], m:FR[m[2].toLowerCase()], y:+m[3]} : null;
   };
   const capture = anchor => {
     if (!anchor?.getAttribute('aria-label')?.startsWith('Photo')) return;
     const bg = anchor.querySelector('[style*="/pw/"]')?.getAttribute('style') || '';
     const idm = bg.match(/\/pw\/(AP1Gcz[A-Za-z0-9_-]+)/);
     const dt = parseAria(anchor.getAttribute('aria-label'));
     if (idm && dt && !window._tiles.has(idm[1]))
       window._tiles.set(idm[1], {id: idm[1], ...dt});
   };
   window._tiles = new Map();
   document.querySelectorAll('a.p137Zd').forEach(capture);
   new MutationObserver(muts => muts.forEach(mu => {
     if (mu.type === 'attributes') { const a = mu.target.closest?.('a.p137Zd'); if (a) capture(a); }
     mu.addedNodes?.forEach(n => n.querySelectorAll?.('a.p137Zd').forEach(capture));
   })).observe(document.body, {subtree:true, attributes:true, attributeFilter:['style'], childList:true});
   ```

3. **Have the user scroll top → bottom slowly.** Synthetic scroll (`scrollTop`, wheel events, PageDown) does NOT trigger Google Photos' virtualized lazy-load — only real user input works. Since newest is on top, they can stop as soon as they pass the oldest date of interest.

4. **Filter in JS**, batch-fetch previews at `=w400` with `credentials:'include'`:

   ```js
   const ids = [...window._tiles.values()]
     .filter(t => (t.y > 2025) || (t.y === 2025 && t.m >= 7))   // Aug 2025+
     .sort((a,b) => (b.y-a.y) || (b.m-a.m) || (b.d-a.d))
     .map(t => t.id);
   window._bytes = [];
   window._progress = {total: ids.length, done: 0, failed: 0};
   const fetchOne = async id => {
     const r = await fetch(`https://photos.fife.usercontent.google.com/pw/${id}=w400`,
                           {credentials: 'include'});
     if (!r.ok) throw new Error(r.status);
     return new Uint8Array(await r.arrayBuffer());
   };
   (async () => {
     for (let i=0; i<ids.length; i+=20) {
       const g = ids.slice(i, i+20);
       const rs = await Promise.allSettled(g.map(fetchOne));
       rs.forEach((r, j) => {
         if (r.status === 'fulfilled') { window._bytes.push({id:g[j], bytes:r.value}); window._progress.done++; }
         else { window._bytes.push({id:g[j], bytes:null}); window._progress.failed++; }
       });
     }
   })();
   ```

   Batching 20 at a time keeps each JS call under the CDP timeout. Poll `window._progress` between calls.

5. **Pack and download** as a single binary blob (CSP blocks JSZip injection, so roll a tiny pack format):

   ```
   [4-byte LE manifest length] [manifest JSON] [concat JPEG bytes]
   manifest = { files: [{ idx, id, offset, size }, ...] }
   ```

   Trigger an anchor download of the blob; it lands in `~/Downloads/`.

6. **Split on disk** with a short Python script (see `scripts/` section below) into `/tmp/40hr-state/previews/pNNN.jpg`.

7. **Build contact sheets** at a readable size:

   ```bash
   cd /tmp/40hr-state/previews && ls p*.jpg | sort > _sorted.txt && split -l 16 _sorted.txt _batch_
   for f in _batch_*; do n=${f#_batch_};
     montage -label '%t' $(cat "$f") -tile 4x4 -geometry 360x270+4+4 \
             -background '#222' -fill white -pointsize 20 "sheets/sheet-${n}.jpg";
   done
   ```

   4×4 @ 360×270 is the readable sweet spot for the Read tool. Don't go denser.

8. **Claude reads sheets and picks indices.** Position in the sheet maps deterministically back to `pNNN` (sheet ordering is alphabetical; filenames on tiles via `-label '%t'` are a secondary check).

9. **Re-fetch chosen IDs at `=w2048`** (same batched fetcher, same pack format), split into `assets/clients/ferme-decembre/` with meaningful names.

### Size suffixes on `/pw/<ID>=<size>` URLs
- `=w400` — preview, ~30KB
- `=w2048` — hero-usable full-res, ~1MB
- `=w0` — original with EXIF

## Gotchas
- Previews are hosted on `lh3.googleusercontent.com/pw/` for **shared albums** (public, `wget`-able) but `photos.fife.usercontent.google.com/pw/` for **personal library** (auth required).
- Photo-page navigation IDs use a different format (`AF1Qip...`) — not the same as image content IDs (`AP1Gcz...`). Always extract `AP1Gcz` from backgrounds, not from anchor hrefs.
- The response filter blocks cookie-looking payloads — avoid echoing raw `style` attribute values in `javascript_tool` results. Extract the match first, return only the match.

## Keep preview assets
Don't auto-delete `/tmp/40hr-state/previews/` or the contact sheets after picking full-res — keep them around so future swaps are a five-second lookup instead of a full re-fetch.
