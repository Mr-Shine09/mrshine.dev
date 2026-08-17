/**
 * Site-wide facts (HANDOFF §8). One data source: the business card, the
 * /contact page, and the vCard all read this file so they can never drift.
 *
 * Values marked TODO(owner) are placeholders so the build runs — do not invent
 * real values for them.
 */

export type SiteConfig = {
  name: string;
  role: string;
  location: string;
  tagline: string;
  /** Any social left as "" is dropped from the page rather than rendered empty. */
  socials: {
    email: string;
    github: string;
    linkedin: string;
    instagram: string;
    facebook: string;
    devpost: string;
  };
  /** "" until resume.pdf exists — the Résumé row drops itself. */
  resumeUrl: string;
  url: string;
  seo: { description: string };
};

// Annotated rather than `as const`: empty placeholders must stay typed as
// `string`, or narrowing them to their literal `""` makes the "drop it if
// blank" checks unreachable.
export const site: SiteConfig = {
  name: "Oak Soe Khant",
  role: "Second-year Computer Engineering student, De Anza Community College",
  location: "Santa Clara, California",
  tagline:
    "Building cool products to boost productivity. Hackathon fanatic. Mindful AI user. Reader in progress.",

  socials: {
    email: "oaksoekhant182209@gmail.com",
    github: "https://github.com/Mr-Shine09",
    linkedin: "https://www.linkedin.com/in/oak-soe-khant-350252362",
    instagram: "https://www.instagram.com/oak_soe_khant909",
    facebook: "https://www.facebook.com/johnwick.wick.37625",
    devpost: "https://devpost.com/oaksoekhant182209",
  },

  // TODO(owner): drop the PDF at site/public/resume.pdf, then set "/resume.pdf".
  resumeUrl: "/resume.pdf",

  // TODO(owner): the real .dev domain. Used for canonical URLs and the vCard.
  url: "https://example.dev",

  seo: {
    description:
      "A personal time capsule — who I am and what I love to do. Projects, reading, and collected phrases.",
  },
};

/** Ordered, labelled contact rows — blank fields dropped, never rendered empty. */
export const contactRows: { label: string; href: string; text: string; me?: boolean }[] = [
  { label: "Email", href: `mailto:${site.socials.email}`, text: site.socials.email },
  { label: "GitHub", href: site.socials.github, text: "Mr-Shine09", me: true },
  { label: "LinkedIn", href: site.socials.linkedin, text: "oak-soe-khant", me: true },
  { label: "Instagram", href: site.socials.instagram, text: "oak_soe_khant909", me: true },
  { label: "Facebook", href: site.socials.facebook, text: "Oak Soe Khant", me: true },
  { label: "Devpost", href: site.socials.devpost, text: "oaksoekhant182209", me: true },
  ...(site.resumeUrl ? [{ label: "Résumé", href: site.resumeUrl, text: "resume.pdf" }] : []),
  { label: "vCard", href: "/contact.vcf", text: "contact.vcf" },
].filter((row) => row.href && row.text);
