// @ts-check
import { defineConfig, fontProviders } from "astro/config";

// Type decision (HANDOFF §4): one family — Geist Pixel — for all site text,
// self-hosted, subset to ~26 KB woff2 (built from the source TTF in
// `Geist_Pixel copy/`, licence at src/assets/fonts/OFL.txt). The five extra
// families below exist ONLY for the W Phrases page, which is explicitly the one
// room where type varies. Every family is self-hosted at build time — no
// third-party request at runtime — and emits size-adjust metrics so the webfont
// swap does not shift layout.
export default defineConfig({
  fonts: [
    {
      provider: fontProviders.local(),
      name: "Geist Pixel",
      cssVariable: "--font-pixel",
      // The single file carries the ELSH (Element Shape) axis, 0–100.
      // Default instance is ELSH 0 — solid pixels, verified legible.
      // Mid-axis values (20–80) render hollow: decorative only, never body.
      options: {
        variants: [
          {
            weight: 400,
            style: "normal",
            src: ["./src/assets/fonts/geist-pixel.woff2"],
          },
        ],
      },
      fallbacks: ["ui-monospace", "Menlo", "monospace"],
    },

    // ---- W Phrases specimen set (HANDOFF §7.4) — weight-limited, Latin only ----
    {
      provider: fontProviders.google(),
      name: "Space Grotesk",
      cssVariable: "--font-grotesque",
      weights: [400],
      styles: ["normal"],
      subsets: ["latin"],
      fallbacks: ["system-ui", "sans-serif"],
    },
    {
      provider: fontProviders.google(),
      name: "Archivo Narrow",
      cssVariable: "--font-condensed",
      weights: [400],
      styles: ["normal"],
      subsets: ["latin"],
      fallbacks: ["Arial Narrow", "sans-serif"],
    },
    {
      provider: fontProviders.google(),
      name: "Caveat",
      cssVariable: "--font-hand",
      weights: [400],
      styles: ["normal"],
      subsets: ["latin"],
      fallbacks: ["cursive"],
    },
    {
      provider: fontProviders.google(),
      name: "Bitter",
      cssVariable: "--font-slab",
      weights: [400, 700],
      styles: ["normal"],
      subsets: ["latin"],
      fallbacks: ["Georgia", "serif"],
    },
    {
      provider: fontProviders.google(),
      name: "Playfair Display",
      cssVariable: "--font-serif",
      weights: [400],
      styles: ["normal", "italic"],
      subsets: ["latin"],
      fallbacks: ["Georgia", "Times New Roman", "serif"],
    },
  ],
});
