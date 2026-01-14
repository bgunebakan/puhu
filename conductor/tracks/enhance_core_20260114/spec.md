# Track Spec: Enhance Core Operations

## Overview
This track focuses on expanding Puhu's core image processing capabilities to bridge the gap with common Pillow operations. The goal is to provide high-performance Rust implementations for critical methods like `paste`, `point`, and basic filters, ensuring full Pillow compatibility where implemented.

## Objectives
- Complete the implementation of the `paste` method, including masking and alpha blending.
- Implement the `point` method for point transformations using lookup tables.
- Add support for basic image filters (e.g., Gaussian Blur, Unsharp Mask).
- Ensure all operations maintain >80% test coverage and match Pillow's behavior.

## Scope
- **Implementation:** Rust core enhancements and Python API bindings.
- **Compatibility:** Strictly follow Pillow's method signatures and behavior.
- **Performance:** Benchmark against Pillow to ensure 2x-10x performance gains.

## Technical Details
- **Paste:** Support 2-tuple (position) and 4-tuple (region) boxes, along with optional mask images.
- **Point:** Implement efficient pixel-wise transformations in Rust using parallel iterators.
- **Filters:** Leverage the `image` crate's filtering capabilities or implement custom high-performance kernels.
