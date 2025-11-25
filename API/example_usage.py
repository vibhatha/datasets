#!/usr/bin/env python3
"""
Example usage of the opendata package.

This script demonstrates how to use the opendata package to traverse
folder structures and save data via third-party API calls.
"""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from opendata import OpenDataProcessor, APIConfig, EntityType, DataFormat
from opendata.traverser import DataTraverser
from opendata.entity_parser import EntityParser


def main():
    """Main function demonstrating opendata usage."""
    
    # Configuration
    data_root = "../data"
    
    # API Configuration (replace with your actual API details)
    api_config = APIConfig(
        base_url="https://api.example.com",
        api_key="your-api-key-here",
        timeout=30,
        retry_attempts=3,
        batch_size=100
    )
    
    print("=== OpenData Package Demo ===\n")
    
    # Example 1: Basic traversal
    print("1. Basic Folder Traversal")
    print("-" * 30)
    
    traverser = DataTraverser(data_root)
    entities = traverser.traverse()
    
    print(f"Found {len(entities)} entities")
    print(f"Entity summary: {traverser.get_entity_summary()}")
    
    # Example 2: Get specific entity types (focused on Dataset and Category)
    print("\n2. Entity Type Analysis (Focused)")
    print("-" * 30)
    
    parser = traverser.parser
    
    # Get focused entity types
    category_entities = parser.get_category_entities()
    dataset_entities = parser.get_data_entities()
    tabular_entities = parser.get_tabular_datasets()
    
    print(f"Category entities: {len(category_entities)}")
    print(f"Dataset entities: {len(dataset_entities)}")
    print(f"Tabular datasets: {len(tabular_entities)}")
    print("Note: Organisation entities are assumed to be already saved")
    
    # Example 3: Get entities by year
    print("\n3. Entities by Year")
    print("-" * 30)
    
    for year in ["2019", "2020", "2021", "2022", "2023"]:
        year_entities = traverser.get_entities_by_year(year)
        print(f"{year}: {len(year_entities)} entities")
    
    # Example 4: Entity relationships
    print("\n4. Entity Relationships")
    print("-" * 30)
    
    relationships = parser.get_entity_relationships()
    print(f"Found {len(relationships)} entity relationships")
    
    # Show some example relationships
    for i, (parent, child) in enumerate(relationships[:5]):
        print(f"  {parent.name} -> {child.name}")
    
    if len(relationships) > 5:
        print(f"  ... and {len(relationships) - 5} more")
    
    # Example 5: Data flow analysis
    print("\n5. Data Flow Analysis")
    print("-" * 30)
    
    data_flow = traverser.get_data_flow()
    print(f"Found {len(data_flow)} organisation data flows")
    
    for org_name, data_entities in list(data_flow.items())[:3]:
        print(f"  {org_name}: {len(data_entities)} data entities")
    
    # Example 6: Using the main processor (focused approach)
    print("\n6. Main Processor Demo (Focused on Dataset and Category)")
    print("-" * 30)
    
    try:
        processor = OpenDataProcessor(data_root, api_config)
        results = processor.process_data()
        
        print("Processing completed successfully!")
        print(f"Results: {results}")
        print("Note: Only Dataset and Category entities are processed")
        print("      Organisation entities are assumed to be already saved")
        
    except Exception as e:
        print(f"Error in main processor: {e}")
    
    # Example 7: Custom traversal callback
    print("\n7. Custom Traversal Callback")
    print("-" * 30)
    
    def custom_callback(context, entity):
        print(f"  Processing: {entity.name} ({entity.major_kind.value})")
        if context.year:
            print(f"    Year: {context.year}")
        if context.country:
            print(f"    Country: {context.country}")
        if context.president:
            print(f"    President: {context.president}")
    
    # Create new traverser with custom callback
    custom_traverser = DataTraverser(data_root)
    custom_traverser.add_traversal_callback(custom_callback)
    
    print("Traversing with custom callback...")
    custom_traverser.traverse()
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
