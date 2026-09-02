// @ts-check
import { defineConfig, fontProviders } from "astro/config";

// Two self-hosted faces (Plan.md §4): Geist Pixel for headings, nav, labels and
// chips; Geist Sans for prose. Both are subset by scripts/subset-fonts.sh. No
// third-party font requests exist anywhere on the site.
export default defineConfig({
  site: "https://mrshine.dev",
  fonts: [
    {
      provider: fontProviders.local(),
      name: "Geist Pixel",
      cssVariable: "--font-pixel",
      // Single ELSH axis 0–100. Default instance ELSH 0 = solid pixels.
      // 20–80 renders hollow: never for real text.
      options: {
        variants: [{ weight: 400, style: "normal", src: ["./src/assets/fonts/geist-pixel.woff2"] }],
      },
      fallbacks: ["ui-monospace", "Menlo", "monospace"],
    },
    {
      provider: fontProviders.local(),
      name: "Geist Sans",
      cssVariable: "--font-sans",
      options: {
        variants: [
          { weight: 400, style: "normal", src: ["./src/assets/fonts/geist-sans.woff2"] },
          { weight: 500, style: "normal", src: ["./src/assets/fonts/geist-sans-medium.woff2"] },
        ],
      },
      fallbacks: ["system-ui", "-apple-system", "Segoe UI", "Helvetica Neue", "sans-serif"],
    },
  ],
});
