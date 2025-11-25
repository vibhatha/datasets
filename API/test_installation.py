#!/usr/bin/env python3
"""
Test script to verify opendata package installation.
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported."""
    try:
        import opendata
        print(f"✓ opendata package imported successfully (version: {opendata.__version__})")
        
        from opendata import EntityParser, DataTraverser, APIUtils
        print("✓ Core modules imported successfully")
        
        from opendata.entity_parser import EntityType, DataFormat
        print("✓ Enums imported successfully")
        
        from opendata.traverser import TraversalContext
        print("✓ Context classes imported successfully")
        
        from opendata.api_utils import APIConfig
        print("✓ API configuration imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality."""
    try:
        from opendata import EntityParser, DataTraverser, APIUtils, APIConfig
        
        # Test entity parser
        parser = EntityParser()
        print("✓ EntityParser created successfully")
        
        # Test traverser
        traverser = DataTraverser("/tmp")
        print("✓ DataTraverser created successfully")
        
        # Test API utils
        config = APIConfig("https://api.example.com", "test-key")
        api_utils = APIUtils(config)
        print("✓ APIUtils created successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

def main():
    """Main test function."""
    print("Testing opendata package installation...")
    print("=" * 50)
    
    # Test imports
    print("\n1. Testing imports...")
    import_success = test_imports()
    
    # Test basic functionality
    print("\n2. Testing basic functionality...")
    functionality_success = test_basic_functionality()
    
    # Summary
    print("\n" + "=" * 50)
    if import_success and functionality_success:
        print("✓ All tests passed! opendata package is working correctly.")
        return 0
    else:
        print("✗ Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
