"""
API Utilities Module

Provides utility functions for third-party API calls to save data.
Focuses on Dataset entities and Category graph nodes.
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from pathlib import Path
import json

from .entity_parser import EntityMetadata, EntityType, DataFormat
from .traverser import TraversalContext


@dataclass
class APIConfig:
    """Configuration for API calls."""
    base_url: str
    api_key: str
    timeout: int = 30
    retry_attempts: int = 3
    batch_size: int = 100


class APIUtils:
    """Utility functions for third-party API calls."""
    
    def __init__(self, config: APIConfig):
        """
        Initialize API utilities.
        
        Args:
            config: API configuration
        """
        self.config = config
        self.api_callbacks: Dict[str, Callable] = {}
        self.batch_data: List[Dict] = []
    
    def register_api_callback(self, entity_type: str, callback: Callable):
        """
        Register a callback function for a specific entity type.
        
        Args:
            entity_type: Type of entity (e.g., 'Dataset', 'Category')
            callback: Function to call for this entity type
        """
        self.api_callbacks[entity_type] = callback
    
    def save_dataset_entity(self, entity: EntityMetadata, context: TraversalContext) -> bool:
        """
        Save dataset entity to database via API.
        This is the main function for saving actual data.
        
        Args:
            entity: Dataset entity metadata
            context: Traversal context
            
        Returns:
            True if successful, False otherwise
        """
        if entity.major_kind != EntityType.DATASET:
            return False
        
        # Read actual data from JSON files
        data_files = self._find_data_files(entity.path)
        data_content = []
        
        for data_file in data_files:
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    data_content.append({
                        'file_path': str(data_file),
                        'data': data
                    })
            except Exception as e:
                print(f"Error reading data file {data_file}: {e}")
                return False
        
        # Prepare data for API call
        api_data = {
            'name': entity.name,
            'type': 'dataset',
            'subtype': entity.minor_kind.value,
            'start_date': entity.start_date,
            'end_date': entity.end_date,
            'path': str(entity.path),
            'data_content': data_content,
            'context': {
                'year': context.year,
                'country': context.country,
                'government': context.government,
                'president': context.president,
                'minister': context.minister,
                'department': context.department
            }
        }
        
        # Call registered callback if available
        if 'Dataset' in self.api_callbacks:
            return self.api_callbacks['Dataset'](api_data)
        
        # Default implementation (TODO: implement actual API call)
        print(f"TODO: Save dataset entity: {entity.name} with {len(data_content)} data files")
        return True
    
    def create_category_node(self, entity: EntityMetadata, context: TraversalContext) -> bool:
        """
        Create a category node in the graph and establish relationships.
        This function creates graph nodes for Category entities and establishes
        relationships with parent entities based on folder structure.
        
        Args:
            entity: Category entity metadata
            context: Traversal context
            
        Returns:
            True if successful, False otherwise
        """
        if entity.major_kind != EntityType.CATEGORY:
            return False
        
        # Determine parent entity from folder structure
        parent_entity = self._get_parent_entity_from_path(entity.path)
        
        # Prepare data for API call
        api_data = {
            'name': entity.name,
            'type': 'category',
            'subtype': entity.minor_kind.value,
            'start_date': entity.start_date,
            'end_date': entity.end_date,
            'path': str(entity.path),
            'parent_entity': parent_entity,
            'context': {
                'year': context.year,
                'country': context.country,
                'government': context.government,
                'president': context.president,
                'minister': context.minister,
                'department': context.department
            }
        }
        
        # Call registered callback if available
        if 'Category' in self.api_callbacks:
            return self.api_callbacks['Category'](api_data)
        
        # Default implementation (TODO: implement actual API call)
        print(f"TODO: Create category node: {entity.name} with parent: {parent_entity}")
        return True
    
    
    def _find_data_files(self, entity_path: Path) -> List[Path]:
        """Find data.json files in entity path."""
        data_files = []
        
        for file_path in entity_path.rglob('data.json'):
            data_files.append(file_path)
        
        return data_files
    
    def _get_parent_entity_from_path(self, entity_path: Path) -> Optional[Dict[str, str]]:
        """
        Determine parent entity from folder structure.
        This method analyzes the folder path to determine the parent entity
        (Minister, Department, etc.) that this category should be related to.
        
        Args:
            entity_path: Path to the entity
            
        Returns:
            Dictionary with parent entity information or None
        """
        path_parts = entity_path.parts
        
        # Look for Minister or Department in the path
        for i, part in enumerate(path_parts):
            if part.startswith('Minister of') or part.startswith('State Minister of'):
                return {
                    'type': 'Minister',
                    'name': part,
                    'path': str(Path(*path_parts[:i+1]))
                }
            elif part.endswith('Bureau') or part.endswith('Authority') or part.endswith('Department'):
                return {
                    'type': 'Department',
                    'name': part,
                    'path': str(Path(*path_parts[:i+1]))
                }
        
        return None
    
    def batch_save_entities(self, entities: List[EntityMetadata], contexts: List[TraversalContext]) -> bool:
        """
        Save multiple entities in batch via API.
        
        Args:
            entities: List of entities to save
            contexts: List of corresponding contexts
            
        Returns:
            True if successful, False otherwise
        """
        if len(entities) != len(contexts):
            return False
        
        # Prepare batch data
        batch_data = []
        for entity, context in zip(entities, contexts):
            api_data = {
                'name': entity.name,
                'type': entity.major_kind.value,
                'subtype': entity.minor_kind.value,
                'start_date': entity.start_date,
                'end_date': entity.end_date,
                'path': str(entity.path),
                'context': {
                    'year': context.year,
                    'country': context.country,
                    'government': context.government,
                    'president': context.president,
                    'minister': context.minister,
                    'department': context.department
                }
            }
            batch_data.append(api_data)
        
        # Call registered callback if available
        if 'BatchSave' in self.api_callbacks:
            return self.api_callbacks['BatchSave'](batch_data)
        
        # Default implementation (TODO: implement actual API call)
        print(f"TODO: Batch save {len(entities)} entities")
        return True
    
    def save_entity_relationships(self, relationships: List[tuple]) -> bool:
        """
        Save entity relationships to database via API.
        
        Args:
            relationships: List of (parent, child) entity tuples
            
        Returns:
            True if successful, False otherwise
        """
        # Prepare relationship data
        relationship_data = []
        for parent, child in relationships:
            relationship_data.append({
                'parent': {
                    'name': parent.name,
                    'type': parent.major_kind.value,
                    'path': str(parent.path)
                },
                'child': {
                    'name': child.name,
                    'type': child.major_kind.value,
                    'path': str(child.path)
                }
            })
        
        # Call registered callback if available
        if 'Relationships' in self.api_callbacks:
            return self.api_callbacks['Relationships'](relationship_data)
        
        # Default implementation (TODO: implement actual API call)
        print(f"TODO: Save {len(relationships)} entity relationships")
        return True
    
    def get_save_statistics(self) -> Dict[str, int]:
        """Get statistics about saved entities."""
        return {
            'total_saved': len(self.batch_data),
            'by_type': {},
            'by_year': {}
        }
    
    def clear_batch_data(self):
        """Clear batch data."""
        self.batch_data.clear()
    
    def validate_entity_data(self, entity: EntityMetadata) -> bool:
        """
        Validate entity data before saving.
        
        Args:
            entity: Entity to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Check required fields
        if not entity.name or not entity.start_date or not entity.end_date:
            return False
        
        # Check date format
        try:
            from datetime import datetime
            datetime.strptime(entity.start_date, '%Y-%m-%d')
            datetime.strptime(entity.end_date, '%Y-%m-%d')
        except ValueError:
            return False
        
        return True
