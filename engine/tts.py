import asyncio
import edge_tts
from dataclasses import dataclass
from datetime import timedelta
from typing import List, Tuple

VOICES = {
    "christopher": {
        "id": "en-US-ChristopherNeural",
        "name": "Christopher (Solemn, Deep & Reverent - Best for Jesus)",
        "gender": "Male"
    },
    "guy": {
        "id": "en-US-GuyNeural",
        "name": "Guy (Passionate, Emotional & Direct)",
        "gender": "Male"
    },
    "brian": {
        "id": "en-US-BrianNeural",
        "name": "Brian (Calm, Warm & Reassuring)",
        "gender": "Male"
    },
    "andrew": {
        "id": "en-US-AndrewMultilingualNeural",
        "name": "Andrew (Modern, Expressive & Relatable)",
        "gender": "Male"
    },
    "jenny": {
        "id": "en-US-JennyNeural",
        "name": "Jenny (Gentle, Caring & Comforting)",
        "gender": "Female"
    }
}

@dataclass
class CueItem:
    start_sec: float
    end_sec: float
    text: str

async def synthesize_speech(text: str, voice_id: str, output_path: str, rate: str = "+0%") -> List[CueItem]:
    """
    Synthesize audio using Edge-TTS and capture boundary timestamps.
    """
    comm = edge_tts.Communicate(text, voice_id, rate=rate)
    submaker = edge_tts.SubMaker()
    
    with open(output_path, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)
                
    result_cues = []
    for cue in submaker.cues:
        result_cues.append(
            CueItem(
                start_sec=cue.start.total_seconds(),
                end_sec=cue.end.total_seconds(),
                text=cue.content
            )
        )
    return result_cues

def get_available_voices():
    return [
        {"key": k, "id": v["id"], "name": v["name"], "gender": v["gender"]}
        for k, v in VOICES.items()
    ]
