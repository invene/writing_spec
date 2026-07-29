#!/usr/bin/env python3
# Copyright 2026 Invene. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""A module whose non-governed comments the adapter must exclude."""

import time  # noqa: F401
from typing import Any


def guarded(value: Any) -> Any:
    """Return the value unchanged."""
    # type: ignore comments and directives stay outside the governed set.
    result = value  # pylint: disable=unused-variable
    return result
