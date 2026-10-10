import numpy as np
import pytest

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
