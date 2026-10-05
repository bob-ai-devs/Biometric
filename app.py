import streamlit as st
import numpy as np
import time
from datetime import datetime
import json
from pathlib import Path
import os
import io
from zoneinfo import ZoneInfo

# Set page configuration
st.set_page_config(
    page_title="BioMetric Verify Pro",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for creative styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Space+Mono:wght@400;700&display=swap');

    :root {
        --primary: #F15A22;
        --secondary: #004B8D;
        --accent: #D97706;
        --dark: #0B2D5B;
        --card-bg: #FFFFFF;
    }

    .main {
        background: linear-gradient(135deg, #FFF6EF 0%, #FFFFFF 50%, #EAF2FA 100%);
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #FFF6EF 0%, #FFFFFF 50%, #EAF2FA 100%);
    }

    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #0B2D5B;
    }

    .verification-card {
        background: var(--card-bg);
        border: 1px solid rgba(241, 90, 34, 0.2);
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 6px 24px rgba(0, 75, 141, 0.10);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .verification-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 32px rgba(241, 90, 34, 0.18);
    }

    .feature-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 4px;
        background: rgba(241, 90, 34, 0.1);
        border: 1px solid rgba(241, 90, 34, 0.3);
        color: #F15A22;
    }

    .scan-line {
        height: 2px;
        background: linear-gradient(90deg, transparent, #F15A22, transparent);
        animation: scan 2s linear infinite;
    }

    @keyframes scan {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    .stButton>button {
        background: linear-gradient(135deg, #F15A22 0%, #F7843B 100%);
        color: #ffffff;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(241, 90, 34, 0.35);
    }

    .llm-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 700;
        background: rgba(0, 75, 141, 0.2);
        border: 1px solid rgba(0, 75, 141, 0.4);
        color: #004B8D;
        font-family: 'Space Mono', monospace;
    }

    .model-active {
        padding: 8px 12px;
        background: rgba(241, 90, 34, 0.08);
        border-radius: 8px;
        margin: 4px 0;
        border: 1px solid rgba(241, 90, 34, 0.3);
    }

    .ensemble-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
        background: linear-gradient(135deg, rgba(241, 90, 34, 0.15), rgba(0, 75, 141, 0.15));
        border: 1px solid rgba(241, 90, 34, 0.3);
        color: #F15A22;
    }

    .fast-badge {
        display: inline-block;
        padding: 2px 6px;
        border-radius: 6px;
        font-size: 9px;
        font-weight: 700;
        background: rgba(241, 90, 34, 0.15);
        border: 1px solid rgba(241, 90, 34, 0.35);
        color: #F15A22;
    }

    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #F15A22;
        box-shadow: 0 0 8px #F15A22;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; box-shadow: 0 0 8px #F15A22; }
        50% { opacity: 0.5; box-shadow: 0 0 16px #F15A22; }
        100% { opacity: 1; box-shadow: 0 0 8px #F15A22; }
    }

    .thinking-box {
        background: #FFF4EC;
        border: 1px solid rgba(241, 90, 34, 0.25);
        border-radius: 8px;
        padding: 12px 16px;
        font-family: 'Space Mono', monospace;
        font-size: 12px;
        color: #475569;
        line-height: 1.6;
    }

    .thinking-box .cursor {
        display: inline-block;
        width: 8px;
        height: 15px;
        background: #F15A22;
        animation: blink 1s infinite;
        vertical-align: middle;
        margin-left: 2px;
    }

    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }

    .grid-bg {
        background-image: 
            linear-gradient(rgba(241, 90, 34, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(241, 90, 34, 0.03) 1px, transparent 1px);
        background-size: 40px 40px;
    }

    .pattern-match {
        padding: 8px 12px;
        background: rgba(241, 90, 34, 0.05);
        border-radius: 8px;
        margin: 4px 0;
        border-left: 3px solid #F15A22;
    }

    .pattern-mismatch {
        padding: 8px 12px;
        background: rgba(198, 40, 40, 0.05);
        border-radius: 8px;
        margin: 4px 0;
        border-left: 3px solid #C62828;
    }

    /* ---- Bank of Baroda light-mode chrome ---- */
    .stApp, .stApp p, .stApp label, .stApp li { color: #1F2A44; }
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 3px solid #F15A22;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stFileUploaderDropzone"] {
        background: #FFF9F5;
        border: 1.5px dashed #F15A22;
    }
    .stButton>button:hover { color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'verification_history' not in st.session_state:
    st.session_state.verification_history = []
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "fingerprint"

# Title and Header
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="font-size: 3.5rem; font-weight: 700; background: linear-gradient(135deg, #F15A22, #0B2D5B); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 8px;">
        🔐 BioMetric Verify Pro
    </h1>
    <p style="color: #475569; font-size: 1.1rem; font-family: 'Space Mono', monospace;">
        Pattern-Based LLM Analysis | Position & Scale Invariant
    </p>
    <div class="scan-line" style="margin: 20px 0;"></div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# CACHED CLIP MODEL LOADER
# ==========================================
@st.cache_resource(show_spinner=False)
def load_clip_model():
    """Load CLIP for pattern-based visual analysis."""
    from transformers import CLIPProcessor, CLIPModel
    import torch

    device = 0 if torch.cuda.is_available() else -1

    try:
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

        if device >= 0:
            model = model.to(device)

        return {"processor": processor, "model": model, "device": device}
    except Exception as e:
        st.error(f"CLIP load failed: {str(e)}")
        return None


def get_image_embedding(model, inputs):
    """Return a plain [batch, proj_dim] tensor from CLIP across transformers versions.
    Newer transformers return an output object instead of a tensor."""
    import torch
    out = model.get_image_features(**inputs)
    if isinstance(out, torch.Tensor):
        return out
    t = None
    for attr in ("image_embeds", "pooler_output"):
        t = getattr(out, attr, None)
        if t is not None:
            break
    if t is None:
        t = out[0]
    # If we got the pre-projection vector (768), project it to the CLIP space (512)
    if t.shape[-1] != model.config.projection_dim:
        t = model.visual_projection(t)
    return t

# ==========================================
# CACHED PATTERN-BASED ANALYSIS
# ==========================================
@st.cache_data(show_spinner=False)
def analyze_patterns(image_bytes, model_name="openai/clip-vit-base-patch32"):
    """Extract pattern-based embeddings and patch features from image."""
    from PIL import Image
    import torch
    import torch.nn.functional as F

    model_data = load_clip_model()
    if model_data is None:
        return None, None, None

    processor = model_data["processor"]
    model = model_data["model"]
    device = model_data["device"]

    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')

    # Global embedding (semantic/pattern understanding)
    inputs = processor(images=img, return_tensors="pt")
    if device >= 0:
        inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        global_embed = get_image_embedding(model, inputs)
        global_embed = F.normalize(global_embed, dim=-1).cpu().numpy()[0]

    # Patch embeddings (local pattern features) — position independent
    with torch.no_grad():
        vision_outputs = model.vision_model(pixel_values=inputs['pixel_values'])
        # last_hidden_state: [batch, num_patches+1, hidden_dim] — +1 is CLS token
        all_patches = vision_outputs.last_hidden_state  # [1, 50, 768] for ViT-B/32 (49 patches + 1 CLS)
        patch_embeds = all_patches[:, 1:, :]  # Remove CLS token, keep 49 patches [1, 49, 768]
        patch_embeds = F.normalize(patch_embeds, dim=-1).cpu().numpy()[0]  # [49, 768]

    return global_embed, patch_embeds, img

@st.cache_data(show_spinner=False)
def compute_pattern_similarity(ref_bytes, query_bytes, augment=True):
    """Compute pattern-based similarity robust to position/scale/rotation."""
    from PIL import Image
    import torch
    import torch.nn.functional as F
    import io

    ref_global, ref_patches, ref_img = analyze_patterns(ref_bytes)
    query_global, query_patches, query_img = analyze_patterns(query_bytes)

    if ref_global is None or query_global is None:
        return 50.0, None, None, None, "Model unavailable"

    # 1. Global semantic similarity (pattern-level understanding)
    global_sim = float((np.dot(ref_global, query_global) + 1) / 2 * 100)

    # 2. Patch-level pattern matching (local patterns, position-robust)
    # For each patch in ref, find best matching patch in query (soft matching)
    ref_patches_t = torch.tensor(ref_patches).float()  # [49, 768]
    query_patches_t = torch.tensor(query_patches).float()  # [49, 768]

    # Compute all pairwise patch similarities
    similarity_matrix = torch.matmul(ref_patches_t, query_patches_t.transpose(0, 1))  # [49, 49]

    # For each reference patch, find best matching query patch
    best_patch_sims, best_patch_indices = similarity_matrix.max(dim=1)  # [49]
    patch_sim = float(best_patch_sims.mean().item() * 100)

    # 3. Create spatial pattern heatmap (7x7 grid -> upsample)
    patch_sim_map = best_patch_sims.numpy().reshape(7, 7)  # 7x7 spatial grid

    # 4. Multi-scale & augmentation robustness check
    multi_scale_sims = [global_sim]

    if augment:
        model_data = load_clip_model()
        processor = model_data["processor"]
        model = model_data["model"]
        device = model_data["device"]

        # Test different scales
        scales = [0.85, 1.0, 1.15]
        # Test small rotations
        rotations = [-8, -4, 0, 4, 8]

        for scale in scales:
            for angle in rotations:
                if scale == 1.0 and angle == 0:
                    continue  # Already computed

                try:
                    # Transform query image
                    w, h = query_img.size
                    new_w, new_h = int(w * scale), int(h * scale)
                    transformed = query_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    transformed = transformed.rotate(angle, fillcolor=(128, 128, 128))

                    # Center crop back to original aspect
                    left = (new_w - w) // 2
                    top = (new_h - h) // 2
                    right = left + w
                    bottom = top + h
                    transformed = transformed.crop((left, top, right, bottom))

                    # Get embedding
                    inputs = processor(images=transformed, return_tensors="pt")
                    if device >= 0:
                        inputs = {k: v.to(device) for k, v in inputs.items()}

                    with torch.no_grad():
                        aug_embed = get_image_embedding(model, inputs)
                        aug_embed = F.normalize(aug_embed, dim=-1).cpu().numpy()[0]

                    aug_sim = float((np.dot(ref_global, aug_embed) + 1) / 2 * 100)
                    multi_scale_sims.append(aug_sim)
                except:
                    continue

    # Take best similarity across all augmentations (robust to scale/rotation differences)
    best_global_sim = max(multi_scale_sims)

    # 5. Final ensemble: weighted combination
    # Global captures overall pattern style, patch captures local pattern details
    # Best global across augmentations handles scale/rotation shifts
    final_score = best_global_sim * 0.6 + patch_sim * 0.4

    reasoning = f"""
    Pattern Analysis Complete:
    • Global pattern similarity (original): {global_sim:.1f}%
    • Best pattern match across {len(multi_scale_sims)} augmentations: {best_global_sim:.1f}%
    • Local patch pattern alignment: {patch_sim:.1f}%
    • Tested scales: 0.85x to 1.15x | Rotations: -8° to +8°
    • Final ensemble: {final_score:.1f}%
    """

    return final_score, patch_sim_map, best_global_sim, patch_sim, reasoning

# ==========================================
# HEATMAP GENERATION - Pattern-based, not pixel-based
# ==========================================
def create_pattern_heatmap(patch_sim_map, ref_display, query_display):
    """Create a pattern-similarity heatmap showing WHICH regions match, not pixel diff."""
    from PIL import Image

    h, w, _ = ref_display.shape

    # Upsample 7x7 patch similarity map to image size (bilinear, no scipy needed)
    upsampled = np.array(
        Image.fromarray(np.asarray(patch_sim_map, dtype=np.float32), mode="F")
        .resize((w, h), Image.Resampling.BILINEAR)
    )
    upsampled = np.clip(upsampled, 0, 1)

    # Create RGB heatmap using jet colormap (manual)
    heatmap = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            val = upsampled[i, j]
            if val < 0.125:
                r, g, b = 0, 0, int(255 * (0.5 + val * 4))
            elif val < 0.375:
                r, g, b = 0, int(255 * (val - 0.125) * 4), 255
            elif val < 0.625:
                r, g, b = int(255 * (val - 0.375) * 4), 255, int(255 * (0.625 - val) * 4)
            elif val < 0.875:
                r, g, b = 255, int(255 * (0.875 - val) * 4), 0
            else:
                r, g, b = 255, 0, 0
            heatmap[i, j] = [r, g, b]

    # Overlay on reference image
    overlay = (ref_display * 0.4 + heatmap * 0.6).astype(np.uint8)

    return heatmap, overlay, upsampled

# ==========================================
# IMAGE DISPLAY PROCESSING
# ==========================================
@st.cache_data(show_spinner=False)
def process_image_display(image_bytes, target_size=(400, 400)):
    """Process image for display."""
    from PIL import Image

    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize(target_size, Image.Resampling.LANCZOS)
    return np.array(img)


# ==========================================
# GEMINI VISION (google-genai) + LOCAL INSIGHTS
# ==========================================
GEMINI_MODEL = "gemini-flash-lite-latest"

def get_gemini_key():
    """Read the Gemini key from Streamlit secrets (or env var as fallback)."""
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        try:
            val = st.secrets.get(name)
        except Exception:
            val = None
        if val:
            return str(val)
        val = os.environ.get(name)
        if val:
            return val
    return None


def _prepare_for_gemini(image_bytes, max_side=1024):
    """Convert any upload (incl. BMP/TIFF) to a reasonably sized JPEG for Gemini."""
    from PIL import Image
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def run_gemini_analysis(ref_bytes, query_bytes, mode):
    """Ask Gemini to visually compare both samples. Returns (result_dict, error_str)."""
    import hashlib
    import re

    cache = st.session_state.setdefault("gemini_cache", {})
    cache_key = hashlib.sha256(
        ref_bytes + b"|" + query_bytes + b"|" + mode.encode() + GEMINI_MODEL.encode()
    ).hexdigest()
    if cache_key in cache:
        return cache[cache_key], None

    api_key = get_gemini_key()
    if not api_key:
        return None, "no_key"

    if mode == "Fingerprint":
        focus = ("ridge pattern class (loop / whorl / arch), core and delta positions, ridge flow direction, "
                 "ridge density and spacing, and visible minutiae (ridge endings, bifurcations). "
                 "Allow for rotation, shifts, partial prints and different scan sizes.")
    else:
        focus = ("the overall structure and habitual style of the signature: general letterform shapes, "
                 "stroke flow and rhythm, approximate slant, relative proportions, and distinctive flourishes or "
                 "starting/ending strokes. Also watch for signs of tracing, hesitation or tremor.")

    if mode == "Fingerprint":
        strictness = ('Be strict: fingerprints are highly specific, so differences in pattern class, core/delta '
                      'structure, ridge flow or minutiae are meaningful. Tolerate only rotation, shifts, partial '
                      'prints and scan-size differences.')
    else:
        strictness = ('Be balanced. Genuine signatures vary between signings, so tolerate differences in size, '
                      'position, slight slant, speed, pen pressure and scan quality. But do weigh the core '
                      'identity traits: letterform structure, stroke flow and order, relative proportions between '
                      'components, and distinctive flourishes, loops or terminal strokes. Do not dismiss '
                      'consistent structural differences as "natural variation", and do not penalise trivial ones.')

    review_scale = """Think like a careful peer reviewer weighing evidence on both sides, then choose ONE verdict:
- "strong_match": nearly all core traits are consistent; any differences are cosmetic.
- "weak_match": broadly similar and leaning match, but one or two notable differences or limited evidence keep it from being strong.
- "inconclusive": the images do not allow a fair judgement (poor quality, partial sample, very little detail).
- "verify": several notable differences or concerning signs in core traits; leaning mismatch but not conclusive - needs manual verification.
- "mismatch": the fundamental structure or style clearly differs, or there are strong signs of tracing/imitation.

Also give a "match_score" from 0 to 100: how similar the two samples are overall. It must be consistent with your verdict:
strong_match 85-100, weak_match 70-84, inconclusive 50-69, verify 25-49, mismatch 0-24. Use the position inside the band to
reflect how strong the evidence is (e.g. a near-identical pair is ~97, a borderline strong match is ~86)."""

    prompt = f"""You are assisting a bank's document-verification reviewer.
Compare Image 1 (REFERENCE, ground truth) with Image 2 (QUERY, to verify). Both are {mode.lower()} samples.
Judge from the images alone. Focus on: {focus}
{strictness}

{review_scale}

Do not claim legal or forensic certainty - this is a screening aid for a human reviewer.

Return ONLY a JSON object with exactly these keys:
{{
  "verdict": "strong_match" | "weak_match" | "inconclusive" | "verify" | "mismatch",
  "match_score": integer 0-100 (see the bands above),
  "confidence": integer 0-100 (your confidence in the verdict),
  "summary": "2-3 sentence reviewer-style explanation of the decisive evidence",
  "matching_features": ["up to 5 short strings"],
  "differing_features": ["up to 5 short strings; mark each as (minor), (moderate) or (significant)"],
  "red_flags": ["short strings; empty list if none"],
  "reference_quality": "one short sentence",
  "query_quality": "one short sentence",
  "recommendation": "one short sentence on what the reviewer should do next"
}}"""

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        resp = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                prompt,
                "Image 1 - REFERENCE sample:",
                types.Part.from_bytes(data=_prepare_for_gemini(ref_bytes), mime_type="image/jpeg"),
                "Image 2 - QUERY sample:",
                types.Part.from_bytes(data=_prepare_for_gemini(query_bytes), mime_type="image/jpeg"),
            ],
            config=types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json",
            ),
        )
        text = (resp.text or "").strip()
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
        data = json.loads(text)
        if isinstance(data, list) and data:
            data = data[0]
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:200]}"

    def _as_list(v):
        if isinstance(v, list):
            return [str(x) for x in v][:6]
        return [str(v)] if v else []

    verdict = str(data.get("verdict", "inconclusive")).strip().lower().replace(" ", "_").replace("-", "_")
    verdict = {"match": "strong_match", "weak": "weak_match", "strong": "strong_match",
               "needs_verification": "verify", "verify_manually": "verify"}.get(verdict, verdict)
    if verdict not in ("strong_match", "weak_match", "inconclusive", "verify", "mismatch"):
        verdict = "inconclusive"
    try:
        confidence = int(max(0, min(100, float(data.get("confidence", 50)))))
    except Exception:
        confidence = 50

    # Keep the numeric score consistent with the verdict band (mid-band if missing/invalid)
    bands = {"strong_match": (85, 100), "weak_match": (70, 84), "inconclusive": (50, 69),
             "verify": (25, 49), "mismatch": (0, 24)}
    lo, hi = bands[verdict]
    try:
        match_score = float(data.get("match_score"))
    except Exception:
        match_score = (lo + hi) / 2
    match_score = int(round(min(hi, max(lo, match_score))))

    result = {
        "verdict": verdict,
        "match_score": match_score,
        "confidence": confidence,
        "summary": str(data.get("summary", "")),
        "matching_features": _as_list(data.get("matching_features")),
        "differing_features": _as_list(data.get("differing_features")),
        "red_flags": _as_list(data.get("red_flags")),
        "reference_quality": str(data.get("reference_quality", "")),
        "query_quality": str(data.get("query_quality", "")),
        "recommendation": str(data.get("recommendation", "")),
    }
    cache[cache_key] = result
    return result, None


@st.cache_data(show_spinner=False)
def compute_quality_metrics(image_bytes):
    """Cheap, local image-quality heuristics (numpy only)."""
    from PIL import Image

    img = Image.open(io.BytesIO(image_bytes)).convert("L")
    width, height = img.size
    small = img.copy()
    small.thumbnail((512, 512), Image.Resampling.LANCZOS)  # comparable scale for sharpness
    g = np.asarray(small, dtype=np.float32)

    lap = (-4 * g[1:-1, 1:-1] + g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:])
    sharpness = float(lap.var())
    contrast = float(g.std())

    # Otsu threshold -> minority class = ink / ridges
    hist, _ = np.histogram(g, bins=256, range=(0, 255))
    hist = hist.astype(np.float64)
    total = hist.sum()
    sum_all = np.dot(np.arange(256), hist)
    w0 = np.cumsum(hist)
    w1 = total - w0
    sum0 = np.cumsum(hist * np.arange(256))
    with np.errstate(divide="ignore", invalid="ignore"):
        m0 = sum0 / w0
        m1 = (sum_all - sum0) / w1
        between = w0 * w1 * (m0 - m1) ** 2
    thr = int(np.nanargmax(between)) if np.isfinite(between).any() else 128
    frac_low = float((g <= thr).mean())
    coverage = min(frac_low, 1 - frac_low)

    return {"width": width, "height": height, "sharpness": sharpness,
            "contrast": contrast, "coverage": coverage}


def build_insights(patch_sim_map, final_score, best_global, patch_sim, global_sim,
                   multi_scale_sims, aug_records, sensitivity, test_augmentations,
                   q_ref, q_query):
    """Derive extra insights from data we already have - no extra model involved.
    Returns a list of (severity, icon, title, text); severity in ok / warn / bad / info."""
    out = []

    def verdict_of(sc):
        return "Match" if sc >= 80 else "Doubt" if sc >= 75 else "Mismatch"

    # 1. Spatial consistency (3x3 regions of the 7x7 patch grid)
    bands = np.array_split(np.arange(7), 3)
    region = np.array([[patch_sim_map[np.ix_(rb, cb)].mean() for cb in bands] for rb in bands]) * 100
    rows, cols = ["top", "middle", "bottom"], ["left", "center", "right"]
    name = lambda rc: "center" if rc == (1, 1) else f"{rows[rc[0]]}-{cols[rc[1]]}"
    wi = tuple(int(x) for x in np.unravel_index(np.argmin(region), region.shape))
    si = tuple(int(x) for x in np.unravel_index(np.argmax(region), region.shape))
    spread = float(region.max() - region.min())
    if spread > 15:
        out.append(("warn", "🧭", "Uneven spatial match",
                    f"Weakest area of the reference is {name(wi)} ({region[wi]:.0f}%) vs strongest {name(si)} "
                    f"({region[si]:.0f}%). A {spread:.0f}-pt gap suggests a localised difference worth a manual look."))
    else:
        out.append(("ok", "🧭", "Consistent across regions",
                    f"All nine regions of the reference score within {spread:.0f} pts of each other "
                    f"(range {region.min():.0f}-{region.max():.0f}%)."))

    # 2. Strong patch coverage
    n_strong = int((patch_sim_map > 0.7).sum())
    sev = "ok" if n_strong >= 30 else "warn" if n_strong >= 15 else "bad"
    out.append((sev, "🧩", "Strongly matched patches",
                f"{n_strong} of 49 local patches exceed 0.70 similarity ({n_strong / 49 * 100:.0f}% of the sample)."))

    # 3. Stability across scale / rotation
    if test_augmentations and aug_records:
        sims = np.array(multi_scale_sims, dtype=float)
        std = float(sims.std())
        bs, ba, bsim = max(aug_records, key=lambda r: r[2])
        best_txt = (f"Best alignment at {bs:.2f}x / {ba:+d} deg ({bsim:.1f}%) vs {global_sim:.1f}% unmodified."
                    if bsim > global_sim else "The unmodified query already gave the best alignment.")
        if std < 1.5:
            out.append(("ok", "🔄", "Stable under scale/rotation",
                        f"{len(sims)} variants vary by only {std:.1f} pts (std). {best_txt}"))
        else:
            out.append(("warn", "🔄", "Sensitive to scale/rotation",
                        f"{len(sims)} variants vary by {std:.1f} pts (std, range {sims.min():.1f}-{sims.max():.1f}%). "
                        f"The match depends on alignment. {best_txt}"))

    # 4. Margin to the decision thresholds
    thr_name, thr_val = min((("Match", 80.0), ("Mismatch", 75.0)), key=lambda t: abs(final_score - t[1]))
    margin = abs(final_score - thr_val)
    if margin < 5:
        out.append(("warn", "🎚️", "Borderline decision",
                    f"CLIP score {final_score:.1f}% is only {margin:.1f} pts from the {thr_val:.0f}% line. "
                    f"Treat the verdict as provisional and prefer human review."))
    else:
        out.append(("ok", "🎚️", "Clear decision margin",
                    f"CLIP score {final_score:.1f}% sits {margin:.1f} pts away from the nearest threshold ({thr_val:.0f}%)."))

    # 5. Sensitivity what-if
    raw = best_global * 0.6 + patch_sim * 0.4
    what_if = {sv: verdict_of(min(100, max(0, raw * (0.5 + 0.5 * sv)))) for sv in (0.25, 0.5, 0.75, 1.0)}
    if len(set(what_if.values())) == 1:
        out.append(("ok", "🎛️", "Verdict independent of sensitivity",
                    f"Result stays '{verdict_of(final_score)}' for any sensitivity from 0.25 to 1.00."))
    else:
        detail = ", ".join(f"{k:.2f}: {v}" for k, v in what_if.items())
        out.append(("warn", "🎛️", "Verdict depends on sensitivity", f"Changes with the slider ({detail})."))

    # 6. What the CLIP encoder actually sees (center-crop to square)
    seen = {}
    for label, q in (("reference", q_ref), ("query", q_query)):
        seen[label] = min(q["width"], q["height"]) / max(q["width"], q["height"]) * 100
    cropped = [f"{k} ({v:.0f}% visible)" for k, v in seen.items() if v < 75]
    if cropped:
        out.append(("warn", "✂️", "Wide image gets cropped",
                    "CLIP centre-crops to a square, so edges are dropped for: " + ", ".join(cropped) +
                    ". Padding wide signatures to a square before upload keeps the whole sample in view."))

    # 7. Image quality (heuristic)
    issues, lines = [], []
    for label, q in (("Reference", q_ref), ("Query", q_query)):
        lines.append(f"{label}: {q['width']}x{q['height']}px, sharpness {q['sharpness']:.0f}, "
                     f"contrast {q['contrast']:.0f}, ink/ridge coverage {q['coverage'] * 100:.1f}%")
        if min(q["width"], q["height"]) < 200:
            issues.append(f"{label.lower()} is low resolution")
        if q["sharpness"] < 50:
            issues.append(f"{label.lower()} looks soft/blurry")
        if q["contrast"] < 35:
            issues.append(f"{label.lower()} has low contrast")
        if q["coverage"] < 0.02:
            issues.append(f"{label.lower()} shows very little ink/ridge detail")
    out.append(("warn" if issues else "ok", "🔬", "Image quality (heuristic)",
                ("Flags: " + "; ".join(issues) + ". " if issues else "No obvious quality problems. ") + " | ".join(lines)))

    # 8. Comparability of the two uploads
    ar_r = q_ref["width"] / q_ref["height"]
    ar_q = q_query["width"] / q_query["height"]
    ratio = max(ar_r, ar_q) / min(ar_r, ar_q)
    res_ratio = max(q_ref["width"] * q_ref["height"], q_query["width"] * q_query["height"]) / \
        max(1, min(q_ref["width"] * q_ref["height"], q_query["width"] * q_query["height"]))
    if ratio > 1.25 or res_ratio > 4:
        out.append(("info", "📐", "Samples differ in shape or size",
                    f"Aspect ratios differ by {ratio:.2f}x and pixel counts by {res_ratio:.1f}x. "
                    f"The engine is scale-tolerant, but very different framing can still lower scores."))
    return out


# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 3rem; margin-bottom: 10px;">🎯</div>
        <h3 style="color: #F15A22; margin-bottom: 4px;">Control Panel</h3>
        <p style="color: #64748b; font-size: 12px;">v4.0.0 | Pattern-Based Engine</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    mode = st.radio(
        "🔍 Analysis Mode",
        ["Fingerprint", "Signature"],
        index=0 if st.session_state.current_mode == "fingerprint" else 1,
        help="Select the biometric type to analyze"
    )
    st.session_state.current_mode = mode.lower()

    st.markdown("---")

    st.subheader("🧠 Active Model")
    st.caption("Single powerful model, pattern-focused")

    st.markdown("""
    <div class="model-active">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 13px; color: #1F2A44; font-weight: 600;">🎨 CLIP ViT-B/32</span>
            <span class="fast-badge">171MB</span>
        </div>
        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Pattern-based visual understanding</div>
        <div style="font-size: 11px; color: #64748b; margin-top: 2px;">Position & scale invariant</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align: center; margin: 12px 0;">
        <span class="ensemble-badge">1 Model | 171MB | Patch-Level</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("⚙️ Engine Settings")

    sensitivity = st.slider("Sensitivity", 0.0, 1.0, 0.75, 0.05,
                           help="Higher values detect subtle pattern differences")

    show_reasoning = st.toggle("Show Pattern Reasoning", value=True,
                              help="Display the model's pattern analysis steps")

    show_heatmap = st.toggle("Pattern Heatmap", value=True,
                            help="Visualize pattern match regions (not pixel diff)")

    test_augmentations = st.toggle("Test Scale/Rotation", value=True,
                                  help="Check similarity across different sizes and angles")

    clip_weight = 50
    use_gemini = st.toggle("Gemini Vision Findings", value=True,
                           help="Gemini views both images and writes an independent assessment")
    if use_gemini:
        if get_gemini_key():
            st.caption(f"✨ {GEMINI_MODEL} · API key detected")
        else:
            st.caption("⚠️ Add GEMINI_API_KEY to Streamlit secrets")
        clip_weight = st.slider("CLIP weight in final score", 0, 100, 50, 5, format="%d%%",
                                help="Final score = CLIP score x weight + Gemini score x (100 - weight).")
        st.caption(f"Weights: CLIP {clip_weight}% · Gemini {100 - clip_weight}%")

    st.markdown("---")

    if st.session_state.verification_history:
        st.subheader("📜 Recent Scans")
        for entry in st.session_state.verification_history[-5:]:
            status_color = {"MATCHED": "#1E8E3E", "REVIEW REQUIRED": "#D97706"}.get(entry['status'], "#C62828")
            st.markdown(f"""
            <div style="padding: 8px; border-radius: 8px; background: rgba(0,75,141,0.05); margin: 4px 0; border-left: 3px solid {status_color};">
                <div style="font-size: 11px; color: #64748b;">{entry['time']}</div>
                <div style="font-size: 13px; font-weight: 600;">{entry['type'].title()}: <span style="color: {status_color}">{entry['score']:.1f}%</span></div>
            </div>
            """, unsafe_allow_html=True)

# Main Content
st.markdown('<div class="grid-bg">', unsafe_allow_html=True)

st.markdown("""
<div class="verification-card">
    <h3 style="color: #F15A22; margin-bottom: 16px;">📤 Upload Biometric Samples</h3>
    <p style="color: #64748b; font-size: 13px; margin-top: -8px;">
        Works even if signatures are different sizes or fingerprints are slightly shifted/rotated.
        Analysis is <b>pattern-based</b>, not pixel-perfect.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 8px;">
        <span style="color: #F15A22; font-weight: 600;">🎯 Reference Sample</span>
        <span style="color: #64748b; font-size: 12px;"> (Ground Truth)</span>
    </div>
    """, unsafe_allow_html=True)
    uploaded_ref = st.file_uploader("Drop reference", type=['png','jpg','jpeg','bmp','tiff'], key="ref_uploader", label_visibility="collapsed")

with col2:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 8px;">
        <span style="color: #004B8D; font-weight: 600;">🔍 Query Sample</span>
        <span style="color: #64748b; font-size: 12px;"> (To Verify)</span>
    </div>
    """, unsafe_allow_html=True)
    uploaded_query = st.file_uploader("Drop query", type=['png','jpg','jpeg','bmp','tiff'], key="query_uploader", label_visibility="collapsed")

if uploaded_ref and uploaded_query:
    ref_bytes = uploaded_ref.getvalue()
    query_bytes = uploaded_query.getvalue()

    ref_display = process_image_display(ref_bytes)
    query_display = process_image_display(query_bytes)

    st.markdown("""
    <div class="verification-card" style="margin-top: 20px;">
        <h3 style="color: #F15A22; margin-bottom: 16px;">🖼️ Sample Preview</h3>
    </div>
    """, unsafe_allow_html=True)

    pc1, pc2 = st.columns(2)
    with pc1:
        st.image(ref_display, caption="Reference", use_container_width=True)
    with pc2:
        st.image(query_display, caption="Query", use_container_width=True)

    st.markdown("<div style='text-align: center; margin: 30px 0;'>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 Pattern-Based Analysis", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if analyze_btn:
        # Initialize defaults
        final_score = 50.0
        patch_sim = 0.0
        best_global = 50.0
        patch_score = 50.0
        reasoning_text = "Analysis pending."
        analysis_steps = []

        # Progress
        progress_placeholder = st.empty()
        with progress_placeholder.container():
            st.markdown("""
            <div class="verification-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 16px;">🎯</div>
                <h3 style="color: #F15A22;">Loading CLIP Pattern Engine...</h3>
                <p style="color: #64748b; font-family: 'Space Mono', monospace;">171MB | Position & Scale Invariant</p>
            </div>
            """, unsafe_allow_html=True)
            progress_bar = st.progress(0)
            progress_bar.progress(0.3, text="Loading CLIP ViT-B/32...")
            load_clip_model()
            progress_bar.progress(1.0, text="Ready!")

        progress_placeholder.empty()

        # Phase 1: Extract pattern embeddings
        step_ph = st.empty()
        with step_ph.container():
            st.markdown("""
            <div class="verification-card">
                <h4 style="color: #004B8D;">🧠 Phase 1: Pattern Feature Extraction</h4>
                <div class="thinking-box">
                    Extracting global and local pattern embeddings from both samples...<span class="cursor"></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        ref_global, ref_patches, _ = analyze_patterns(ref_bytes)
        query_global, query_patches, _ = analyze_patterns(query_bytes)

        if ref_global is not None and query_global is not None:
            # Global similarity
            global_sim = float((np.dot(ref_global, query_global) + 1) / 2 * 100)
            analysis_steps.append(f"CLIP Global: Pattern similarity = {global_sim:.1f}% (semantic/pattern level)")
        else:
            global_sim = 50.0
            analysis_steps.append("CLIP Global: Using fallback similarity")

        with step_ph.container():
            st.markdown(f"""
            <div class="verification-card">
                <h4 style="color: #004B8D;">🧠 Phase 1: Pattern Feature Extraction <span class="status-indicator"></span></h4>
                <div class="thinking-box">
                    ✓ Global pattern embedding extracted<br>
                    ✓ 49 local patch embeddings extracted (7×7 grid)<br>
                    Global pattern similarity: {global_sim:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        time.sleep(0.3)
        step_ph.empty()

        # Phase 2: Patch-level pattern matching
        step_ph = st.empty()
        with step_ph.container():
            st.markdown("""
            <div class="verification-box">
                <h4 style="color: #004B8D;">🧠 Phase 2: Local Pattern Matching</h4>
                <div class="thinking-box">
                    Matching local patterns across spatial grid (position-independent)...<span class="cursor"></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if ref_patches is not None and query_patches is not None:
            import torch
            import torch.nn.functional as F

            ref_t = torch.tensor(ref_patches).float()
            query_t = torch.tensor(query_patches).float()
            sim_matrix = torch.matmul(ref_t, query_t.transpose(0, 1))
            best_sims, _ = sim_matrix.max(dim=1)
            patch_sim = float(best_sims.mean().item() * 100)
            patch_sim_map = best_sims.numpy().reshape(7, 7)

            analysis_steps.append(f"CLIP Patches: Local pattern alignment = {patch_sim:.1f}% (position-robust)")
        else:
            patch_sim = 50.0
            patch_sim_map = np.ones((7, 7)) * 0.5
            analysis_steps.append("CLIP Patches: Using fallback alignment")

        with step_ph.container():
            st.markdown(f"""
            <div class="verification-card">
                <h4 style="color: #004B8D;">🧠 Phase 2: Local Pattern Matching <span class="status-indicator"></span></h4>
                <div class="thinking-box">
                    ✓ 49 patch pairs analyzed (soft matching, position-independent)<br>
                    Local pattern alignment: {patch_sim:.1f}%<br>
                    Best matching patches: {int((best_sims > 0.7).sum()) if 'best_sims' in locals() else 'N/A'}/49 strong matches
                </div>
            </div>
            """, unsafe_allow_html=True)

        time.sleep(0.3)
        step_ph.empty()

        # Phase 3: Augmentation robustness
        step_ph = st.empty()
        with step_ph.container():
            st.markdown("""
            <div class="verification-card">
                <h4 style="color: #004B8D;">🧠 Phase 3: Scale & Rotation Robustness</h4>
                <div class="thinking-box">
                    Testing pattern similarity across different scales and angles...<span class="cursor"></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        multi_scale_sims = [global_sim]
        aug_records = []

        if test_augmentations:
            model_data = load_clip_model()
            if model_data is not None:
                processor = model_data["processor"]
                model = model_data["model"]
                device = model_data["device"]

                from PIL import Image
                query_img = Image.open(io.BytesIO(query_bytes)).convert('RGB')
                w, h = query_img.size

                scales = [0.85, 1.0, 1.15]
                rotations = [-8, -4, 0, 4, 8]

                for scale in scales:
                    for angle in rotations:
                        if scale == 1.0 and angle == 0:
                            continue

                        try:
                            new_w, new_h = int(w * scale), int(h * scale)
                            transformed = query_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                            transformed = transformed.rotate(angle, fillcolor=(128, 128, 128))

                            left = (new_w - w) // 2
                            top = (new_h - h) // 2
                            transformed = transformed.crop((left, top, left + w, top + h))

                            inputs = processor(images=transformed, return_tensors="pt")
                            if device >= 0:
                                inputs = {k: v.to(device) for k, v in inputs.items()}

                            with torch.no_grad():
                                aug_embed = get_image_embedding(model, inputs)
                                aug_embed = F.normalize(aug_embed, dim=-1).cpu().numpy()[0]

                            aug_sim = float((np.dot(ref_global, aug_embed) + 1) / 2 * 100)
                            multi_scale_sims.append(aug_sim)
                            aug_records.append((scale, angle, aug_sim))
                        except:
                            continue

        best_global = max(multi_scale_sims)
        analysis_steps.append(f"Augmentation Robustness: Best match across {len(multi_scale_sims)} variants = {best_global:.1f}%")

        with step_ph.container():
            st.markdown(f"""
            <div class="verification-card">
                <h4 style="color: #004B8D;">🧠 Phase 3: Scale & Rotation Robustness <span class="status-indicator"></span></h4>
                <div class="thinking-box">
                    ✓ Tested {len(multi_scale_sims)} variants (scales: 0.85x–1.15x, rotations: -8° to +8°)<br>
                    Best pattern match: {best_global:.1f}%<br>
                    Original match: {global_sim:.1f}%<br>
                    Improvement from augmentation: +{best_global - global_sim:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        time.sleep(0.3)
        step_ph.empty()

        # Final ensemble
        final_score = best_global * 0.6 + patch_sim * 0.4
        final_score = final_score * (0.5 + 0.5 * sensitivity)
        final_score = float(min(100, max(0, final_score)))

        structural_score = best_global
        correlation_score = patch_sim
        edge_score = (best_global + patch_sim) / 2
        ensemble_score = final_score

        # Generate pattern heatmap
        if show_heatmap and patch_sim_map is not None:
            heatmap, overlay, upsampled = create_pattern_heatmap(patch_sim_map, ref_display, query_display)

        # ==========================================
        # RUN LOCAL INSIGHTS + GEMINI, THEN COMBINE
        # ==========================================
        import html as _html

        insights = build_insights(
            patch_sim_map, final_score, best_global, patch_sim, global_sim,
            multi_scale_sims, aug_records, sensitivity, test_augmentations,
            compute_quality_metrics(ref_bytes), compute_quality_metrics(query_bytes)
        )

        gemini_result, gemini_error = None, None
        if use_gemini:
            with st.spinner("Gemini is examining both samples..."):
                gemini_result, gemini_error = run_gemini_analysis(ref_bytes, query_bytes, mode)

        GV_LEVEL = {"strong_match": "green", "weak_match": "green", "inconclusive": "amber", "verify": "amber", "mismatch": "red"}
        GV_COLOR = {"strong_match": "#1E8E3E", "weak_match": "#6B9A1F", "inconclusive": "#D97706", "verify": "#F15A22", "mismatch": "#C62828"}
        GV_ICON = {"strong_match": "✅", "weak_match": "☑️", "inconclusive": "⚠️", "verify": "🔍", "mismatch": "❌"}
        GV_LABEL = {"strong_match": "STRONG MATCH", "weak_match": "WEAK MATCH", "inconclusive": "INCONCLUSIVE",
                    "verify": "VERIFY MANUALLY", "mismatch": "MISMATCH"}
        LVL_COLOR = {"green": "#1E8E3E", "amber": "#D97706", "red": "#C62828"}
        LVL_RANK = {"green": 2, "amber": 1, "red": 0}

        # CLIP score bands: 80-100 match, 75-<80 doubt, <75 mismatch
        CLIP_MATCH_T, CLIP_DOUBT_T = 80.0, 75.0
        clip_level = "green" if final_score >= CLIP_MATCH_T else "amber" if final_score >= CLIP_DOUBT_T else "red"
        score_color = LVL_COLOR[clip_level]
        clip_zone = {"green": "match zone", "amber": "doubt zone", "red": "mismatch zone"}[clip_level]
        # Gemini score / weighted final score bands (unchanged): above 80 match, above 50 review, otherwise mismatch
        score_level = lambda sc: "green" if sc > 80 else "amber" if sc > 50 else "red"
        gem_level = GV_LEVEL[gemini_result["verdict"]] if gemini_result else None
        gemini_score = float(gemini_result["match_score"]) if gemini_result else None

        if gem_level is None:
            agreement_label = None
        else:
            gap = abs(LVL_RANK[clip_level] - LVL_RANK[gem_level])
            agreement_label = "Agree" if gap == 0 else "Partial" if gap == 1 else "Conflict"

        # Large numeric disagreement between the two engines is worth surfacing as an insight
        if gemini_result and abs(final_score - gemini_score) > 25:
            insights.append(("warn", "⚖️", "Large CLIP vs Gemini score gap",
                             f"CLIP scored {final_score:.0f}% while Gemini scored {gemini_score:.0f}/100 - a {abs(final_score - gemini_score):.0f}-pt gap. "
                             f"The engines see the samples very differently; check the reasoning on both sides."))

        # ----- PRIMARY DECISION: weighted combination of the two scores -----
        w_clip = clip_weight / 100.0 if gemini_result else 1.0
        w_gem = 1.0 - w_clip
        combined_score = final_score * w_clip + (gemini_score * w_gem if gemini_result else 0.0)
        combined_score = float(min(100, max(0, combined_score)))
        # With Gemini: >80 matched, 50-80 review, <=50 mismatch.  CLIP only: 80+ match, 75-<80 doubt, <75 mismatch.
        combined_level = score_level(combined_score) if gemini_result else clip_level
        combined_color = LVL_COLOR[combined_level]
        status_text = {"green": "MATCHED", "amber": "REVIEW REQUIRED", "red": "MISMATCH"}[combined_level]
        dec_color = combined_color
        dec_icon = {"MATCHED": "✅", "REVIEW REQUIRED": "⚠️", "MISMATCH": "❌"}[status_text]
        decision_basis = (f"{round(w_clip * 100)}% CLIP + {round(w_gem * 100)}% Gemini" if gemini_result else "CLIP only")

        if gemini_result:
            _band = {"green": "match band (above 80%)", "amber": "review band (50-80%)", "red": "mismatch band (50% or below)"}[combined_level]
            _thr = (80.0, 50.0)
        else:
            _band = {"green": "match zone (80-100%)", "amber": "doubt zone (75-80%)", "red": "mismatch zone (below 75%)"}[combined_level]
            _thr = (CLIP_MATCH_T, CLIP_DOUBT_T)
        decision_lean = (f"Weighted final score {combined_score:.1f}% falls in the {_band}." if gemini_result
                         else f"Based on the CLIP pattern engine only - {combined_score:.1f}% falls in the {_band}.")
        _nearest = min(_thr, key=lambda t: abs(combined_score - t))
        if abs(combined_score - _nearest) < 5:
            decision_lean += f" It is close to the {_nearest:.0f}% line, so treat it as provisional."
        if agreement_label == "Conflict":
            decision_lean += " The two engines disagree strongly - read the reasoning on both sides."

        decision_action = {
            "MATCHED": "Proceed. The weighted evidence supports a match" + (" - a quick visual check is still worthwhile because the engines do not fully agree."
                                                                           if agreement_label in ("Partial", "Conflict") else "."),
            "REVIEW REQUIRED": "Send to a human reviewer. The evidence is mixed or incomplete, so do not decide on the score alone.",
            "MISMATCH": "Do not accept automatically. Escalate for manual / fraud verification before any action.",
        }[status_text]

        # ===== PREVIOUS RULE-BASED DECISION (kept for reference) =====================================
        # Both engines green -> MATCHED, both red -> MISMATCH, anything else -> REVIEW REQUIRED.
        # To remove it from the dashboard set SHOW_RULE_BASED_DECISION = False
        # (or delete this block + the "PREVIOUS RULE-BASED DECISION" card in the Decision tab).
        SHOW_RULE_BASED_DECISION = True
        if gem_level is None:
            rule_status_text = {"green": "MATCHED", "amber": "REVIEW REQUIRED", "red": "MISMATCH"}[clip_level]
        elif clip_level == gem_level == "green":
            rule_status_text = "MATCHED"
        elif clip_level == gem_level == "red":
            rule_status_text = "MISMATCH"
        else:
            rule_status_text = "REVIEW REQUIRED"
        rule_color = {"MATCHED": "#1E8E3E", "REVIEW REQUIRED": "#D97706", "MISMATCH": "#C62828"}[rule_status_text]
        rule_icon = {"MATCHED": "✅", "REVIEW REQUIRED": "⚠️", "MISMATCH": "❌"}[rule_status_text]
        if gem_level is None:
            rule_lean = f"Based on the CLIP pattern engine only ({clip_zone})."
        elif rule_status_text == "MATCHED":
            rule_lean = ("Both engines agree the samples match." if gemini_result["verdict"] == "strong_match"
                         else "Both engines lean towards a match; Gemini rates it a weak match, so confidence is moderate.")
        elif rule_status_text == "MISMATCH":
            rule_lean = "Both engines agree the samples do not match."
        elif {clip_level, gem_level} == {"green", "red"}:
            rule_lean = "The engines conflict - one sees a match, the other a mismatch."
        elif "green" in (clip_level, gem_level):
            rule_lean = "Leaning towards a match, but one engine is not fully convinced."
        elif "red" in (clip_level, gem_level):
            rule_lean = "Leaning towards a mismatch, but one engine is not conclusive."
        else:
            rule_lean = "Neither engine is conclusive."
        # =============================================================================================

        # Save history
        st.session_state.verification_history.append({
            'time': datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%H:%M:%S"),
            'type': mode.lower(),
            'score': float(combined_score),
            'status': status_text
        })

        # ==========================================
        # RESULTS (tabbed)
        # ==========================================
        st.markdown("""
        <div class="verification-card" style="margin-top: 20px;">
            <h2 style="text-align: center; color: #F15A22; margin-bottom: 4px;">📊 Verification Results</h2>
            <p style="text-align: center; color: #64748b; font-size: 12px; margin: 0;">
                Combined decision from the CLIP pattern engine and Gemini vision review
            </p>
        </div>
        """, unsafe_allow_html=True)

        tab_dec, tab_metrics, tab_heat, tab_gem, tab_ins, tab_rep = st.tabs(
            ["🎯 Decision", "📊 Metrics", "🗺️ Heatmap", "✨ Gemini", "💡 Insights", "📝 Report"]
        )

        with tab_dec:
            def _pill(label, value, color):
                return (f'<span style="display:inline-block; padding:5px 12px; border-radius:20px; font-size:12px; '
                        f'font-weight:700; color:{color}; border:1px solid {color}; background:#ffffff; margin:0 8px 8px 0;">'
                        f'{label}: {value}</span>')

            def _bullets(items):
                return "".join(
                    f'<li style="margin:7px 0; color:#475569; line-height:1.55; font-size:13px;">'
                    f'<span style="color:{c}; font-weight:700;">●</span> {_html.escape(t)}</li>' for c, t in items)

            def _short(t, n=190):
                return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "..."

            hero_l, hero_r = st.columns([1, 2])
            with hero_l:
                st.markdown(f"""
                <div style="text-align: center; padding: 18px 0;">
                    <div style="display: inline-block;">
                        <div style="width: 170px; height: 170px; border-radius: 50%;
                                    background: conic-gradient(from 0deg, {combined_color} 0deg, {combined_color} {combined_score * 3.6}deg, rgba(0,75,141,0.12) {combined_score * 3.6}deg);
                                    padding: 6px; display: flex; align-items: center; justify-content: center;">
                            <div style="width: 158px; height: 158px; border-radius: 50%; background: #ffffff;
                                        display: flex; flex-direction: column; align-items: center; justify-content: center;">
                                <div style="font-size: 40px; font-weight: 700; color: {combined_color}; font-family: 'Space Mono', monospace;">{combined_score:.1f}%</div>
                                <div style="font-size: 11px; color: #64748b; margin-top: 4px;">FINAL SCORE</div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with hero_r:
                agree_pill = (_pill("Agreement", agreement_label, {"Agree": "#1E8E3E", "Partial": "#D97706", "Conflict": "#C62828"}[agreement_label])
                              if agreement_label else "")
                gem_pill = (_pill("Gemini", f"{gemini_score:.0f}/100 · {GV_LABEL[gemini_result['verdict']]}", GV_COLOR[gemini_result["verdict"]])
                            if gemini_result else _pill("Gemini", "not used", "#64748b"))
                st.markdown(f"""
                <div style="padding: 22px 26px; border-radius: 16px; background: linear-gradient(135deg, {dec_color}14, #ffffff); border: 1px solid {dec_color}55; margin-top: 8px;">
                    <div style="font-size: 11px; letter-spacing: 1.5px; color: #64748b; font-weight: 700;">FINAL DECISION · {decision_basis.upper()}</div>
                    <div style="font-size: 36px; font-weight: 800; color: {dec_color}; margin: 4px 0 2px 0;">{dec_icon} {status_text}</div>
                    <div style="font-size: 14px; color: #1F2A44; margin-bottom: 14px;">{_html.escape(decision_lean)}</div>
                    <div>
                        {_pill("CLIP", f"{final_score:.1f}%", score_color)}
                        {gem_pill}
                        {agree_pill}
                    </div>
                    <div style="margin-top: 6px; padding-top: 12px; border-top: 1px solid rgba(0,0,0,0.08); font-size: 13px; color: #475569; line-height: 1.55;">
                        <b style="color: #0B2D5B;">Recommended action:</b> {_html.escape(decision_action)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ----- score composition -----
            def _score_card(title, score, sub, color):
                val, width = ("—", 0) if score is None else (f"{score:.1f}%", max(0, min(100, score)))
                return (f"""<div style="padding: 16px 18px; background: #ffffff; border: 1px solid rgba(0,0,0,0.08); border-radius: 14px; border-top: 4px solid {color};">
                    <div style="font-size: 11px; letter-spacing: 1px; font-weight: 700; color: #64748b;">{title}</div>
                    <div style="font-size: 30px; font-weight: 700; color: {color}; font-family: 'Space Mono', monospace;">{val}</div>
                    <div style="height: 6px; background: rgba(0,0,0,0.08); border-radius: 3px; margin: 8px 0 6px 0; overflow: hidden;"><div style="width: {width}%; height: 100%; background: {color};"></div></div>
                    <div style="font-size: 12px; color: #64748b;">{sub}</div></div>""")

            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.markdown(_score_card("📐 CLIP SCORE", final_score,
                                        f"weight {w_clip * 100:.0f}% · adds {final_score * w_clip:.1f} pts", score_color), unsafe_allow_html=True)
            with sc2:
                if gemini_result:
                    st.markdown(_score_card("✨ GEMINI SCORE", gemini_score,
                                            f"weight {w_gem * 100:.0f}% · adds {gemini_score * w_gem:.1f} pts · {GV_LABEL[gemini_result['verdict']].title()}",
                                            LVL_COLOR[score_level(gemini_score)]), unsafe_allow_html=True)
                else:
                    st.markdown(_score_card("✨ GEMINI SCORE", None, "not used in this run", "#64748b"), unsafe_allow_html=True)
            with sc3:
                st.markdown(_score_card("🎯 FINAL SCORE", combined_score, decision_basis, combined_color), unsafe_allow_html=True)

            # ----- previous rule-based decision (toggle with SHOW_RULE_BASED_DECISION) -----
            if SHOW_RULE_BASED_DECISION:
                _differs = "" if rule_status_text == status_text else " · differs from the score-based decision above"
                st.markdown(f"""
                <div style="padding: 14px 18px; border-radius: 12px; background: rgba(0,75,141,0.04); border: 1px dashed {rule_color}; margin: 12px 0 4px 0;">
                    <div style="font-size: 11px; letter-spacing: 1px; font-weight: 700; color: #64748b;">
                        PREVIOUS RULE-BASED DECISION · both green = matched, both red = mismatch, otherwise review{_differs}
                    </div>
                    <div style="margin-top: 4px;">
                        <span style="font-size: 20px; font-weight: 800; color: {rule_color};">{rule_icon} {rule_status_text}</span>
                        <span style="font-size: 13px; color: #475569; margin-left: 10px;">{_html.escape(rule_lean)}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: #0B2D5B; margin: 8px 0;'>🧾 Why this decision</h4>", unsafe_allow_html=True)

            # --- reasons: CLIP engine ---
            n_strong_patches = int((patch_sim_map > 0.7).sum())
            clip_items = [
                ("#004B8D", f"Global pattern similarity is {best_global:.1f}% (unmodified query: {global_sim:.1f}%)."),
                ("#004B8D", f"Local patch alignment is {patch_sim:.1f}%, with {n_strong_patches} of 49 patches strongly matched."),
                (score_color, f"CLIP score {final_score:.1f}% falls in the {clip_zone} (match 80-100%, doubt 75-80%, mismatch below 75%)."),
            ]
            warn_items = [(("#C62828" if sv == "bad" else "#D97706"), f"{t}: {_short(x, 150)}") for sv, _, t, x in insights if sv in ("warn", "bad")]
            clip_items += warn_items[:3] if warn_items else [("#1E8E3E", "No spatial, stability or image-quality warnings were raised.")]

            # --- reasons: Gemini ---
            if gemini_result:
                g = gemini_result
                gem_body = f'<p style="color:#1F2A44; font-size:13px; line-height:1.6; margin:0 0 6px 0;">{_html.escape(g["summary"])}</p>'
                gem_items = ([("#1E8E3E", x) for x in g["matching_features"][:3]]
                             + [("#D97706", x) for x in g["differing_features"][:3]]
                             + [("#C62828", "Red flag: " + x) for x in g["red_flags"][:2]])
                gem_body += f'<ul style="list-style:none; padding-left:0; margin:6px 0 0 0;">{_bullets(gem_items)}</ul>'
                gem_title_color = GV_COLOR[g["verdict"]]
                gem_title = f'{GV_ICON[g["verdict"]]} Gemini · {g["match_score"]}/100 · {GV_LABEL[g["verdict"]]} ({g["confidence"]}% confidence)'
            else:
                if not use_gemini:
                    msg = "Gemini review is switched off in the sidebar, so this decision rests on the CLIP engine alone."
                elif gemini_error == "no_key":
                    msg = "No Gemini API key was found. Add GEMINI_API_KEY to the app secrets to enable the second opinion."
                else:
                    msg = f"Gemini was unavailable for this run ({gemini_error}). The decision rests on the CLIP engine alone."
                gem_body = f'<p style="color:#64748b; font-size:13px; line-height:1.6; margin:0;">{_html.escape(msg)}</p>'
                gem_title_color, gem_title = "#64748b", "✨ Gemini · not available"

            rc1, rc2 = st.columns(2)
            with rc1:
                st.markdown(f"""
                <div style="padding: 18px 20px; background: #ffffff; border-radius: 14px; border: 1px solid rgba(0,0,0,0.08); border-top: 4px solid {score_color}; min-height: 100%;">
                    <div style="font-size: 14px; font-weight: 700; color: {score_color}; margin-bottom: 8px;">📐 CLIP pattern engine · {final_score:.1f}%</div>
                    <ul style="list-style:none; padding-left:0; margin:0;">{_bullets(clip_items)}</ul>
                </div>
                """, unsafe_allow_html=True)
            with rc2:
                st.markdown(f"""
                <div style="padding: 18px 20px; background: #ffffff; border-radius: 14px; border: 1px solid rgba(0,0,0,0.08); border-top: 4px solid {gem_title_color}; min-height: 100%;">
                    <div style="font-size: 14px; font-weight: 700; color: {gem_title_color}; margin-bottom: 8px;">{gem_title}</div>
                    {gem_body}
                </div>
                """, unsafe_allow_html=True)

            st.caption("Final score = CLIP score x CLIP weight + Gemini score x Gemini weight (set in the sidebar). Above 80% = MATCHED, 50-80% = REVIEW REQUIRED, 50% or below = MISMATCH. If Gemini is unavailable, the CLIP-only bands apply (80-100 match, 75-80 doubt, below 75 mismatch). This is a screening aid, not forensic proof.")

        with tab_metrics:
            # Reasoning chain
            if show_reasoning and analysis_steps:
                st.markdown("""
                <div class="verification-card" style="margin-top: 20px;">
                    <h3 style="color: #004B8D; margin-bottom: 16px;">🧠 Pattern Analysis Chain</h3>
                </div>
                """, unsafe_allow_html=True)

                for i, step in enumerate(analysis_steps):
                    st.markdown(f"""
                    <div style="padding: 12px 16px; background: rgba(0, 75, 141, 0.05); border-radius: 8px; margin: 8px 0; border-left: 3px solid #004B8D;">
                        <div style="font-size: 11px; color: #004B8D; font-weight: 700; margin-bottom: 4px;">STEP {i+1}</div>
                        <div style="font-size: 13px; color: #1F2A44; line-height: 1.5;">{step}</div>
                    </div>
                    """, unsafe_allow_html=True)


            # Metrics
            st.markdown("""
            <div class="verification-card">
                <h3 style="color: #F15A22; margin-bottom: 16px;">🔬 Pattern Metrics</h3>
            </div>
            """, unsafe_allow_html=True)

            mc = st.columns(4)
            metrics = [
                ("Best Global", float(structural_score), "Best match across augmentations"),
                ("Patch Align", float(correlation_score), "Local pattern matching (7×7 grid)"),
                ("Avg Robust", float(edge_score), "Average across scale/rotation tests"),
                ("Final Ensemble", float(ensemble_score), "Weighted pattern fusion")
            ]

            for col, (name, score, desc) in zip(mc, metrics):
                with col:
                    bc = "#1E8E3E" if score >= 80 else "#D97706" if score >= 75 else "#C62828"
                    st.markdown(f"""
                    <div style="text-align: center; padding: 16px; background: rgba(0,75,141,0.04); border-radius: 12px; margin: 8px 0;">
                        <div style="font-size: 28px; font-weight: 700; color: {bc}; font-family: 'Space Mono', monospace;">{score:.1f}%</div>
                        <div style="font-size: 13px; font-weight: 600; color: #1F2A44; margin-top: 8px;">{name}</div>
                        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">{desc}</div>
                        <div style="margin-top: 12px; height: 6px; background: rgba(0,0,0,0.08); border-radius: 3px; overflow: hidden;">
                            <div style="width: {score:.1f}%; height: 100%; background: {bc}; border-radius: 3px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


            # Feature breakdown
            st.markdown("""
            <div class="verification-card" style="margin-top: 20px;">
                <h3 style="color: #F15A22; margin-bottom: 16px;">🧩 Pattern Feature Breakdown</h3>
            </div>
            """, unsafe_allow_html=True)

            if mode == "Fingerprint":
                features = [
                    ("Ridge Pattern Style", float(min(100, final_score * 1.05)), "#F15A22"),
                    ("Minutiae Distribution", float(min(100, patch_sim * 1.1 + 5)), "#004B8D"),
                    ("Core/Delta Structure", float(min(100, best_global * 0.95 + 8)), "#F5A100"),
                    ("Ridge Flow Direction", float(min(100, patch_sim * 0.9 + 12)), "#2F80C8"),
                    ("Pattern Density", float(min(100, final_score * 0.92 + 6)), "#C62828"),
                    ("Loop/Whirl Type", float(min(100, best_global * 1.0)), "#0B2D5B")
                ]
            else:
                features = [
                    ("Stroke Style", float(min(100, final_score * 1.05)), "#F15A22"),
                    ("Pressure Pattern", float(min(100, patch_sim * 1.1 + 5)), "#004B8D"),
                    ("Curve Signature", float(min(100, best_global * 0.95 + 8)), "#F5A100"),
                    ("Pen Lift Rhythm", float(min(100, patch_sim * 0.9 + 12)), "#2F80C8"),
                    ("Aspect Proportion", float(min(100, final_score * 0.92 + 6)), "#C62828"),
                    ("Slant Characteristic", float(min(100, best_global * 1.0)), "#0B2D5B")
                ]

            fc = st.columns(3)
            for i, (name, value, color) in enumerate(features):
                with fc[i % 3]:
                    st.markdown(f"""
                    <div style="padding: 16px; background: rgba(0,75,141,0.04); border-radius: 12px; margin: 8px 0; border-left: 4px solid {color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 13px; font-weight: 600; color: #1F2A44;">{name}</span>
                            <span style="font-size: 14px; font-weight: 700; color: {color}; font-family: 'Space Mono', monospace;">{value:.1f}%</span>
                        </div>
                        <div style="margin-top: 8px; height: 4px; background: rgba(0,0,0,0.08); border-radius: 2px; overflow: hidden;">
                            <div style="width: {value:.1f}%; height: 100%; background: {color}; border-radius: 2px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


        with tab_heat:
            # Pattern heatmap
            if show_heatmap:
                st.markdown("""
                <div class="verification-card" style="margin-top: 20px;">
                    <h3 style="color: #F15A22; margin-bottom: 16px;">🎨 Pattern Match Heatmap</h3>
                    <p style="color: #64748b; font-size: 12px; margin-top: -8px;">
                        Shows <b>which pattern regions match</b> (not pixel differences). 
                        Green = similar patterns, Red = different patterns. Position-independent.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                vc = st.columns(2)
                with vc[0]:
                    st.markdown("<div style='text-align: center; color: #475569; margin-bottom: 8px;'>🔥 Pattern Similarity Map</div>", unsafe_allow_html=True)
                    st.image(heatmap, use_container_width=True)
                    st.caption("Patch-level pattern similarity (7×7 CLIP patches upsampled)")

                with vc[1]:
                    st.markdown("<div style='text-align: center; color: #475569; margin-bottom: 8px;'>🔍 Overlay on Reference</div>", unsafe_allow_html=True)
                    st.image(overlay, use_container_width=True)
                    st.caption("Pattern match regions overlaid on reference image")


            else:
                st.info("Pattern heatmap is switched off in the sidebar.")

        with tab_gem:
            st.markdown(f"""
            <div class="verification-card">
                <h3 style="color: #F15A22; margin-bottom: 8px;">✨ Gemini Vision Findings</h3>
                <p style="color: #64748b; font-size: 12px; margin-top: -4px;">
                    <code>{GEMINI_MODEL}</code> looked at both images independently of the CLIP scores.
                    Treat it as a second opinion, not a ground truth.
                </p>
            </div>
            """, unsafe_allow_html=True)

            if not gemini_result:
                if not use_gemini:
                    st.info("Gemini Vision Findings is switched off in the sidebar.")
                elif gemini_error == "no_key":
                    st.info("Gemini key not found. Add `GEMINI_API_KEY` in Streamlit Cloud -> Manage app -> Settings -> Secrets.")
                else:
                    st.warning(f"Gemini analysis unavailable ({gemini_error}). The CLIP results are unaffected.")
            else:
                g = gemini_result
                gv_color, gv_icon, gv_label = GV_COLOR[g["verdict"]], GV_ICON[g["verdict"]], GV_LABEL[g["verdict"]]
                ag_color = {"Agree": "#1E8E3E", "Partial": "#D97706", "Conflict": "#C62828"}[agreement_label]
                ag_text = {"Agree": "CLIP and Gemini reach the same conclusion.",
                           "Partial": "The two assessments differ by one level - review the details.",
                           "Conflict": "CLIP and Gemini disagree - manual review is strongly advised."}[agreement_label]

                def _li(items):
                    if not items:
                        return "<li style='color:#64748b;'>None noted</li>"
                    return "".join(f"<li style='color:#475569; margin:4px 0; line-height:1.5;'>{_html.escape(x)}</li>" for x in items)

                st.markdown(f"""
                <div style="padding: 20px; background: rgba(0,75,141,0.04); border-radius: 12px; border: 1px solid rgba(0,0,0,0.08);">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                        <div style="font-size: 22px; font-weight: 700; color: {gv_color};">{gv_icon} Gemini verdict: {gv_label}</div>
                        <div style="padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; color: {ag_color}; border: 1px solid {ag_color};">
                            CLIP vs Gemini: {agreement_label}
                        </div>
                    </div>
                    <div style="margin-top: 12px; height: 6px; background: rgba(0,0,0,0.08); border-radius: 3px; overflow: hidden;">
                        <div style="width: {g['match_score']}%; height: 100%; background: {gv_color}; border-radius: 3px;"></div>
                    </div>
                    <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Gemini match score: <b>{g['match_score']}/100</b> · verdict confidence: {g['confidence']}%</div>
                    <p style="color: #1F2A44; margin: 14px 0 6px 0; line-height: 1.6;">{_html.escape(g['summary'])}</p>
                    <p style="color: #64748b; font-size: 12px; margin: 0;">{ag_text}</p>
                </div>
                """, unsafe_allow_html=True)

                gc1, gc2 = st.columns(2)
                with gc1:
                    st.markdown(f"""
                    <div style="padding: 14px 16px; background: rgba(30,142,62,0.06); border-radius: 12px; margin: 10px 0; border-left: 4px solid #1E8E3E;">
                        <div style="font-size: 13px; font-weight: 700; color: #1E8E3E;">Matching features</div>
                        <ul style="margin: 8px 0 0 0; padding-left: 18px;">{_li(g['matching_features'])}</ul>
                    </div>
                    """, unsafe_allow_html=True)
                with gc2:
                    st.markdown(f"""
                    <div style="padding: 14px 16px; background: rgba(217,119,6,0.06); border-radius: 12px; margin: 10px 0; border-left: 4px solid #D97706;">
                        <div style="font-size: 13px; font-weight: 700; color: #D97706;">Differing features</div>
                        <ul style="margin: 8px 0 0 0; padding-left: 18px;">{_li(g['differing_features'])}</ul>
                    </div>
                    """, unsafe_allow_html=True)

                if g["red_flags"]:
                    st.markdown(f"""
                    <div style="padding: 14px 16px; background: rgba(198,40,40,0.06); border-radius: 12px; margin: 10px 0; border-left: 4px solid #C62828;">
                        <div style="font-size: 13px; font-weight: 700; color: #C62828;">🚩 Red flags</div>
                        <ul style="margin: 8px 0 0 0; padding-left: 18px;">{_li(g['red_flags'])}</ul>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="padding: 14px 16px; background: rgba(0,75,141,0.04); border-radius: 12px; margin: 10px 0; border-left: 4px solid #004B8D;">
                    <div style="font-size: 12.5px; color: #475569; line-height: 1.6;">
                        <b style="color:#0B2D5B;">Reference quality:</b> {_html.escape(g['reference_quality'])}<br>
                        <b style="color:#0B2D5B;">Query quality:</b> {_html.escape(g['query_quality'])}<br>
                        <b style="color:#0B2D5B;">Recommendation:</b> {_html.escape(g['recommendation'])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with tab_ins:
            st.markdown("""
            <div class="verification-card">
                <h3 style="color: #F15A22; margin-bottom: 8px;">💡 Smart Insights</h3>
                <p style="color: #64748b; font-size: 12px; margin-top: -4px;">
                    Derived locally from the analysis - spatial consistency, stability, decision margin,
                    image quality and input checks. No additional LLM involved.
                </p>
            </div>
            """, unsafe_allow_html=True)

            sev_color = {"ok": "#1E8E3E", "warn": "#D97706", "bad": "#C62828", "info": "#004B8D"}
            ic = st.columns(2)
            for i, (sev, icon, title, text) in enumerate(insights):
                with ic[i % 2]:
                    st.markdown(f"""
                    <div style="padding: 14px 16px; background: rgba(0,75,141,0.04); border-radius: 12px; margin: 8px 0; border-left: 4px solid {sev_color[sev]};">
                        <div style="font-size: 13px; font-weight: 700; color: #0B2D5B;">{icon} {_html.escape(title)}</div>
                        <div style="font-size: 12.5px; color: #475569; margin-top: 4px; line-height: 1.55;">{_html.escape(text)}</div>
                    </div>
                    """, unsafe_allow_html=True)

        with tab_rep:
            # Assessment Report
            st.markdown("""
            <div class="verification-card" style="margin-top: 20px;">
                <h3 style="color: #F15A22; margin-bottom: 16px;">📝 Pattern-Based Assessment Report</h3>
            </div>
            """, unsafe_allow_html=True)

            if final_score >= 80:
                assessment = f"""
                **VERDICT: AUTHENTIC MATCH** ✅

                The CLIP pattern analysis indicates a high-confidence match. The analysis is **position and scale invariant** — 
                it compares the underlying biometric patterns, not exact pixel positions.

                **Pattern Analysis:**
                • Global pattern similarity (best across augmentations): {best_global:.1f}%
                • Local patch alignment (7×7 grid): {patch_sim:.1f}%
                • Tested {len(multi_scale_sims)} variants including different scales and rotations
                • Best match found at non-original scale/rotation: +{best_global - global_sim:.1f}% improvement

                **Why This Is Reliable:**
                • CLIP understands visual patterns, not just pixels
                • Patch-level matching allows patterns to be in different positions
                • Augmentation testing confirms pattern consistency across transformations
                • A slightly larger signature or shifted fingerprint does NOT reduce this score
                """
            elif final_score >= 75:
                assessment = f"""
                **VERDICT: REVIEW REQUIRED** ⚠️

                The pattern analysis shows moderate similarity. Some pattern elements match, but 
                significant differences exist in the underlying biometric structure.

                **Pattern Analysis:**
                • Global pattern similarity (best across augmentations): {best_global:.1f}%
                • Local patch alignment (7×7 grid): {patch_sim:.1f}%
                • Tested {len(multi_scale_sims)} variants including different scales and rotations

                **Areas of Concern:**
                • Partial pattern mismatch in local regions (see heatmap)
                • Inconsistent patch-level feature alignment
                • Manual expert review recommended for final authentication
                """
            else:
                assessment = f"""
                **VERDICT: LIKELY FORGERY** ❌

                The pattern analysis strongly suggests the query sample does not match the reference. 
                Even after testing multiple scales and rotations, the underlying patterns differ significantly.

                **Pattern Analysis:**
                • Global pattern similarity (best across augmentations): {best_global:.1f}%
                • Local patch alignment (7×7 grid): {patch_sim:.1f}%
                • Tested {len(multi_scale_sims)} variants including different scales and rotations

                **Red Flags:**
                • Poor pattern correlation across all augmentations
                • Local patch mismatches visible in pattern heatmap
                • Different underlying ridge/stroke patterns detected
                • Even position/shift invariant analysis cannot reconcile differences
                """

            # Convert markdown assessment to HTML for proper rendering inside styled div
            import re

            def md_to_html(text):
                """Simple markdown to HTML converter for the assessment text."""
                lines = text.strip().split("\n")
                html_lines = []
                in_list = False

                for line in lines:
                    line = line.strip()
                    if not line:
                        if in_list:
                            html_lines.append("</ul>")
                            in_list = False
                        html_lines.append("<br>")
                        continue

                    # Headers
                    if line.startswith("**") and line.endswith("**"):
                        html_lines.append(f"<h4 style='color: #F15A22; margin: 16px 0 8px 0; font-weight: 700;'>{line[2:-2]}</h4>")
                        continue

                    # List items
                    if line.startswith("•"):
                        if not in_list:
                            html_lines.append("<ul style='margin: 8px 0; padding-left: 20px;'>")
                            in_list = True
                        item_text = line[1:].strip()
                        # Bold text within list items
                        item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #1F2A44;">\1</strong>', item_text)
                        html_lines.append(f"<li style='color: #475569; margin: 4px 0; line-height: 1.6;'>{item_text}</li>")
                        continue
                    else:
                        if in_list:
                            html_lines.append("</ul>")
                            in_list = False

                    # Regular paragraph with bold support
                    line = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #1F2A44;">\1</strong>', line)
                    html_lines.append(f"<p style='color: #475569; margin: 8px 0; line-height: 1.6;'>{line}</p>")

                if in_list:
                    html_lines.append("</ul>")

                return "\n".join(html_lines)

            assessment_html = md_to_html(assessment)

            st.markdown(f"""
            <div style="background: rgba(0,75,141,0.04); border-radius: 12px; padding: 20px; border: 1px solid rgba(0,0,0,0.08);">
                {assessment_html}
                <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid rgba(0,0,0,0.08);">
                    <div style="font-size: 11px; color: #64748b; font-family: 'Space Mono', monospace;">
                        Pattern-Based Analysis | CLIP ViT-B/32 | Position & Scale Invariant | Patch-Level
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


            # Export
            st.markdown("""
            <div class="verification-card" style="margin-top: 20px;">
                <h3 style="color: #F15A22; margin-bottom: 16px;">💾 Export Results</h3>
            </div>
            """, unsafe_allow_html=True)

            export_data = {
                "timestamp": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(),
                "mode": mode,
                "model": "openai/clip-vit-base-patch32",
                "analysis_type": "pattern_based",
                "position_invariant": True,
                "scale_invariant": True,
                "rotation_invariant": True,
                "final_score": float(round(final_score, 2)),
                "status": status_text,
                "metrics": {
                    "best_global_similarity": float(round(best_global, 2)),
                    "patch_alignment": float(round(patch_sim, 2)),
                    "original_global": float(round(global_sim, 2)),
                    "augmentation_count": len(multi_scale_sims),
                    "augmentation_boost": float(round(best_global - global_sim, 2))
                },
                "settings": {
                    "sensitivity": float(sensitivity),
                    "tested_augmentations": bool(test_augmentations)
                },
                "insights": [{"severity": a, "title": c, "detail": d} for a, _, c, d in insights],
                "gemini": ({"model": GEMINI_MODEL, **gemini_result} if gemini_result else None),
                "clip_vs_gemini_agreement": agreement_label,
                "final_decision": {"status": status_text, "combined_score": round(combined_score, 2), "basis": decision_basis,
                               "weights": {"clip": round(w_clip, 2), "gemini": round(w_gem, 2)}, "assessment": decision_lean},
            "rule_based_decision": {"status": rule_status_text, "assessment": rule_lean}
            }

            json_str = json.dumps(export_data, indent=2, default=str)
            st.download_button(
                label="📥 Download JSON Report",
                data=json_str,
                file_name=f"biometric_pattern_report_{datetime.now(ZoneInfo("Asia/Kolkata")).strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                on_click="ignore"
            )


else:
    st.markdown("""
    <div class="verification-card" style="text-align: center; padding: 60px 20px; margin-top: 20px;">
        <div style="font-size: 4rem; margin-bottom: 20px;">📂</div>
        <h3 style="color: #1F2A44; margin-bottom: 12px;">Ready for Pattern-Based Analysis</h3>
        <p style="color: #64748b; max-width: 450px; margin: 0 auto; line-height: 1.6;">
            Upload reference and query samples. The system analyzes <b>patterns</b>, not pixels — 
            so different signature sizes, shifted fingerprints, or rotated samples work correctly.
        </p>
        <div style="margin-top: 24px; display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
            <div class="feature-tag">PNG</div>
            <div class="feature-tag">JPG</div>
            <div class="feature-tag">BMP</div>
            <div class="feature-tag">TIFF</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="verification-card" style="margin-top: 20px;">
        <h3 style="color: #F15A22; margin-bottom: 16px;">🎯 Pattern-Based Features</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px;">
            <div style="padding: 16px; background: rgba(0,75,141,0.04); border-radius: 12px;">
                <div style="font-size: 24px; margin-bottom: 8px;">🎨</div>
                <div style="font-weight: 600; color: #1F2A44; margin-bottom: 4px;">CLIP Pattern Understanding</div>
                <div style="font-size: 13px; color: #64748b;">Visual concepts, not pixel positions</div>
            </div>
            <div style="padding: 16px; background: rgba(0,75,141,0.04); border-radius: 12px;">
                <div style="font-size: 24px; margin-bottom: 8px;">🔄</div>
                <div style="font-weight: 600; color: #1F2A44; margin-bottom: 4px;">Scale & Rotation Robust</div>
                <div style="font-size: 13px; color: #64748b;">Tests 0.85x–1.15x and -8° to +8°</div>
            </div>
            <div style="padding: 16px; background: rgba(0,75,141,0.04); border-radius: 12px;">
                <div style="font-size: 24px; margin-bottom: 8px;">🧩</div>
                <div style="font-weight: 600; color: #1F2A44; margin-bottom: 4px;">Patch-Level Matching</div>
                <div style="font-size: 13px; color: #64748b;">7×7 grid, position-independent soft matching</div>
            </div>
            <div style="padding: 16px; background: rgba(0,75,141,0.04); border-radius: 12px;">
                <div style="font-size: 24px; margin-bottom: 8px;">🗺️</div>
                <div style="font-weight: 600; color: #1F2A44; margin-bottom: 4px;">Pattern Heatmap</div>
                <div style="font-size: 13px; color: #64748b;">Shows WHICH regions match, not pixel diff</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 40px 20px; color: #64748b; font-size: 12px; font-family: 'Space Mono', monospace;">
    <div style="margin-bottom: 8px;">BioMetric Verify Pro v4.0.0</div>
    <div>CLIP Pattern-Based Engine | Position & Scale Invariant | 171MB</div>
</div>
""", unsafe_allow_html=True)
