// Verification harness (dev only, not shipped): serves the site over local HTTP under the same
// base path GitHub Pages uses, renders every page at three viewports, measures horizontal
// overflow, screenshots to _verify/, and crawls every internal link including fragments.
//
//   node tools/verify.mjs
//
// Playwright: resolved from the project (npm i -D playwright) or from PLAYWRIGHT_DIR, so the
// harness is not tied to one machine's global install.
import { readdirSync, statSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { join, dirname, resolve, extname } from 'node:path';
import { createServer } from 'node:http';
import { createRequire } from 'node:module';

const ROOT = resolve(dirname(new URL(import.meta.url).pathname), '..');
const BASE = '/capelli-institute-site/';   // must match BASE_PATH in tools/build-pages.py

async function loadPlaywright() {
  const candidates = [process.env.PLAYWRIGHT_DIR, 'playwright'].filter(Boolean);
  const req = createRequire(join(ROOT, 'package.json'));
  for (const c of candidates) {
    try {
      if (c.includes('/')) {
        // A directory (the documented form) or a file path.
        const entry = existsSync(c) && statSync(c).isDirectory() ? ['index.mjs', 'index.js'].map(f => join(c, f)).find(existsSync) : c;
        if (entry) return await import(entry);
      } else {
        return await import(req.resolve(c));
      }
    } catch {}
  }
  // Common global locations, last resort.
  for (const g of ['/opt/homebrew/lib/node_modules/playwright/index.mjs', '/usr/local/lib/node_modules/playwright/index.mjs', '/usr/lib/node_modules/playwright/index.mjs']) {
    if (existsSync(g)) return import(g);
  }
  throw new Error('Playwright not found. npm i -D playwright, or set PLAYWRIGHT_DIR to its install directory.');
}
const { chromium } = await loadPlaywright();

const pages = [];
(function walk(d) {
  for (const f of readdirSync(d)) {
    // offer/ is the standalone offer sheet with its own styling, checked on its own.
    if (f.startsWith('_') || f.startsWith('.') || f === 'node_modules' || f === 'tools' || f === 'offer') continue;
    const p = join(d, f);
    if (statSync(p).isDirectory()) walk(p); else if (f.endsWith('.html')) pages.push(p);
  }
})(ROOT);
pages.sort();

// Static server rooted at BASE, like Pages. Unknown paths get 404.html with status 404, like Pages.
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.svg': 'image/svg+xml' };
const server = createServer((req, res) => {
  let path = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (!path.startsWith(BASE)) { res.writeHead(404); return res.end(); }
  path = path.slice(BASE.length) || 'index.html';
  if (path.endsWith('/')) path += 'index.html';
  const file = resolve(ROOT, path);
  if (!file.startsWith(ROOT) || !existsSync(file) || statSync(file).isDirectory()) {
    res.writeHead(404, { 'content-type': MIME['.html'] }); return res.end(readFileSync(join(ROOT, '404.html')));
  }
  res.writeHead(200, { 'content-type': MIME[extname(file)] || 'application/octet-stream' });
  res.end(readFileSync(file));
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const ORIGIN = `http://127.0.0.1:${server.address().port}`;
const urlFor = p => ORIGIN + BASE + p.slice(ROOT.length + 1);

const bands = [[360, 'm'], [768, 't'], [1920, 'd']];
const browser = await chromium.launch();
let overflow = 0, blank = 0, brokenImgs = 0, unstyled = 0;
for (const [w, tag] of bands) {
  mkdirSync(join(ROOT, '_verify', tag), { recursive: true });
  const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  for (const p of pages) {
    await page.goto(urlFor(p));
    // Scroll through so loading="lazy" images are requested, then wait for every image to settle.
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } window.scrollTo(0, 0); });
    // Force every image eager (lazy ones hidden at this width would otherwise never load), then settle.
    await page.evaluate(() => Promise.race([
      Promise.all([...document.images].map(i => { i.loading = 'eager'; return i.complete ? null : new Promise(r => { i.addEventListener('load', r); i.addEventListener('error', r); }); })),
      new Promise(r => setTimeout(r, 5000)),
    ]));
    const r = await page.evaluate(() => ({
      sw: document.documentElement.scrollWidth, iw: window.innerWidth,
      text: document.body.innerText.trim().length, imgs: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src')),
      css: getComputedStyle(document.body).fontFamily.includes('Garamond'),
    }));
    const rel = p.slice(ROOT.length + 1);
    const flag = (r.sw > r.iw ? '  OVERFLOW' : '') + (r.css ? '' : '  NO-STYLESHEET');
    if (r.sw > r.iw) overflow++;
    if (r.text < 200) blank++;
    if (r.imgs.length) brokenImgs++;
    if (!r.css) unstyled++;
    if (w === 360 || flag || r.imgs.length) console.log(`${w}px ${rel.padEnd(52)} scrollWidth=${r.sw} text=${r.text}${flag}${r.imgs.length ? ' BROKEN-IMG ' + r.imgs.join(',') : ''}`);
    await page.screenshot({ path: join(ROOT, '_verify', tag, rel.replace(/\//g, '__').replace(/\.html$/, '.png')), fullPage: true });
  }
  await ctx.close();
}

// Link crawl over HTTP: every internal href, including fragment-only links on the same page.
const ctx = await browser.newContext();
const page = await ctx.newPage();
let checked = 0, broken = [];
for (const p of pages) {
  await page.goto(urlFor(p));
  const hrefs = await page.evaluate(() => [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')));
  for (const h of hrefs) {
    if (/^(https?:|mailto:|tel:)/.test(h)) continue;
    checked++;
    const [path, hash] = h.split('#');
    let target;
    if (!path) target = p;
    else if (path.startsWith(BASE)) target = join(ROOT, path.slice(BASE.length));
    else if (path.startsWith('/')) { broken.push(`${p.slice(ROOT.length + 1)} -> ${h} (absolute path outside base ${BASE})`); continue; }
    else target = resolve(dirname(p), path);
    if (!existsSync(target)) { broken.push(`${p.slice(ROOT.length + 1)} -> ${h} (missing file)`); continue; }
    if (hash) {
      if (target !== p) await page.goto(urlFor(target));
      const ok = await page.evaluate(id => !!document.getElementById(id), hash);
      if (!ok) broken.push(`${p.slice(ROOT.length + 1)} -> ${h} (missing #${hash})`);
      if (target !== p) await page.goto(urlFor(p));
    }
  }
}
// The 404 page as Pages serves it: any unknown path, at any depth.
await page.goto(ORIGIN + BASE + 'books/does-not-exist/deep.html');
const nf = await page.evaluate(() => ({ styled: getComputedStyle(document.body).fontFamily.includes('Garamond'), imgs: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).length, text: document.body.innerText.includes('not here') }));
console.log(`\n404 served at depth: styled=${nf.styled} brokenImgs=${nf.imgs} text=${nf.text}`);
console.log(`Pages rendered: ${pages.length}  blank pages: ${blank}  overflow cases: ${overflow}  pages with broken images: ${brokenImgs}  unstyled renders: ${unstyled}`);
console.log(`Links checked: ${checked}, broken: ${broken.length}`);
broken.forEach(b => console.log('  BROKEN ' + b));
await browser.close();
server.close();
if (!nf.styled || nf.imgs || broken.length || overflow || blank || brokenImgs || unstyled) process.exitCode = 1;
