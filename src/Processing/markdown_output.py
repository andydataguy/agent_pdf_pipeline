import os

class MarkdownOutput:
    """
    Assembles and saves the final Markdown output.
    """
    def __init__(self, config, logger):
        """
        Initializes the MarkdownOutput with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
            logger (LogfireLogger): LogfireLogger instance for logging.
        """
        self.config = config.get('output_module', {})
        self.logger = logger
        self.markdown_filename_suffix = self.config.get('markdown_filename_suffix', '_parsed')
        self.asset_subdirectory = self.config.get('asset_subdirectory', 'assets')

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
        self.logger.log_info("Assembling final Markdown output")
        markdown_content = ""

        # Add metadata as YAML frontmatter if present
        if document_metadata:
            markdown_content += "---\n"
            for key, value in document_metadata.items():
                markdown_content += f"{key}: {value}\n"
            markdown_content += "---\n\n"

        # Add table of contents if present
        if table_of_contents:
            markdown_content += table_of_contents + "\n"

        # Add page content
        markdown_content += page_markdown_content

        return markdown_content

    def save_markdown_file(self, markdown_content, output_path):
        """
        Saves the Markdown content to a file in the specified output path.

        Args:
            markdown_content (str): Markdown content string.
            output_path (str): Path to save the output Markdown file.
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            self.logger.log_info(f"Markdown file saved successfully: {output_path}", output_path=output_path)
        except Exception as e:
            self.logger.log_error(f"Error saving Markdown file: {str(e)}", output_path=output_path, exc_info=True)
            raise

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
        relative_path = os.path.join(asset_subdirectory, image_filename).replace("\\", "/")
        return f"![{image_filename}]({relative_path})"
