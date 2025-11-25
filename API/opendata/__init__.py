"""
OpenData Package

A Python library for traversing folder structures with meta.yml files
and understanding graph entities for database integration.
"""

from .entity_parser import EntityParser, EntityType, DataFormat
from .traverser import DataTraverser
from .api_utils import APIUtils, APIConfig
from .main import OpenDataProcessor

__version__ = "1.0.0"
__all__ = ["EntityParser", "DataTraverser", "APIUtils", "APIConfig", "OpenDataProcessor", "EntityType", "DataFormat"]
