# Synesthetic AV Sequencer (DeepSeek Prompt Blueprint)

A production-oriented prompt blueprint for generating **audio-reactive color sequences** where palettes, timing, and transitions follow explicit logic.

## Goal

Translate textual mood + rhythmic structure into:

- coherent color themes,
- measurable time-based transitions,
- intensity curves that react to rhythm,
- reusable JSON output for downstream renderers.

## Prompt Template

Use this with DeepSeek models when you need a logical audiovisual sequence.

```text
You are an audiovisual sequencing engine.

Task:
Create a synesthetic color-reaction plan where color themes reflect auditory rhythm in a perfectly logical escalation sequence.

Input:
- Mood: {{mood}}
- Tempo BPM: {{bpm}}
- Time Signature: {{time_signature}}
- Total Duration (seconds): {{duration_s}}
- Sections: {{sections}}  # e.g., intro, build, peak, release
- Preferred Palette Hints: {{palette_hints}}

Rules:
1) Build a section-by-section timeline with exact start/end timestamps.
2) Map rhythmic intensity to color properties:
   - saturation,
   - brightness,
   - hue drift,
   - transition speed.
3) Enforce monotonic escalation from intro -> build -> peak, then controlled release.
4) Every change must include a measurable reason tied to beat density or section energy.
5) Keep transitions smooth and physically plausible for LED/UI playback.
6) Return strictly valid JSON.

Return JSON schema:
{
  "global": {
    "bpm": number,
    "duration_s": number,
    "time_signature": "string",
    "theme": "string"
  },
  "sections": [
    {
      "name": "string",
      "start_s": number,
      "end_s": number,
      "energy": number,
      "palette": ["#RRGGBB"],
      "logic": "why these colors and transitions fit rhythm",
      "animation": {
        "transition_ms": number,
        "pulse_multiplier": number,
        "hue_shift_deg": number,
        "brightness_curve": "string",
        "saturation_curve": "string"
      }
    }
  ],
  "beat_map": [
    {
      "t_s": number,
      "accent": boolean,
      "visual_event": "string"
    }
  ]
}
```

## Example Input

- Mood: Futuristic uplift
- BPM: 128
- Time Signature: 4/4
- Total Duration: 60
- Sections: intro(0-12), build(12-32), peak(32-48), release(48-60)
- Palette hints: cyan, magenta, violet, warm white

## Implementation Notes

- Keep core sequence generation separate from rendering.
- Validate JSON schema before sending to renderer.
- Add guardrails for out-of-range BPM, invalid durations, and malformed sections.
- Use deterministic seeds when reproducibility matters.

## Productization Path

- Expose this as a reusable "Theme-to-Timeline" API.
- Offer presets (club, ambient, cinematic) as paid tiers.
- Add real-time mode for stream overlays and stage visuals.
