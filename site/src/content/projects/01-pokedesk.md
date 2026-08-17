---
title: PokeDesk
order: 1
year: "2026"
stack: ["Swift", "SwiftUI", "AppKit", "Python 3", "XcodeGen"]
summary: A tiny pixel-art mascot that lives at the bottom of your Mac's screen and shows, at a glance, what your coding agent is doing.
collaborators: []
links:
  github: https://github.com/Mr-Shine09/PokeDesk
draft: false
# TODO(owner): drop pokedesk-hero into src/assets/projects/ and add
#   image: ../../assets/projects/pokedesk-hero.png
#   imageAlt: Two pixel mascots on a purple desktop — one working at a desk, one walking.
---

The hard part was never drawing the character. It was making sixteen separate
animation states feel like one creature. Every frame is authored against a
fixed contract: a 96×112 cell, a shared ground baseline at `y=102`, binary
alpha, and a frozen twelve-colour palette that props and effects are not
allowed to extend. That contract is enforced, not just documented — the frame
checks reject any sprite that crosses the four-pixel cell guard or drifts off
the baseline, which is what keeps the mascot from subtly changing size as it
walks.

Chat detection rests on a single English UI string in the Claude desktop app —
one string I don't control — so the feature is opt-in and asks for
Accessibility permission for exactly that reason.
