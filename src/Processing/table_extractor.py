class TableExtractor:
    """
    Extracts tables from PDF pages using PyMuPDF's table finding functionality.
    """
    def __init__(self, config, logger):
        """
        Initializes the TableExtractor with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
            logger (LogfireLogger): LogfireLogger instance for logging.
        """
        self.config = config.get('table_extraction_module', {})
        self.logger = logger

    def extract_tables_from_page(self, page):
        """
        Extracts tables from a PDF page using PyMuPDF's find_tables method, configured by YAML.

        Args:
            page (pymupdf.Page): PyMuPDF Page object.

        Yields:
            str: Markdown formatted table strings, one at a time.
        """
        self.logger.log_info(f"Extracting tables from page {page.number + 1}", page_number=page.number + 1)
        tables = page.find_tables()

        if not tables:
            self.logger.log_info("No tables found on page", page_number=page.number + 1)
            return

        for table_idx, table in enumerate(tables, 1):
            markdown_table = self._convert_table_to_markdown(table, table_idx)
            if markdown_table:
                yield markdown_table + "\n\n"

    def _convert_table_to_markdown(self, table, table_idx):
        """
        Converts a PyMuPDF table object to Markdown format.

        Args:
            table (pymupdf.Table): PyMuPDF Table object.
            table_idx (int): Index of the table on the page.

        Returns:
            str: Markdown formatted table string.
        """
        if not table.cells:
            return ""

        markdown_table = f"#### Table {table_idx}\n\n"
        
        # Calculate column widths
        col_widths = [0] * len(table.cells[0])
        for row in table.cells:
            for col_idx, cell in enumerate(row):
                # Handle both string and float cell content
                cell_text = str(cell.text) if hasattr(cell, 'text') else str(cell)
                col_widths[col_idx] = max(col_widths[col_idx], len(cell_text.strip()))

        # Create header row
        header_row = "|"
        separator_row = "|"
        for width in col_widths:
            header_row += " " + "-" * width + " |"
            separator_row += " " + "-" * width + " |"

        markdown_table += header_row + "\n" + separator_row + "\n"

        # Create data rows
        for row in table.cells:
            markdown_row = "|"
            for col_idx, cell in enumerate(row):
                # Handle both string and float cell content
                cell_text = str(cell.text) if hasattr(cell, 'text') else str(cell)
                text = cell_text.strip()
                padding = " " * (col_widths[col_idx] - len(text))
                markdown_row += f" {text}{padding} |"
            markdown_table += markdown_row + "\n"

        return markdown_table
