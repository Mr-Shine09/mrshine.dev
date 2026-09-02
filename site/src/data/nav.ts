/** The five sections, in page order. TopBar and index.astro both read this. */
export const sections = [
  { id: "about", label: "About" },
  { id: "highlights", label: "Highlights" },
  { id: "projects", label: "Projects" },
  { id: "personal", label: "Personal" },
  { id: "contact", label: "Contact" },
] as const;
export type SectionId = (typeof sections)[number]["id"];
