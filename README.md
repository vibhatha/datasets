# Datasets Project

This project contains structured data with metadata files and a Python API package for traversing and processing the data.

## Project Structure

```
datasets/
├── data/                    # Data directory with meta.yml files
│   ├── 2019/               # 2019 data
│   ├── 2020/               # 2020 data
│   ├── 2021/               # 2021 data
│   ├── 2022/               # 2022 data
│   └── 2023/               # 2023 data
├── API/                    # Python API package
│   ├── opendata/           # Main package
│   ├── example_usage.py   # Usage examples
│   ├── test_installation.py # Installation test
│   ├── install.sh         # Installation script
│   ├── pyproject.toml     # Modern Python packaging
│   ├── setup.py           # Traditional setup script
│   ├── MANIFEST.in        # Package manifest
│   └── README.md          # API documentation
└── README.md               # This file
```

## Data Structure

The `data/` directory contains structured data organized by year, with each folder containing `meta.yml` files that define:

- **Entity Types**: Organisation, Category, Dataset, Person, Land Parcel
- **Data Formats**: Tabular, Minister, Department, Government, Citizen, Country, Data
- **Metadata**: Name, kind, start_date, end_date for each entity

## API Package

The `API/` directory contains a complete Python package for:

- **Traversing** folder structures with meta.yml files
- **Parsing** entity metadata and relationships
- **Processing** data with context awareness
- **Integrating** with third-party APIs

### Quick Start with API

```bash
# Navigate to API directory
cd API

# Install the package
pip install -e .

# Run example
python example_usage.py
```

For detailed API documentation, see [API/README.md](API/README.md).

## Features

- **Structured Data**: Organized by year with consistent metadata
- **Entity Relationships**: Parent-child relationships between entities
- **Context Awareness**: Year, country, government, president context
- **Data Flow Analysis**: From organisations to datasets
- **API Integration**: Ready for database integration

## Usage

### Using the Data

The data is organized in a hierarchical structure:

```
data/
├── 2023/
│   └── Sri Lanka/
│       └── Government/
│           └── Ranil Wickremesinghe/
│               ├── Minister of Foreign Affairs/
│               │   ├── meta.yml
│               │   ├── human_resources/
│               │   │   ├── meta.yml
│               │   │   └── data.json
│               │   └── official_communications/
│               │       ├── meta.yml
│               │       └── data.json
│               └── ...
└── ...
```

### Using the API

```python
from opendata import OpenDataProcessor, APIConfig

# Configure API
api_config = APIConfig(
    base_url="https://api.example.com",
    api_key="your-api-key-here"
)

# Create processor
processor = OpenDataProcessor("../data", api_config)

# Process data
results = processor.process_data()
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License