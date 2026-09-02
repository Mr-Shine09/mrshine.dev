import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "zod";

/**
 * Content lives in files. Every schema fails the build BY NAME on an invalid
 * state (Plan.md §8) — silent fallbacks are how unfinished books grow ratings.
 */

export const MYANMAR_FONT_READY = false; // flip to true once a Myanmar-capable font is registered in astro.config.mjs (Plan.md §4.3)

const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/projects" }),
  schema: ({ image }) =>
    z
      .object({
        title: z.string(),
        order: z.number().default(99),
        year: z.string(),
        stack: z.array(z.string()).default([]),
        summary: z.string(),
        image: image().optional(),
        imageAlt: z.string().optional(),
        /** Empty = no line rendered. Never claims "solo". */
        collaborators: z.array(z.string()).default([]),
        builtAt: z.string().optional(),
        links: z.object({ github: z.url().optional(), devpost: z.url().optional(), live: z.url().optional() }).default({}),
        draft: z.boolean().default(false),
      })
      .superRefine((data, ctx) => {
        if (data.image && !data.imageAlt) {
          ctx.addIssue({ code: "custom", path: ["imageAlt"], message: `"${data.title}": an image needs \`imageAlt\` describing what it shows` });
        }
      }),
});

const books = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/books" }),
  schema: ({ image }) =>
    z
      .object({
        title: z.string(),
        author: z.string(),
        /** ISBN-13 digits only. Drives `npm run covers`. */
        isbn: z.string().regex(/^\d{13}$/, "isbn must be 13 digits, no dashes").optional(),
        /** Output of `npm run covers`; Astro fails the build if the file is missing. */
        cover: image().optional(),
        language: z.enum(["en", "my"]),
        genre: z.enum(["nonfiction", "fiction"]),
        status: z.enum(["reading", "finished"]),
        started: z.string().optional(),
        ended: z.string().optional(),
        progress: z.number().min(0).max(100).optional(),
        rating: z.union([z.literal(1), z.literal(2), z.literal(3), z.literal(4), z.literal(5)]).optional(),
        review: z.string().optional(),
        /** A brief note, any status. */
        note: z.string().optional(),
        pageCount: z.number().positive().optional(),
      })
      .superRefine((data, ctx) => {
        const name = `"${data.title}"`;
        const finishedOnly = ["ended", "rating", "review"] as const;
        for (const key of finishedOnly) {
          if (data[key] !== undefined && data.status !== "finished") {
            ctx.addIssue({ code: "custom", path: [key], message: `${name}: \`${key}\` is set but status is "${data.status}" — only finished books have it` });
          }
        }
        if (data.progress !== undefined && data.status !== "reading") {
          ctx.addIssue({ code: "custom", path: ["progress"], message: `${name}: \`progress\` is set but status is "${data.status}" — progress only means something mid-read` });
        }
        if (data.isbn && !data.cover) {
          ctx.addIssue({ code: "custom", path: ["cover"], message: `${name}: has an isbn but no \`cover\` — run \`npm run covers\` and add \`cover: ../../assets/books/<slug>.jpg\`` });
        }
        if (data.language === "my" && !MYANMAR_FONT_READY) {
          ctx.addIssue({ code: "custom", path: ["language"], message: `${name}: Burmese needs a Myanmar-capable font registered in astro.config.mjs first (Plan.md §4.3)` });
        }
      }),
});

const achievements = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/achievements" }),
  schema: z.object({
    title: z.string(),
    org: z.string(),
    year: z.string().regex(/^\d{4}$/, "year must be four digits"),
    kind: z.enum(["competition", "hackathon", "award", "other"]),
    link: z.url().optional(),
    order: z.number().default(99),
  }),
});

export const collections = { projects, books, achievements };
