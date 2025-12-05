"""Test ID: 1.4-UNIT-002

Test that ValidationError exception imports correctly and inherits from DataError.

Ref: docs/qa/assessments/1.4-test-design-20251205.md#14-unit-002-validationerror-exception-imports-and-inherits

Steps:
1. Import ValidationError from momo.utils.exceptions
2. Import DataError from momo.utils.exceptions
3. Verify ValidationError is a subclass of DataError
4. Verify raising ValidationError can be caught as DataError

Expected: ValidationError is properly defined and inherits from DataError
"""

from __future__ import annotations

import pytest

from momo.utils.exceptions import DataError, ValidationError


@pytest.mark.p0
@pytest.mark.unit
def test_validation_error_imports_and_inherits() -> None:
    """Test ID: 1.4-UNIT-002

    Verify ValidationError imports correctly and inherits from DataError.
    """
    # Step 3: Verify ValidationError is a subclass of DataError
    assert issubclass(ValidationError, DataError), "ValidationError must be a subclass of DataError"

    # Step 4: Verify raising ValidationError can be caught as DataError
    try:
        raise ValidationError("Test validation failure")
    except DataError:
        pass  # Should successfully catch as DataError parent
    else:
        pytest.fail("ValidationError should be catchable as DataError")
