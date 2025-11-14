# Puhu vs. Pillow Benchmarks

This document summarizes benchmarks comparing **Puhu** with **Pillow** for common image operations.

All benchmarks were run on the same machine using the same input image and aligned operations to make the comparison as fair as possible.

---

## Benchmark Setup

- **Libraries**
  - Puhu: 0.2.2
  - Pillow: 12.0.0
- **Harness**
  - Tool: [`hyperfine`](https://github.com/sharkdp/hyperfine)
  - Each benchmark is run **30 times** per library after **3 warmup runs**.
  - Hyperfine reports mean time, standard deviation, range, and speedup with uncertainty.
- **Environment**
  - Same Python interpreter and virtual environment for both libraries.
  - Same Macbook Air M3, 2024, 16GB RAM, macOS 15.7.1
  - Single large (4000x3000) JPEG input image.

---

## Results

All times are in **milliseconds** (ms). Lower is better. Speedup is reported as:

> `Puhu speedup` = (Pillow time) / (Puhu time)

so values **> 1.0** mean Puhu is faster, and values **< 1.0** mean Pillow is faster.

### Summary Table

| Test        | Description                                                   | Pillow mean ± σ (ms) | Puhu mean ± σ (ms) |        Speedup (Puhu vs. Pillow) |
| ----------- | ------------------------------------------------------------- | -------------------: | -----------------: | -------------------------------: |
| `open_save` | Open JPEG and save as PNG (disk I/O)                          |          184.6 ± 3.9 |        107.4 ± 5.3 |          **1.72 ± 0.09× faster** |
| `resize`    | Open, resize to 800×600 (LANCZOS), save PNG                   |          194.0 ± 2.7 |        223.8 ± 2.4 | **0.87 ± 0.02×** (Pillow faster) |
| `crop`      | Open, crop a sub-rectangle, save PNG                          |          127.2 ± 5.4 |         85.2 ± 1.8 |          **1.49 ± 0.07× faster** |
| `rotate`    | Open, rotate by 90°, save PNG                                 |          245.1 ± 7.2 |        147.4 ± 2.3 |          **1.66 ± 0.06× faster** |
| `transpose` | Open, flip image (left–right), save PNG                       |          206.9 ± 8.5 |        122.7 ± 1.6 |          **1.69 ± 0.07× faster** |
| `thumbnail` | Open, generate 128 px thumbnail (LANCZOS), save PNG           |           86.0 ± 0.9 |        190.3 ± 2.0 | **0.45 ± 0.01×** (Pillow faster) |
| `to_bytes`  | Open, convert image to raw pixel bytes in memory              |          142.0 ± 2.9 |        101.6 ± 1.9 |          **1.40 ± 0.04× faster** |
| `new`       | Create a new 1920×1080 RGBA image, fill solid color, save PNG |           94.8 ± 1.5 |         59.2 ± 1.1 |          **1.60 ± 0.04× faster** |
| `pipeline`  | Open → resize → crop → 180° rotate → save PNG                 |          191.0 ± 1.1 |        224.3 ± 2.5 | **0.85 ± 0.01×** (Pillow faster) |

> Note: All values above are a single run of `hyperfine --runs 30` for each test on the same machine. Absolute values will vary across hardware, but relative trends are informative.
