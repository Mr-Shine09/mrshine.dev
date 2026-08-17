/**
 * Site-wide facts.
 *
 * Values marked TODO(owner) are placeholders chosen so the page renders and can
 * be reviewed — they are not researched claims. Replace them before deploying.
 */

export type SiteConfig = {
  name: string;
  role: string;
  location: string;
  tagline: string;
  /** Any social left as "" is dropped from the page rather than rendered empty. */
  socials: { github: string; linkedin: string; email: string };
  resumeUrl: string;
  url: string;
  seo: { description: string };
};

// Annotated rather than `as const`: the empty placeholders must stay typed as
// `string`, or narrowing them to their literal `""` makes the "drop it if
// blank" checks unreachable.
export const site: SiteConfig = {
  name: "Oak Soe Khant",
  // TODO(owner): real programme and school.
  role: "Computer Engineering student",
  // TODO(owner): city, country.
  location: "TODO: your city",
  // TODO(owner): one line, personal register — not a job title restated.
  tagline:
    "I build small, careful things — and read old books about why people build at all.",

  socials: {
    github: "https://github.com/Mr-Shine09",
    // TODO(owner): LinkedIn URL, or delete this line to drop it from the page.
    linkedin: "",
    email: "oaksoekhant182209@gmail.com",
  },

  // TODO(owner): drop the PDF at site/public/resume.pdf. Until it exists, set
  // this to "" and the Résumé button removes itself.
  resumeUrl: "",

  /** Used for canonical URLs and the vCard. TODO(owner): the real domain. */
  url: "https://example.dev",

  seo: {
    description:
      "Portfolio and personal introduction — projects built, what I'm reading now, and where I'm heading next.",
  },
};
