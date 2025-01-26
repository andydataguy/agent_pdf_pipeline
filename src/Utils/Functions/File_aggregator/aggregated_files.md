# Aggregated Files

## File: C:\Users\Anand\Documents\Code Projects\agent_data_platform\experiments\agent_pdf_pipeline\main.py
```python
import os
import yaml
import pathlib
from src.Processing.pdf_to_markdown import PDFParsingModule
from src.Utils.Logger.logfire import LogfireLogger

def load_config(config_path="src/Processing/pdf_parser_config.yaml"):
    """
    Loads configuration from a YAML file.

    Args:
        config_path (str, optional): Path to the YAML configuration file. Defaults to "src/Processing/pdf_parser_config.yaml".

    Returns:
        dict: Configuration dictionary, or None if loading fails.
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            print(f"Configuration loaded from: {config_path}")
            return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found at: {config_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML configuration: {e}")
        return None

def main():
    """
    Main function to orchestrate PDF parsing and Markdown conversion.
    """
    # Load configuration
    config = load_config()
    if not config:
        print("Exiting due to configuration error.")
        return

    # Initialize logger with error handling
    try:
        logger = LogfireLogger(config=config)
    except Exception as e:
        print(f"Warning: Logger initialization failed: {e}")
        print("Continuing with default console logging...")
        logger = LogfireLogger()  # Fallback to default console logging

    # Define paths
    pdf_path = "Uploads/samples/monolith_realtime_recommend.pdf"
    output_dir = ".output"

    logger.log_info("Starting main PDF parsing process.", pdf_path=pdf_path, output_dir=output_dir)

    # Create output directory
    output_path_dir = os.path.join(output_dir, pathlib.Path(pdf_path).stem)
    os.makedirs(output_path_dir, exist_ok=True)

    # Define output markdown path
    output_markdown_path = os.path.join(
        output_path_dir,
        pathlib.Path(pdf_path).stem + config['output_module'].get('markdown_filename_suffix', '_parsed') + ".md"
    )

    # Initialize and run PDF parsing
    try:
        pdf_parsing_module = PDFParsingModule(config)
        success = pdf_parsing_module.process_pdf(pdf_path, output_markdown_path)
        
        if success:
            logger.log_info("PDF processing completed successfully", 
                          output_path=output_markdown_path)
        else:
            logger.log_error("PDF processing failed", 
                           pdf_path=pdf_path)
    except Exception as e:
        logger.log_error(f"Error during PDF processing: {str(e)}", 
                        pdf_path=pdf_path,
                        error_type=type(e).__name__)

if __name__ == "__main__":
    main()
```

## File: C:\Users\Anand\Documents\Code Projects\agent_data_platform\experiments\agent_pdf_pipeline\src\Utils\Logger\logfire.py
```python
import logfire
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LogfireLogger:
    """
    The ABSOLUTE SIMPLEST, copy-paste ready template for Logfire logging in any Python project.
    Provides basic, configurable console logging and Logfire platform integration.
    """

    def __init__(self, config=None): 
        """
        Initializes the LogfireLogger with configuration from YAML and environment variables.

        Args:
            config (dict, optional): Configuration dictionary loaded from YAML. Defaults to None.
        """
        # Get Logfire token from environment variables
        self.logfire_token = os.getenv('LOGFIRE_TOKEN')
        
        # Default configuration using string log levels
        self.console_log_level = "info"
        self.logfire_enabled = True

        # Override defaults with YAML config if provided
        if config and 'logging_module' in config:
            logging_config = config['logging_module']
            # Map config log levels to Logfire log levels
            level_map = {
                'DEBUG': 'debug',
                'INFO': 'info',
                'WARNING': 'warning',
                'ERROR': 'error',
                'CRITICAL': 'fatal'
            }
            config_level = logging_config.get('console_log_level', 'INFO').upper()
            self.console_log_level = level_map.get(config_level, 'info')
            self.logfire_enabled = logging_config.get('logfire_enabled', True)

        try:
            # Configure console logging
            console_options = logfire.ConsoleOptions(
                min_log_level=self.console_log_level,
                colors=True
            )

            # Configure Logfire if enabled and token is available
            if self.logfire_enabled and self.logfire_token:
                logfire.configure(
                    token=self.logfire_token,
                    console=console_options
                )
            else:
                # Console-only logging
                logfire.configure(console=console_options)
        except Exception as e:
            print(f"Warning: Failed to configure Logfire: {e}")
            # Fallback to basic console configuration
            logfire.configure(
                console=logfire.ConsoleOptions(
                    min_log_level='info',
                    colors=True
                )
            )

    def log_debug(self, message, **kwargs):
        """Log debug message."""
        logfire.debug(message, **kwargs)

    def log_info(self, message, **kwargs):
        """Log info message."""
        logfire.info(message, **kwargs)

    def log_warning(self, message, **kwargs):
        """Log warning message."""
        logfire.warning(message, **kwargs)

    def log_error(self, message, **kwargs):
        """Log error message."""
        logfire.error(message, **kwargs)

    def log_critical(self, message, **kwargs):
        """Log critical message."""
        logfire.fatal(message, **kwargs)

# Example usage (in your application modules):
# from src.Utils.Logger.logfire import LogfireLogger
# logger = LogfireLogger(config=config) # Simplest initialization - no arguments
# logger.log_info("Starting processing...") # Simple logging calls
```

## File: C:\Users\Anand\Documents\Code Projects\agent_data_platform\experiments\agent_pdf_pipeline\src\Processing\pdf_parser_config.yaml
```yaml
# YAML Configuration for PyMuPDF PDF Parsing Pipeline

pdf_parsing_module:
  log_level: INFO  # Minimum log level for PDFParsingModule (TRACE, DEBUG, INFO, NOTICE, WARN, ERROR, FATAL) - Case-insensitive string from Python's logging levels # Corrected: String log level

text_extraction_module:
  text_blocks_strategy: "blocks_sorted"  # Options: "blocks_sorted", "words", "dict", "rawdict", "html", "xml", "xhtml", "text"
  text_formatting:
    bold_style: "**"  # Markdown style for bold text
    italic_style: "_"  # Markdown style for italic text

table_extraction_module:
  strategy: "lines"          # Table detection strategy: "lines", "lines_strict", "text"
  snap_tolerance: 5          # Snap tolerance for line detection (adjust for table line thickness)
  join_tolerance: 5          # Join tolerance for table cell merging (adjust for cell spacing)
  intersection_tolerance: 5  # Intersection tolerance for line intersection detection
  text_tolerance: 5          # Text tolerance for text-based table detection
  edge_min_length: 10        # Minimum line length to be considered a table edge

image_extraction_module:
  image_format: "png"            # Output image format: "png", "jpeg"
  image_quality: 90              # Image quality for JPEG (0-100, ignored for PNG)
  output_subdirectory: "assets/images" # Subdirectory to save extracted images within the output folder

math_notation_module:
  latex_display_delimiter: "$$"  # Markdown delimiter for display LaTeX equations
  latex_inline_delimiter: "$"   # Markdown delimiter for inline LaTeX equations
  # custom_regex_patterns: # Future: List of custom regex patterns for advanced LaTeX detection

code_snippet_module:
  code_fence_style: "```"       # Markdown code fence style: "```", "~~~"
  code_language_detection: true # Future: Enable automatic code language detection
  # custom_keywords_lists: # Future: Dictionaries of custom keywords for language detection

logging_module:
  console_log_level: "INFO"      # Minimum console log level (TRACE, DEBUG, INFO, NOTICE, WARN, ERROR, FATAL)
  logfire_enabled: true         # Enable sending logs to Logfire platform (requires LOGFIRE_TOKEN in .env)

output_module:
  markdown_filename_suffix: "_parsed"  # Suffix to add to output markdown files
```

## File: C:\Users\Anand\Documents\Code Projects\agent_data_platform\experiments\agent_pdf_pipeline\src\Processing\pdf_to_markdown.py
```python
import pymupdf
import os
import yaml
import re
from src.Utils.Logger.logfire import LogfireLogger  # Import LogfireLogger

class PDFParsingModule:
    """
    Orchestrates the PDF parsing process, leveraging sub-modules for element extraction.
    """

    def __init__(self, config):
        """
        Initializes the PDFParsingModule with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
        """
        self.config = config.get('pdf_parsing_module', {}) # Get module specific config, default to empty dict
        self.logger = LogfireLogger(config=config) # Initialize LogfireLogger - SIMPLIFIED, project/service externally configured
        self.log_level = self.config.get('log_level', "INFO") # Default log level if not in config, from YAML


    def parse_pdf_document(self, pdf_path, output_dir):
        """
        Parses a PDF document and returns structured Markdown content.

        Args:
            pdf_path (str): Path to the input PDF file.
            output_dir (str): Directory to save output Markdown and assets.

        Returns:
            str: Markdown content of the document, or None in case of error.
        """
        self.logger.log_info(f"Starting PDF parsing for: {pdf_path}", pdf_path=pdf_path) # Log start of parsing

        markdown_content = "" # Initialize markdown content variable

        try:
            doc = pymupdf.open(pdf_path) # Open the PDF document using PyMuPDF
            self.logger.log_info(f"Document loaded successfully: {pdf_path}", pdf_path=pdf_path, page_count=doc.page_count) # Log document loading

            # Metadata Extraction
            metadata_module = MetadataExtractionModule(self.config) # Initialize MetadataExtractionModule with config
            document_metadata = metadata_module.extract_document_metadata(doc) # Extract document metadata
            markdown_content += self._assemble_yaml_frontmatter(document_metadata) # Add YAML frontmatter to markdown

            # Table of Contents Extraction
            toc_module = MetadataExtractionModule(self.config) # Initialize MetadataExtractionModule for TOC extraction (can reuse)
            table_of_contents = toc_module.extract_table_of_contents(doc) # Extract TOC
            markdown_content += self._format_table_of_contents_markdown(table_of_contents) # Format TOC to Markdown

            # Page Parsing and Content Extraction
            page_parsing_module = PageParsingModule(self.config) # Initialize PageParsingModule with config
            for page in doc: # Iterate through each page in the document
                page_markdown = page_parsing_module.parse_page_content(page, output_dir) # Parse page content
                markdown_content += page_markdown # Append page markdown to document markdown
                self.logger.log_info(f"Page {page.number + 1} parsed.", pdf_path=pdf_path, page_number=page.number + 1) # Log page parsing completion

            doc.close() # Close the PDF document
            self.logger.log_info(f"PDF parsing completed successfully: {pdf_path}", pdf_path=pdf_path) # Log overall parsing completion
            return markdown_content # Return the complete Markdown content

        except FileNotFoundError: # Catch file not found error
            self.logger.log_error(f"File not found: {pdf_path}", pdf_path=pdf_path, exc_info=True) # Log file not found error
            return None # Return None to indicate failure

        except RuntimeError as e: # Catch PyMuPDF runtime errors (e.g., corrupted PDF)
            self.logger.log_error(f"Error processing PDF: {pdf_path} - {e}", pdf_path=pdf_path, exc_info=True) # Log PDF processing error
            return None # Return None to indicate failure

        except Exception as e: # Catch any other unexpected exceptions
            self.logger.log_error(f"Unexpected error during PDF parsing: {pdf_path} - {e}", pdf_path=pdf_path, exc_info=True) # Log unexpected error
            return None # Return None to indicate failure

    def _assemble_yaml_frontmatter(self, metadata):
        """
        Assembles YAML frontmatter from document metadata.

        Args:
            metadata (dict): Dictionary of document metadata.

        Returns:
            str: YAML frontmatter string.
        """
        yaml_str = "---\n" # Start YAML frontmatter
        yaml_str += yaml.dump(metadata, indent=2) # Dump metadata to YAML format
        yaml_str += "---\n\n" # End YAML frontmatter
        return yaml_str # Return YAML frontmatter string


    def _format_table_of_contents_markdown(self, toc):
        """
        Formats the table of contents into a Markdown list.

        Args:
            toc (list): Table of contents data from PyMuPDF.

        Returns:
            str: Markdown representation of the table of contents.
        """
        if not toc: # Check if TOC is empty
            return "" # Return empty string if no TOC

        markdown_toc = "## Table of Contents\n\n" # Start TOC section in Markdown
        for level, title, page_num in toc: # Iterate through TOC entries
            indent = "  " * (level - 1) # Calculate indentation based on level
            markdown_toc += f"{indent}- [{title}](#page-{page_num})\n" # Add list item with link
        markdown_toc += "\n" # Add extra newline for spacing
        return markdown_toc # Return Markdown TOC string


class MetadataExtractionModule:
    """
    Extracts document-level metadata and table of contents from PDF documents.
    """
    def __init__(self, config):
        """
        Initializes the MetadataExtractionModule with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
        """
        self.config = config # Store config, though not directly used in this module yet
        self.logger = LogfireLogger(config=config) # Initialize LogfireLogger - SIMPLIFIED

    def extract_document_metadata(self, doc):
        """
        Extracts document metadata using PyMuPDF.

        Args:
            doc (pymupdf.Document): PyMuPDF Document object.

        Returns:
            dict: Dictionary containing document metadata.
        """
        metadata = doc.metadata if doc.metadata else {} # Get metadata or empty dict if None
        self.logger.log_info("Document metadata extracted.", metadata_keys=list(metadata.keys())) # Log metadata extraction
        return metadata # Return metadata dictionary


    def extract_table_of_contents(self, doc):
        """
        Extracts the table of contents from a PyMuPDF document.

        Args:
            doc (pymupdf.Document): PyMuPDF Document object.

        Returns:
            list: Table of contents list from PyMuPDF.
        """
        toc = doc.get_toc() # Extract table of contents
        self.logger.log_info("Table of Contents extracted.", toc_entry_count=len(toc)) # Log TOC extraction
        return toc # Return TOC list


class PageParsingModule:
    """
    Parses individual PDF pages to extract text, tables, and images.
    """
    def __init__(self, config):
        """
        Initializes the PageParsingModule with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
        """
        self.config = config # Store config for use in this module and sub-modules
        self.logger = LogfireLogger(config=config) # Initialize LogfireLogger - SIMPLIFIED

    def parse_page_content(self, page, output_dir):
        """
        Parses a single PDF page and extracts relevant content.

        Args:
            page (pymupdf.Page): PyMuPDF Page object.
            output_dir (str): Directory to save output assets (e.g., images).

        Returns:
            str: Markdown content of the parsed page.
        """
        self.logger.log_info(f"Parsing page: {page.number + 1}", page_number=page.number + 1) # Log page parsing start
        page_markdown = f"## Page {page.number + 1}\n\n" # Initialize page markdown with header

        # Text Extraction
        text_extraction_module = TextExtractionModule(self.config) # Initialize TextExtractionModule with config
        text_content = text_extraction_module.extract_text_blocks(page) # Extract text blocks
        page_markdown += "### Text Content\n\n" + text_content + "\n\n" # Add text content to page markdown

        # Table Extraction
        table_extraction_module = TableExtractionModule(self.config) # Initialize TableExtractionModule with config
        tables_markdown = table_extraction_module.extract_tables_from_page(page) # Extract tables as Markdown
        if tables_markdown: # Check if tables were extracted
            page_markdown += "### Tables\n\n" # Add Tables section header if tables exist
            for table_md in tables_markdown: # Iterate through extracted tables
                page_markdown += table_md + "\n\n" # Add each table's markdown

        # Image Extraction
        image_extraction_module = ImageExtractionModule(self.config) # Initialize ImageExtractionModule with config
        image_links = image_extraction_module.extract_images_from_page(page, output_dir) # Extract images and get Markdown links
        if image_links: # Check if images were extracted
            page_markdown += "### Images\n\n" # Add Images section header if images exist
            for link in image_links: # Iterate through image links
                page_markdown += link + "\n" # Add each image link

        self.logger.log_debug(f"Page {page.number + 1} parsing complete.", page_number=page.number + 1) # Log page parsing completion
        return page_markdown # Return the Markdown content for the page


class TextExtractionModule:
    """
    Extracts text content from PDF pages using various strategies.
    """
    def __init__(self, config):
        """
        Initializes the TextExtractionModule with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
        """
        self.config = config.get('text_extraction_module', {}) # Get module specific config, default to empty dict
        self.logger = LogfireLogger(config=config) # Initialize LogfireLogger - SIMPLIFIED
        self.text_blocks_strategy = self.config.get('text_blocks_strategy', 'blocks_sorted') # Default strategy from YAML config


    def extract_text_blocks(self, page):
        """
        Extracts text blocks from a PDF page using PyMuPDF's get_text("blocks") method.

        Args:
            page (pymupdf.Page): PyMuPDF Page object.

        Returns:
            str: Markdown formatted text blocks.
        """
        blocks = page.get_text(self.text_blocks_strategy, sort=True) # Extract text blocks using strategy from config, sorted by reading order
        markdown_text = "" # Initialize markdown text
        for block in blocks: # Iterate through extracted blocks
            text = block[4] # Extract text content from block (item 5 in block tuple)
            markdown_text += text + "\n\n" # Append text and newlines to markdown
        self.logger.log_debug(f"Extracted text blocks using strategy: {self.text_blocks_strategy}", page_number=page.number + 1, strategy=self.text_blocks_strategy) # Debug log
        return markdown_text # Return Markdown text string


class TableExtractionModule:
    """
    Extracts tables from PDF pages using PyMuPDF's table finding functionality.
    """
    def __init__(self, config):
        """
        Initializes the TableExtractionModule with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
        """
        self.config = config.get('table_extraction_module', {}) # Get module specific config, default to empty dict
        self.logger = LogfireLogger(config=config) # Initialize LogfireLogger - SIMPLIFIED


    def extract_tables_from_page(self, page):
        """
        Extracts tables from a PDF page using PyMuPDF's find_tables method, configured by YAML.

        Args:
            page (pymupdf.Page): PyMuPDF Page object.

        Returns:
            list: List of Markdown formatted tables (strings).
        """
        table_config = self.config # Get table config from module config - directly from YAML
        tables = page.find_tables(**table_config) # Find tables using configuration from YAML
        tables_markdown = [] # Initialize list to store markdown tables

        for table in tables.tables: # Iterate through found tables
            markdown = table.to_markdown() # Convert table to Markdown format
            tables_markdown.append(markdown) # Add markdown table to list

        self.logger.log_debug(f"Extracted {len(tables_markdown)} tables.", page_number=page.number + 1, table_count=len(tables_markdown), strategy=table_config.get('strategy')) # Debug log
        return tables_markdown # Return list of Markdown tables


class ImageExtractionModule:
    """
    Extracts and saves images from PDF pages.
    """
    def __init__(self, config):
        """
        Initializes the ImageExtractionModule with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
        """
        self.config = config.get('image_extraction_module', {}) # Get module specific config, default to empty dict
        self.logger = LogfireLogger(config=config) # Initialize LogfireLogger - SIMPLIFIED
        self.image_format = self.config.get('image_format', 'png') # Image format from YAML config
        self.image_quality = self.config.get('image_quality', 90) # Image quality from YAML config
        self.output_subdirectory = self.config.get('output_subdirectory', 'assets/images') # Output subdirectory from YAML config


    def extract_images_from_page(self, page, output_dir):
        """
        Extracts images from a PDF page and saves them to the output directory.

        Args:
            page (pymupdf.Page): PyMuPDF Page object.
            output_dir (str): Directory to save output images.

        Returns:
            list: List of Markdown image links for extracted images.
        """
        image_list = page.get_images() # Get list of images on the page
        image_links = [] # Initialize list to store image links
        image_output_path = os.path.join(output_dir, self.output_subdirectory) # Construct image output path from config
        os.makedirs(image_output_path, exist_ok=True) # Ensure image output directory exists

        # Accessing image_format and image_quality from self.config for YAML configuration
        for img_index, img in enumerate(image_list, start=1): # Iterate through images
            xref = img[0] # get the XREF of the image
            base_image = doc.extract_image(xref) # Extract image data
            image_bytes = base_image["image"] # get the image bytes
            image_ext = base_image["ext"] # get the image extension, e.g. 'png', 'jpeg'
            image_filename = f"page_{page.number + 1}_image_{img_index}.{self.image_format}" # Construct image filename using format from config
            image_path = os.path.join(image_output_path, image_filename) # Construct full image path

            pix = pymupdf.Pixmap(doc, xref) # Make pixmap from image
            if pix.n - pix.alpha > 3: # Check and convert CMYK to RGB if needed
                pix = pymupdf.Pixmap(pymupdf.csRGB, pix) # Convert color space

            pix.save(image_path, format=self.image_format, quality=self.image_quality) # Save image with format and quality from config
            image_links.append(MarkdownOutputModule.create_markdown_image_link(image_filename, self.output_subdirectory)) # Create Markdown link and add to list
            pix = None # Release pixmap

        self.logger.log_debug(f"Extracted {len(image_links)} images.", page_number=page.number + 1, image_count=len(image_links), output_dir=image_output_path) # Debug log
        return image_links # Return list of Markdown image links


class MarkdownOutputModule:
    """
    Assembles and saves the final Markdown output.
    """
    def __init__(self, config):
        """
        Initializes the MarkdownOutputModule with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
        """
        self.config = config.get('output_module', {}) # Get module specific config, default to empty dict
        self.logger = LogfireLogger(config=config) # Initialize LogfireLogger - SIMPLIFIED
        self.markdown_filename_suffix = self.config.get('markdown_filename_suffix', '_parsed') # Filename suffix from YAML config
        self.asset_subdirectory = self.config.get('asset_subdirectory', 'assets') # Asset subdirectory from YAML config


    def assemble_markdown_output(self, document_metadata, table_of_contents, page_markdown_content):
        """
        Assembles the final Markdown output from different components.

        Args:
            document_metadata (dict): Document-level metadata dictionary.
            table_of_contents (str): Markdown representation of the table of contents.
            page_markdown_content (str): Combined Markdown content of all pages.

        Returns:
            str: Complete Markdown output string.
        """
        markdown_output = "" # Initialize markdown output string
        markdown_output += document_metadata # Add YAML frontmatter
        markdown_output += table_of_contents # Add Table of Contents
        markdown_output += page_markdown_content # Add page content
        return markdown_output # Return assembled markdown output


    def save_markdown_file(self, markdown_content, output_path):
        """
        Saves the Markdown content to a file in the specified output path.

        Args:
            markdown_content (str): Markdown content string.
            output_path (str): Path to save the output Markdown file.
        """
        try:
            with open(output_path, "w", encoding="utf-8") as f: # Open file for writing with UTF-8 encoding
                f.write(markdown_content) # Write markdown content to file
            self.logger.log_info(f"Markdown output saved to: {output_path}", output_path=output_path) # Log successful save
        except Exception as e: # Catch any exceptions during file saving
            self.logger.log_error(f"Error saving Markdown output to: {output_path} - {e}", output_path=output_path, exc_info=True) # Log error during save


    @staticmethod
    def create_markdown_image_link(image_filename, asset_subdirectory):
        """
        Creates a Markdown image link.

        Args:
            image_filename (str): Filename of the image.
            asset_subdirectory (str): Subdirectory where assets are stored.

        Returns:
            str: Markdown image link string.
        """
        return f"![Page Image](<{asset_subdirectory}/{image_filename}>)" # Return Markdown image link string


class MathNotationModule:
    """
    Detects and formats LaTeX math notations in text for Markdown output.
    """
    def __init__(self, config):
        """
        Initializes the MathNotationModule with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
        """
        self.config = config.get('math_notation_module', {}) # Get module specific config, default to empty dict
        self.logger = LogfireLogger(config=config) # Initialize LogfireLogger - SIMPLIFIED
        self.latex_display_delimiter = self.config.get('latex_display_delimiter', '$$') # Delimiter from YAML config
        self.latex_inline_delimiter = self.config.get('latex_inline_delimiter', '$') # Delimiter from YAML config


    def format_latex_in_markdown(self, text):
        """
        Formats LaTeX-like math notations in text to Markdown compatible format.

        Args:
            text (str): Input text string.

        Returns:
            str: Text with LaTeX notations formatted for Markdown.
        """
        # Basic regex-based LaTeX detection and formatting (can be enhanced)
        text = re.sub(r'(\$\$.*?\$\$)', r'\1', text, flags=re.DOTALL) # Wrap display equations in delimiters from config
        text = re.sub(r'(\$.*?\$)', r'\1', text) # Wrap inline equations in delimiters from config
        self.logger.log_debug("Formatted LaTeX notations in text.") # Debug log
        return text # Return text with formatted LaTeX


class CodeSnippetModule:
    """
    Detects and formats code snippets in text for Markdown output.
    """
    def __init__(self, config):
        """
        Initializes the CodeSnippetModule with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
        """
        self.config = config.get('code_snippet_module', {}) # Get module specific config, default to empty dict
        self.logger = LogfireLogger(config=config) # Initialize LogfireLogger - SIMPLIFIED
        self.code_fence_style = self.config.get('code_fence_style', '```') # Code fence style from YAML config


    def format_code_in_markdown(self, text):
        """
        Formats code snippets in text using Markdown code fences.

        Args:
            text (str): Input text string.

        Returns:
            str: Text with code snippets formatted for Markdown.
        """
        # Basic heuristic-based code detection and formatting (can be enhanced)
        lines = text.splitlines() # Split text into lines
        formatted_lines = [] # Initialize list for formatted lines
        in_code_block = False # Flag to track if inside code block

        code_fence = self.code_fence_style # Code fence style from YAML config - for cleaner code

        for line in lines: # Iterate through lines
            if line.strip().startswith(code_fence): # Check for existing code fences (using style from config)
                formatted_lines.append(line) # Append code fence lines as is
                in_code_block = not in_code_block # Toggle code block flag
            elif line.strip().startswith("#") and not in_code_block: # Heuristic: Python-style comments at start of line
                formatted_lines.append(f"{code_fence}python") # Start code fence with python language (using style from config)
                formatted_lines.append(line) # Append code line
                formatted_lines.append(code_fence) # End code fence (using style from config)
            elif len(line) > 40 and  " " not in line and not in_code_block: # Heuristic: Long lines with no spaces (potential code)
                formatted_lines.append(f"{code_fence}") # Start code fence (using style from config)
                formatted_lines.append(line) # Append code line
                formatted_lines.append(code_fence) # End code fence (using style from config)
            else:
                formatted_lines.append(line) # Append non-code lines as is

        formatted_text = "\n".join(formatted_lines) # Join lines back into text
        self.logger.log_debug("Formatted code snippets in text.") # Debug log
        return formatted_text # Return text with formatted code snippets
```

