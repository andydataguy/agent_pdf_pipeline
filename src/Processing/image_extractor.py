import os

class ImageExtractor:
    """
    Extracts and saves images from PDF pages.
    """
    def __init__(self, config, logger):
        """
        Initializes the ImageExtractor with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
            logger (LogfireLogger): LogfireLogger instance for logging.
        """
        self.config = config.get('image_extraction_module', {})
        self.logger = logger
        self.image_format = self.config.get('image_format', 'png')
        self.image_quality = self.config.get('image_quality', 90)
        self.output_subdirectory = self.config.get('output_subdirectory', 'assets/images')

    def extract_images_from_page(self, page, output_dir):
        """
        Extracts images from a PDF page and saves them to the output directory.

        Args:
            page (pymupdf.Page): PyMuPDF Page object.
            output_dir (str): Directory to save output images.

        Yields:
            str: Markdown image links for extracted images, one at a time.
        """
        self.logger.log_info(f"Extracting images from page {page.number + 1}", page_number=page.number + 1)
        image_list = page.get_images()

        if not image_list:
            self.logger.log_info("No images found on page", page_number=page.number + 1)
            return

        # Create output directory if it doesn't exist
        image_output_dir = os.path.join(output_dir, self.output_subdirectory)
        os.makedirs(image_output_dir, exist_ok=True)

        for img_idx, img in enumerate(image_list, 1):
            try:
                xref = img[0]  # Get image reference number
                base_image = page.parent.extract_image(xref)
                
                if base_image:
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image_filename = f"page_{page.number + 1}_image_{img_idx}.{self.image_format}"
                    image_path = os.path.join(image_output_dir, image_filename)

                    with open(image_path, "wb") as image_file:
                        image_file.write(image_bytes)

                    # Create relative path for Markdown link
                    relative_path = os.path.join(self.output_subdirectory, image_filename).replace("\\", "/")
                    yield f"![Image {img_idx} from page {page.number + 1}]({relative_path})\n\n"
                    self.logger.log_info(f"Saved image {img_idx} from page {page.number + 1}", 
                                       page_number=page.number + 1, 
                                       image_number=img_idx,
                                       image_path=image_path)

            except Exception as e:
                self.logger.log_error(f"Error extracting image {img_idx} from page {page.number + 1}: {str(e)}", 
                                    page_number=page.number + 1,
                                    image_number=img_idx,
                                    exc_info=True)
                continue
