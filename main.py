import os
import yaml
import pathlib
from src.Processing.pdf_parser import PDFParser
from src.Processing.markdown_output import MarkdownOutput
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

    # Initialize markdown output handler
    markdown_output = MarkdownOutput(config, logger)

    # Initialize and run PDF parsing
    try:
        pdf_parser = PDFParser(config)
        
        # Define output markdown path
        output_markdown_path = os.path.join(
            output_path_dir,
            pathlib.Path(pdf_path).stem + config['output_module'].get('markdown_filename_suffix', '_parsed') + ".md"
        )
        
        # Process PDF and write content incrementally
        with open(output_markdown_path, 'w', encoding='utf-8') as f:
            for content_chunk in pdf_parser.parse_pdf_document(pdf_path, output_path_dir):
                f.write(content_chunk)
                f.flush()  # Ensure content is written immediately
        
        logger.log_info("PDF processing completed successfully", 
                      output_path=output_markdown_path)
    except Exception as e:
        logger.log_error(f"Error during PDF processing: {str(e)}", 
                        pdf_path=pdf_path,
                        error_type=type(e).__name__)

if __name__ == "__main__":
    main()