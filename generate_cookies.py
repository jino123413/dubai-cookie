"""
Generate 22 Dubai Cookie CHARACTER images using ComfyUI Flux Schnell GGUF.
Style: 2D chibi character with brown hood + green body, personality via costume/pose/expression.
Output: dubai-cookie/public/cookies/1.png ~ 22.png (512x512px)
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
HEIGHT = 768
FINAL_WIDTH = 512
FINAL_HEIGHT = 512
DENOISE = 0.85
REF_IMAGE = "dubai_cookie_ref.png"

# Base character description (fixed across all 22)
BASE = (
    "a single cute chibi character, 2d digital art, anime style illustration, simple flat shading, "
    "bold black outlines, cel shading, "
    "the character has a round head with brown chocolate colored hood and light green pistachio colored face and body, "
    "head to body ratio is 1:1, stubby arms and legs, "
    "plain white background, clean simple background, no background pattern, Sanrio style, LINE Friends style"
)

# 22 cookie characters — personality via expression, pose, costume
COOKIE_DATA = {
    1: {
        "name": "설렘쫀쿠",
        "seed": 77701,
        "clip_l": "chibi character, brown hood green face, 2d anime, sparkling eyes, blushing cheeks, wearing pink ribbon, holding a pink heart, happy excited expression",
        "personality": "sparkling big eyes with star highlights, pink blushing cheeks, wearing a cute pink ribbon on head, holding a glowing pink heart with both hands, bouncing happy pose, white background",
    },
    2: {
        "name": "용기쫀쿠",
        "seed": 77702,
        "clip_l": "chibi character, brown hood green face, 2d anime, determined eyes, wearing red cape, heroic pose, confident expression",
        "personality": "sharp determined eyes, wearing a small flowing red cape, standing in a heroic confident pose with one fist raised, bold and strong expression, white background",
    },
    3: {
        "name": "평온쫀쿠",
        "seed": 77703,
        "clip_l": "chibi character, brown hood green face, 2d anime, closed peaceful eyes, holding lavender flower, meditating sitting pose",
        "personality": "eyes gently closed with a serene peaceful smile, sitting in a calm meditation pose, holding a small lavender flower, soft aura around, white background",
    },
    4: {
        "name": "행복쫀쿠",
        "seed": 77704,
        "clip_l": "chibi character, brown hood green face, 2d anime, big wide smile, arms up celebrating, wearing party hat, confetti",
        "personality": "the biggest happiest smile with closed happy eyes, both arms raised up in celebration, wearing a small colorful party hat, confetti falling around, white background",
    },
    5: {
        "name": "몽상쫀쿠",
        "seed": 77705,
        "clip_l": "chibi character, brown hood green face, 2d anime, dreamy half-closed eyes, wearing wizard hat with stars, floating pose",
        "personality": "dreamy half-closed eyes looking upward, wearing a small purple wizard hat decorated with silver stars, floating slightly above ground, sparkles and stars around, white background",
    },
    6: {
        "name": "열정쫀쿠",
        "seed": 77706,
        "clip_l": "chibi character, brown hood green face, 2d anime, burning determined eyes, wearing headband, running pose, flames",
        "personality": "intensely burning determined eyes, wearing a red headband with fluttering tails, dynamic running pose leaning forward, small flame effects around, white background",
    },
    7: {
        "name": "포근쫀쿠",
        "seed": 77707,
        "clip_l": "chibi character, brown hood green face, 2d anime, warm gentle smile, wearing knitted scarf, holding hot cocoa mug",
        "personality": "warm gentle smile with soft eyes, wrapped in a cozy knitted brown scarf, holding a small steaming hot cocoa mug with both hands, warm cozy atmosphere, white background",
    },
    8: {
        "name": "자유쫀쿠",
        "seed": 77708,
        "clip_l": "chibi character, brown hood green face, 2d anime, carefree happy expression, wearing pilot goggles on head, arms spread like flying",
        "personality": "carefree happy expression with wind-blown feel, wearing retro pilot goggles pushed up on head, arms spread wide like flying free, small clouds around, white background",
    },
    9: {
        "name": "순수쫀쿠",
        "seed": 77709,
        "clip_l": "chibi character, brown hood green face, 2d anime, innocent big round eyes, wearing angel wings and halo, shy cute pose",
        "personality": "extra large innocent round sparkling eyes, tiny angel wings on back and a small floating halo above head, shy cute pose with hands together, soft glow around, white background",
    },
    10: {
        "name": "카리스마쫀쿠",
        "seed": 77710,
        "clip_l": "chibi character, brown hood green face, 2d anime, cool confident smirk, wearing golden crown, arms crossed, royal pose",
        "personality": "cool confident smirk expression, wearing a small golden crown, arms crossed in a commanding pose, royal aura sparkle effect, white background",
    },
    11: {
        "name": "장난쫀쿠",
        "seed": 77711,
        "clip_l": "chibi character, brown hood green face, 2d anime, tongue sticking out, wearing jester hat, playful mischievous pose",
        "personality": "tongue sticking out with one eye winking, wearing a colorful jester hat with bells, arms spread wide in silly playful pose, confetti around, white background",
    },
    12: {
        "name": "지혜쫀쿠",
        "seed": 77712,
        "clip_l": "chibi character, brown hood green face, 2d anime, wise thoughtful eyes, wearing round glasses, holding open book",
        "personality": "wise thoughtful eyes behind small round glasses, holding an open book in one hand, other hand on chin in thinking pose, small sparkle of insight, white background",
    },
    13: {
        "name": "다정쫀쿠",
        "seed": 77713,
        "clip_l": "chibi character, brown hood green face, 2d anime, soft caring eyes, wearing nurse cap, offering a bandaid with gentle smile",
        "personality": "soft caring eyes with the gentlest smile, wearing a small nurse cap with a heart, gently offering a heart-shaped bandaid, nurturing caring pose, white background",
    },
    14: {
        "name": "도도쫀쿠",
        "seed": 77714,
        "clip_l": "chibi character, brown hood green face, 2d anime, cool aloof expression, wearing sunglasses, one hand on hip, stylish pose",
        "personality": "cool aloof expression with a slight smirk, wearing sleek black sunglasses, one hand on hip in a stylish confident pose, sparkle effect, white background",
    },
    15: {
        "name": "여유쫀쿠",
        "seed": 77715,
        "clip_l": "chibi character, brown hood green face, 2d anime, relaxed sleepy smile, wearing straw hat, lying down on cloud, peaceful",
        "personality": "relaxed sleepy content smile, wearing a small straw hat tilted on head, casually lying on a fluffy cloud, one arm behind head, peaceful atmosphere, white background",
    },
    16: {
        "name": "감성쫀쿠",
        "seed": 77716,
        "clip_l": "chibi character, brown hood green face, 2d anime, teary sparkly eyes, wearing beret, holding paintbrush, artistic pose",
        "personality": "sparkly teary emotional eyes full of feeling, wearing a purple artist beret, holding a small paintbrush, surrounded by floating music notes and paint drops, white background",
    },
    17: {
        "name": "뚝심쫀쿠",
        "seed": 77717,
        "clip_l": "chibi character, brown hood green face, 2d anime, firm serious eyes, wearing construction hard hat, flexing muscle pose",
        "personality": "firm serious focused eyes, wearing a yellow construction hard hat, flexing one arm showing determination, solid sturdy stance, white background",
    },
    18: {
        "name": "호기심쫀쿠",
        "seed": 77718,
        "clip_l": "chibi character, brown hood green face, 2d anime, wide curious eyes, holding magnifying glass, peeking exploring pose",
        "personality": "extra wide curious sparkling eyes, holding a large magnifying glass up to one eye, leaning forward in an exploring pose, question marks floating around, white background",
    },
    19: {
        "name": "정의쫀쿠",
        "seed": 77719,
        "clip_l": "chibi character, brown hood green face, 2d anime, sharp righteous eyes, wearing judge robe, holding gavel, standing firm",
        "personality": "sharp righteous determined eyes, wearing a small black judge robe, holding a tiny wooden gavel raised up, standing in a firm just pose, white background",
    },
    20: {
        "name": "사랑쫀쿠",
        "seed": 77720,
        "clip_l": "chibi character, brown hood green face, 2d anime, loving warm eyes, blowing a kiss, hearts floating, wearing flower crown",
        "personality": "loving warm eyes with heart-shaped pupils, blowing a kiss with one hand, wearing a beautiful flower crown of roses, multiple hearts floating around, white background",
    },
    21: {
        "name": "그리움쫀쿠",
        "seed": 77721,
        "clip_l": "chibi character, brown hood green face, 2d anime, nostalgic gentle sad eyes, hugging a teddy bear, looking at distance",
        "personality": "nostalgic gentle slightly sad but warm eyes, hugging a small worn teddy bear close to chest, looking into the distance with a wistful smile, autumn leaves falling, white background",
    },
    22: {
        "name": "도전쫀쿠",
        "seed": 77722,
        "clip_l": "chibi character, brown hood green face, 2d anime, excited fearless eyes, wearing climbing helmet, one foot on rock, victory pose",
        "personality": "excited fearless eyes full of ambition, wearing a small climbing helmet with headlamp, one foot planted on a rock in a victory pose, pointing forward, gold sparkle effects, white background",
    },
}


def build_workflow(cookie_id: int) -> dict:
    """Build ComfyUI img2img workflow using reference image + denoise 0.85."""
    cookie = COOKIE_DATA[cookie_id]
    t5xxl = f"{BASE}, {cookie['personality']}"
    prefix = f"cookie_{cookie_id}"

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
                    "clip_l": cookie["clip_l"],
                    "t5xxl": t5xxl,
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
                    "width": WIDTH,
                    "height": HEIGHT,
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
                    "seed": cookie["seed"],
                    "steps": 4,
                    "cfg": 1.0,
                    "sampler_name": "euler",
                    "scheduler": "simple",
                    "positive": ["3", 0],
                    "negative": ["4", 0],
                    "latent_image": ["12", 0],
                    "denoise": DENOISE
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


def queue_prompt(workflow: dict) -> str:
    data = json.dumps(workflow).encode('utf-8')
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())['prompt_id']


def wait_for_completion(prompt_id: str, timeout: int = 600) -> dict:
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


def find_output_file(history: dict) -> str:
    try:
        outputs = history.get('outputs', {})
        for node_id, node_out in outputs.items():
            if 'images' in node_out:
                for img in node_out['images']:
                    return img.get('filename', '')
    except Exception as e:
        print(f"  Error parsing output: {e}")
    return ''


def resize_image(src: str, dst: str, w: int, h: int):
    try:
        from PIL import Image
        from rembg import remove
        img = Image.open(src)
        img = img.resize((w, h), Image.LANCZOS)
        # Remove background → transparent PNG
        img = remove(img)
        img.save(dst, 'PNG', optimize=True)
        return True
    except ImportError:
        shutil.copy2(src, dst)
        return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("Generating 22 Dubai Cookie CHARACTERS via ComfyUI Flux")
    print(f"Resolution: {WIDTH}x{HEIGHT} -> {FINAL_WIDTH}x{FINAL_HEIGHT}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    try:
        resp = urllib.request.urlopen(f"{COMFYUI_URL}/system_stats")
        stats = json.loads(resp.read())
        gpu = stats.get("devices", [{}])[0].get("name", "unknown")
        print(f"ComfyUI connected: {gpu}")
    except Exception as e:
        print(f"ComfyUI not available: {e}")
        print("Please start ComfyUI first!")
        return

    success_count = 0
    fail_count = 0

    for cookie_id in range(1, 23):
        cookie = COOKIE_DATA[cookie_id]
        print(f"\n[{cookie_id:2d}/22] {cookie['name']} (seed={cookie['seed']})")

        workflow = build_workflow(cookie_id)
        try:
            prompt_id = queue_prompt(workflow)
            print(f"  Queued: {prompt_id}")
        except Exception as e:
            print(f"  FAILED to queue: {e}")
            fail_count += 1
            continue

        history = wait_for_completion(prompt_id, timeout=300)
        if not history:
            fail_count += 1
            continue

        filename = find_output_file(history)
        if not filename:
            print("  No output file found")
            fail_count += 1
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
            print(f"  Saved: {dst_path.name} ({size_kb:.0f}KB) {'(resized)' if resized else '(copy)'}")
            success_count += 1
        else:
            print(f"  Output file not found: {src_path}")
            fail_count += 1

    print(f"\n{'=' * 60}")
    print(f"DONE: {success_count} succeeded, {fail_count} failed")
    if list(OUTPUT_DIR.glob('*.png')):
        total_size = sum(f.stat().st_size for f in OUTPUT_DIR.glob('*.png')) / 1024
        print(f"Total size: {total_size:.0f}KB")
    print("=" * 60)


if __name__ == '__main__':
    main()
