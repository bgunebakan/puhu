Contributing to Puhu
====================

Thank you for your interest in contributing to Puhu! This guide will help you get started.

Areas Where Help is Needed
---------------------------

1. **High Priority Features**

   - ``paste()`` - Paste images onto other images
   - ``fromarray()`` - NumPy array integration
   - ``split()`` - Split image into color bands

2. **Performance Optimization**

   - Further speed improvements
   - Memory usage optimization
   - Parallel processing for batch operations

3. **Format Support**

   - Additional image formats
   - Better format-specific optimization
   - Metadata handling (EXIF, etc.)

4. **Documentation**

   - Examples and tutorials
   - Use case documentation
   - API documentation improvements

5. **Testing**

   - Edge case testing
   - Compatibility tests
   - Performance benchmarks

Development Setup
-----------------

Prerequisites
~~~~~~~~~~~~~

- Python 3.8 or later
- Rust 1.70 or later
- Git

Clone the Repository
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/bgunebakan/puhu.git
   cd puhu

Install Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Install Python dependencies
   pip install -r requirements.txt

   # Install pre-commit hooks (optional but recommended)
   pip install pre-commit
   pre-commit install

Build the Project
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Build in development mode (faster iteration)
   maturin develop

   # Build in release mode (optimized)
   maturin develop --release

Run Tests
~~~~~~~~~

.. code-block:: bash

   # Run all tests
   pytest python/puhu/tests/

   # Run specific test file
   pytest python/puhu/tests/test_image.py

   # Run with verbose output
   pytest -v python/puhu/tests/

Project Structure
-----------------

.. code-block:: text

   puhu/
   ├── src/                    # Rust source code
   │   ├── lib.rs             # Main library entry
   │   ├── image.rs           # Image class implementation
   │   ├── conversions.rs     # Type conversions
   │   └── errors.rs          # Error handling
   ├── python/
   │   └── puhu/              # Python package
   │       ├── __init__.py    # Python API
   │       ├── enums.py       # Enums and constants
   │       └── tests/         # Test suite
   ├── docs/                  # Documentation
   ├── Cargo.toml            # Rust dependencies
   └── pyproject.toml        # Python package config

Contribution Workflow
---------------------

1. Fork and Clone
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Fork the repository on GitHub, then:
   git clone https://github.com/YOUR_USERNAME/puhu.git
   cd puhu
   git remote add upstream https://github.com/bgunebakan/puhu.git

2. Create a Branch
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix

3. Make Changes
~~~~~~~~~~~~~~~

- Write code following the project style
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass

4. Commit Changes
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git add .
   git commit -m "Add feature: description of your change"

Write clear commit messages:

- Use present tense ("Add feature" not "Added feature")
- Keep first line under 72 characters
- Add detailed description if needed

5. Push and Create PR
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git push origin feature/your-feature-name

Then create a Pull Request on GitHub with:

- Clear description of changes
- Reference to related issues
- Screenshots for UI changes (if applicable)

Coding Guidelines
-----------------

Python Code
~~~~~~~~~~~

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for public functions
- Keep functions focused and small

.. code-block:: python

   def resize_image(img: Image, size: tuple[int, int]) -> Image:
       """
       Resize an image to the specified dimensions.

       Args:
           img: The image to resize
           size: Target size as (width, height)

       Returns:
           Resized image
       """
       return img.resize(size)

Rust Code
~~~~~~~~~

- Follow Rust conventions (rustfmt)
- Use descriptive variable names
- Add comments for complex logic
- Handle errors explicitly

.. code-block:: rust

   /// Resize the image to the specified dimensions
   pub fn resize(&self, width: u32, height: u32) -> PyResult<Self> {
       let resized_buffer = self.ensure_loaded()?
           .resize_exact(width, height, FilterType::Triangle);

       Ok(LazyImage::Buffer(resized_buffer))
   }

Documentation
~~~~~~~~~~~~~

- Update relevant documentation files
- Add examples for new features
- Include docstrings in code
- Update API reference if needed

Testing Guidelines
------------------

Writing Tests
~~~~~~~~~~~~~

Add tests for all new features and bug fixes:

.. code-block:: python

   # python/puhu/tests/test_new_feature.py
   import puhu
   import pytest

   def test_new_feature():
       """Test description"""
       img = puhu.new("RGB", (100, 100), "red")
       result = img.new_feature()

       assert result.size == (100, 100)
       assert result.mode == "RGB"

   def test_new_feature_error_handling():
       """Test error cases"""
       img = puhu.new("RGB", (100, 100))

       with pytest.raises(ValueError):
           img.new_feature(invalid_param)

Running Tests
~~~~~~~~~~~~~

.. code-block:: bash

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=puhu

   # Run specific test
   pytest python/puhu/tests/test_image.py::test_resize

Benchmarking
~~~~~~~~~~~~

If your change affects performance, run benchmarks:

.. code-block:: bash

   python benchmark.py

Pull Request Guidelines
-----------------------

Before Submitting
~~~~~~~~~~~~~~~~~

Checklist:

- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Code follows project style
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

PR Description
~~~~~~~~~~~~~~

Include in your PR description:

1. **What**: Brief description of changes
2. **Why**: Reason for the changes
3. **How**: Implementation approach
4. **Testing**: How you tested the changes

Example:

.. code-block:: markdown

   ## What
   Add `paste()` method to Image class

   ## Why
   Frequently requested feature for image composition

   ## How
   - Implemented paste logic in Rust
   - Added Python bindings
   - Handles RGB and RGBA modes

   ## Testing
   - Added unit tests for basic pasting
   - Added tests for edge cases (out of bounds, mode mismatch)
   - Verified performance with benchmarks

Review Process
~~~~~~~~~~~~~~

1. Automated tests will run on your PR
2. Maintainers will review your code
3. Address any feedback
4. Once approved, your PR will be merged

Getting Help
------------

If you need help:

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Security**: Email maintainers directly

Code of Conduct
---------------

Be respectful and inclusive:

- Welcome newcomers
- Be patient with questions
- Provide constructive feedback
- Respect different perspectives

Recognition
-----------

All contributors are recognized:

- Listed in GitHub contributors
- Mentioned in release notes
- Featured in documentation

Thank you for contributing to Puhu! 🦉
