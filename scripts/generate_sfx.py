import os
import wave
import subprocess
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFX_DIR = os.path.join(BASE_DIR, "assets", "audio", "sfx")
os.makedirs(SFX_DIR, exist_ok=True)

SR = 44100

def synthesize_scroll_stopper():
    """Impacto cinemático sub-grave con whoosh suave para el segundo 0.0 (Scroll-Stopper)."""
    dur = 1.4
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    
    # Sweep descendente de frecuencia sub-grave (85Hz a 32Hz)
    freq_sweep = 85.0 * np.exp(-t * 2.5) + 32.0
    phase = 2 * np.pi * np.cumsum(freq_sweep) / SR
    sub_bass = np.sin(phase)
    
    # Envolvente de impacto y desvanecimiento
    env_sub = np.exp(-t * 3.2)
    # Aire / textura suave de apertura
    noise = np.random.uniform(-0.15, 0.15, len(t)) * np.exp(-t * 5.0)
    
    audio = (sub_bass * env_sub * 0.9) + (noise * 0.2)
    
    # Normalizar
    max_val = np.max(np.abs(audio)) or 1.0
    audio_int16 = (audio / max_val * 0.92 * 32767).astype(np.int16)
    
    temp_wav = os.path.join(SFX_DIR, "temp_whoosh.wav")
    with wave.open(temp_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(audio_int16.tobytes())
        
    out_mp3 = os.path.join(SFX_DIR, "sfx_scroll_stopper.mp3")
    # Añadir eco espacioso y calidez con FFmpeg
    cmd = [
        "ffmpeg", "-y", "-i", temp_wav,
        "-af", "aecho=0.8:0.7:120|240:0.35|0.2,lowpass=f=450,bass=g=5:f=60",
        "-c:a", "libmp3lame", "-b:a", "192k",
        out_mp3
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    if os.path.exists(temp_wav):
        os.remove(temp_wav)
    print(f"Generated {out_mp3}")

def synthesize_divine_chime():
    """Campanilla celestial armónica de bendición (Divine Chime / Shimmer)."""
    dur = 2.0
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    
    # Armónicos puros de cristal / campana (E6, B6, E7, G#7)
    harmonics = [
        (1318.5, 0.40, 1.8),   # E6
        (1975.5, 0.30, 2.2),   # B6
        (2637.0, 0.20, 2.8),   # E7
        (3322.4, 0.10, 3.4)    # G#7
    ]
    
    chime = np.zeros_like(t)
    for f, amp, decay in harmonics:
        env = np.exp(-t * decay)
        # Sutil modulación de coro / brillo
        shimmer = 1.0 + 0.08 * np.sin(2 * np.pi * 6.0 * t)
        chime += amp * env * shimmer * np.sin(2 * np.pi * f * t)
        
    max_val = np.max(np.abs(chime)) or 1.0
    audio_int16 = (chime / max_val * 0.85 * 32767).astype(np.int16)
    
    temp_wav = os.path.join(SFX_DIR, "temp_chime.wav")
    with wave.open(temp_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(audio_int16.tobytes())
        
    out_mp3 = os.path.join(SFX_DIR, "sfx_divine_chime.mp3")
    cmd = [
        "ffmpeg", "-y", "-i", temp_wav,
        "-af", "aecho=0.85:0.88:140|280|420:0.4|0.25|0.15,highpass=f=600",
        "-c:a", "libmp3lame", "-b:a", "192k",
        out_mp3
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    if os.path.exists(temp_wav):
        os.remove(temp_wav)
    print(f"Generated {out_mp3}")

def synthesize_holy_swell():
    """Riser / Swell suave celestial para transición de escenas."""
    dur = 1.8
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    
    # Crescendo suave
    env = (1.0 - np.cos(np.pi * t / dur)) * 0.5
    freqs = [220.0, 329.6, 440.0, 554.3] # A3, E4, A4, C#5 (acorde cálido de paz)
    
    pad = np.zeros_like(t)
    for f in freqs:
        pad += np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
        
    audio = pad * env
    max_val = np.max(np.abs(audio)) or 1.0
    audio_int16 = (audio / max_val * 0.88 * 32767).astype(np.int16)
    
    temp_wav = os.path.join(SFX_DIR, "temp_swell.wav")
    with wave.open(temp_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(audio_int16.tobytes())
        
    out_mp3 = os.path.join(SFX_DIR, "sfx_holy_swell.mp3")
    cmd = [
        "ffmpeg", "-y", "-i", temp_wav,
        "-af", "aecho=0.8:0.85:100|200:0.4|0.2,lowpass=f=2800",
        "-c:a", "libmp3lame", "-b:a", "192k",
        out_mp3
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    if os.path.exists(temp_wav):
        os.remove(temp_wav)
    print(f"Generated {out_mp3}")

if __name__ == "__main__":
    synthesize_scroll_stopper()
    synthesize_divine_chime()
    synthesize_holy_swell()
    print("All SFX generated successfully in assets/audio/sfx/")
