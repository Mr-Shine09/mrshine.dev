import type { APIRoute } from "astro";
import { site } from "../data/site";

/**
 * The contact card as a real downloadable file, built at build time.
 *
 * Generating this in the browser from a Blob would work, but a static endpoint
 * means the link is an ordinary href: it survives no-JS, right-click-save, and
 * link previews.
 */

/** vCard escaping: backslash, comma, semicolon, newline. */
const esc = (value: string) =>
  value
    .replace(/\\/g, "\\\\")
    .replace(/,/g, "\\,")
    .replace(/;/g, "\\;")
    .replace(/\n/g, "\\n");

export const GET: APIRoute = () => {
  const { name, role, location, socials, url } = site;

  const lines = [
    "BEGIN:VCARD",
    "VERSION:3.0",
    // TODO(owner): split into family;given if you want phone contacts to sort
    // by surname. Left whole so the display name is never mangled.
    `N:;${esc(name)};;;`,
    `FN:${esc(name)}`,
    `TITLE:${esc(role)}`,
    `ADR;TYPE=home:;;;${esc(location)};;;`,
    socials.email ? `EMAIL;TYPE=INTERNET,PREF:${esc(socials.email)}` : null,
    `URL:${esc(url)}`,
    socials.github ? `URL;TYPE=github:${esc(socials.github)}` : null,
    socials.linkedin ? `URL;TYPE=linkedin:${esc(socials.linkedin)}` : null,
    `REV:${new Date().toISOString()}`,
    "END:VCARD",
  ].filter((line): line is string => line !== null);

  // vCard requires CRLF line endings.
  return new Response(lines.join("\r\n") + "\r\n", {
    headers: {
      "Content-Type": "text/vcard; charset=utf-8",
      "Content-Disposition": `attachment; filename="${name.replace(/\s+/g, "-").toLowerCase()}.vcf"`,
    },
  });
};
