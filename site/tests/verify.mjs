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
  const bad = await p.$$eval(".oak-scene img, .hero-welcome img[data-welcome-sprite], .runner img", (imgs) =>
    imgs.filter((i) => getComputedStyle(i).imageRendering !== "pixelated").map((i) => i.getAttribute("src")));
  assert(bad.length === 0, `not pixelated: ${bad.join(", ")}`);
  const count = await p.locator(".oak-scene img, .hero-welcome img[data-welcome-sprite]").count();
  assert(count >= 4, `expected ≥4 mascot images, found ${count}`);
  await ctx.close();
});

check("reduced-motion-scenes", async (browser) => {
  const { ctx, p } = await page(browser, { reducedMotion: "reduce" });
  await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await p.waitForTimeout(600);
  const srcs = await p.$$eval(".oak-scene img, .hero-welcome img[data-welcome-sprite]", (imgs) => imgs.map((i) => i.getAttribute("src")));
  const animated = srcs.filter((s) => !s.includes("-static."));
  assert(animated.length === 0, `animated under reduced motion: ${animated.join(", ")}`);
  const planeAnim = await p.locator(".plane__icon").evaluate((el) => getComputedStyle(el).animationName);
  assert(planeAnim === "none", `plane animates under reduced motion: ${planeAnim}`);
  const cardAnims = await p.$$eval("section#projects .card", (els) => els.map((e) => e.getAnimations().length));
  assert(cardAnims.every((n) => n === 0), `slider scale animates under reduced motion: ${cardAnims.join(",")}`);
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

check("runner", async (browser) => {
  const { ctx, p } = await page(browser);
  const sprite = p.locator("[data-runner-sprite]");
  assert(await sprite.count() === 1, "runner sprite missing");
  const xAt = async () => p.locator("[data-runner]").evaluate((el) => new DOMMatrix(getComputedStyle(el).transform).m41);
  const x0 = await xAt();
  await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await p.waitForTimeout(250);
  assert((await sprite.getAttribute("src")).includes("run-atlas.png"), "runner should animate while scrolling");
  await p.waitForTimeout(1500);
  const x1 = await xAt();
  assert(x1 < x0 - 200, `runner did not travel left (x ${x0} → ${x1})`);
  assert((await sprite.getAttribute("src")).endsWith("run-static.png"), "runner should freeze when idle");
  const scaleX = await p.locator("[data-runner]").evaluate((el) => new DOMMatrix(getComputedStyle(el).transform).a);
  assert(scaleX < 0, "runner should face left (scaleX(-1))");
  await ctx.close();
});

check("reduced-motion-runner", async (browser) => {
  const { ctx, p } = await page(browser, { reducedMotion: "reduce" });
  const display = await p.locator(".runner-layer").evaluate((el) => getComputedStyle(el).display);
  assert(display === "none", `runner layer visible under reduced motion (display ${display})`);
  await ctx.close();
});

check("highlights", async (browser) => {
  const { ctx, p } = await page(browser);
  const s = p.locator("section#highlights");
  assert((await s.locator("h2").innerText()).toUpperCase().includes("HIGHLIGHTS"), "heading");
  assert(await s.locator(".achievements li").count() === 1, "expected one achievement row");
  const row = await s.locator(".achievements li").first().innerText();
  assert(row.includes("ICPC") && row.includes("2025"), `row text: ${row}`);
  assert((await s.innerText()).includes("More achievements coming soon."), "coming-soon line missing");
  assert(await s.locator('.oak-scene[aria-label*="trophy"]').count() === 1, "trophy-lift scene missing");
  await ctx.close();
});

check("projects", async (browser) => {
  const { ctx, p } = await page(browser);
  const titles = await p.$$eval("section#projects .card h3", (els) => els.map((e) => e.textContent.trim()));
  assert(titles.join("|") === "PokeDesk|Look-Out|VisionAssist|Echo", `card order: ${titles.join(" · ")}`);
  const echo = p.locator("section#projects .card", { hasText: "Echo" });
  const echoText = await echo.innerText();
  for (const n of ["aadityad12", "shahxsheel", "Mr-Shine09"]) assert(echoText.includes(n), `Echo must credit ${n}`);
  assert(await echo.locator('a[href="https://github.com/aadityad12/Echo"]').count() === 1, "Echo repo link");
  const fit = await p.locator("section#projects .card img").first().evaluate((i) => getComputedStyle(i).objectFit);
  assert(fit === "contain", `card images must be object-fit: contain, got ${fit}`);
  const boxes = await p.$$eval("section#projects .card", (els) => els.map((e) => { const c = e.getBoundingClientRect(); const pl = e.querySelector(".card__plate").getBoundingClientRect(); return { card: Math.round(c.width), plate: [Math.round(pl.width), Math.round(pl.height)] }; }));
  for (const b of boxes) {
    assert(b.card <= 34 * 16 + 2, `card wider than 34rem: ${b.card}px`);
    assert(Math.abs(b.plate[1] - b.plate[0] * 0.625) <= 2, `plate not 16:10: ${b.plate.join("x")}`);
  }
  await p.locator("section#projects").scrollIntoViewIfNeeded();
  await p.waitForTimeout(300);
  const motion = await p.$$eval("section#projects .card", (els) => ({ supports: CSS.supports("animation-timeline: view()"), anims: els.map((e) => e.getAnimations().length), transforms: els.map((e) => getComputedStyle(e).transform) }));
  if (motion.supports) {
    assert(motion.anims.every((n) => n >= 1), `coverflow animation missing on cards: ${motion.anims.join(",")}`);
    assert(motion.transforms.slice(1).some((t) => t !== "none"), "no neighbour card is scaled — scroll-driven scale not applying");
  }
  const track = p.locator("section#projects .slider__track");
  const before = await track.evaluate((t) => t.scrollLeft);
  await p.locator("[data-slider-next]").click();
  await p.waitForTimeout(600);
  assert((await track.evaluate((t) => t.scrollLeft)) > before, "next button did not scroll the track");
  assert(await p.locator('section#projects .oak-scene[aria-label*="workbench"]').count() === 1, "workbench-zap scene missing");
  await ctx.close();
});

check("nojs", async (browser) => {
  const { ctx, p } = await page(browser, { javaScriptEnabled: false });
  for (const id of SECTIONS) assert(await p.locator(`section#${id}`).count() === 1, `no-JS: section ${id} missing`);
  assert(await p.locator("section#projects .card").count() === 4, "no-JS: cards missing");
  assert(await p.locator('section#projects a[href="https://github.com/Mr-Shine09/PokeDesk"]').count() === 1, "no-JS: repo link");
  await ctx.close();
  // With JS off the palette comes from the <noscript> block, not the toggle.
  const { ctx: dctx, p: dp } = await page(browser, { javaScriptEnabled: false, colorScheme: "dark" });
  const nojsBg = await dp.evaluate(() => getComputedStyle(document.body).backgroundColor);
  assert(nojsBg === "rgb(21, 14, 43)", `no-JS dark theme not applied: body bg ${nojsBg}`);
  await dctx.close();
});

check("reading", async (browser) => {
  const { ctx, p } = await page(browser);
  const s = p.locator("section#personal");
  assert((await s.locator("h2").innerText()).toUpperCase().includes("READING LIST"), "heading");
  assert((await s.locator(".label").first().innerText()).match(/2 VOLUMES/i), "count must derive from data (2 volumes)");
  assert(await s.locator(".current__card").count() === 2, "expected two currently-reading cards");
  const ring = s.locator('[role="progressbar"]').first();
  assert(await ring.getAttribute("aria-valuenow") === "73", "Dune ring should be 73");
  assert(await s.locator(".current__card img").count() === 2, "current cards should show covers");
  assert(await s.locator(".shelf").count() === 2, "expected Fiction and Non-Fiction shelves");
  assert(await s.locator(".shelf__empty").count() === 2, "both shelves should render the empty state");
  assert((await s.innerText()).includes("Nothing finished yet"), "empty state copy");
  assert(await s.locator('.oak-scene[aria-label*="stove"], .oak-scene[aria-label*="reading"]').count() === 1, "reading-fire scene missing");
  await ctx.close();
});

check("contact", async (browser) => {
  const { ctx, p } = await page(browser);
  const s = p.locator("section#contact");
  for (const href of ["https://mrshine.dev", "mailto:oaksoekhant182209@gmail.com", "https://www.linkedin.com/in/oak-soe-khant-350252362", "https://github.com/Mr-Shine09", "/contact.vcf"]) {
    assert(await s.locator(`a[href="${href}"]`).count() === 1, `contact row ${href} missing`);
  }
  assert((await s.innerText()).includes("oaksoekhant182209@gmail.com"), "email must be visible text");
  await ctx.grantPermissions(["clipboard-read", "clipboard-write"]);
  await s.locator("[data-copy]").click();
  await p.waitForTimeout(200);
  assert((await s.locator("[data-copy-status]").innerText()).toLowerCase().includes("copied"), "copy button must announce success");
  assert(await s.locator("form").count() === 0, "no contact form");
  assert(await s.locator(".oak-scene").count() === 0, "no mascot in contact");
  const me = await s.locator('a[href="https://github.com/Mr-Shine09"]').getAttribute("rel");
  assert(me && me.includes("me"), 'social links need rel="me"');
  await ctx.close();
});

check("contact-nojs", async (browser) => {
  const { ctx, p } = await page(browser, { javaScriptEnabled: false });
  assert(await p.locator("section#contact a[href^='mailto:']").count() === 1, "no-JS: email link");
  assert(!(await p.locator("section#contact [data-copy]").isVisible()), "no-JS: copy button must be hidden");
  await ctx.close();
});

check("focus", async (browser) => {
  const { ctx, p } = await page(browser);
  const total = await p.locator("a, button, [tabindex='0'], summary").count();
  const missing = [];
  await p.keyboard.press("Tab"); // skip link
  for (let i = 0; i < total; i++) {
    const info = await p.evaluate(() => {
      const el = document.activeElement;
      if (!el || el === document.body) return null;
      const cs = getComputedStyle(el);
      return { tag: el.tagName + (el.getAttribute("href") ? `[${el.getAttribute("href")}]` : ""), outline: cs.outlineStyle !== "none" && parseFloat(cs.outlineWidth) > 0 };
    });
    if (info && !info.outline) missing.push(info.tag);
    await p.keyboard.press("Tab");
  }
  assert(missing.length === 0, `no visible focus on: ${[...new Set(missing)].join(", ")}`);
  await ctx.close();
});

check("tap-targets", async (browser) => {
  const { ctx, p } = await page(browser, { viewport: { width: 375, height: 700 } });
  await p.evaluate(() => document.documentElement.classList.add("js"));
  const small = await p.$$eval("a, button, summary", (els) =>
    els.filter((e) => { const r = e.getBoundingClientRect(); const vis = r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== "hidden"; return vis && (r.width < 44 || r.height < 44); })
       .map((e) => `${e.tagName}${e.className ? "." + e.className.split(" ")[0] : ""} ${Math.round(e.getBoundingClientRect().width)}×${Math.round(e.getBoundingClientRect().height)}`));
  assert(small.length === 0, `tap targets under 44px: ${small.join(", ")}`);
  await ctx.close();
});

check("theme", async (browser) => {
  const { ctx, p } = await page(browser);
  await p.locator("[data-theme-toggle]").click();
  assert((await p.getAttribute("html", "data-theme")) === "dark", "toggle should switch to dark");
  await p.reload({ waitUntil: "networkidle" });
  assert((await p.getAttribute("html", "data-theme")) === "dark", "theme should persist across reload");
  const bg = await p.evaluate(() => getComputedStyle(document.body).backgroundColor);
  assert(bg === "rgb(21, 14, 43)", `dark --bg should be #150E2B, got ${bg}`);
  await ctx.close();
});

check("fonts", async (browser) => {
  const { ctx, p } = await page(browser);
  const loaded = await p.evaluate(async () => { await document.fonts.ready; return [...document.fonts].filter((f) => f.status === "loaded").map((f) => f.family.replace(/"/g, "")); });
  assert(loaded.some((f) => /Geist Pixel/.test(f)), `Geist Pixel not loaded: ${loaded.join(", ")}`);
  assert(loaded.some((f) => /Geist Sans/.test(f)), `Geist Sans not loaded: ${loaded.join(", ")}`);
  const synth = await p.evaluate(() => getComputedStyle(document.documentElement).fontSynthesis);
  assert(synth === "none", `font-synthesis is ${synth}`);
  const heavy = await p.$$eval("body *", (els) => els.filter((e) => parseInt(getComputedStyle(e).fontWeight) >= 600 && e.textContent.trim()).length);
  assert(heavy === 0, `${heavy} elements render at weight ≥600 (faux bold risk)`);
  await ctx.close();
});

check("vcard", async (browser) => {
  const { ctx, p } = await page(browser);
  const res = await p.request.get(`${BASE}contact.vcf`);
  assert(res.status() === 200, `contact.vcf status ${res.status()}`);
  const body = await res.text();
  assert(body.startsWith("BEGIN:VCARD"), `vcf does not start with BEGIN:VCARD: ${body.slice(0, 24)}`);
  for (const line of ["FN:Oak Soe Khant", "EMAIL;TYPE=INTERNET,PREF:oaksoekhant182209@gmail.com", "URL:https://mrshine.dev"]) {
    assert(body.includes(line), `vcf missing ${line}`);
  }
  assert(body.endsWith("END:VCARD\r\n"), "vcf must end with END:VCARD and a CRLF");
  await ctx.close();
});

check("third-party", async (browser) => {
  const ctx = await browser.newContext();
  const p = await ctx.newPage();
  const foreign = [];
  p.on("request", (r) => { const u = new URL(r.url()); if (u.origin !== new URL(BASE).origin) foreign.push(r.url()); });
  await p.goto(BASE, { waitUntil: "networkidle" });
  await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await p.waitForTimeout(800);
  assert(foreign.length === 0, `third-party requests: ${foreign.slice(0, 5).join(", ")}`);
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
