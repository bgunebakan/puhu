# Puhu vs. Pillow Benchmarks

This document summarizes benchmarks comparing **Puhu** with **Pillow** for common image operations.

All benchmarks were run on the same machine using the same input image and aligned operations to make the comparison as fair as possible.

---

## Benchmark Setup

- **Libraries**
  - Puhu: 0.3.0
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

| Test          | Description                                                   | Pillow mean ± σ (ms) | Puhu mean ± σ (ms) |        Speedup (Puhu vs. Pillow) |
| :------------ | :------------------------------------------------------------ | -------------------: | -----------------: | -------------------------------: |
| `open_save`   | Open JPEG and save as PNG (disk I/O)                          |          192.1 ± 3.7 |        105.1 ± 4.9 |          **1.83 ± 0.09× faster** |
| `resize`      | Open, resize to 800×600 (LANCZOS), save PNG                   |          198.4 ± 3.9 |       226.6 ± 10.3 | **0.88 ± 0.04×** (Pillow faster) |
| `crop`        | Open, crop a sub-rectangle, save PNG                          |          141.0 ± 4.4 |         89.9 ± 7.0 |          **1.57 ± 0.13× faster** |
| `rotate`      | Open, rotate by 90°, save PNG                                 |        310.8 ± 188.5 |        155.5 ± 8.5 |          **2.00 ± 1.22× faster** |
| `transpose`   | Open, flip image (left–right), save PNG                       |         213.1 ± 10.8 |        135.1 ± 9.4 |          **1.58 ± 0.14× faster** |
| `thumbnail`   | Open, generate 128 px thumbnail (LANCZOS), save PNG           |           91.7 ± 4.2 |        192.9 ± 8.7 | **0.48 ± 0.03×** (Pillow faster) |
| `to_bytes`    | Open, convert image to raw pixel bytes in memory              |          147.5 ± 2.7 |       100.4 ± 11.2 |          **1.47 ± 0.17× faster** |
| `new`         | Create a new 1920×1080 RGBA image, fill solid color, save PNG |          102.6 ± 4.7 |         63.1 ± 4.2 |          **1.63 ± 0.13× faster** |
| `paste`       | Open, paste 800×600 image, save PNG                           |          211.0 ± 5.2 |        124.5 ± 9.7 |          **1.69 ± 0.14× faster** |
| `paste_mask`  | Open, paste image with transparency mask, save PNG            |          208.4 ± 3.8 |        123.5 ± 9.3 |          **1.69 ± 0.13× faster** |
| `paste_color` | Open, fill region with solid color, save PNG                  |          209.1 ± 5.1 |        117.8 ± 7.8 |          **1.78 ± 0.13× faster** |
| `pipeline`    | Open → resize → crop → 180° rotate → save PNG                 |          198.5 ± 4.1 |       222.0 ± 13.4 | **0.89 ± 0.06×** (Pillow faster) |

> Note: All values above are a single run of `hyperfine --runs 30` for each test on the same machine. Absolute values will vary across hardware, but relative trends are informative.
