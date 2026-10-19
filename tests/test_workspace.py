import numpy as np
import pytest

from app.core.operations import Operation
from app.workspace import Workspace


def test_new_workspace_has_no_input() -> None:
    assert Workspace().input is None


def test_set_input_stores_a_copy() -> None:
    workspace = Workspace()
    image = np.zeros((2, 2, 3), dtype=np.uint8)

    workspace.set_input(image)
    image[0, 0] = 255  # changing the caller's array must not change the workspace

    assert workspace.input is not None
    assert workspace.input[0, 0, 0] == 0


def test_require_input_without_image_raises() -> None:
    with pytest.raises(LookupError):
        Workspace().require_input()


def make_color_image() -> np.ndarray:
    return np.full((4, 4, 3), 100, dtype=np.uint8)


def test_set_input_makes_result_equal_to_input() -> None:
    workspace = Workspace()

    workspace.set_input(make_color_image())

    np.testing.assert_array_equal(workspace.require_result(), make_color_image())


def test_apply_grayscale_changes_result_but_not_input() -> None:
    workspace = Workspace()
    workspace.set_input(make_color_image())

    workspace.apply(Operation.GRAYSCALE)

    assert workspace.require_result().ndim == 2
    assert workspace.require_input().ndim == 3


def test_reset_restores_result_to_input() -> None:
    workspace = Workspace()
    workspace.set_input(make_color_image())
    workspace.apply(Operation.GRAYSCALE)

    workspace.reset()

    np.testing.assert_array_equal(workspace.require_result(), make_color_image())


def test_apply_without_input_raises() -> None:
    with pytest.raises(LookupError):
        Workspace().apply(Operation.GRAYSCALE)
