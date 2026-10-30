"""Align three visual scenes to the *actual* voiceover cue times.

There is no guarantee that TTS uses a constant words-per-second rate. Prefer
word-aligned cues (Whisper) and fall back to a proportion of measured duration.
The CTA remains in the final shot, never becomes a request to draw a comment.
"""
import re
from typing import Optional, Sequence, Tuple

def _words(text):
    return len(re.findall(r"\b[\w']+\b", text or ""))

def compute_scene_breaks(hook: str, body: str, cta: str, duration: float,
                         cues: Optional[Sequence] = None) -> Tuple[float, float]:
    """Return boundaries in seconds: after the hook and before final resolution."""
    if duration < 7.0:
        return (round(duration * 0.23, 2), round(duration * 0.69, 2))
    h, b, c = _words(hook), _words(body), _words(cta)
    total = max(h + b + c, 1)
    first_count = h
    second_count = h + int(b * 0.62)
    first = duration * first_count / total
    second = duration * second_count / total
    if cues:
        spoken = 0
        cue_first = cue_second = None
        for cue in cues:
            spoken += _words(getattr(cue, "text", ""))
            if cue_first is None and spoken >= first_count:
                cue_first = float(getattr(cue, "end_sec", first))
            if cue_second is None and spoken >= second_count:
                cue_second = float(getattr(cue, "end_sec", second))
        if cue_first is not None:
            first = cue_first
        if cue_second is not None:
            second = cue_second
    # Preserve sufficient time for all three scenes, and valid xfade offsets.
    first = min(max(2.6, first), min(duration * 0.40, duration - 4.5))
    second = min(max(first + 2.5, second), duration - 2.4)
    return round(first, 2), round(second, 2)
