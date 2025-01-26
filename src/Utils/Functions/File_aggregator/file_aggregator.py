import os
import yaml
from pathlib import Path
from typing import List, Dict, Set
import fnmatch
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FileInfo:
    """Data class to store file information"""
    path: str
    language: str
    content: str

class FileAggregator:
    """Class to aggregate file contents based on YAML configuration"""
    
    # Language mapping based on file extensions
    LANGUAGE_MAP = {
        '.py': 'python',
        '.js': 'javascript',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.md': 'markdown',
        '.json': 'json',
        '.html': 'html',
        '.css': 'css',
        '.txt': 'text'
    }
    
    def __init__(self, config_path: str):
        """Initialize with path to YAML config file"""
        self.config_path = Path(config_path)
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        self.config = self._load_config(self.config_path)
        self.processed_files: Set[str] = set()
        
    def _normalize_path(self, path_str: str) -> Path:
        """
        Normalize a path string to handle both Windows and Unix-style paths.
        Handles paths with single or double backslashes and forward slashes.
        Also handles YAML literal style paths with extra newlines.
        
        Args:
            path_str (str): Input path string
            
        Returns:
            Path: Normalized pathlib.Path object
        """
        # Remove quotes and strip whitespace/newlines
        path_str = path_str.strip('"').strip("'").strip()
        
        try:
            # Convert to Path object (handles both forward and backward slashes)
            path = Path(path_str).resolve()
            logger.debug(f"Normalized path: {path_str} -> {path}")
            return path
        except Exception as e:
            logger.error(f"Error normalizing path '{path_str}': {e}")
            raise
            
    def _load_config(self, config_path: Path) -> Dict:
        """Load and validate YAML configuration"""
        try:
            with config_path.open('r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
            # Normalize all paths in config
            if 'include' in config:
                if 'files' in config['include']:
                    config['include']['files'] = [str(self._normalize_path(p)) for p in config['include']['files']]
                if 'directories' in config['include']:
                    config['include']['directories'] = [str(self._normalize_path(p)) for p in config['include']['directories']]
                    
            return config
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML config: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            raise
            
    def _get_file_language(self, file_path: str) -> str:
        """Determine the language based on file extension"""
        ext = Path(file_path).suffix.lower()
        return self.LANGUAGE_MAP.get(ext, 'text')
        
    def _should_exclude(self, path: str) -> bool:
        """
        Check if path should be excluded based on patterns.
        Matches against both full path and filename.
        
        Args:
            path (str): Path to check for exclusion
            
        Returns:
            bool: True if path should be excluded, False otherwise
        """
        patterns = self.config.get('exclude', {}).get('patterns', [])
        path_obj = Path(path)
        
        # Check filename against patterns
        for pattern in patterns:
            # Special handling for __init__ pattern
            if pattern == "__init__" and path_obj.name == "__init__.py":
                return True
            # Check both filename and full path
            if fnmatch.fnmatch(path_obj.name, pattern) or fnmatch.fnmatch(str(path_obj), pattern):
                return True
        return False
        
    def _read_file(self, file_path: str) -> FileInfo:
        """Read file contents and create FileInfo object"""
        try:
            path = Path(file_path)
            if not path.exists():
                logger.warning(f"File not found: {file_path}")
                return None
                
            if self._should_exclude(file_path):
                logger.debug(f"Skipping excluded file: {file_path}")
                return None
                
            if str(path.absolute()) in self.processed_files:
                logger.debug(f"Skipping already processed file: {file_path}")
                return None
                
            with path.open('r', encoding='utf-8') as f:
                content = f.read()
                
            self.processed_files.add(str(path.absolute()))
            return FileInfo(
                path=str(path),
                language=self._get_file_language(file_path),
                content=content
            )
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None
            
    def process_files(self) -> List[FileInfo]:
        """Process all files based on configuration"""
        file_infos = []
        
        # Process individual files
        for file_path in self.config.get('include', {}).get('files', []):
            file_info = self._read_file(file_path)
            if file_info:
                file_infos.append(file_info)
                
        # Process directories
        for dir_path in self.config.get('include', {}).get('directories', []):
            try:
                dir_path = Path(dir_path)
                if not dir_path.exists():
                    logger.warning(f"Directory not found: {dir_path}")
                    continue
                    
                for root, _, files in os.walk(str(dir_path)):
                    for file in files:
                        file_path = Path(root) / file
                        file_info = self._read_file(str(file_path))
                        if file_info:
                            file_infos.append(file_info)
            except Exception as e:
                logger.error(f"Error processing directory {dir_path}: {e}")
                
        return file_infos
        
    def generate_markdown(self, output_path: str):
        """Generate markdown file with aggregated contents"""
        file_infos = self.process_files()
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("# Aggregated Files\n\n")
                for file_info in file_infos:
                    relative_path = str(Path(file_info.path))
                    f.write(f"## File: {relative_path}\n")
                    f.write(f"```{file_info.language}\n")
                    f.write(file_info.content)
                    f.write("\n```\n\n")
            logger.info(f"Successfully generated markdown file: {output_path}")
        except Exception as e:
            logger.error(f"Error generating markdown file: {e}")
            raise

if __name__ == '__main__':
    # Example usage
    config_path = "file_aggregator.yaml"
    output_path = "aggregated_files.md"
    
    try:
        aggregator = FileAggregator(config_path)
        aggregator.generate_markdown(output_path)
    except Exception as e:
        logger.error(f"Failed to aggregate files: {e}")
        raise