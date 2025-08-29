from __future__ import annotations

"""Minimal unit conversion utilities."""

from typing import Dict

import math


_LENGTH_TO_M = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}


def _angle_to_rad(unit: str) -> float:
    if unit == "rad":
        return 1.0
    if unit == "deg":
        return math.pi / 180.0
    raise ValueError(f"unknown angle unit: {unit}")


def convert(value: float, src: str, dst: str) -> Dict[str, object]:
    """
    Minimal unit map: m↔cm↔mm, km↔m, deg↔rad. Use a dict of factors (src->m etc.).
    Return: status, converted_value, factor; error on unknown units.
    """
    try:
        # Length units
        if src in _LENGTH_TO_M and dst in _LENGTH_TO_M:
            to_m = _LENGTH_TO_M[src]
            from_m = 1.0 / _LENGTH_TO_M[dst]
            factor = to_m * from_m
            return {"status": "ok", "converted_value": value * factor, "factor": factor}

        # Angle units
        if (src in {"deg", "rad"}) and (dst in {"deg", "rad"}):
            to_rad = _angle_to_rad(src)
            from_rad = 1.0 / _angle_to_rad(dst)
            factor = to_rad * from_rad
            return {"status": "ok", "converted_value": value * factor, "factor": factor}

        raise ValueError(f"unknown conversion: {src} -> {dst}")
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "message": str(exc)}


