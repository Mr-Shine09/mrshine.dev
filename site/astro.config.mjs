// @ts-check
import { defineConfig, fontProviders } from "astro/config";

// Locked type decision (#10): high-contrast serif for display, monospace for
// body and labels, no pixel font anywhere. Both families are self-hosted at
// build time via Astro's font pipeline — no third-party request at runtime,
// and size-adjust metrics are emitted so swapping in the webfont does not
// shift layout.
export default defineConfig({
  fonts: [
    {
      provider: fontProviders.google(),
      name: "Playfair Display",
      cssVariable: "--font-display",
      weights: [400, 700],
      styles: ["normal", "italic"],
      fallbacks: ["Georgia", "Times New Roman", "serif"],
    },
    {
      provider: fontProviders.google(),
      name: "JetBrains Mono",
      cssVariable: "--font-body",
      weights: [400, 500, 700],
      styles: ["normal"],
      fallbacks: ["ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
    },
  ],
});
