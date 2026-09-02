/**
 * Site-wide facts (Plan.md §8). The hero, the contact card, and contact.vcf
 * all read this file so they can never drift. Do not invent TODO(owner) values.
 */
export type SiteConfig = {
  name: string;
  role: string;
  shortRole: string;
  location: string;
  origin: string;
  destination: string;
  lead: string;
  tagline: string;
  closing: string;
  socials: {
    email: string;
    github: string;
    linkedin: string;
    instagram: string;
    facebook: string;
    devpost: string;
  };
  resumeUrl: string;
  url: string;
  seo: { description: string };
};

export const site: SiteConfig = {
  name: "Oak Soe Khant",
  role: "Second-year Computer Engineering student, De Anza Community College",
  shortRole: "Computer Engineering @ De Anza",
  location: "Santa Clara, California",
  origin: "Yangon",
  destination: "Bay Area, CA",
  // Verbatim, owner's own words. Three exclamation marks are intentional.
  lead:
    "What's up everyone!!! My name is Oak, a Second-year Computer Engineering student at DeAnza Community College, transferring in 2027.",
  tagline:
    "Building cool products to boost productivity. Hackathon fanatic. Mindful AI user. Reader in progress.",
  closing: "Leveraging artificial intelligence to sharpen actual intelligence.",
  socials: {
    email: "oaksoekhant182209@gmail.com",
    github: "https://github.com/Mr-Shine09",
    linkedin: "https://www.linkedin.com/in/oak-soe-khant-350252362",
    instagram: "https://www.instagram.com/oak_soe_khant909", // vCard only
    facebook: "https://www.facebook.com/johnwick.wick.37625", // vCard only
    devpost: "https://devpost.com/oaksoekhant182209", // vCard only
  },
  resumeUrl: "/resume.pdf",
  // Registered 2 Sep 2026 through Cloudflare Registrar.
  url: "https://mrshine.dev",
  seo: {
    description: "A personal time capsule — who I am and what I love to do. Projects, highlights, and what I'm reading.",
  },
};

/** Rows on the contact card, in order. Blank hrefs drop rather than render empty. */
export const contactRows: { label: string; href: string; text: string; me?: boolean; copy?: boolean }[] = [
  { label: "Website", href: site.url, text: site.url.replace(/^https?:\/\//, "") },
  { label: "Email", href: `mailto:${site.socials.email}`, text: site.socials.email, copy: true },
  { label: "LinkedIn", href: site.socials.linkedin, text: "oak-soe-khant", me: true },
  { label: "GitHub", href: site.socials.github, text: "Mr-Shine09", me: true },
  { label: "Save contact", href: "/contact.vcf", text: "contact.vcf" },
].filter((row) => row.href && row.text);
