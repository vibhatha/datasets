"""
Entity Parser Module

Parses meta.yml files and identifies graph entity types and relationships.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class EntityType(Enum):
    """Enumeration of entity types based on major kind."""
    ORGANISATION = "Organisation"
    CATEGORY = "Category"
    DATASET = "Dataset"
    PERSON = "Person"
    LAND_PARCEL = "Land Parcel"


class DataFormat(Enum):
    """Enumeration of data formats based on minor kind."""
    TABULAR = "Tabular"
    MINISTER = "Minister"
    DEPARTMENT = "Department"
    GOVERNMENT = "Government"
    CITIZEN = "Citizen"
    COUNTRY = "Country"
    DATA = "Data"


@dataclass
class EntityMetadata:
    """Represents metadata for a graph entity."""
    name: str
    path: Path
    major_kind: EntityType
    minor_kind: DataFormat
    start_date: str
    end_date: str
    parent_path: Optional[Path] = None
    children: List['EntityMetadata'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class EntityParser:
    """Parses meta.yml files and creates entity metadata."""
    
    def __init__(self):
        """Initialize the entity parser."""
        self.entities: List[EntityMetadata] = []
        self.entity_map: Dict[Path, EntityMetadata] = {}
    
    def parse_meta_file(self, meta_file_path: Path) -> Optional[EntityMetadata]:
        """
        Parse a single meta.yml file and return entity metadata.
        
        Args:
            meta_file_path: Path to the meta.yml file
            
        Returns:
            EntityMetadata object or None if parsing fails
        """
        try:
            with open(meta_file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not data:
                return None
            
            # Extract entity information
            name = data.get('name', '')
            kind = data.get('kind', {})
            major_kind_str = kind.get('major', '')
            minor_kind_str = kind.get('minor', '')
            start_date = data.get('start_date', '')
            end_date = data.get('end_date', '')
            
            # Convert to enums
            major_kind = self._parse_major_kind(major_kind_str)
            minor_kind = self._parse_minor_kind(minor_kind_str)
            
            # Determine parent path
            parent_path = meta_file_path.parent.parent if meta_file_path.parent.name != 'data' else None
            
            entity = EntityMetadata(
                name=name,
                path=meta_file_path.parent,
                major_kind=major_kind,
                minor_kind=minor_kind,
                start_date=start_date,
                end_date=end_date,
                parent_path=parent_path
            )
            
            return entity
            
        except Exception as e:
            print(f"Error parsing {meta_file_path}: {e}")
            return None
    
    def _parse_major_kind(self, major_kind_str: str) -> EntityType:
        """Parse major kind string to EntityType enum."""
        kind_mapping = {
            'Organisation': EntityType.ORGANISATION,
            'Category': EntityType.CATEGORY,
            'Dataset': EntityType.DATASET,
            'Person': EntityType.PERSON,
            'Land Parcel': EntityType.LAND_PARCEL
        }
        return kind_mapping.get(major_kind_str, EntityType.ORGANISATION)
    
    def _parse_minor_kind(self, minor_kind_str: str) -> DataFormat:
        """Parse minor kind string to DataFormat enum."""
        format_mapping = {
            'Tabular': DataFormat.TABULAR,
            'Minister': DataFormat.MINISTER,
            'Department': DataFormat.DEPARTMENT,
            'Government': DataFormat.GOVERNMENT,
            'Citizen': DataFormat.CITIZEN,
            'Country': DataFormat.COUNTRY,
            'Data': DataFormat.DATA
        }
        return format_mapping.get(minor_kind_str, DataFormat.DATA)
    
    def get_entity_by_path(self, path: Path) -> Optional[EntityMetadata]:
        """Get entity metadata by path."""
        return self.entity_map.get(path)
    
    def get_entities_by_type(self, entity_type: EntityType) -> List[EntityMetadata]:
        """Get all entities of a specific type."""
        return [entity for entity in self.entities if entity.major_kind == entity_type]
    
    def get_data_entities(self) -> List[EntityMetadata]:
        """Get all entities that contain actual data (Dataset type)."""
        return self.get_entities_by_type(EntityType.DATASET)
    
    def get_organisation_entities(self) -> List[EntityMetadata]:
        """Get all organisation entities."""
        return self.get_entities_by_type(EntityType.ORGANISATION)
    
    def get_category_entities(self) -> List[EntityMetadata]:
        """Get all category entities."""
        return self.get_entities_by_type(EntityType.CATEGORY)
    
    def build_entity_hierarchy(self) -> Dict[Path, List[EntityMetadata]]:
        """
        Build entity hierarchy based on parent-child relationships.
        
        Returns:
            Dictionary mapping parent paths to their children
        """
        hierarchy = {}
        
        for entity in self.entities:
            if entity.parent_path:
                if entity.parent_path not in hierarchy:
                    hierarchy[entity.parent_path] = []
                hierarchy[entity.parent_path].append(entity)
        
        return hierarchy
    
    def get_entity_relationships(self) -> List[Tuple[EntityMetadata, EntityMetadata]]:
        """
        Get parent-child relationships between entities.
        
        Returns:
            List of (parent, child) tuples
        """
        relationships = []
        
        for entity in self.entities:
            if entity.parent_path:
                parent = self.get_entity_by_path(entity.parent_path)
                if parent:
                    relationships.append((parent, entity))
        
        return relationships
    
    def get_tabular_datasets(self) -> List[EntityMetadata]:
        """Get all entities that are tabular datasets."""
        return [
            entity for entity in self.entities 
            if entity.major_kind == EntityType.DATASET and entity.minor_kind == DataFormat.TABULAR
        ]
    
    def get_entities_in_date_range(self, start_date: str, end_date: str) -> List[EntityMetadata]:
        """
        Get entities that are active within a date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of entities active in the date range
        """
        active_entities = []
        
        for entity in self.entities:
            if (entity.start_date <= end_date and entity.end_date >= start_date):
                active_entities.append(entity)
        
        return active_entities
