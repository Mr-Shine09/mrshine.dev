import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
// Imported directly — the `z` re-export from `astro:content` is deprecated.
import { z } from "zod";

/**
 * Content lives in files in the repo. Every schema fails the build BY NAME on
 * an invalid state (HANDOFF §8) — silent fallbacks are how phrases vanish and
 * unfinished books grow ratings.
 */

const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/projects" }),
  schema: ({ image }) =>
    z
      .object({
        title: z.string(),
        /** Controls deck order; lower sorts first. */
        order: z.number().default(99),
        year: z.string(),
        stack: z.array(z.string()).default([]),
        /** One sentence. Front of the card. */
        summary: z.string(),
        image: image().optional(),
        imageAlt: z.string().optional(),
        /** Optional standout stat. */
        metric: z.string().optional(),
        /** Empty = solo. Non-empty renders on the card back — attribution is
         *  not optional (Echo is a three-person project in someone else's repo). */
        collaborators: z.array(z.string()).default([]),
        /** The hackathon or context, e.g. "Hack for Humanity 2026". */
        builtAt: z.string().optional(),
        links: z
          .object({
            github: z.url().optional(),
            devpost: z.url().optional(),
            live: z.url().optional(),
          })
          .default({}),
        /** true = filtered out of the build. Flipping to false is the only
         *  action needed to publish. */
        draft: z.boolean().default(false),
      })
      .superRefine((data, ctx) => {
        if (data.image && !data.imageAlt) {
          ctx.addIssue({
            code: "custom",
            path: ["imageAlt"],
            message: `"${data.title}": an image needs \`imageAlt\` describing what it shows`,
          });
        }
      }),
});

const books = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/books" }),
  schema: z
    .object({
      title: z.string(),
      author: z.string(),
      language: z.enum(["en", "my"]),
      genre: z.enum(["nonfiction", "fiction"]),
      status: z.enum(["reading", "finished", "want"]),
      /** ISO dates. */
      started: z.string().optional(),
      ended: z.string().optional(),
      /** 0–100, only while status is "reading". */
      progress: z.number().min(0).max(100).optional(),
      /** Only once finished. */
      rating: z.union([
        z.literal(1),
        z.literal(2),
        z.literal(3),
        z.literal(4),
        z.literal(5),
      ]).optional(),
      /** Short. Only once finished. */
      review: z.string().optional(),
      /** Drives spine width when present. */
      pageCount: z.number().positive().optional(),
      /** Optional override; otherwise assigned from the mascot palette. */
      spineColor: z.string().optional(),
    })
    .superRefine((data, ctx) => {
      const name = `"${data.title}"`;
      if (data.ended && data.status !== "finished") {
        ctx.addIssue({
          code: "custom",
          path: ["ended"],
          message: `${name}: \`ended\` is set but status is "${data.status}" — only finished books have an end date`,
        });
      }
      if (data.rating !== undefined && data.status !== "finished") {
        ctx.addIssue({
          code: "custom",
          path: ["rating"],
          message: `${name}: \`rating\` is set but status is "${data.status}" — rate it when it's finished`,
        });
      }
      if (data.review && data.status !== "finished") {
        ctx.addIssue({
          code: "custom",
          path: ["review"],
          message: `${name}: \`review\` is set but status is "${data.status}" — review it when it's finished`,
        });
      }
      if (data.progress !== undefined && data.status !== "reading") {
        ctx.addIssue({
          code: "custom",
          path: ["progress"],
          message: `${name}: \`progress\` is set but status is "${data.status}" — progress only means something mid-read`,
        });
      }
    }),
});

/**
 * Phrase colours are THEME tokens, not raw hex and not the mascot palette —
 * ink/accent/muted are contrast-measured AA in both themes (HANDOFF §5.2), so
 * a phrase can never silently vanish in one mode. Fonts validate against the
 * closed six-token set; a typo fails the build instead of silently falling
 * back (HANDOFF §7.4).
 */
export const PHRASE_FONTS = [
  "geist",
  "grotesque",
  "condensed",
  "hand",
  "slab",
  "serif",
] as const;
export const PHRASE_COLORS = ["ink", "accent", "muted"] as const;

const phrases = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/phrases" }),
  schema: z.object({
    /** The phrase itself — words, not paragraphs. */
    text: z.string(),
    /** Who said it, where it came from. "Unknown" is honest; invented is not. */
    source: z.string().optional(),
    /** Optional gloss — use rarely; a gloss on a phrase that lands kills it. */
    meaning: z.string().optional(),
    /** ISO date. Stored on every phrase, displayed quietly. */
    dateAdded: z.string(),
    style: z.object({
      font: z.enum(PHRASE_FONTS),
      size: z.enum(["sm", "md", "lg", "xl"]),
      color: z.enum(PHRASE_COLORS),
      weight: z.number().optional(),
      italic: z.boolean().optional(),
    }),
    /** Cross-link to a book on the Reading List. Checked against the books
     *  collection at build time in /w-phrases — a dead link fails the build. */
    bookSlug: z.string().optional(),
  }),
});

export const collections = { projects, books, phrases };
