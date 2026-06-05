class Lab6AppError(Exception):
    """Base exception for lab6_app."""


class TerritoryNotFoundError(Lab6AppError):
    """Raised when territory is not found."""


class MetricNotFoundError(Lab6AppError):
    """Raised when metric is not found."""


class MetricAlreadyExistsError(Lab6AppError):
    """Raised when metric for territory and year already exists."""
