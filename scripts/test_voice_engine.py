import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import engine.tts as tts

def main():
    avail = tts.check_engine_availability()
    print("Engine availability:", avail)

    voices = tts.get_available_voices()
    print(f"Available voices count: {len(voices)}")
    for v in voices:
        print(f" - {v['key']}: {v['name']} ({v['engine']})")

    async def run_test():
        # Test 1: Kokoro Adam
        cues = await tts.synthesize_speech("May the peace of Jesus guard your home tonight.", "adam", "outputs/test_adam.mp3")
        print(f"\n[ADAM KOKORO TEST SUCCESS]: Generated outputs/test_adam.mp3 with cues: {len(cues)}")
        for c in cues:
            print(f"   {c.start_sec:.2f}s - {c.end_sec:.2f}s: {c.text}")

        # Test 2: Edge-TTS Christopher
        cues_edge = await tts.synthesize_speech("May the peace of Jesus guard your home tonight.", "christopher", "outputs/test_christopher.mp3")
        print(f"\n[CHRISTOPHER EDGE TEST SUCCESS]: Generated outputs/test_christopher.mp3 with cues: {len(cues_edge)}")
        for c in cues_edge:
            print(f"   {c.start_sec:.2f}s - {c.end_sec:.2f}s: {c.text}")

    asyncio.run(run_test())

if __name__ == "__main__":
    main()
