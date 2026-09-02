---
title: VisionAssist
order: 3
year: "2026"
stack: ["Python", "YOLOv8n", "Raspberry Pi 5", "Arducam IMX708", "Piper TTS", "Flask"]
summary: Wearable obstacle detection and spoken navigation for the visually impaired. Runs fully offline on a Raspberry Pi 5.
collaborators: []
builtAt: "De Anza College, Infineon-sponsored capstone"
links:
  github: https://github.com/Mr-Shine09/VisionAssist
image: ../../assets/projects/visionassist-hero.jpg
imageAlt: The 3D-printed head-mounted enclosure holding a Raspberry Pi 5 with an Arducam camera on the lid.
draft: false
---

There is no depth sensor. Distance comes from the pinhole relation between a
known object height, the focal length, and the bounding-box height YOLO
reports — and it overestimates at close range, because a partially visible
chair produces a short box. The zones were widened to compensate; the honest
fix, edge-clip detection, is on the roadmap.
