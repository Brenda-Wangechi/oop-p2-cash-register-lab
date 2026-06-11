#!/usr/bin/env python3
"""Simple test runner to execute test methods in the project's test file
without requiring pytest. It imports the test module, instantiates the
`TestCashRegister` class, and runs any method whose name starts with
`test_`. Failures raise AssertionError and return a non-zero exit code.
"""
import importlib.util
import sys
from pathlib import Path


def load_module_from_path(path, name="test_module"):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    repo_root = Path(__file__).parent
    test_path = repo_root / "lib" / "testing" / "cash_register_test.py"
    if not test_path.exists():
        print(f"Test file not found: {test_path}")
        sys.exit(2)

    mod = load_module_from_path(str(test_path), "cash_register_test")

    if not hasattr(mod, "TestCashRegister"):
        print("No TestCashRegister class found in test module.")
        sys.exit(2)

    TestClass = getattr(mod, "TestCashRegister")

    # Instantiate the test class (it contains setup-level attributes)
    tests = TestClass()

    failures = 0
    total = 0

    # Iterate test methods in the order they were defined in the class
    for name in TestClass.__dict__:
        if name.startswith("test_") and callable(getattr(tests, name)):
            total += 1
            try:
                getattr(tests, name)()
            except AssertionError as e:
                failures += 1
                print(f"FAIL: {name} -> {e}")
            except Exception as e:
                failures += 1
                print(f"ERROR: {name} -> {type(e).__name__}: {e}")
            else:
                print(f"PASS: {name}")

    print(f"\nRan {total} tests: {total - failures} passed, {failures} failed.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
