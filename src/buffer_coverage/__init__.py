"""
buffer_coverage - a library for analyzing the coverage of a territory by buffers.
"""

from .exceptions import (
    BufferCoverageError,
    CRSMismatchError,
    EmptyDataError,
    InvalidCRSError,
)
from .services.analysis import coverage_area, coverage_ratio, uncovered_areas

__all__ = [
    "coverage_area",
    "coverage_ratio",
    "uncovered_areas",
    "BufferCoverageError",
    "EmptyDataError",
    "CRSMismatchError",
    "InvalidCRSError",
]