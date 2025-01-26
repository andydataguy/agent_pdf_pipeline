import os
import yaml
import pathlib
import logging # Import the standard logging library
from src.Processing.pdf_to_markdown import PDFParsingModule  # Import PDFParsingModule
from src.Utils.Logger.logfire import LogfireLogger # Import LogfireLogger

def load_config(config_path="src/Processing/pdf_parser_config.yaml"):
    """
    Loads configuration from a YAML file.

    Args:
        config_path (str, optional): Path to the YAML configuration file. Defaults to "src/Processing/pdf_parser_config.yaml".

    Returns:
        dict: Configuration dictionary, or None if loading fails.
    """
    try:
        with open(config_path, 'r') as f: # Open and read YAML config file
            config = yaml.safe_load(f) # Load YAML data safely
            print(f"Configuration loaded from: {config_path}") # Inform user config is loaded
            return config # Return configuration dictionary
    except FileNotFoundError: # Handle file not found error
        print(f"Error: Configuration file not found at: {config_path}") # Print error message
        return None # Return None to indicate failure
    except yaml.YAMLError as e: # Handle YAML parsing errors
        print(f"Error parsing YAML configuration: {e}") # Print YAML parsing error
        return None # Return None to indicate failure


def main():
    """
    Main function to orchestrate PDF parsing and Markdown conversion.
    """
    config = load_config() # Load configuration from YAML file
    if not config: # Check if configuration loading failed
        print("Exiting due to configuration error.") # Inform user about config error
        return # Exit if config loading failed

    logger = LogfireLogger(config=config, project_name="agent-pdf-pipeline", service_name="main-orchestration", environment="development") # Initialize LogfireLogger

    pdf_path = "Uploads/samples/monolith_realtime_recommend.pdf" # Define input PDF path
    output_dir = ".output" # Define root output directory

    logger.log_info("Starting main PDF parsing process.", pdf_path=pdf_path, output_dir=output_dir) # Log start of main process

    output_path_dir = os.path.join(output_dir, pathlib.Path(pdf_path).stem) # Create output directory path based on PDF filename
    os.makedirs(output_path_dir, exist_ok=True) # Ensure output directory exists

    output_markdown_path = os.path.join(output_path_dir,  pathlib.Path(pdf_path).stem + config['output_module'].get('markdown_filename_suffix', '_parsed') + ".md") # Create Markdown output file path

    pdf_parsing_module = PDFParsingModule(config) # Initialize PDFParsingModule with configuration
    markdown_content = pdf_parsing_module.parse_pdf_document(pdf_path, output_path_dir) # Parse PDF document

    if markdown_content: # Check if markdown content was successfully generated
        markdown_output_module = MarkdownOutputModule(config) # Initialize MarkdownOutputModule with config
        markdown_output_module.save_markdown_file(markdown_content, output_markdown_path) # Save Markdown output to file
        logger.log_info("Markdown output successfully saved.", output_path=output_markdown_path) # Log successful output saving
    else:
        logger.log_warning("No Markdown output generated due to errors.", pdf_path=pdf_path) # Log warning if no markdown output


    logger.log_info("Main PDF parsing process completed.", pdf_path=pdf_path, output_dir=output_dir) # Log completion of main process


if __name__ == "__main__":
    main() # Execute main function when script is run