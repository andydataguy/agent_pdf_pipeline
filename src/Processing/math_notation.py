import re

class MathNotation:
    """
    Detects and formats LaTeX math notations in text for Markdown output.
    """
    def __init__(self, config, logger):
        """
        Initializes the MathNotation with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
            logger (LogfireLogger): LogfireLogger instance for logging.
        """
        self.config = config.get('math_notation_module', {})
        self.logger = logger
        self.latex_display_delimiter = self.config.get('latex_display_delimiter', '$$')
        self.latex_inline_delimiter = self.config.get('latex_inline_delimiter', '$')

    def format_latex_in_markdown(self, text):
        """
        Formats LaTeX-like math notations in text to Markdown compatible format.

        Args:
            text (str): Input text string.

        Returns:
            str: Text with LaTeX notations formatted for Markdown.
        """
        self.logger.log_info("Processing LaTeX math notations in text")

        # Handle display math (block equations)
        display_pattern = re.compile(r'\$\$(.*?)\$\$', re.DOTALL)
        text = display_pattern.sub(lambda m: f"\n{self.latex_display_delimiter}{m.group(1)}{self.latex_display_delimiter}\n", text)

        # Handle inline math
        inline_pattern = re.compile(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)')
        text = inline_pattern.sub(lambda m: f"{self.latex_inline_delimiter}{m.group(1)}{self.latex_inline_delimiter}", text)

        return text
