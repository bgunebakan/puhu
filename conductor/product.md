# Initial Concept\n\nA high-performance image processing library for Python, powered by Rust, with a Pillow-compatible API.

# Product Guide: Puhu

## Vision
Puhu aims to be the go-to image processing library for Python developers who require the performance of Rust without sacrificing the ease of use provided by the Pillow API. By providing a high-performance, memory-safe alternative to traditional libraries, Puhu enables faster data processing pipelines and more efficient web services.

## Target Users
- **Performance-Oriented Python Developers:** Developers who have hit performance bottlenecks with Pillow and need a drop-in replacement that scales.
- **Backend & Web Engineers:** Developers building high-concurrency services where server-side image manipulation (resizing, watermarking, format conversion) must be as fast and resource-efficient as possible.

## Primary Goals
- **API Compatibility:** Provide a familiar experience by matching the most commonly used Pillow operations, allowing for a seamless transition.
- **Efficiency & Safety:** Leverage Rust's memory safety and performance characteristics to minimize memory footprint and eliminate common categories of bugs like memory leaks.
- **Superior Performance:** Target 2x to 10x faster execution for core operations such as resizing, cropping, and filtering compared to pure Python or C-based alternatives.

## Key Features
- **Core Manipulation:** Comprehensive support for opening, saving, resizing, cropping, rotating, and converting between popular image formats (PNG, JPEG, WEBP, etc.).
- **Advanced Processing:** High-performance implementations of blurs, color adjustments, and kernel convolutions.
- **Compositing & Drawing:** Robust support for drawing primitives (lines, shapes, text) and complex layer compositing.

## Technical Philosophy
- **No Silent Fallbacks:** To ensure users always benefit from Rust's performance, operations not yet implemented in the Rust core will raise a `NotImplementedError`. This prevents performance regressions that might occur with hidden fallbacks to slower libraries.
- **Flexible Distribution:** Prioritize a "batteries-included" experience with pre-built wheels for all major platforms (Windows, macOS, Linux) while maintaining a clean, well-documented source build process for developers and contributors.
