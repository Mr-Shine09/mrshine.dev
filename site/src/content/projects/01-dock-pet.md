---
title: Dock Pet
weight: text-only
order: 1
year: "2026"
stack: ["Swift", "AppKit", "Python"]
summary: A pixel-art mascot that lives on the macOS desktop and reacts to what the machine is doing.
metric: 16 animation states, 12 colours, 0 external art dependencies
links:
  github: https://github.com/Mr-Shine09/dock-pet
---

TODO(owner): rewrite this in your own voice — lead with what was *hard*, not
what was used. The notes below are pulled from the project's own atlas contract
and are true, but they are a starting point, not your writeup.

The hard part was never drawing the character. It was making sixteen separate
animation states feel like one creature. Every frame is authored against a
fixed contract: a 96×112 cell, a shared ground baseline at `y=102`, binary
alpha, and a frozen twelve-colour palette that props and effects are not
allowed to extend.

That contract is enforced, not just documented — the frame checks reject any
sprite that crosses the four-pixel cell guard or drifts off the baseline, which
is what keeps the mascot from subtly changing size as it walks.
