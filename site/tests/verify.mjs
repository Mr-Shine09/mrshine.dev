// Playwright acceptance harness (Plan.md §10). Usage:
//   node tests/verify.mjs            # all checks
//   node tests/verify.mjs a b        # named checks
// Expects `npm run preview -- --port 4321` running against a fresh build.
import { chromium } from "playwright";

const BASE = process.env.PREVIEW_URL ?? "http://localhost:4321/";
const WIDTHS = [320, 375, 768, 1280];
const SECTIONS = ["about", "highlights", "projects", "personal", "contact"];

const checks = {};
const results = [];
function check(name, fn) { checks[name] = fn; }
function assert(cond, msg) { if (!cond) throw new Error(msg); }

async function page(browser, opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, ...opts });
  const p = await ctx.newPage();
  await p.goto(BASE, { waitUntil: "networkidle" });
  return { ctx, p };
}

check("sections", async (browser) => {
  const { ctx, p } = await page(browser);
  for (const id of SECTIONS) {
    assert(await p.locator(`section#${id}`).count() === 1, `missing <section id="${id}">`);
    assert(await p.locator(`nav a[href="#${id}"]`).count() === 1, `nav lacks link to #${id}`);
  }
  const order = await p.$$eval("main > section", (els) => els.map((e) => e.id));
  assert(order.join() === SECTIONS.join(), `section order is ${order.join(" · ")}`);
  await ctx.close();
});

check("overflow", async (browser) => {
  for (const width of WIDTHS) {
    const { ctx, p } = await page(browser, { viewport: { width, height: 800 } });
    const { sw, iw } = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: window.innerWidth }));
    assert(sw <= iw, `horizontal overflow at ${width}px: scrollWidth ${sw} > innerWidth ${iw}`);
    await ctx.close();
  }
});

check("pixelated", async (browser) => {
  const { ctx, p } = await page(browser);
  const bad = await p.$$eval(".oak-scene img, .hero-welcome img, .runner img", (imgs) =>
    imgs.filter((i) => getComputedStyle(i).imageRendering !== "pixelated").map((i) => i.getAttribute("src")));
  assert(bad.length === 0, `not pixelated: ${bad.join(", ")}`);
  const count = await p.locator(".oak-scene img, .hero-welcome img").count();
  assert(count >= 4, `expected ≥4 mascot images, found ${count}`);
  await ctx.close();
});

check("reduced-motion-scenes", async (browser) => {
  const { ctx, p } = await page(browser, { reducedMotion: "reduce" });
  await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await p.waitForTimeout(600);
  const srcs = await p.$$eval(".oak-scene img, .hero-welcome img", (imgs) => imgs.map((i) => i.getAttribute("src")));
  const animated = srcs.filter((s) => !s.includes("-static."));
  assert(animated.length === 0, `animated under reduced motion: ${animated.join(", ")}`);
  await ctx.close();
});

check("hero", async (browser) => {
  const { ctx, p } = await page(browser);
  const s = p.locator("section#about");
  assert((await s.locator("h1").innerText()).trim() === "OAK SOE KHANT", "h1 must be the name in caps");
  const text = await s.innerText();
  assert(text.includes("What's up everyone!!!"), "lead line missing or altered");
  assert(text.includes("Reader in progress."), "tagline missing");
  assert(text.includes("Leveraging artificial intelligence to sharpen actual intelligence."), "closing line missing");
  assert(text.toUpperCase().includes("YANGON") && text.toUpperCase().includes("BAY AREA, CA"), "plane motif missing");
  for (const [label, href] of [["Résumé", "/resume.pdf"], ["GitHub", "https://github.com/Mr-Shine09"], ["LinkedIn", "https://www.linkedin.com/in/oak-soe-khant-350252362"]]) {
    const a = s.locator(`a[href="${href}"]`);
    assert(await a.count() === 1, `hero link ${label} → ${href} missing`);
    assert((await a.innerText()).toUpperCase().includes(label.toUpperCase()), `hero link ${href} has no visible label "${label}"`);
  }
  assert(await s.locator(".hero-welcome").count() === 1, "welcome mascot missing");
  const border = await s.locator(".hero__portrait").evaluate((el) => getComputedStyle(el).borderWidth);
  assert(border === "2px", `portrait border is ${border}, want 2px`);
  await ctx.close();
});

// ---- runner ----
const only = process.argv.slice(2);
const names = only.length ? only : Object.keys(checks);
const browser = await chromium.launch();
for (const name of names) {
  if (!checks[name]) { results.push([name, "UNKNOWN"]); continue; }
  try { await checks[name](browser); results.push([name, "PASS"]); }
  catch (e) { results.push([name, `FAIL — ${e.message}`]); }
}
await browser.close();
for (const [n, r] of results) console.log(`${r.startsWith("PASS") ? "✓" : "✗"} ${n}: ${r}`);
process.exit(results.some(([, r]) => !r.startsWith("PASS")) ? 1 : 0);
