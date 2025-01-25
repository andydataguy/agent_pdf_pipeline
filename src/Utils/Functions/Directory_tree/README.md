# Directory Tree Generator

A simple and efficient Python utility to generate markdown-formatted directory trees with configurable depth and exclusion patterns. Now with YAML-based configuration for easier customization!

## Features

- Generate directory trees in markdown format
- YAML-based configuration
- Configurable maximum depth
- Pattern-based file/directory exclusion
- Clean, emoji-based visual indicators
- Optional file size and modification date display
- Output to file or stdout
- Cross-platform compatibility using `pathlib`

## Configuration

Create a `directory_tree.yaml` file with your desired settings:

```yaml
# Root directory path (default: current directory)
path: "."

# Maximum depth to traverse (default: unlimited)
# Set to -1 for unlimited depth
depth: -1

# List of patterns to exclude
exclude:
  - "*.pyc"
  - "__pycache__"
  - "node_modules"
  - ".git"
  - ".vscode"

# Output markdown file (default: tree.md)
output: "tree.md"

# Optional settings
settings:
  show_size: true           # Show file sizes
  show_modified_date: false # Show last modified dates
  emoji_style: true         # Use emoji indicators for files/folders
```

## Usage

```bash
# Use default config file (directory_tree.yaml)
python directory_tree.py

# Specify custom config file
python directory_tree.py --config custom_config.yaml
```

## Sample Output

```markdown
# Directory Tree
Generated for: `/your/project/path`

📁 src
  📁 components
    📄 app.py (2.3KB) [2024-01-08 12:00]
    📄 utils.py (1.1KB)
  📁 tests
    📄 test_app.py (3.4KB)
📄 README.md (1.2KB)
📄 requirements.txt (156B)
```

## Requirements

- Python 3.6+
- PyYAML

Install dependencies:
```bash
pip install pyyaml
```

## Implementation Details

The script uses:
- `pathlib` for cross-platform path handling
- `yaml` for configuration parsing
- `dataclasses` for type-safe configuration
- `fnmatch` for pattern matching
- Type hints for better code clarity

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.