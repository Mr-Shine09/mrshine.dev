---
title: Echo
order: 2
year: "2026"
stack: ["Flutter", "Dart", "Kotlin", "Swift", "SQLite", "Python 3"]
summary: A Flutter prototype for receiving, storing, and relaying emergency alerts between nearby devices over Bluetooth Low Energy when an internet connection is unavailable.
collaborators: ["aadityad12", "shahxsheel", "Mr-Shine09"]
builtAt: "Hack for Humanity 2026 (V3) — SCU"
links:
  github: https://github.com/aadityad12/Echo
  # TODO(owner): the H4H Devpost submission URL, if there is one.
draft: false
# TODO(owner): drop echo-hero into src/assets/projects/ and add
#   image: ../../assets/projects/echo-hero.png
#   imageAlt: Alert list with the MESH ACTIVE badge lit and severity chips down the feed.
---

Alert identifiers don't appear consistently in BLE advertisements across
platforms. Without a stable ID visible at advertisement time, a device can't
tell whether an alert it's hearing is one it has already relayed — which breaks
background deduplication and makes iOS-to-Android relay coordination
unreliable.

Devices act as both BLE client and server, so alerts propagate mesh-like. A
custom indexed-chunk protocol with gzip moves alerts that don't fit in a single
BLE payload. On-device translation into 22 languages with native
text-to-speech, so an alert reaches someone who doesn't read English.
