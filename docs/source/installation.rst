Installation
============

Quick Install
-------------

Install puhu using pip:

.. code-block:: bash

   pip install puhu

Platform Support
----------------

Puhu provides pre-built wheels for:

**Linux**

- x86_64 (Intel/AMD 64-bit)
- ARM64 (aarch64)

**macOS**

- Intel processors (x86_64)
- Apple Silicon (M1/M2/M3)

**Windows**

- x64 (64-bit Intel/AMD)

**Python Versions**

- Python 3.8+

If a wheel is not available for your platform, pip will attempt to build from source (requires Rust toolchain).

Building from Source
--------------------

Requirements
~~~~~~~~~~~~

To build puhu from source, you need:

- Python 3.8 or later
- Rust 1.70 or later
- Maturin

Install Rust
~~~~~~~~~~~~

If you don't have Rust installed:

.. code-block:: bash

   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

Or visit `rustup.rs <https://rustup.rs/>`_ for other installation methods.

Install Maturin
~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install maturin

Clone and Build
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/bgunebakan/puhu.git
   cd puhu

   # Install development dependencies
   pip install -r requirements.txt

   # Build and install in development mode
   maturin develop --release

   # Or build a wheel
   maturin build --release

Running Tests
~~~~~~~~~~~~~

After building from source, run the test suite:

.. code-block:: bash

   pytest python/puhu/tests/

Verifying Installation
----------------------

To verify that puhu is installed correctly:

.. code-block:: python

   import puhu
   print(puhu.__version__)

   # Create a test image
   img = puhu.new("RGB", (100, 100), "red")
   print(f"Created image: {img.size}, {img.mode}")

Troubleshooting
---------------

Installation Fails
~~~~~~~~~~~~~~~~~~

If installation fails, ensure you have:

1. Updated pip: ``pip install --upgrade pip``
2. Rust installed (for source builds): ``rustc --version``
3. Maturin installed: ``pip install maturin``

Import Errors
~~~~~~~~~~~~~

If you get import errors after installation:

1. Verify installation: ``pip show puhu``
2. Check Python version compatibility (3.8+)
3. Try reinstalling: ``pip install --force-reinstall puhu``

Platform-Specific Issues
~~~~~~~~~~~~~~~~~~~~~~~~

**macOS**: If you encounter code signing issues, you may need to allow the library in System Preferences > Security & Privacy.

**Linux**: Ensure you have the required system libraries (usually pre-installed on most distributions).

Getting Help
------------

If you encounter issues:

- Check `GitHub Issues <https://github.com/bgunebakan/puhu/issues>`_
- Open a new issue with details about your platform and error messages
- Include Python version (``python --version``) and Rust version (``rustc --version``) if building from source
