import os
import subprocess
import shutil

def get_audio_duration(audio_path: str) -> float:
    """Get precise duration of audio file using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def render_reel(
    image_path: str,
    audio_path: str,
    ass_path: str,
    output_mp4_path: str,
    fps: int = 30
) -> str:
    """
    Renders high-quality 1080x1920 vertical Reel with smooth, dynamic Ken Burns camera zoom-in animation
    towards Jesus' face and burned ASS dynamic subtitles.
    """
    duration = get_audio_duration(audio_path)
    total_frames = int((duration + 0.5) * fps)
    
    # Velocidad de zoom dinámico: acercamiento progresivo y fluido del 1.0 hasta 1.25 durante todo el audio
    zoom_speed = 0.22 / max(total_frames, 1)

    # Windows path formatting for FFmpeg ass filter
    norm_ass = os.path.abspath(ass_path).replace("\\", "/").replace(":", "\\:")
    
    # Cadena de filtros FFmpeg:
    # 1. Escala la imagen a 1080x1920 manteniendo aspecto y recorta sobrante
    # 2. zoompan: recibe la imagen y genera `total_frames` fotogramas realizando un acercamiento (zoom-in)
    #    constante y cinematográfico centrado en el rostro de Jesús (x=50%, y=35%).
    # 3. ass: quema los subtítulos dinámicos sincronizados palabra por palabra.
    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"zoompan=z='min(zoom+{zoom_speed:.6f},1.26)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih*0.35-(ih*0.35/zoom)':s=1080x1920:fps={fps},"
        f"ass='{norm_ass}'[v]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-threads", "2",
        "-i", image_path,
        "-i", audio_path,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_mp4_path
    ]

    print(f"Running FFmpeg render with smooth zoom-in ({total_frames} frames)...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("FFmpeg Error:", result.stderr)
        raise RuntimeError(f"FFmpeg rendering failed: {result.stderr[-500:]}")
        
    print(f"Render complete: {output_mp4_path} ({os.path.getsize(output_mp4_path)} bytes)")
    return output_mp4_path
