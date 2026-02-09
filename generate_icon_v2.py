"""
Generate dubai-cookie app icon v2:
Mascot buried among multiple dark brown dubai kunafa cookies with green pistachio filling.
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
        "name": "icon2_v1",
        "seed": 99901,
        "denoise": 0.90,
        "clip_l": (
            "app icon, cute chibi character with brown hood and green face buried among many dark brown dubai cookies, "
            "cookies have dark chocolate brown exterior and bright green pistachio filling visible, "
            "character peeking out happily from pile of cookies, 2d anime, bold outlines, centered"
        ),
        "t5xxl": (
            "a mobile app icon, perfectly centered square composition, "
            "a cute small chibi mascot character with brown chocolate hood and light green pistachio face, "
            "the character is adorably buried among a pile of many round dark brown dubai kunafa cookies, "
            "each cookie has a dark chocolate brown crispy exterior shell and bright green pistachio cream filling visible from the cross section, "
            "the character is peeking out from the middle of the cookie pile with only head and hands visible, "
            "big happy sparkly eyes and cute smile, surrounded by cookies on all sides, "
            "2d digital art, anime style, bold black outlines, cel shading, flat colors, "
            "warm cream solid background, cute kawaii style, no text"
        ),
    },
    {
        "name": "icon2_v2",
        "seed": 99902,
        "denoise": 0.92,
        "clip_l": (
            "app icon, small green face chibi character swimming in a sea of dark brown round cookies, "
            "cookies are dark chocolate with green pistachio filling cross section visible, "
            "character happy and overwhelmed by cookies, 2d cute, bold outlines"
        ),
        "t5xxl": (
            "a mobile app icon, centered composition, "
            "a tiny cute chibi mascot with brown hood and green pistachio face, "
            "happily swimming and drowning in a huge pile of dark brown dubai kunafa chocolate cookies, "
            "the cookies are round with dark brown chocolate shell exterior and green pistachio cream filling oozing out, "
            "some cookies are cut in half showing the green pistachio cross section, "
            "the character's head and raised hands peek out from the center of the cookie mountain, "
            "cookies scattered everywhere filling the frame, "
            "2d digital art, anime illustration, bold black outlines, cel shading, "
            "warm light background, Sanrio kawaii style, no text no letters"
        ),
    },
    {
        "name": "icon2_v3",
        "seed": 99903,
        "denoise": 0.88,
        "clip_l": (
            "app icon, chibi character green face brown hood sitting on top of stacked dark brown cookies, "
            "cookies with green pistachio filling, character hugging cookies, happy, 2d anime cute"
        ),
        "t5xxl": (
            "a mobile app icon, centered square composition, "
            "an adorable chibi mascot with brown chocolate hood and light green pistachio face, "
            "sitting on top of and surrounded by a tall stack of dark brown dubai kunafa cookies, "
            "hugging multiple cookies with both arms, cookies piled around the character, "
            "each cookie is dark chocolate brown with visible green pistachio cream filling layer, "
            "some green pistachio cream dripping, character has loving happy expression, "
            "2d digital art, anime style, bold black outlines, cel shading, flat shading, "
            "solid warm cream background, LINE Friends cute style, no text"
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
        f"{COMFYUI_URL}/prompt", data=data,
        headers={'Content-Type': 'application/json'}
    )
    return json.loads(urllib.request.urlopen(req).read())['prompt_id']


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
                    return None
        except Exception:
            pass
        time.sleep(3)
    return None


def find_output_file(history):
    try:
        for nid, nout in history.get('outputs', {}).items():
            if 'images' in nout:
                return nout['images'][0].get('filename', '')
    except Exception:
        pass
    return ''


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating 3 icon v2 variants (cookies with green pistachio filling)...")

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
            print("  Failed/timeout")
            continue

        filename = find_output_file(history)
        if not filename:
            print("  No output")
            continue

        src_path = COMFYUI_OUTPUT / filename
        if not src_path.exists():
            for subdir in COMFYUI_OUTPUT.iterdir():
                if subdir.is_dir() and (subdir / filename).exists():
                    src_path = subdir / filename
                    break

        if src_path.exists():
            dst_path = OUTPUT_DIR / f"dubai-cookie-{p['name']}.png"
            try:
                from PIL import Image
                img = Image.open(str(src_path)).resize((600, 600), Image.LANCZOS)
                img.save(str(dst_path), 'PNG', optimize=True)
            except ImportError:
                shutil.copy2(str(src_path), str(dst_path))
            print(f"  Saved: {dst_path.name} ({os.path.getsize(str(dst_path))//1024}KB)")

    print("\nDone!")


if __name__ == '__main__':
    main()
