# OpenData Package

A Python library for traversing folder structures with meta.yml files and understanding graph entities for database integration.

## Features

- **Entity Parsing**: Parse meta.yml files and identify graph entity types
- **Folder Traversal**: Traverse folder structures with context awareness
- **API Integration**: Utility functions for third-party API calls
- **Entity Relationships**: Build and manage entity hierarchies
- **Data Flow Analysis**: Understand data flow from organisations to datasets

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from opendata import OpenDataProcessor, APIConfig

# Configure API
api_config = APIConfig(
    base_url="https://api.example.com",
    api_key="your-api-key-here"
)

# Create processor
processor = OpenDataProcessor("/path/to/data", api_config)

# Process data
results = processor.process_data()
```

### Advanced Usage

```python
from opendata import DataTraverser, EntityParser, APIUtils

# Create traverser
traverser = DataTraverser("/path/to/data")

# Add custom callback
def my_callback(context, entity):
    print(f"Processing: {entity.name}")

traverser.add_traversal_callback(my_callback)

# Traverse and get entities
entities = traverser.traverse()

# Get specific entity types
data_entities = traverser.parser.get_data_entities()
org_entities = traverser.parser.get_organisation_entities()
```

## Entity Types

The library recognizes the following entity types:

- **Organisation**: May or may not contain data
- **Category**: Tracks a particular type of data
- **Dataset**: Actual data values to save in database
- **Person**: Individual entities
- **Land Parcel**: Geographic entities

## Data Formats

- **Tabular**: Data saved as tabular format
- **Minister**: Government minister entities
- **Department**: Government department entities
- **Government**: Government organisation entities
- **Citizen**: Individual citizen entities
- **Country**: Country entities
- **Data**: Data category entities

## API Integration

The library provides utility functions for third-party API calls:

```python
# Register custom API callbacks
api_utils.register_api_callback('Organisation', my_org_callback)
api_utils.register_api_callback('Dataset', my_dataset_callback)

# Save entities
api_utils.save_organisation_entity(entity, context)
api_utils.save_dataset_entity(entity, context)
api_utils.save_tabular_data(entity, context)
```

## Examples

### Processing All Data

```python
from opendata import OpenDataProcessor, APIConfig

# Setup
api_config = APIConfig(
    base_url="https://api.example.com",
    api_key="your-api-key"
)

processor = OpenDataProcessor("/path/to/data", api_config)
results = processor.process_data()
```

### Getting Specific Entities

```python
# Get entities by year
entities_2023 = processor.get_entities_by_year("2023")

# Get entities by type
org_entities = processor.get_entities_by_type(EntityType.ORGANISATION)

# Get data flow
data_flow = processor.get_data_flow()
```

## TODO Functions

The library includes TODO utility functions for third-party API calls:

- `save_organisation_entity()`: Save organisation entities
- `save_category_entity()`: Save category entities  
- `save_dataset_entity()`: Save dataset entities
- `save_tabular_data()`: Save tabular data
- `batch_save_entities()`: Save multiple entities in batch
- `save_entity_relationships()`: Save entity relationships

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
