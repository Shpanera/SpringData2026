class BufferCoverageError(Exception):
    """Base exception of library"""

    pass


class EmptyDataError(BufferCoverageError):
    """Empty GeoDataFrame error"""

    pass


class CRSMismatchError(BufferCoverageError):
    """CRS not matches error"""

    pass


class InvalidCRSError(BufferCoverageError):
    """CRS is None or invalid error"""

    pass
