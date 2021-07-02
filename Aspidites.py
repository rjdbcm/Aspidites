import sys
import pytest_cov
import pytest_mypy
import pytest_sugar

if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
    import pytest

    sys.exit(pytest.main(sys.argv[2:], plugins=[pytest_cov, pytest_mypy, pytest_sugar]))
else:
    ...
