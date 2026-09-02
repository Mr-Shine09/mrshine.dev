// Download Open Library covers by ISBN into src/assets/books/<slug>.jpg (Plan.md §7.4).
// Skips existing files. Fails loudly on 404 or the 1×1 placeholder so a missing
// cover is noticed, never silently blank.
import { readdir, readFile, writeFile, mkdir, stat } from "node:fs/promises";
import path from "node:path";

const BOOKS = "src/content/books";
const OUT = "src/assets/books";
await mkdir(OUT, { recursive: true });

let failures = 0;
for (const file of (await readdir(BOOKS)).filter((f) => f.endsWith(".md"))) {
  const slug = file.replace(/\.md$/, "");
  const fm = (await readFile(path.join(BOOKS, file), "utf8")).match(/^---\n([\s\S]*?)\n---/)?.[1] ?? "";
  const isbn = fm.match(/^isbn:\s*"?(\d{13})"?\s*$/m)?.[1];
  if (!isbn) { console.log(`· ${slug}: no isbn, skipped`); continue; }
  const dest = path.join(OUT, `${slug}.jpg`);
  if (await stat(dest).then(() => true, () => false)) { console.log(`· ${slug}: cover exists`); continue; }
  const res = await fetch(`https://covers.openlibrary.org/b/isbn/${isbn}-L.jpg?default=false`);
  const bytes = res.ok ? Buffer.from(await res.arrayBuffer()) : null;
  if (!bytes || bytes.length < 2000) {
    console.error(`✗ ${slug}: no cover for ISBN ${isbn} (HTTP ${res.status}, ${bytes?.length ?? 0} bytes). Try another edition's ISBN.`);
    failures++; continue;
  }
  await writeFile(dest, bytes);
  console.log(`✓ ${slug}: ${bytes.length} bytes → ${dest}`);
}
process.exit(failures ? 1 : 0);
