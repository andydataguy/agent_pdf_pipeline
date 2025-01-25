#!/usr/bin/env python3
"""
Directory Tree Generator
A utility to generate markdown-formatted directory trees with configurable depth and exclusion patterns.
"""

import os
import sys
from pathlib import Path
import fnmatch
import argparse
import datetime
import yaml
from typing import List, Dict, Optional, Union
from dataclasses import dataclass

@dataclass
class TreeConfig:
    """Configuration for directory tree generation"""
    path: str = "."
    depth: int = -1
    exclude: List[str] = None
    output: str = "tree.md"
    show_size: bool = True
    show_modified_date: bool = False
    emoji_style: bool = True

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'TreeConfig':
        """Create configuration from YAML file"""
        with open(yaml_path, 'r') as f:
            config_dict = yaml.safe_load(f)
            
        # Extract settings from nested dict if present
        settings = config_dict.pop('settings', {})
        config_dict.update(settings)
        
        # Convert to TreeConfig object
        return cls(
            path=config_dict.get('path', "."),
            depth=config_dict.get('depth', -1),
            exclude=config_dict.get('exclude', []),
            output=config_dict.get('output', "tree.md"),
            show_size=config_dict.get('show_size', True),
            show_modified_date=config_dict.get('show_modified_date', False),
            emoji_style=config_dict.get('emoji_style', True)
        )

class DirectoryTree:
    """Generate a markdown-formatted directory tree"""
    
    def __init__(self, config: TreeConfig):
        self.config = config
        self.output_lines = []
        self.root_path = Path(config.path).resolve()
    
    def format_size(self, size: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
    
    def format_date(self, timestamp: float) -> str:
        """Format modification date"""
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")
    
    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded based on patterns"""
        if not self.config.exclude:
            return False
        return any(fnmatch.fnmatch(path.name, pattern) for pattern in self.config.exclude)
    
    def add_node(self, path: Path, prefix: str = "", depth: int = 0):
        """Add a node (file or directory) to the tree"""
        if self.should_exclude(path):
            return
            
        if self.config.depth != -1 and depth > self.config.depth:
            return
            
        # Prepare node indicators
        if self.config.emoji_style:
            indicator = "📁 " if path.is_dir() else "📄 "
        else:
            indicator = "└── " if path.is_dir() else "├── "
            
        # Build node line
        node_line = f"{prefix}{indicator}{path.name}"
        
        # Add file size if enabled
        if self.config.show_size and path.is_file():
            size = self.format_size(path.stat().st_size)
            node_line += f" ({size})"
            
        # Add modification date if enabled
        if self.config.show_modified_date:
            mtime = self.format_date(path.stat().st_mtime)
            node_line += f" [{mtime}]"
            
        self.output_lines.append(node_line)
        
        # Process subdirectories
        if path.is_dir():
            children = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name))
            for child in children:
                self.add_node(child, prefix + "  ", depth + 1)
    
    def generate_tree(self) -> str:
        """Generate the complete directory tree"""
        # Add header
        self.output_lines = [
            "# Latest Directory Tree",
            f"Generated for: `{self.root_path}`\n"
        ]
        
        # Generate tree structure
        self.add_node(self.root_path)
        
        return "\n".join(self.output_lines)
    
    def save_tree(self):
        """Save the generated tree to file or print to stdout"""
        tree_content = self.generate_tree()
        
        if self.config.output == "-":
            print(tree_content)
        else:
            with open(self.config.output, 'w', encoding='utf-8') as f:
                f.write(tree_content)
            print(f"Directory tree saved to: {self.config.output}")

def main():
    """Main entry point for the directory tree generator"""
    parser = argparse.ArgumentParser(description="Generate a markdown-formatted directory tree")
    parser.add_argument("--config", type=str, default="directory_tree.yaml",
                      help="Path to YAML configuration file")
    args = parser.parse_args()
    
    try:
        # Load configuration from YAML
        config = TreeConfig.from_yaml(args.config)
        
        # Generate and save tree
        tree = DirectoryTree(config)
        tree.save_tree()
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()