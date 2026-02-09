"""
Generate dubai-cookie app icon: mascot buried in a dubai kunafa cookie.
Output: 600x600 PNG
"""
import urllib.request
import json
import time
import os
import shutil
from pathlib import Path

COMFYUI_URL = "http://127.0.0.1:8188"
OUTPUT_DIR = Path(r"C:\Users\USER-PC\Desktop\appintoss-project\app-logos")
COMFYUI_OUTPUT = Path(r"C:\Users\USER-PC\Downloads\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\output")
REF_IMAGE = "dubai_cookie_ref.png"

ICON_PROMPTS = [
    {
        "name": "icon_v1",
        "seed": 88801,
        "denoise": 0.88,
        "clip_l": (
            "app icon, cute chibi character with brown hood and green face peeking out from inside a large dubai kunafa cookie, "
            "the character is half buried in the cookie with only head and arms visible, "
            "2d digital art, bold outlines, simple flat colors, centered composition, "
            "round icon design, warm cream background"
        ),
        "t5xxl": (
            "a mobile app icon design, perfectly centered composition, "
            "a cute chibi mascot character with round brown chocolate hood and light green pistachio face, "
            "the character is adorably buried inside a large round dubai kunafa chocolate cookie, "
            "only the head and two small hands are peeking out from the top of the cookie, "
            "the cookie has visible layers of kunafa pastry shreds and melted chocolate, "
            "the character has big sparkly happy eyes and a cute smile, "
            "2d digital art, anime style illustration, bold black outlines, cel shading, simple flat shading, "
            "warm cream solid background, Sanrio style, LINE Friends style, "
            "app icon format, square composition, no text"
        ),
    },
    {
        "name": "icon_v2",
        "seed": 88802,
        "denoise": 0.90,
        "clip_l": (
            "app icon, cute round chibi character with brown hood green face sitting inside a giant cookie, "
            "sinking into melted chocolate and pastry, happy expression, peeking out, "
            "2d anime style, bold outlines, warm tones, centered icon"
        ),
        "t5xxl": (
            "a mobile app icon, perfectly centered, "
            "an adorable chibi mascot with round brown chocolate colored hood and light green pistachio colored face and body, "
            "the character is happily sitting inside a giant cracked open dubai cookie, "
            "sinking into the gooey melted chocolate and shredded kunafa pastry filling, "
            "chocolate dripping around, the character looks up with big joyful eyes and wide smile, "
            "arms resting on the cookie edge, "
            "2d digital art, anime style, bold black outlines, cel shading, flat colors, "
            "warm golden cream solid background, Sanrio cute style, "
            "square icon composition, no text, no letters"
        ),
    },
    {
        "name": "icon_v3",
        "seed": 88803,
        "denoise": 0.85,
        "clip_l": (
            "app icon, chibi character brown hood green face popping out of a cookie, "
            "surprise expression, cookie crumbs, chocolate, 2d anime, cute, centered"
        ),
        "t5xxl": (
            "a mobile app icon, centered composition, "
            "a cute chibi character with brown chocolate hood and light green pistachio face, "
            "bursting out from the center of a large round dubai cookie like a surprise, "
            "cookie crumbs and chocolate pieces flying around, "
            "the character has excited surprised happy eyes and an open mouth smile, "
            "hands raised up in excitement, "
            "the cookie is golden brown with visible chocolate layers, "
            "2d digital art, anime illustration, bold black outlines, cel shading, "
            "solid warm pastel background, Sanrio style, LINE Friends style, "
            "app icon square format, no text"
        ),
    },
]


def build_workflow(prompt_data):
    prefix = prompt_data["name"]
    return {
        "prompt": {
            "1": {
                "class_type": "UnetLoaderGGUF",
                "inputs": {"unet_name": "flux1-schnell-Q4_K_S.gguf"}
            },
            "2": {
                "class_type": "DualCLIPLoaderGGUF",
                "inputs": {
                    "clip_name1": "clip_l.safetensors",
                    "clip_name2": "t5-v1_1-xxl-encoder-Q4_K_M.gguf",
                    "type": "flux"
                }
            },
            "3": {
                "class_type": "CLIPTextEncodeFlux",
                "inputs": {
                    "clip": ["2", 0],
                    "clip_l": prompt_data["clip_l"],
                    "t5xxl": prompt_data["t5xxl"],
                    "guidance": 3.5
                }
            },
            "4": {
                "class_type": "CLIPTextEncodeFlux",
                "inputs": {
                    "clip": ["2", 0],
                    "clip_l": "",
                    "t5xxl": "",
                    "guidance": 3.5
                }
            },
            "10": {
                "class_type": "LoadImage",
                "inputs": {"image": REF_IMAGE}
            },
            "11": {
                "class_type": "ImageScale",
                "inputs": {
                    "image": ["10", 0],
                    "width": 768,
                    "height": 768,
                    "upscale_method": "lanczos",
                    "crop": "center"
                }
            },
            "12": {
                "class_type": "VAEEncode",
                "inputs": {
                    "pixels": ["11", 0],
                    "vae": ["7", 0]
                }
            },
            "6": {
                "class_type": "KSampler",
                "inputs": {
                    "model": ["1", 0],
                    "seed": prompt_data["seed"],
                    "steps": 4,
                    "cfg": 1.0,
                    "sampler_name": "euler",
                    "scheduler": "simple",
                    "positive": ["3", 0],
                    "negative": ["4", 0],
                    "latent_image": ["12", 0],
                    "denoise": prompt_data["denoise"]
                }
            },
            "7": {
                "class_type": "VAELoader",
                "inputs": {"vae_name": "ae.safetensors"}
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {"samples": ["6", 0], "vae": ["7", 0]}
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {"images": ["8", 0], "filename_prefix": prefix}
            }
        }
    }


def queue_prompt(workflow):
    data = json.dumps(workflow).encode('utf-8')
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
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
    print(f"  TIMEOUT")
    return None


def find_output_file(history):
    try:
        outputs = history.get('outputs', {})
        for node_id, node_out in outputs.items():
            if 'images' in node_out:
                for img in node_out['images']:
                    return img.get('filename', '')
    except Exception:
        pass
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
    print("Generating 3 icon variants...")

    for p in ICON_PROMPTS:
        print(f"\n[{p['name']}] seed={p['seed']} denoise={p['denoise']}")
        workflow = build_workflow(p)
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
            print("  No output")
            continue

        src_path = COMFYUI_OUTPUT / filename
        if not src_path.exists():
            for subdir in COMFYUI_OUTPUT.iterdir():
                if subdir.is_dir():
                    candidate = subdir / filename
                    if candidate.exists():
                        src_path = candidate
                        break

        if src_path.exists():
            dst_path = OUTPUT_DIR / f"dubai-cookie-{p['name']}.png"
            resized = resize_image(str(src_path), str(dst_path), 600, 600)
            size_kb = os.path.getsize(str(dst_path)) / 1024
            print(f"  Saved: {dst_path.name} ({size_kb:.0f}KB)")
        else:
            print(f"  Not found: {src_path}")

    print("\nDone!")


if __name__ == '__main__':
    main()
