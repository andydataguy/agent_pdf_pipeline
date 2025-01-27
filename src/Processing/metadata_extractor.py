from src.Utils.Logger.logfire import LogfireLogger

class MetadataExtractor:
    """
    Extracts document-level metadata and table of contents from PDF documents.
    """
    def __init__(self, config, logger):
        """
        Initializes the MetadataExtractor with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
            logger (LogfireLogger): LogfireLogger instance for logging.
        """
        self.config = config
        self.logger = logger

    def extract_document_metadata(self, doc):
        """
        Extracts document metadata using PyMuPDF.

        Args:
            doc (pymupdf.Document): PyMuPDF Document object.

        Returns:
            dict: Dictionary containing document metadata.
        """
        metadata = doc.metadata if doc.metadata else {}
        self.logger.log_info("Document metadata extracted.", metadata_keys=list(metadata.keys()))
        return metadata

    def extract_table_of_contents(self, doc):
        """
        Extracts the table of contents from a PyMuPDF document.

        Args:
            doc (pymupdf.Document): PyMuPDF Document object.

        Returns:
            list: Table of contents list from PyMuPDF.
        """
        toc = doc.get_toc()
        self.logger.log_info("Table of Contents extracted.", toc_entry_count=len(toc))
        return toc
