"""
Simple validation test to verify the Arigold setup.

This test verifies that the basic structure is correct without requiring
Google API credentials.
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from arigold import __version__
        print(f"  ✓ arigold package version: {__version__}")
        
        from arigold import config
        print(f"  ✓ config module imported")
        print(f"    - Agent: {config.config.agent_name}")
        print(f"    - Model: {config.config.model_name}")
        
        # Note: agent module requires google-genai which may not be installed
        # This is expected for local validation
        print("  ℹ agent module requires google-genai (not tested here)")
        print("  ℹ main module requires functions-framework (not tested here)")
        
        assert True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        assert False


def test_config():
    """Test configuration system."""
    print("\nTesting configuration...")
    
    try:
        from arigold import config
        
        # Test default values
        config_instance = config.AgentConfig(api_key="test-key")
        assert config_instance.agent_name == "Ari Gold Super Agent"
        assert config_instance.model_name == "gemini-2.0-flash-exp"
        assert config_instance.temperature == 0.7
        assert config_instance.max_tokens == 512
        assert config_instance.location == "us-central1"
        assert config_instance.log_level == "INFO"
        
        print("  ✓ Default configuration values correct")
        
        # Test custom values
        custom_config = config.AgentConfig(
            agent_name="Test Agent",
            temperature=0.5
        )
        assert custom_config.agent_name == "Test Agent"
        assert custom_config.temperature == 0.5
        
        print("  ✓ Custom configuration values work")
    except Exception as e:
        print(f"  ✗ Configuration test failed: {e}")
        assert False


def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    
    required_files = [
        "src/arigold/__init__.py",
        "src/arigold/config.py",
        "src/arigold/agent.py",
        "src/arigold/main.py",
        "pyproject.toml",
        "requirements.txt",
        "README.md",
        ".env.example",
        ".gcloudignore",
        "scripts/deploy.sh",
        "scripts/test_function.sh",
        "examples/basic_usage.py",
    ]
    
    base_path = Path(__file__).parent.parent
    all_exist = True
    
    for file in required_files:
        file_path = base_path / file
        if file_path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (missing)")
            all_exist = False
    
    assert all_exist


def test_entry_points():
    """Test that Cloud Functions entry points are defined."""
    print("\nTesting Cloud Functions entry points...")
    
    try:
        import ast
        base_path = Path(__file__).parent.parent
        
        with open(base_path / "src/arigold/main.py", "r") as f:
            tree = ast.parse(f.read())
            # Only get top-level functions
            functions = [node.name for node in tree.body 
                        if isinstance(node, ast.FunctionDef)]
        
        required = ["arigold_agent", "health_check", "get_orchestrator"]
        
        for func in required:
            if func in functions:
                print(f"  ✓ {func}")
            else:
                print(f"  ✗ {func} (missing)")
                assert False
        
        assert True
    except Exception as e:
        print(f"  ✗ Entry point test failed: {e}")
        assert False


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("Arigold Setup Validation")
    print("=" * 60)
    
    tests = [
        test_file_structure,
        test_imports,
        test_config,
        test_entry_points,
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ All validation tests passed!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up environment: cp .env.example .env")
        print("3. Configure your Google API key in .env")
        print("4. Test locally: python examples/basic_usage.py")
        print("5. Deploy: ./scripts/deploy.sh")
        assert 0
    else:
        print("✗ Some validation tests failed")
        print("=" * 60)
        assert 1


if __name__ == "__main__":
    sys.exit(main())
