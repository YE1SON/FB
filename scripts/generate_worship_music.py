import os
import wave
import subprocess
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SR = 44100
DUR = 65.0  # 65 seconds (covers any reel and loops seamlessly)

def create_pad(freqs, piano_notes, filename, reverb_preset="peace"):
    t = np.linspace(0, DUR, int(SR * DUR), endpoint=False)
    left = np.zeros_like(t)
    right = np.zeros_like(t)

    # Pad harmonics & breathing LFO
    for i, f in enumerate(freqs):
        amp = 0.16 / (i * 0.45 + 1.0)
        lfo = 0.72 + 0.28 * np.sin(2 * np.pi * 0.10 * t + i * 0.7)
        
        # Subtle stereo detuning (wide ambient spread)
        sig_l = amp * lfo * (np.sin(2 * np.pi * (f - 0.22) * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.1 * np.sin(6 * np.pi * f * t))
        sig_r = amp * lfo * (np.sin(2 * np.pi * (f + 0.22) * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.1 * np.sin(6 * np.pi * f * t))
        
        left += sig_l
        right += sig_r

    # Melodic notes / chimes
    if piano_notes:
        for idx, (note_t, note_f) in enumerate(piano_notes):
            if note_t + 5.0 < DUR:
                mask = (t >= note_t) & (t < note_t + 5.0)
                dt = t[mask] - note_t
                env = np.exp(-dt * 0.75) * 0.22
                tone = env * (np.sin(2 * np.pi * note_f * dt) + 0.4 * np.sin(4 * np.pi * note_f * dt) + 0.15 * np.sin(6 * np.pi * note_f * dt))
                # Alternate panning
                pan = 0.3 if idx % 2 == 0 else 0.7
                left[mask] += tone * (1.0 - pan)
                right[mask] += tone * pan

    # Normalize volume
    max_val = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-5)
    left = (left / max_val * 0.88 * 32767).astype(np.int16)
    right = (right / max_val * 0.88 * 32767).astype(np.int16)

    stereo = np.empty((left.size + right.size,), dtype=np.int16)
    stereo[0::2] = left
    stereo[1::2] = right

    temp_wav = os.path.join(OUTPUT_DIR, "temp.wav")
    with wave.open(temp_wav, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(stereo.tobytes())

    target_mp3 = os.path.join(OUTPUT_DIR, filename)

    if reverb_preset == "peace":
        af = "aecho=0.8:0.88:80|180|320:0.4|0.25|0.15,lowpass=f=2900"
    elif reverb_preset == "celestial":
        af = "aecho=0.85:0.90:100|220|400:0.45|0.3|0.2,lowpass=f=3400,highpass=f=80"
    else:
        af = "aecho=0.75:0.80:90|200:0.35|0.2,lowpass=f=2400"

    cmd = [
        "ffmpeg", "-y", "-i", temp_wav,
        "-af", af,
        "-c:a", "libmp3lame", "-b:a", "192k",
        target_mp3
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(temp_wav):
        os.remove(temp_wav)
    print(f"Generated {filename} ({os.path.getsize(target_mp3)} bytes)")

if __name__ == "__main__":
    print("Generating ambient worship tracks...")
    
    # 1. Piano & Peace (D Major: D2, A2, D3, F#3, A3, D4)
    create_pad(
        freqs=[73.42, 110.0, 146.83, 185.0, 220.0, 293.66],
        piano_notes=[(2.0, 293.66), (8.5, 369.99), (15.0, 440.0), (22.0, 587.33), (29.0, 440.0), (36.0, 369.99), (43.0, 293.66), (50.0, 440.0)],
        filename="worship_piano_peace.mp3",
        reverb_preset="peace"
    )

    # 2. Celestial Strings of Hope (G Major: G2, D3, G3, B3, D4, F#4)
    create_pad(
        freqs=[98.0, 146.83, 196.0, 246.94, 293.66, 369.99],
        piano_notes=[(3.0, 392.0), (10.0, 493.88), (18.0, 587.33), (26.0, 739.99), (34.0, 587.33), (42.0, 493.88), (51.0, 392.0)],
        filename="celestial_strings_hope.mp3",
        reverb_preset="celestial"
    )

    # 3. Midnight Prayer & Comfort (A Minor: A2, E3, A3, C4, E4)
    create_pad(
        freqs=[82.41, 110.0, 164.81, 220.0, 261.63, 329.63],
        piano_notes=[(4.0, 220.0), (12.0, 261.63), (20.0, 329.63), (28.0, 440.0), (37.0, 329.63), (46.0, 261.63), (54.0, 220.0)],
        filename="midnight_prayer_acoustic.mp3",
        reverb_preset="night"
    )

    print("All 3 worship tracks successfully created!")
