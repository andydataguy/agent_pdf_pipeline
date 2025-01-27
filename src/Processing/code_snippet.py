import re

class CodeSnippet:
    """
    Detects and formats code snippets in text for Markdown output.
    """
    def __init__(self, config, logger):
        """
        Initializes the CodeSnippet with a configuration dictionary.

        Args:
            config (dict): Configuration dictionary loaded from YAML.
            logger (LogfireLogger): LogfireLogger instance for logging.
        """
        self.config = config.get('code_snippet_module', {})
        self.logger = logger
        self.code_fence_style = self.config.get('code_fence_style', '```')

    def format_code_in_markdown(self, text):
        """
        Formats code snippets in text using Markdown code fences.

        Args:
            text (str): Input text string.

        Returns:
            str: Text with code snippets formatted for Markdown.
        """
        self.logger.log_info("Processing code snippets in text")

        # Pattern for code blocks with language specification
        code_block_pattern = re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL)
        text = code_block_pattern.sub(self._format_code_block, text)

        # Pattern for inline code
        inline_code_pattern = re.compile(r'`([^`]+)`')
        text = inline_code_pattern.sub(r'`\1`', text)

        return text

    def _format_code_block(self, match):
        """
        Formats a code block with proper fencing and language specification.

        Args:
            match: Regular expression match object.

        Returns:
            str: Formatted code block.
        """
        language = match.group(1) or ''
        code = match.group(2).strip()
        return f"{self.code_fence_style}{language}\n{code}\n{self.code_fence_style}"
