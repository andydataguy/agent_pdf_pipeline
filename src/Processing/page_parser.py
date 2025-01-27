from src.Utils.Logger.logfire import LogfireLogger
from .text_extractor import TextExtractor
from .table_extractor import TableExtractor
from .image_extractor import ImageExtractor

class PageParser:
    """
    Parses individual PDF pages to extract text, tables, and images.
    """
    def __init__(self, config, logger):
        """
        Initializes the PageParser with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
            logger (LogfireLogger): LogfireLogger instance for logging.
        """
        self.config = config
        self.logger = logger

    def parse_page_content(self, page, output_dir):
        """
        Parses a single PDF page and extracts relevant content.

        Args:
            page (pymupdf.Page): PyMuPDF Page object.
            output_dir (str): Directory to save output assets (e.g., images).

        Returns:
            str: Markdown content of the parsed page.
        """
        self.logger.log_info(f"Parsing page: {page.number + 1}", page_number=page.number + 1)
        page_markdown = f"## Page {page.number + 1}\n\n"

        # Text Extraction
        text_extractor = TextExtractor(self.config, self.logger)
        text_content = text_extractor.extract_text_blocks(page)
        page_markdown += "### Text Content\n\n" + text_content + "\n\n"

        # Table Extraction
        table_extractor = TableExtractor(self.config, self.logger)
        tables_markdown = table_extractor.extract_tables_from_page(page)
        if tables_markdown:
            page_markdown += "### Tables\n\n"
            for table_md in tables_markdown:
                page_markdown += table_md + "\n\n"

        # Image Extraction
        image_extractor = ImageExtractor(self.config, self.logger)
        image_links = image_extractor.extract_images_from_page(page, output_dir)
        if image_links:
            page_markdown += "### Images\n\n"
            for link in image_links:
                page_markdown += link + "\n\n"

        return page_markdown
