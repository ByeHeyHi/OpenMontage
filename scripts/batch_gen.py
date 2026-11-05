import time
from pathlib import Path
from tools.video.wan_video import WanVideo

clips = [
    {
        "id": "clip_1b",
        "prompt": "3D stylized cartoon CGI animation, Pixar and Clash Royale aesthetic. A friendly 45-year-old male bartender with a neat stylish mustache, wearing a red checkered flannel shirt and brown leather apron. He is wiping a glass with a clean cloth behind the wooden bar counter, smiling with curiosity and talking to a customer. Warm golden pub tavern lighting, soft bokeh, expressive facial features.",
        "num_frames": 81,
        "path": "projects/002-short-pub-whisky/assets/video/clip_1b.mp4"
    },
    {
        "id": "clip_2a",
        "prompt": "3D stylized cartoon CGI animation, Pixar and Clash Royale aesthetic. Close-up on the face of a young man with brown hair and black leather jacket sitting at a pub bar. He speaks with a shy, subtle half-smile, looking slightly awkward. Warm cozy tavern bokeh background, amber lighting, detailed stylized facial animation, expressive eyes.",
        "num_frames": 65,
        "path": "projects/002-short-pub-whisky/assets/video/clip_2a.mp4"
    },
    {
        "id": "clip_2b",
        "prompt": "3D stylized cartoon CGI animation, Pixar and Clash Royale aesthetic. Medium shot of the 45-year-old bartender with mustache in red checkered shirt and brown apron. He has a broad delighted grin, laughing happily and clapping a hand near the customer shoulder while placing a fifth whiskey shot glass on the polished wooden counter. Warm glowing pub interior, cheerful lively atmosphere.",
        "num_frames": 81,
        "path": "projects/002-short-pub-whisky/assets/video/clip_2b.mp4"
    },
    {
        "id": "clip_3a",
        "prompt": "3D stylized cartoon CGI animation, Pixar and Clash Royale aesthetic. Tight close-up on the young man face at the bar. His eyebrows furrow into an exaggerated cartoon grimace of intense disgust and revulsion, curling his lip in distaste while pushing the whiskey glass away with his hand. Warm tavern background, dramatic comedic expression.",
        "num_frames": 81,
        "path": "projects/002-short-pub-whisky/assets/video/clip_3a.mp4"
    },
    {
        "id": "clip_3b",
        "prompt": "3D stylized cartoon CGI animation, Pixar and Clash Royale aesthetic. Medium close-up of the young man with brown hair at the wooden pub bar surrounded by small empty shot glasses. He speaks with a nauseated, disgusted and defeated expression, looking weary. Warm cozy pub lighting, amber glow, expressive comedic 3D CGI acting.",
        "num_frames": 81,
        "path": "projects/002-short-pub-whisky/assets/video/clip_3b.mp4"
    }
]

def main():
    wan = WanVideo()
    print("Starting batch clip generation (5 clips)...")

    for idx, c in enumerate(clips, 1):
        c_path = Path(c["path"])
        if c_path.exists() and c_path.stat().st_size > 10000:
            print(f"[{idx}/5] {c['id']} already exists ({c_path.stat().st_size} bytes), skipping.")
            continue

        print(f"[{idx}/5] Generating {c['id']} ({c['num_frames']} frames)...")
        t0 = time.time()
        res = wan.execute({
            "prompt": c["prompt"],
            "model_variant": "wan2.1-1.3b",
            "operation": "text_to_video",
            "width": 480,
            "height": 848,
            "num_frames": c["num_frames"],
            "fps": 16,
            "num_inference_steps": 20,
            "guidance_scale": 5.0,
            "enable_model_offload": True,
            "offload_mode": "model",
            "output_path": str(c_path)
        })
        elapsed = round(time.time() - t0, 1)
        if not res.success:
            print(f"[{idx}/5] Error on {c['id']}: {res.error}")
            break
        else:
            print(f"[{idx}/5] Success on {c['id']} in {elapsed}s! Output size: {c_path.stat().st_size} bytes")

    print("Batch generation loop finished.")

if __name__ == "__main__":
    main()

