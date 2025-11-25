"""
Main Module

Demonstrates how to use the opendata package to traverse folder structures
and save data via third-party API calls.
"""

from pathlib import Path
from typing import Dict, List, Any

from .traverser import DataTraverser, TraversalContext
from .entity_parser import EntityMetadata, EntityType, DataFormat
from .api_utils import APIUtils, APIConfig


class OpenDataProcessor:
    """Main processor class that orchestrates the entire workflow."""
    
    def __init__(self, data_root: str, api_config: APIConfig):
        """
        Initialize the OpenData processor.
        
        Args:
            data_root: Root directory containing the data
            api_config: API configuration for saving data
        """
        self.traverser = DataTraverser(data_root)
        self.api_utils = APIUtils(api_config)
        self.setup_callbacks()
    
    def setup_callbacks(self):
        """Setup traversal and API callbacks."""
        # Add traversal callback to handle entities during traversal
        self.traverser.add_traversal_callback(self._handle_entity)
        
        # Register API callbacks for focused entity types
        self.api_utils.register_api_callback('Dataset', self._save_dataset)
        self.api_utils.register_api_callback('Category', self._create_category_node)
    
    def process_data(self) -> Dict[str, Any]:
        """
        Process all data in the folder structure.
        
        Returns:
            Dictionary containing processing results and statistics
        """
        print("Starting data processing...")
        
        # Traverse the folder structure
        entities = self.traverser.traverse()
        print(f"Found {len(entities)} entities")
        
        # Get entity summary
        summary = self.traverser.get_entity_summary()
        print(f"Entity summary: {summary}")
        
        # Process different types of entities
        results = {
            'total_entities': len(entities),
            'summary': summary,
            'processing_results': {}
        }
        
        # Process organisations
        org_entities = self.traverser.parser.get_organisation_entities()
        results['processing_results']['organisations'] = len(org_entities)
        
        # Process categories
        category_entities = self.traverser.parser.get_category_entities()
        results['processing_results']['categories'] = len(category_entities)
        
        # Process datasets
        dataset_entities = self.traverser.parser.get_data_entities()
        results['processing_results']['datasets'] = len(dataset_entities)
        
        # Process tabular data
        tabular_entities = self.traverser.parser.get_tabular_datasets()
        results['processing_results']['tabular_datasets'] = len(tabular_entities)
        
        # Get entity relationships
        relationships = self.traverser.parser.get_entity_relationships()
        results['processing_results']['relationships'] = len(relationships)
        
        print("Data processing completed!")
        return results
    
    def _handle_entity(self, context: TraversalContext, entity: EntityMetadata):
        """
        Handle an entity during traversal.
        Focuses on Dataset and Category entities only.
        
        Args:
            context: Traversal context
            entity: Entity metadata
        """
        print(f"Processing entity: {entity.name} ({entity.major_kind.value})")
        
        # Validate entity data
        if not self.api_utils.validate_entity_data(entity):
            print(f"Invalid entity data: {entity.name}")
            return
        
        # Process only Dataset and Category entities
        if entity.major_kind == EntityType.DATASET:
            # Save dataset with actual data
            self.api_utils.save_dataset_entity(entity, context)
        elif entity.major_kind == EntityType.CATEGORY:
            # Create category node and establish relationships
            self.api_utils.create_category_node(entity, context)
        else:
            # Skip Organisation, Person, Land Parcel entities (assumed already saved)
            print(f"Skipping {entity.major_kind.value} entity: {entity.name} (assumed already saved)")
    
    def _save_dataset(self, api_data: Dict[str, Any]) -> bool:
        """
        Save dataset entity via API.
        This function receives the dataset data and should call the third-party API
        to save the actual data content.
        
        Args:
            api_data: Dictionary containing dataset information and data content
            
        Returns:
            True if successful, False otherwise
        """
        print(f"TODO: API call to save dataset: {api_data['name']}")
        print(f"  - Data files: {len(api_data['data_content'])}")
        print(f"  - Context: {api_data['context']}")
        
        # TODO: Implement actual API call
        # Example structure:
        # - Call third-party API endpoint for dataset
        # - Send data_content to the API
        # - Handle response and errors
        
        return True
    
    def _create_category_node(self, api_data: Dict[str, Any]) -> bool:
        """
        Create category node and establish relationships via API.
        This function creates a graph node for the category and establishes
        relationships with the parent entity.
        
        Args:
            api_data: Dictionary containing category information and parent entity
            
        Returns:
            True if successful, False otherwise
        """
        print(f"TODO: API call to create category node: {api_data['name']}")
        print(f"  - Parent entity: {api_data['parent_entity']}")
        print(f"  - Context: {api_data['context']}")
        
        # TODO: Implement actual API call
        # Example structure:
        # - Call third-party API to create category node
        # - Establish relationship with parent entity
        # - Handle response and errors
        
        return True
    
    def get_entities_by_year(self, year: str) -> List[EntityMetadata]:
        """Get entities for a specific year."""
        return self.traverser.get_entities_by_year(year)
    
    def get_entities_by_type(self, entity_type: EntityType) -> List[EntityMetadata]:
        """Get entities by type."""
        return self.traverser.parser.get_entities_by_type(entity_type)
    
    def get_data_flow(self) -> Dict[str, List[EntityMetadata]]:
        """Get data flow from organisations to datasets."""
        return self.traverser.get_data_flow()
    
    def export_entity_graph(self, output_file: str):
        """Export entity graph to a file."""
        # TODO: Implement entity graph export
        print(f"TODO: Export entity graph to {output_file}")


def main():
    """Main function to demonstrate usage."""
    # Example usage
    data_root = "../data"
    
    # Configure API
    api_config = APIConfig(
        base_url="https://api.example.com",
        api_key="your-api-key-here",
        timeout=30,
        retry_attempts=3,
        batch_size=100
    )
    
    # Create processor
    processor = OpenDataProcessor(data_root, api_config)
    
    # Process data
    results = processor.process_data()
    
    # Print results
    print("\nProcessing Results:")
    for key, value in results.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
