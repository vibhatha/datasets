"""
Data Traverser Module

Traverses folder structures and builds entity graphs with context.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass

from .entity_parser import EntityParser, EntityMetadata, EntityType, DataFormat


@dataclass
class TraversalContext:
    """Context information during traversal."""
    current_path: Path
    depth: int
    parent_entity: Optional[EntityMetadata] = None
    year: Optional[str] = None
    country: Optional[str] = None
    government: Optional[str] = None
    president: Optional[str] = None
    minister: Optional[str] = None
    department: Optional[str] = None


class DataTraverser:
    """Traverses folder structures and builds entity graphs."""
    
    def __init__(self, root_path: str):
        """
        Initialize the data traverser.
        
        Args:
            root_path: Root directory to traverse
        """
        self.root_path = Path(root_path)
        self.parser = EntityParser()
        self.context_stack: List[TraversalContext] = []
        self.traversal_callbacks: List[Callable[[TraversalContext, EntityMetadata], None]] = []
    
    def add_traversal_callback(self, callback: Callable[[TraversalContext, EntityMetadata], None]):
        """
        Add a callback function to be called during traversal.
        
        Args:
            callback: Function that takes (context, entity) parameters
        """
        self.traversal_callbacks.append(callback)
    
    def traverse(self) -> List[EntityMetadata]:
        """
        Traverse the folder structure and parse all meta.yml files.
        
        Returns:
            List of all parsed entities
        """
        self.parser.entities.clear()
        self.parser.entity_map.clear()
        
        # Start traversal from root
        self._traverse_directory(self.root_path, 0)
        
        return self.parser.entities
    
    def _traverse_directory(self, directory: Path, depth: int):
        """
        Recursively traverse a directory.
        
        Args:
            directory: Directory to traverse
            depth: Current depth level
        """
        # Check if this directory has a meta.yml file
        meta_file = directory / 'meta.yml'
        
        if meta_file.exists():
            # Parse the meta.yml file
            entity = self.parser.parse_meta_file(meta_file)
            if entity:
                self.parser.entities.append(entity)
                self.parser.entity_map[directory] = entity
                
                # Create traversal context
                context = self._create_context(directory, depth, entity)
                self.context_stack.append(context)
                
                # Call traversal callbacks
                for callback in self.traversal_callbacks:
                    callback(context, entity)
        
        # Continue traversing subdirectories
        try:
            for item in directory.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    self._traverse_directory(item, depth + 1)
        except PermissionError:
            print(f"Permission denied: {directory}")
    
    def _create_context(self, path: Path, depth: int, entity: EntityMetadata) -> TraversalContext:
        """Create traversal context from current state."""
        context = TraversalContext(
            current_path=path,
            depth=depth,
            parent_entity=self._get_parent_entity(path)
        )
        
        # Extract context information from path
        path_parts = path.parts
        
        # Extract year from path
        for part in path_parts:
            if part.isdigit() and len(part) == 4:
                context.year = part
                break
        
        # Extract country, government, president, minister, department
        if 'Sri Lanka' in path_parts:
            context.country = 'Sri Lanka'
        
        if 'Government' in path_parts:
            context.government = 'Government'
        
        # Extract president
        for part in path_parts:
            if part in ['Gotabaya Rajapaksa', 'Ranil Wickremesinghe']:
                context.president = part
                break
        
        # Extract minister and department from entity
        if entity.major_kind == EntityType.ORGANISATION:
            if entity.minor_kind == DataFormat.MINISTER:
                context.minister = entity.name
            elif entity.minor_kind == DataFormat.DEPARTMENT:
                context.department = entity.name
        
        return context
    
    def _get_parent_entity(self, path: Path) -> Optional[EntityMetadata]:
        """Get parent entity from the context stack."""
        if self.context_stack:
            return self.context_stack[-1].parent_entity
        return None
    
    def get_entities_by_year(self, year: str) -> List[EntityMetadata]:
        """Get all entities for a specific year."""
        return [
            entity for entity in self.parser.entities
            if entity.start_date.startswith(year) or entity.end_date.startswith(year)
        ]
    
    def get_entities_by_president(self, president: str) -> List[EntityMetadata]:
        """Get all entities for a specific president."""
        # This would need to be implemented based on the actual data structure
        # For now, return all entities
        return self.parser.entities
    
    def get_data_flow(self) -> Dict[str, List[EntityMetadata]]:
        """
        Get data flow from organisations to datasets.
        
        Returns:
            Dictionary mapping organisation names to their data entities
        """
        data_flow = {}
        
        for entity in self.parser.entities:
            if entity.major_kind == EntityType.ORGANISATION:
                # Find related data entities
                related_data = []
                for data_entity in self.parser.get_data_entities():
                    if self._is_related(entity, data_entity):
                        related_data.append(data_entity)
                
                if related_data:
                    data_flow[entity.name] = related_data
        
        return data_flow
    
    def _is_related(self, org_entity: EntityMetadata, data_entity: EntityMetadata) -> bool:
        """Check if an organisation entity is related to a data entity."""
        # Simple path-based relationship check
        try:
            data_entity.path.relative_to(org_entity.path)
            return True
        except ValueError:
            return False
    
    def get_entity_summary(self) -> Dict[str, Any]:
        """Get summary statistics of the entity graph."""
        summary = {
            'total_entities': len(self.parser.entities),
            'by_type': {},
            'by_format': {},
            'by_year': {},
            'data_entities': len(self.parser.get_data_entities()),
            'organisation_entities': len(self.parser.get_organisation_entities()),
            'category_entities': len(self.parser.get_category_entities()),
            'tabular_datasets': len(self.parser.get_tabular_datasets())
        }
        
        # Count by entity type
        for entity in self.parser.entities:
            entity_type = entity.major_kind.value
            summary['by_type'][entity_type] = summary['by_type'].get(entity_type, 0) + 1
            
            # Count by format
            format_type = entity.minor_kind.value
            summary['by_format'][format_type] = summary['by_format'].get(format_type, 0) + 1
            
            # Count by year
            year = entity.start_date[:4] if entity.start_date else 'unknown'
            summary['by_year'][year] = summary['by_year'].get(year, 0) + 1
        
        return summary
    
    def find_entities_by_name(self, name: str) -> List[EntityMetadata]:
        """Find entities by name (case-insensitive)."""
        return [
            entity for entity in self.parser.entities
            if name.lower() in entity.name.lower()
        ]
    
    def get_entity_hierarchy(self) -> Dict[str, List[str]]:
        """Get entity hierarchy as a dictionary."""
        hierarchy = {}
        
        for entity in self.parser.entities:
            if entity.parent_path:
                parent_name = entity.parent_path.name
                if parent_name not in hierarchy:
                    hierarchy[parent_name] = []
                hierarchy[parent_name].append(entity.name)
        
        return hierarchy
