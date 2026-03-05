#!/usr/bin/env python3
from __future__ import annotations
"""
Hyperfine benchmark runner for Puhu vs Pillow.

One-line change notes:
- Uses fixed defaults (`--runs 30`, `--warmup 3`) for stable comparisons.
- Reuses generated input fixtures in `benchmark_results/` across runs.
- Prints a markdown table matching the BENCHMARKS.md column format.
- Can optionally write only the table via `--table-out` for easy copy/paste.
- Does not mutate BENCHMARKS.md automatically.
"""

import argparse
import json
import math
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

TESTS: List[Tuple[str, str]] = [
    ("open_save", "Open JPEG and save as PNG (disk I/O)"),
    ("resize", "Open, resize to 800x600 (LANCZOS), save PNG"),
    ("crop", "Open, crop a sub-rectangle, save PNG"),
    ("rotate", "Open, rotate by 90 deg, save PNG"),
    ("transpose", "Open, flip image (left-right), save PNG"),
    ("thumbnail", "Open, generate 128 px thumbnail (LANCZOS), save PNG"),
    ("to_bytes", "Open, convert image to raw pixel bytes in memory"),
    ("new", "Create a new 1920x1080 RGBA image, fill solid color, save PNG"),
    ("paste", "Open, paste 800x600 image, save PNG"),
    ("paste_mask", "Open, paste image with transparency mask, save PNG"),
    ("paste_color", "Open, fill region with solid color, save PNG"),
    ("pipeline", "Open -> resize -> crop -> 180 deg rotate -> save PNG"),
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run hyperfine benchmarks and print a copyable markdown table.")
    parser.add_argument("--runs", type=int, default=30)
    parser.add_argument("--warmup", type=int, default=3)
    parser.add_argument("--work-dir", default="benchmark_results")
    parser.add_argument("--table-out", default=None, help="Optional file path to also write the markdown table.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    work_dir = repo_root / args.work_dir
    work_dir.mkdir(parents=True, exist_ok=True)

    hyperfine = shutil.which("hyperfine")
    if not hyperfine:
        raise SystemExit("hyperfine is required. Install it and rerun.")

    try:
        import PIL
        from PIL import Image, ImageDraw
    except ModuleNotFoundError as exc:
        raise SystemExit("Missing dependency: Pillow. Install with `python -m pip install pillow`.") from exc

    try:
        import puhu
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing dependency: puhu. Build/install the extension first with `maturin develop --release`."
        ) from exc

    input_path = work_dir / "input_4000x3000.jpg"
    overlay_path = work_dir / "overlay_800x600.png"
    if not input_path.exists():
        img = Image.new("RGB", (4000, 3000), (45, 58, 73))
        d = ImageDraw.Draw(img)
        for i in range(0, 4000, 200):
            d.line((i, 0, i, 3000), fill=(70, 90, 110), width=2)
        for j in range(0, 3000, 200):
            d.line((0, j, 4000, j), fill=(70, 90, 110), width=2)
        img.save(input_path, quality=90)
    if not overlay_path.exists():
        fg = Image.new("RGB", (800, 600), (220, 80, 70))
        d = ImageDraw.Draw(fg)
        d.rectangle((50, 50, 750, 550), outline=(255, 255, 255), width=6)
        fg.save(overlay_path)

    py = sys.executable
    run_pillow = repo_root / "benchmark_results" / "_run_pillow.py"
    run_puhu = repo_root / "benchmark_results" / "_run_puhu.py"

    run_pillow.write_text(
        """
from pathlib import Path
from PIL import Image
if hasattr(Image, 'Resampling'): RESAMPLE_LANCZOS = Image.Resampling.LANCZOS
else: RESAMPLE_LANCZOS = Image.LANCZOS
if hasattr(Image, 'Transpose'): TRANSPOSE_FLIP_LR = Image.Transpose.FLIP_LEFT_RIGHT
else: TRANSPOSE_FLIP_LR = Image.FLIP_LEFT_RIGHT

def run(test, input_path, overlay_path, output_path):
    if test=='open_save': Image.open(input_path).save(output_path); return
    if test=='resize': Image.open(input_path).resize((800,600), RESAMPLE_LANCZOS).save(output_path); return
    if test=='crop': Image.open(input_path).crop((300,300,3300,2500)).save(output_path); return
    if test=='rotate': Image.open(input_path).rotate(90, expand=False).save(output_path); return
    if test=='transpose': Image.open(input_path).transpose(TRANSPOSE_FLIP_LR).save(output_path); return
    if test=='thumbnail':
        img=Image.open(input_path); img.thumbnail((128,128), RESAMPLE_LANCZOS); img.save(output_path); return
    if test=='to_bytes': _=Image.open(input_path).tobytes(); return
    if test=='new': Image.new('RGBA',(1920,1080),(64,128,255,255)).save(output_path); return
    if test=='paste':
        bg=Image.open(input_path).convert('RGB'); fg=Image.open(overlay_path).convert('RGB'); bg.paste(fg,(200,200)); bg.save(output_path); return
    if test=='paste_mask':
        bg=Image.open(input_path).convert('RGB'); fg=Image.open(overlay_path).convert('RGB'); mask=Image.new('L',fg.size,128); bg.paste(fg,(200,200),mask); bg.save(output_path); return
    if test=='paste_color':
        img=Image.open(input_path).convert('RGB'); img.paste((255,0,0),(200,200,1000,800)); img.save(output_path); return
    if test=='pipeline':
        img=Image.open(input_path).convert('RGB'); img=img.resize((1600,1200), RESAMPLE_LANCZOS); img=img.crop((100,100,1200,900)); img=img.rotate(180,expand=False); img.save(output_path); return
    raise ValueError(test)

if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--test', required=True); p.add_argument('--input', required=True); p.add_argument('--overlay', required=True); p.add_argument('--output', required=True)
    a=p.parse_args(); run(a.test, Path(a.input), Path(a.overlay), Path(a.output))
""".strip()
        + "\n",
        encoding="utf-8",
    )

    run_puhu.write_text(
        """
from pathlib import Path
import puhu

def run(test, input_path, overlay_path, output_path):
    if test=='open_save': img=puhu.open(input_path); img.save(output_path); return
    if test=='resize': img=puhu.open(input_path).resize((800,600), resample=puhu.Resampling.LANCZOS); img.save(output_path); return
    if test=='crop': img=puhu.open(input_path).crop((300,300,3300,2500)); img.save(output_path); return
    if test=='rotate': img=puhu.open(input_path).rotate(90); img.save(output_path); return
    if test=='transpose': img=puhu.open(input_path).transpose(puhu.Transpose.FLIP_LEFT_RIGHT); img.save(output_path); return
    if test=='thumbnail':
        img=puhu.open(input_path); img.thumbnail((128,128), resample=puhu.Resampling.LANCZOS); img.save(output_path); return
    if test=='to_bytes': _=puhu.open(input_path).to_bytes(); return
    if test=='new': puhu.new('RGBA',(1920,1080),(64,128,255,255)).save(output_path); return
    if test=='paste':
        bg=puhu.open(input_path); fg=puhu.open(overlay_path); bg.paste(fg,(200,200)); bg.save(output_path); return
    if test=='paste_mask':
        bg=puhu.open(input_path); fg=puhu.open(overlay_path); mask=puhu.new('L', fg.size, 128); bg.paste(fg,(200,200),mask); bg.save(output_path); return
    if test=='paste_color':
        img=puhu.open(input_path); img.paste((255,0,0),(200,200,1000,800)); img.save(output_path); return
    if test=='pipeline':
        img=puhu.open(input_path); img=img.resize((1600,1200), resample=puhu.Resampling.LANCZOS); img=img.crop((100,100,1200,900)); img=img.rotate(180); img.save(output_path); return
    raise ValueError(test)

if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--test', required=True); p.add_argument('--input', required=True); p.add_argument('--overlay', required=True); p.add_argument('--output', required=True)
    a=p.parse_args(); run(a.test, Path(a.input), Path(a.overlay), Path(a.output))
""".strip()
        + "\n",
        encoding="utf-8",
    )

    def parse_export(path: Path) -> Dict[str, Dict[str, float]]:
        obj = json.loads(path.read_text(encoding="utf-8"))
        out: Dict[str, Dict[str, float]] = {}
        for row in obj["results"]:
            out[row["command"]] = {
                "mean_ms": row["mean"] * 1000.0,
                "stddev_ms": row["stddev"] * 1000.0,
            }
        return out

    def speedup_with_error(pillow_mean: float, pillow_std: float, puhu_mean: float, puhu_std: float) -> Tuple[float, float]:
        ratio = pillow_mean / puhu_mean
        rel_var = (pillow_std / pillow_mean) ** 2 + (puhu_std / puhu_mean) ** 2
        return ratio, abs(ratio) * math.sqrt(rel_var)

    def fmt_speedup(value: float, err: float) -> str:
        if value >= 1.0:
            return f"**{value:.2f} +/- {err:.2f}x faster**"
        return f"**{value:.2f} +/- {err:.2f}x** (Pillow faster)"

    export_json = work_dir / "hyperfine.json"
    rows: List[Dict[str, str]] = []

    for test_name, description in TESTS:
        out_puhu = work_dir / f"out_{test_name}_puhu.png"
        out_pillow = work_dir / f"out_{test_name}_pillow.png"
        pillow_cmd = f"{py} {run_pillow} --test {test_name} --input {input_path} --overlay {overlay_path} --output {out_pillow}"
        puhu_cmd = f"{py} {run_puhu} --test {test_name} --input {input_path} --overlay {overlay_path} --output {out_puhu}"

        subprocess.run(
            [
                hyperfine,
                "--runs", str(args.runs),
                "--warmup", str(args.warmup),
                "--export-json", str(export_json),
                "--shell=none",
                pillow_cmd,
                puhu_cmd,
            ],
            cwd=repo_root,
            check=True,
        )

        parsed = parse_export(export_json)
        pillow = parsed[pillow_cmd]
        puhu_row = parsed[puhu_cmd]
        ratio, err = speedup_with_error(
            pillow["mean_ms"], pillow["stddev_ms"], puhu_row["mean_ms"], puhu_row["stddev_ms"]
        )

        rows.append(
            {
                "test": test_name,
                "description": description,
                "pillow": f"{pillow['mean_ms']:.1f} +/- {pillow['stddev_ms']:.1f}",
                "puhu": f"{puhu_row['mean_ms']:.1f} +/- {puhu_row['stddev_ms']:.1f}",
                "speedup": fmt_speedup(ratio, err),
            }
        )

    table_lines = [
        "| Test | Description | Pillow mean +/- sigma (ms) | Puhu mean +/- sigma (ms) | Speedup (Puhu vs. Pillow) |",
        "| :--- | :--- | ---: | ---: | ---: |",
    ]
    for r in rows:
        table_lines.append(
            f"| `{r['test']}` | {r['description']} | {r['pillow']} | {r['puhu']} | {r['speedup']} |"
        )

    table_lines.append("")
    table_lines.append(
        f"> Note: All values above are a single run of `hyperfine --runs {args.runs}` for each test on the same machine. "
        "Absolute values will vary across hardware, but relative trends are informative."
    )
    table = "\n".join(table_lines) + "\n"

    print("\nCopyable benchmark table:\n")
    print(table)

    if args.table_out:
        out_path = Path(args.table_out)
        out_path.write_text(table, encoding="utf-8")
        print(f"Wrote table to {out_path}")

    hf_version = subprocess.run([hyperfine, "--version"], check=True, text=True, capture_output=True).stdout.strip()
    print(f"Environment: Python {platform.python_version()}, Pillow {PIL.__version__}, Puhu {puhu.__version__}, {hf_version}")
