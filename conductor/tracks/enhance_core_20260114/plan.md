# Track Plan: Enhance Core Operations

This plan outlines the steps to implement and optimize core image operations in Puhu.

## Phase 1: Robust Paste Implementation
Implement a fully Pillow-compatible `paste` method in Rust with support for masking and blending.

- [ ] Task: Write Tests - Verify current `paste` implementation against Pillow edge cases (e.g., negative coordinates, mismatched modes).
- [ ] Task: Implement Feature - Refine Rust `paste` implementation to handle clipping, signed coordinates, and optimized alpha blending.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Robust Paste Implementation' (Protocol in workflow.md)

## Phase 2: Point Transformations
Implement the `point` method for efficient pixel-wise lookups and transformations.

- [ ] Task: Write Tests - Define test cases for `point` with single-channel and multi-channel lookup tables.
- [ ] Task: Implement Feature - Implement the `point` logic in Rust and expose it via Python bindings.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Point Transformations' (Protocol in workflow.md)

## Phase 3: Basic Image Filters
Add high-performance implementations for common blurs and sharpening filters.

- [ ] Task: Write Tests - Create benchmarks and correctness tests for Gaussian Blur and Unsharp Mask.
- [ ] Task: Implement Feature - Implement filters in Rust and expose them to Python.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Basic Image Filters' (Protocol in workflow.md)
