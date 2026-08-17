import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
// Imported directly — the `z` re-export from `astro:content` is deprecated.
import { z } from "zod";

/**
 * Content lives in files in the repo (locked decision #2). A Keystatic admin
 * panel can be layered on these same schemas later — that is why the shapes
 * are strict and every field is described.
 */

const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/projects" }),
  schema: ({ image }) =>
    z
      .object({
        title: z.string(),
        /** Card treatment. Only `featured` and `standard` show an image. */
        weight: z.enum(["featured", "standard", "text-only"]),
        /** Controls document order; lower sorts first. */
        order: z.number().default(99),
        stack: z.array(z.string()).default([]),
        /** One sentence. Appears on the card. */
        summary: z.string(),
        image: image().optional(),
        imageAlt: z.string().optional(),
        links: z
          .object({
            github: z.url().optional(),
            live: z.url().optional(),
          })
          .default({}),
        /** Optional standout stat, e.g. "2nd place, hackathon 2026". */
        metric: z.string().optional(),
        year: z.string().optional(),
      })
      .superRefine((data, ctx) => {
        if (data.weight !== "text-only" && !data.image) {
          ctx.addIssue({
            code: "custom",
            path: ["image"],
            message: `weight "${data.weight}" renders an image, so \`image\` is required (use weight: text-only otherwise)`,
          });
        }
        if (data.image && !data.imageAlt) {
          ctx.addIssue({
            code: "custom",
            path: ["imageAlt"],
            message: "an image needs `imageAlt` describing what it shows",
          });
        }
      }),
});

const books = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/books" }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      author: z.string(),
      status: z.enum(["current", "past"]),
      /** Percent complete. Only meaningful while `status: current`. */
      progress: z.number().min(0).max(100).default(0),
      /** What it is about, one line. */
      oneLiner: z.string(),
      /** The "why now" line — why this book, at this moment. */
      whyReading: z.string().optional(),
      cover: image().optional(),
      finished: z.string().optional(),
    }),
});

const hobbies = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/hobbies" }),
  schema: z.object({
    title: z.string(),
    blurb: z.string(),
    order: z.number().default(99),
    /** Must name a row in the atlas contract. */
    spriteState: z.enum([
      "offline",
      "idle",
      "working",
      "ideating",
      "waiting",
      "success",
      "failure",
      "sleeping",
      "paused",
      "walk-right",
      "walk-left",
      "sit-shake-right",
      "sit-shake-left",
      "hanging",
      "hand-sign",
    ]),
  }),
});

export const collections = { projects, books, hobbies };
