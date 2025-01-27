import pymupdf
import yaml
from src.Utils.Logger.logfire import LogfireLogger
from .metadata_extractor import MetadataExtractor
from .page_parser import PageParser

class PDFParser:
    """
    Orchestrates the PDF parsing process, leveraging sub-modules for element extraction.
    """

    def __init__(self, config):
        """
        Initializes the PDFParser with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
        """
        self.config = config.get('pdf_parsing_module', {})
        self.logger = LogfireLogger(config=config)

    def parse_pdf_document(self, pdf_path, output_dir):
        """
        Parses a PDF document and yields structured Markdown content.

        Args:
            pdf_path (str): Path to the input PDF file.
            output_dir (str): Directory to save output Markdown and assets.

        Yields:
            str: Markdown content chunks of the document.
        """
        self.logger.log_info(f"Starting PDF parsing for: {pdf_path}", pdf_path=pdf_path)

        try:
            doc = pymupdf.open(pdf_path)
            self.logger.log_info(f"Document loaded successfully: {pdf_path}", pdf_path=pdf_path, page_count=doc.page_count)

            # Metadata Extraction
            metadata_extractor = MetadataExtractor(self.config, self.logger)
            document_metadata = metadata_extractor.extract_document_metadata(doc)
            yield self._assemble_yaml_frontmatter(document_metadata)

            # Table of Contents Extraction
            table_of_contents = metadata_extractor.extract_table_of_contents(doc)
            yield self._format_table_of_contents_markdown(table_of_contents)

            # Page Parsing and Content Extraction
            page_parser = PageParser(self.config, self.logger)
            for page in doc:
                yield from page_parser.parse_page_content(page, output_dir)
                self.logger.log_info(f"Page {page.number + 1} parsed.", pdf_path=pdf_path, page_number=page.number + 1)

            doc.close()
            self.logger.log_info(f"PDF parsing completed successfully: {pdf_path}", pdf_path=pdf_path)

        except FileNotFoundError:
            self.logger.log_error(f"File not found: {pdf_path}", pdf_path=pdf_path, exc_info=True)
            return

        except RuntimeError as e:
            self.logger.log_error(f"Error processing PDF: {pdf_path} - {e}", pdf_path=pdf_path, exc_info=True)
            return

        except Exception as e:
            self.logger.log_error(f"Unexpected error during PDF parsing: {pdf_path} - {e}", pdf_path=pdf_path, exc_info=True)
            return

    def _assemble_yaml_frontmatter(self, metadata):
        """
        Assembles YAML frontmatter from document metadata.

        Args:
            metadata (dict): Dictionary of document metadata.

        Returns:
            str: YAML frontmatter string.
        """
        yaml_str = "---\n"
        yaml_str += yaml.dump(metadata, indent=2)
        yaml_str += "---\n\n"
        return yaml_str

    def _format_table_of_contents_markdown(self, toc):
        """
        Formats the table of contents into a Markdown list.

        Args:
            toc (list): Table of contents data from PyMuPDF.

        Returns:
            str: Markdown representation of the table of contents.
        """
        if not toc:
            return ""

        markdown_toc = "## Table of Contents\n\n"
        for level, title, page_num in toc:
            indent = "  " * (level - 1)
            markdown_toc += f"{indent}- [{title}](#page-{page_num})\n"
        markdown_toc += "\n"
        return markdown_toc
