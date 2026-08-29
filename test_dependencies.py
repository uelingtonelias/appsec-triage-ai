"""
Dependency Validation Script
AI Triage Project
"""

import importlib

DEPENDENCIES = {
    "requests": "requests",
    "pandas": "pandas",
    "gitpython": "git",
    "pyyaml": "yaml",
    "rich": "rich",
    "pydantic": "pydantic",
    "numpy": "numpy",
    "tree-sitter": "tree_sitter",
    "chromadb": "chromadb",
    "sentence-transformers": "sentence_transformers"
}


def test_dependency(name, module_name):
    try:
        importlib.import_module(module_name)
        print(f"[PASS] {name}")
        return True

    except Exception as e:
        print(f"[FAIL] {name}")
        print(f"       {e}")
        return False


def main():

    print("=" * 50)
    print("AI TRIAGE - DEPENDENCY CHECK")
    print("=" * 50)
    print()

    passed = 0
    failed = 0

    for name, module in DEPENDENCIES.items():

        if test_dependency(name, module):
            passed += 1
        else:
            failed += 1

    print()
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Passed : {passed}")
    print(f"Failed : {failed}")
    print("=" * 50)

    if failed == 0:
        print()
        print("Environment is ready.")
    else:
        print()
        print("Some dependencies are missing.")


if __name__ == "__main__":
    main()