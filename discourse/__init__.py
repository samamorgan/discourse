import pkg_resources

from .session import Session

__version__ = pkg_resources.require("discourse")[0].version

__all__ = ("Session",)
