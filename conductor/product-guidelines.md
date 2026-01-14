# Product Guidelines: Puhu

## Prose Style & Tone
- **Professional & Precision-Driven:** Our communication should reflect the high-performance nature of the library. Use technical language accurately, provide detailed benchmarks where relevant, and ensure API documentation is exhaustive and precise.
- **Educational Bridge:** While maintaining a professional tone, we must also be approachable for users migrating from Pillow. Include clear "migration tips" or side-by-side examples to demonstrate how Puhu's API maps to familiar Pillow patterns.

## Error Handling & Messaging
- **Actionable Feedback:** Error messages must never be vague. Every exception should clearly identify the invalid input or state and, whenever possible, suggest the correct usage or a link to relevant documentation.
- **Pythonic Standards:** Use standard Python exception types (e.g., `ValueError`, `TypeError`, `RuntimeError`) so that Puhu fits naturally into existing Python error-handling logic, but enhance them with specific, Puhu-contextual messages.

## Visual Identity & Branding
- **The "Puhu" Owl:** The brand should be represented by a minimalist, modern owl icon (Puhu means "owl" in some contexts), symbolizing wisdom (safety) and night-vision (precision).
- **Aesthetic:** Use a professional palette of deep blues, charcoal grays, and a sharp accent color (like a bright cyan) to denote speed and modern engineering. Documentation and the GitHub repository should maintain a clean, high-contrast, and well-organized layout.
