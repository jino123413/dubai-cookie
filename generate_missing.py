"""
Generate missing cookies 1-12 using the same prompts as generate_cookies.py.
"""

import urllib.request
import json
import time
import os
import shutil
from pathlib import Path

COMFYUI_URL = "http://127.0.0.1:8188"
OUTPUT_DIR = Path(r"C:\Users\USER-PC\Desktop\appintoss-project\dubai-cookie\public\cookies")
COMFYUI_OUTPUT = Path(r"C:\Users\USER-PC\Downloads\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\output")

WIDTH = 768
HEIGHT = 1152
FINAL_WIDTH = 384
FINAL_HEIGHT = 576

BASE_PROMPT = (
    "a single cute chibi mascot character shaped like a round pastry, "
    "2d digital art, anime style illustration, simple flat shading, "
    "bold black outlines, cel shading, the character has tiny dot eyes and a small happy mouth, "
    "stubby tiny arms and legs, the body is a round layered pastry with green cream filling visible, "
    "solid pastel color background, children book illustration style, "
    "Sanrio character design, LINE Friends style mascot"
)

COOKIE_DATA = {
    1: {"name": "Strawberry Sprinkle", "deco": "heart-shaped pink sprinkles, strawberry drizzle"},
    2: {"name": "Red Velvet Gold", "deco": "red velvet glaze, bold gold leaf stripes"},
    3: {"name": "Lavender Dream", "deco": "dried lavender flowers, soft purple powder dusting"},
    4: {"name": "Rainbow Joy", "deco": "rainbow sprinkles, bright yellow glaze coating"},
    5: {"name": "Galaxy Swirl", "deco": "purple marble chocolate swirl, silver star-shaped glitter"},
    6: {"name": "Orange Flame", "deco": "orange zest garnish, fiery red caramel drizzle pattern"},
    7: {"name": "Cinnamon Cloud", "deco": "cinnamon heavy dusting, mini marshmallows on top"},
    8: {"name": "Tropical Paradise", "deco": "coconut flakes, colorful tropical fruit pieces"},
    9: {"name": "Snow White", "deco": "heavy powdered sugar snow, white chocolate drizzle"},
    10: {"name": "Royal Crown", "deco": "dark chocolate mirror glaze, gold leaf crown decoration"},
    11: {"name": "Candy Pop", "deco": "colorful candy pieces, popping candy, playful decoration"},
    12: {"name": "Matcha Zen", "deco": "matcha green tea powder, thin gold dust lines"},
}


def build_workflow(cookie_id, seed):
    cookie = COOKIE_DATA[cookie_id]
    deco_2d = cookie['deco'].replace('fresh ', '').replace('dried ', '').replace('visible ', '')
    clip_l = f"chibi mascot character, 2d anime illustration, flat shading, bold outlines, {deco_2d}, solid color background"
    t5xxl = f"{BASE_PROMPT}, decorated with {deco_2d}"
    prefix = f"cookie_{cookie_id}"
    return {
        "prompt": {
            "1": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": "flux1-schnell-Q4_K_S.gguf"}},
            "2": {"class_type": "DualCLIPLoaderGGUF", "inputs": {"clip_name1": "clip_l.safetensors", "clip_name2": "t5-v1_1-xxl-encoder-Q4_K_M.gguf", "type": "flux"}},
            "3": {"class_type": "CLIPTextEncodeFlux", "inputs": {"clip": ["2", 0], "clip_l": clip_l, "t5xxl": t5xxl, "guidance": 3.5}},
            "4": {"class_type": "CLIPTextEncodeFlux", "inputs": {"clip": ["2", 0], "clip_l": "", "t5xxl": "", "guidance": 3.5}},
            "5": {"class_type": "EmptySD3LatentImage", "inputs": {"width": WIDTH, "height": HEIGHT, "batch_size": 1}},
            "6": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "seed": seed, "steps": 4, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "positive": ["3", 0], "negative": ["4", 0], "latent_image": ["5", 0], "denoise": 1.0}},
            "7": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
            "8": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["7", 0]}},
            "9": {"class_type": "SaveImage", "inputs": {"images": ["8", 0], "filename_prefix": prefix}}
        }
    }


def queue_prompt(workflow):
    data = json.dumps(workflow).encode('utf-8')
    req = urllib.request.Request(f"{COMFYUI_URL}/prompt", data=data, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())['prompt_id']


def wait_for_completion(prompt_id, timeout=600):
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = urllib.request.urlopen(f"{COMFYUI_URL}/history/{prompt_id}")
            history = json.loads(resp.read())
            if prompt_id in history:
                status = history[prompt_id].get('status', {})
                if status.get('completed', False) or status.get('status_str') == 'success':
                    return history[prompt_id]
                if status.get('status_str') == 'error':
                    print(f"  ERROR: {json.dumps(status, indent=2)[:500]}")
                    return None
        except Exception:
            pass
        time.sleep(3)
    print(f"  TIMEOUT after {timeout}s")
    return None


def find_output_file(history):
    try:
        outputs = history.get('outputs', {})
        for node_id, node_out in outputs.items():
            if 'images' in node_out:
                for img in node_out['images']:
                    return img.get('filename', '')
    except Exception as e:
        print(f"  Error parsing output: {e}")
    return ''


def resize_image(src, dst, w, h):
    try:
        from PIL import Image
        img = Image.open(src)
        img = img.resize((w, h), Image.LANCZOS)
        img.save(dst, 'PNG', optimize=True)
        return True
    except ImportError:
        shutil.copy2(src, dst)
        return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Check which cookies are missing
    missing = []
    for i in range(1, 23):
        if not (OUTPUT_DIR / f"{i}.png").exists():
            missing.append(i)

    if not missing:
        print("All 22 cookies already exist!")
        return

    print(f"Missing cookies: {missing}")
    print(f"Generating {len(missing)} missing cookies...")

    base_seed = 55000
    success = 0

    for cookie_id in missing:
        cookie = COOKIE_DATA[cookie_id]
        seed = base_seed + cookie_id * 100
        print(f"\n[{cookie_id}] {cookie['name']} (seed={seed})")

        workflow = build_workflow(cookie_id, seed)
        try:
            prompt_id = queue_prompt(workflow)
            print(f"  Queued: {prompt_id}")
        except Exception as e:
            print(f"  FAILED: {e}")
            continue

        history = wait_for_completion(prompt_id, timeout=300)
        if not history:
            continue

        filename = find_output_file(history)
        if not filename:
            print("  No output file found")
            continue

        src_path = COMFYUI_OUTPUT / filename
        dst_path = OUTPUT_DIR / f"{cookie_id}.png"

        if not src_path.exists():
            for subdir in COMFYUI_OUTPUT.iterdir():
                if subdir.is_dir():
                    candidate = subdir / filename
                    if candidate.exists():
                        src_path = candidate
                        break

        if src_path.exists():
            resized = resize_image(str(src_path), str(dst_path), FINAL_WIDTH, FINAL_HEIGHT)
            size_kb = os.path.getsize(str(dst_path)) / 1024
            print(f"  Saved: {dst_path.name} ({size_kb:.0f}KB)")
            success += 1
        else:
            print(f"  Output file not found: {src_path}")

    print(f"\nDone: {success}/{len(missing)} generated")
    total = len(list(OUTPUT_DIR.glob('*.png')))
    print(f"Total cookies: {total}/22")


if __name__ == '__main__':
    main()
