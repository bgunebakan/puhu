#!/usr/bin/env python3
"""
Test script to verify the structure of our new features without requiring the Rust extension.
"""

import sys
import os

# Add the python directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python'))

def test_imports():
    """Test that all our new functions can be imported."""
    try:
        from puhu import convert, fromarray, split, paste
        print("✓ All new functions can be imported")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_image_class_methods():
    """Test that Image class has all the new methods."""
    try:
        from puhu.image import Image
        
        # Check if methods exist
        methods = ['convert', 'split', 'paste', 'fromarray']
        missing_methods = []
        
        for method in methods:
            if not hasattr(Image, method):
                missing_methods.append(method)
        
        if missing_methods:
            print(f"✗ Missing methods in Image class: {missing_methods}")
            return False
        else:
            print("✓ All new methods exist in Image class")
            return True
            
    except ImportError as e:
        print(f"✗ Could not import Image class: {e}")
        return False

def test_operations_module():
    """Test that operations module has all the new functions."""
    try:
        from puhu import operations
        
        # Check if functions exist
        functions = ['convert', 'fromarray', 'split', 'paste']
        missing_functions = []
        
        for func in functions:
            if not hasattr(operations, func):
                missing_functions.append(func)
        
        if missing_functions:
            print(f"✗ Missing functions in operations module: {missing_functions}")
            return False
        else:
            print("✓ All new functions exist in operations module")
            return True
            
    except ImportError as e:
        print(f"✗ Could not import operations module: {e}")
        return False

def test_numpy_handling():
    """Test numpy import handling."""
    try:
        from puhu.image import HAS_NUMPY
        print(f"✓ NumPy availability detected: {HAS_NUMPY}")
        return True
    except ImportError as e:
        print(f"✗ Could not check NumPy availability: {e}")
        return False

def main():
    """Run all structure tests."""
    print("Testing Puhu new features structure...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_image_class_methods,
        test_operations_module,
        test_numpy_handling,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All structure tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
