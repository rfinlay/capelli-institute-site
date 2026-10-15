// Verification harness (dev only, not shipped): renders every page at three viewports,
// measures horizontal overflow, screenshots to _verify/, and crawls every internal link.
import { chromium } from '/opt/homebrew/lib/node_modules/playwright/index.mjs';
import { readdirSync, statSync, existsSync, mkdirSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';

const ROOT = resolve(dirname(new URL(import.meta.url).pathname), '..');
const pages = [];
(function walk(d) {
  for (const f of readdirSync(d)) {
    if (f.startsWith('_') || f.startsWith('.') || f === 'node_modules' || f === 'tools') continue;
    const p = join(d, f);
    if (statSync(p).isDirectory()) walk(p); else if (f.endsWith('.html')) pages.push(p);
  }
})(ROOT);
pages.sort();

const bands = [[360, 'm'], [768, 't'], [1920, 'd']];
const browser = await chromium.launch();
let overflow = 0, blank = 0;
for (const [w, tag] of bands) {
  mkdirSync(join(ROOT, '_verify', tag), { recursive: true });
  const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  for (const p of pages) {
    await page.goto('file://' + p);
    await page.waitForTimeout(150);
    const r = await page.evaluate(() => ({
      sw: document.documentElement.scrollWidth, iw: window.innerWidth,
      text: document.body.innerText.trim().length, imgs: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute('src')),
    }));
    const rel = p.slice(ROOT.length + 1);
    const flag = r.sw > r.iw ? '  OVERFLOW' : '';
    if (r.sw > r.iw) overflow++;
    if (r.text < 200) blank++;
    if (w === 360 || flag || r.imgs.length) console.log(`${w}px ${rel.padEnd(52)} scrollWidth=${r.sw} text=${r.text}${flag}${r.imgs.length ? ' BROKEN-IMG ' + r.imgs.join(',') : ''}`);
    await page.screenshot({ path: join(ROOT, '_verify', tag, rel.replace(/\//g, '__').replace(/\.html$/, '.png')), fullPage: true });
  }
  await ctx.close();
}

// Link crawl (file:// resolution; 404.html uses absolute paths so it is resolved against ROOT).
const ctx = await browser.newContext();
const page = await ctx.newPage();
let checked = 0, broken = [];
for (const p of pages) {
  await page.goto('file://' + p);
  const hrefs = await page.evaluate(() => [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')));
  for (const h of hrefs) {
    if (/^(https?:|mailto:|tel:|#)/.test(h)) continue;
    checked++;
    const [path, hash] = h.split('#');
    let target = path.startsWith('/') ? join(ROOT, path) : resolve(dirname(p), path);
    if (!existsSync(target)) { broken.push(`${p.slice(ROOT.length + 1)} -> ${h} (missing file)`); continue; }
    if (hash) {
      await page.goto('file://' + target);
      const ok = await page.evaluate(id => !!document.getElementById(id), hash);
      if (!ok) broken.push(`${p.slice(ROOT.length + 1)} -> ${h} (missing #${hash})`);
      await page.goto('file://' + p);
    }
  }
}
console.log(`\nPages rendered: ${pages.length}  blank pages: ${blank}  overflow cases: ${overflow}`);
console.log(`Links checked: ${checked}, broken: ${broken.length}`);
broken.forEach(b => console.log('  BROKEN ' + b));
await browser.close();
