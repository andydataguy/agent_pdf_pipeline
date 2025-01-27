class TextExtractor:
    """
    Extracts text content from PDF pages using various strategies.
    """
    def __init__(self, config, logger):
        """
        Initializes the TextExtractor with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
            logger (LogfireLogger): LogfireLogger instance for logging.
        """
        self.config = config.get('text_extraction_module', {})
        self.logger = logger
        self.text_blocks_strategy = self.config.get('text_blocks_strategy', 'blocks_sorted')

    def extract_text_blocks(self, page):
        """
        Extracts text blocks from a PDF page using PyMuPDF's get_text("blocks") method.

        Args:
            page (pymupdf.Page): PyMuPDF Page object.

        Yields:
            str: Markdown formatted text blocks, one at a time.
        """
        self.logger.log_info(f"Extracting text blocks from page {page.number + 1}", page_number=page.number + 1)
        blocks = page.get_text("blocks")
        
        if not blocks:
            self.logger.log_info("No text blocks found on page", page_number=page.number + 1)
            return

        for block in blocks:
            text = block[4].strip()  # Text content is at index 4
            if text:
                yield text + "\n\n"
