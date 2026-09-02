---
title: Look-Out
order: 2
year: "2026"
stack: ["Python 3.11", "FastAPI", "Redis Stack", "Vite", "Ollama / Claude", "Browserbase"]
summary: The first alert tool built to notify you less — semantic dedup in Redis vector search plus an LLM relevance judge, so only genuinely new and relevant items surface.
collaborators: []
builtAt: "UC Berkeley AI Hackathon 2026"
links:
  github: https://github.com/Mr-Shine09/Look-Out
image: ../../assets/projects/lookout-eye.png
imageAlt: The Lookout logo — a single watchful eye.
draft: false
---

Every alert tool is built to notify you more. Lookout is a suppression engine:
for each change it detects, it asks whether it has effectively shown you this
already (a semantic-duplicate check against alert history in Redis vector
search) and whether it actually matters (an LLM judge against a spec compiled
from your plain-English ask). It only surfaces an alert when both clear the bar.
