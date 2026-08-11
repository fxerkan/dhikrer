#!/usr/bin/env python3
"""Gemini "nano banana" image generate/edit via the Gemini API key (stdlib only).

Usage:
  GEMINI_API_KEY=... python3 tools/nano_banana.py OUT.png "PROMPT" [IN1.png IN2.png ...]
  # optional: NB_MODEL=gemini-3-pro-image  (default: gemini-2.5-flash-image)

Passing input image(s) does image-to-image editing; no input = text-to-image.
This ONLY calls the Gemini image model — it does not draw anything locally.
"""
import base64, json, os, sys, urllib.request

MODEL = os.environ.get("NB_MODEL", "gemini-2.5-flash-image")
KEY = os.environ["GEMINI_API_KEY"]


def main():
    out, prompt, *inputs = sys.argv[1:]
    parts = [{"text": prompt}]
    for p in inputs:
        with open(p, "rb") as f:
            parts.append({"inline_data": {"mime_type": "image/png",
                                          "data": base64.b64encode(f.read()).decode()}})
    gen = {"responseModalities": ["IMAGE"]}
    img_cfg = {}
    if os.environ.get("NB_ASPECT"): img_cfg["aspectRatio"] = os.environ["NB_ASPECT"]
    if os.environ.get("NB_SIZE"): img_cfg["imageSize"] = os.environ["NB_SIZE"]  # 1K/2K/4K (gemini-3-pro-image)
    if img_cfg: gen["imageConfig"] = img_cfg
    body = json.dumps({"contents": [{"parts": parts}], "generationConfig": gen}).encode()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}"
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    resp = json.load(urllib.request.urlopen(req, timeout=180))

    for part in resp.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        blob = part.get("inline_data") or part.get("inlineData")
        if blob:
            with open(out, "wb") as f:
                f.write(base64.b64decode(blob["data"]))
            print("wrote", out)
            return
        if part.get("text"):
            print("model text:", part["text"][:500])
    sys.exit("no image in response: " + json.dumps(resp)[:800])


if __name__ == "__main__":
    main()
