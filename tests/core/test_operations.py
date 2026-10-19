import numpy as np
import pytest

from app.core.operations import Operation, apply_operation, to_grayscale


def test_grayscale_of_color_image_has_one_channel() -> None:
    image = np.zeros((4, 4, 3), dtype=np.uint8)

    assert to_grayscale(image).shape == (4, 4)


def test_grayscale_uses_luminance_weights() -> None:
    # Pure green is perceived brighter than pure blue (weights 0.587 vs 0.114).
    image = np.zeros((1, 2, 3), dtype=np.uint8)
    image[0, 0] = (0, 255, 0)  # green (BGR)
    image[0, 1] = (255, 0, 0)  # blue (BGR)

    gray = to_grayscale(image)

    assert gray[0, 0] == 150  # round(0.587 * 255)
    assert gray[0, 1] == 29  # round(0.114 * 255)


def test_grayscale_of_image_with_alpha_has_one_channel() -> None:
    image = np.zeros((4, 4, 4), dtype=np.uint8)

    assert to_grayscale(image).shape == (4, 4)


def test_grayscale_of_grayscale_image_is_unchanged_copy() -> None:
    image = np.full((3, 3), 7, dtype=np.uint8)

    result = to_grayscale(image)

    np.testing.assert_array_equal(result, image)
    assert result is not image


@pytest.mark.parametrize("operation", list(Operation))
def test_apply_operation_does_not_modify_input(operation: Operation) -> None:
    image = np.full((3, 3, 3), 50, dtype=np.uint8)
    before = image.copy()

    apply_operation(image, operation)

    np.testing.assert_array_equal(image, before)


def test_none_operation_returns_copy_of_input() -> None:
    image = np.full((3, 3, 3), 50, dtype=np.uint8)

    np.testing.assert_array_equal(apply_operation(image, Operation.NONE), image)
