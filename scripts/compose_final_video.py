import subprocess
import time
from pathlib import Path

def main():
    project_dir = Path("projects/002-short-pub-whisky")
    output_mp4 = project_dir / "final_joke_whisky.mp4"
    renders_dir = project_dir / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)
    canonical_output = renders_dir / "final.mp4"

    # Input files
    v1a = project_dir / "assets/video/clip_1a.mp4"
    v1b = project_dir / "assets/video/clip_1b.mp4"
    v2a = project_dir / "assets/video/clip_2a.mp4"
    v2b = project_dir / "assets/video/clip_2b.mp4"
    v3a = project_dir / "assets/video/clip_3a.mp4"
    v3b = project_dir / "assets/video/clip_3b.mp4"

    a_bgm = project_dir / "assets/music/bgm_pub_jazz.mp3"
    a_sfx = project_dir / "assets/music/sfx_pub_ambience.mp3"

    v1b_tts = project_dir / "assets/audio/voice_1b_barman.mp3"
    v2a_tts = project_dir / "assets/audio/voice_2a_client.mp3"
    v2b_tts = project_dir / "assets/audio/voice_2b_barman.mp3"
    v3a_tts = project_dir / "assets/audio/voice_3a_client.mp3"
    v3b_tts = project_dir / "assets/audio/voice_3b_client.mp3"

    subtitles_ass = project_dir / "assets/subtitles.ass"

    # We need forward slashes for ffmpeg filter path
    sub_filter_path = str(subtitles_ass.resolve()).replace("\\", "/")
    # Escape colons for ffmpeg filter syntax (e.g. C\:...)
    if ":" in sub_filter_path:
        drive, rest = sub_filter_path.split(":", 1)
        sub_filter_path = f"{drive}\\:{rest}"

    print(f"Composing final video to {output_mp4}...")
    t0 = time.time()

    # Filter complex construction:
    # Scale each video to 1080x1920, trim/pad to scene length, set pts
    # Scene 1a: 0 to 3.0s (3.0s)
    # Scene 1b: 3.0 to 8.5s (5.5s)
    # Scene 2a: 8.5 to 12.5s (4.0s)
    # Scene 2b: 12.5 to 18.5s (6.0s)
    # Scene 3a: 18.5 to 23.5s (5.0s)
    # Scene 3b: 23.5 to 30.0s (6.5s)
    filter_complex = (
        "[0:v]scale=1080:1920:flags=lanczos,tpad=stop_mode=clone:stop_duration=1.0,trim=duration=3.0,setpts=PTS-STARTPTS,fps=30[v0];"
        "[1:v]scale=1080:1920:flags=lanczos,tpad=stop_mode=clone:stop_duration=1.5,trim=duration=5.5,setpts=PTS-STARTPTS,fps=30[v1];"
        "[2:v]scale=1080:1920:flags=lanczos,tpad=stop_mode=clone:stop_duration=1.0,trim=duration=4.0,setpts=PTS-STARTPTS,fps=30[v2];"
        "[3:v]scale=1080:1920:flags=lanczos,tpad=stop_mode=clone:stop_duration=1.5,trim=duration=6.0,setpts=PTS-STARTPTS,fps=30[v3];"
        "[4:v]scale=1080:1920:flags=lanczos,tpad=stop_mode=clone:stop_duration=1.0,trim=duration=5.0,setpts=PTS-STARTPTS,fps=30[v4];"
        "[5:v]scale=1080:1920:flags=lanczos,tpad=stop_mode=clone:stop_duration=2.0,trim=duration=6.5,setpts=PTS-STARTPTS,fps=30[v5];"
        "[v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0[vcat];"
        f"[vcat]subtitles=filename='{sub_filter_path}'[vfinal];"
        # Audio delays
        "[8:a]adelay=3300|3300,volume=1.0[a_1b];"
        "[9:a]adelay=9000|9000,volume=1.0[a_2a];"
        "[10:a]adelay=12800|12800,volume=1.0[a_2b];"
        "[11:a]adelay=19500|19500,volume=1.0[a_3a];"
        "[12:a]adelay=24200|24200,volume=1.0[a_3b];"
        "[6:a]volume=0.22,afade=t=out:st=28.0:d=2.0[abgm];"
        "[7:a]volume=0.18[asfx];"
        "[a_1b][a_2a][a_2b][a_3a][a_3b][abgm][asfx]amix=inputs=7:duration=first:dropout_transition=2[afinal]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(v1a),
        "-i", str(v1b),
        "-i", str(v2a),
        "-i", str(v2b),
        "-i", str(v3a),
        "-i", str(v3b),
        "-i", str(a_bgm),
        "-i", str(a_sfx),
        "-i", str(v1b_tts),
        "-i", str(v2a_tts),
        "-i", str(v2b_tts),
        "-i", str(v3a_tts),
        "-i", str(v3b_tts),
        "-filter_complex", filter_complex,
        "-map", "[vfinal]",
        "-map", "[afinal]",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", "30.0",
        str(output_mp4)
    ]

    subprocess.check_call(cmd)
    elapsed = round(time.time() - t0, 2)
    print(f"Render completed in {elapsed}s!")
    print(f"Saved deliverable to {output_mp4} (size: {output_mp4.stat().st_size} bytes)")

    # Also copy to canonical renders/final.mp4 for OpenMontage convention
    import shutil
    shutil.copyfile(output_mp4, canonical_output)
    print(f"Copied to canonical renders path: {canonical_output}")

if __name__ == "__main__":
    main()

