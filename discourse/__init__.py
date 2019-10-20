import pkg_resources

from .client import Client

__version__ = pkg_resources.require("discourse")[0].version

__all__ = ("Client",)
