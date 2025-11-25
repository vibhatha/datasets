# OpenData API Package

A Python library for traversing folder structures with meta.yml files and understanding graph entities for database integration.

## Features

- **Focused Processing**: Processes only Dataset and Category entities
- **Dataset Processing**: Saves actual data content from JSON files
- **Category Graph Nodes**: Creates graph nodes and establishes relationships
- **Folder Structure Analysis**: Uses folder structure to determine parent entities
- **API Integration**: Utility functions for third-party API calls
- **Assumes Existing Entities**: Organisation/Minister/Department entities are already saved

## Installation

### Option 1: Install from source (Development)

```bash
# Navigate to the API directory
cd API

# Install in development mode
pip install -e .

# Or use the installation script
./install.sh
```

### Option 2: Install as a package

```bash
# Install the package
pip install opendata

# Or install with development dependencies
pip install opendata[dev]
```

## Quick Start

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

## Usage Examples

### Basic Traversal

```python
from opendata import DataTraverser

# Create traverser
traverser = DataTraverser("/path/to/data")

# Traverse and get entities
entities = traverser.traverse()
print(f"Found {len(entities)} entities")
```

### Entity Analysis

```python
from opendata import EntityParser, EntityType

# Get entity parser
parser = traverser.parser

# Get different entity types
org_entities = parser.get_organisation_entities()
dataset_entities = parser.get_data_entities()
tabular_entities = parser.get_tabular_datasets()

print(f"Organisations: {len(org_entities)}")
print(f"Datasets: {len(dataset_entities)}")
print(f"Tabular datasets: {len(tabular_entities)}")
```

### Custom Traversal Callback

```python
def my_callback(context, entity):
    print(f"Processing: {entity.name} ({entity.major_kind.value})")
    if context.year:
        print(f"  Year: {context.year}")
    if context.country:
        print(f"  Country: {context.country}")

# Add callback to traverser
traverser.add_traversal_callback(my_callback)
traverser.traverse()
```

## Entity Types (Focused Processing)

The library focuses on processing the following entity types:

- **Dataset**: Actual data values to save in database (main focus)
- **Category**: Creates graph nodes and establishes relationships

**Assumed Already Saved:**
- **Organisation**: Minister and Department entities
- **Person**: President and other individual entities
- **Land Parcel**: Country entities

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
from opendata import APIUtils, APIConfig

# Configure API
api_config = APIConfig(
    base_url="https://api.example.com",
    api_key="your-api-key"
)

api_utils = APIUtils(api_config)

# Register custom API callbacks
def my_org_callback(api_data):
    # Your API call implementation
    print(f"Saving organisation: {api_data['name']}")
    return True

api_utils.register_api_callback('Organisation', my_org_callback)

# Save entities
api_utils.save_organisation_entity(entity, context)
api_utils.save_dataset_entity(entity, context)
api_utils.save_tabular_data(entity, context)
```

## Testing

Run the test script to verify installation:

```bash
python test_installation.py
```

Run the example usage:

```bash
python example_usage.py
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run linting
flake8 opendata/
black opendata/
mypy opendata/
```

### Project Structure

```
API/
├── opendata/              # Main package
│   ├── __init__.py        # Package initialization
│   ├── entity_parser.py  # Entity parsing logic
│   ├── traverser.py      # Folder traversal logic
│   ├── api_utils.py      # API utility functions
│   ├── main.py           # Main processor
│   ├── requirements.txt # Package dependencies
│   └── README.md         # Package documentation
├── example_usage.py      # Usage examples
├── test_installation.py  # Installation test
├── install.sh           # Installation script
├── pyproject.toml       # Modern Python packaging
├── setup.py             # Traditional setup script
├── MANIFEST.in          # Package manifest
└── README.md            # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License

## Support

For issues and questions, please use the GitHub issues page.
