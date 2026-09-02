import { chromium } from "playwright";
import { mkdir } from "node:fs/promises";
const BASE = process.env.PREVIEW_URL ?? "http://localhost:4321/";
await mkdir("tests/shots", { recursive: true });
const browser = await chromium.launch();
for (const theme of ["light", "dark"]) for (const width of [375, 1280]) {
  const ctx = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: theme });
  const p = await ctx.newPage();
  await p.goto(BASE, { waitUntil: "networkidle" });
  await p.screenshot({ path: `tests/shots/${theme}-${width}.png`, fullPage: true });
  await ctx.close();
}
await browser.close();
console.log("wrote tests/shots/*.png");
