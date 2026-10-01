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
    Renders high-quality 1080x1920 vertical Reel with smooth Ken Burns animation and burned ASS subtitles.
    """
    duration = get_audio_duration(audio_path)
    total_frames = int((duration + 0.5) * fps)
    
    # Calculate subtle zoom speed: zoom from 1.0 to 1.10 over total_frames
    zoom_step = 0.10 / max(total_frames, 1)

    # Windows path formatting for FFmpeg ass filter
    # FFmpeg ass filter requires forward slashes and colon escaping if absolute
    norm_ass = os.path.abspath(ass_path).replace("\\", "/").replace(":", "\\:")
    
    # Filter complex:
    # 1. Scale image to at least 1080x1920, center-crop.
    # 2. zoompan: slow zoom towards upper-center (face).
    # 3. ass: burn subtitles.
    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        f"zoompan=z='min(zoom+{zoom_step:.6f},1.12)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih*0.4-(ih*0.4/zoom)':s=1080x1920:fps={fps},"
        f"ass='{norm_ass}'[v]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_mp4_path
    ]

    print("Running FFmpeg render...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("FFmpeg Error:", result.stderr)
        raise RuntimeError(f"FFmpeg rendering failed: {result.stderr[-500:]}")
        
    print(f"Render complete: {output_mp4_path} ({os.path.getsize(output_mp4_path)} bytes)")
    return output_mp4_path
