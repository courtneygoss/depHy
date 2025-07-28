#!/usr/bin/env python3
"""
Test script to verify Python 3.10 compatibility
"""

def test_imports():
    """Test that all required packages can be imported"""
    try:
        print("Testing imports with Python 3.10 compatible versions...")
        
        # Test Flask
        from flask import Flask
        print("✓ Flask imported successfully")
        
        # Test Flask-CORS
        from flask_cors import CORS
        print("✓ Flask-CORS imported successfully")
        
        # Test numpy
        import numpy as np
        print(f"✓ NumPy {np.__version__} imported successfully")
        
        # Test scikit-learn
        import sklearn
        print(f"✓ Scikit-learn {sklearn.__version__} imported successfully")
        
        # Test requests
        import requests
        print(f"✓ Requests {requests.__version__} imported successfully")
        
        print("\n🎉 All imports successful with Python 3.10 compatible versions!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_app():
    """Test that the Flask app can be created"""
    try:
        from app import app
        print("✓ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating Flask app: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Python 3.10 Compatibility")
    print("=" * 50)
    
    imports_ok = test_imports()
    app_ok = test_app()
    
    if imports_ok and app_ok:
        print("\n✅ All tests passed! Ready for deployment.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.") 