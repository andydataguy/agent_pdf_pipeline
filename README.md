# Agent Data Platform: PDF Parsing Pipeline

## Overview

This document outlines the PDF parsing pipeline, a component of the Agent Data Platform, designed to extract structured information from PDF documents and convert it into Markdown format. This pipeline is built using PyMuPDF for PDF processing and Logfire for comprehensive observability. It is **fully configurable via a YAML file**, allowing for easy customization of parsing behavior and logging verbosity.

## Directory Structure

agent_pdf_pipeline/
├── .logfire/                  # Logfire credentials and configuration (ignored by Git)
├── .output/                   # Output directory for parsed Markdown and assets
├── Uploads/                   # Directory to place input PDF documents
│   └── samples/             # Example PDF samples
│       └── monolith_realtime_recommend.pdf
├── src/                       # Source code directory
│   ├── Chunking/              # (Future: Chunking modules)
│   ├── Enrichment/            # (Future: Enrichment modules)
│   ├── Processing/           # PDF Parsing modules
│   │   ├── pdf_to_markdown.py # Main PDF parsing script (modular pipeline)
│   │   └── pdf_parser_config.yaml # YAML configuration file for parsing pipeline
│   ├── Retrieval/             # (Future: Retrieval modules)
│   ├── Storage/               # (Future: Storage modules)
│   ├── Utils/                 # Utility modules
│   │   ├── Functions/
│   │   │   └── ARCHIVE/     # (Future: Archive functions)
│   │   │       └── ARHHIVE_pdf_parser.py
│   │   └── Logger/
│   │       └── logfire.py   # Generic Logfire logging template (copy-paste ready)
├── .env                       # Environment variables (e.g., Logfire token)
├── .gitignore                 # Git ignore file
├── .python-version            # Python version specification
├── README.md                  # This README file
├── main.py                    # Orchestration script to run the PDF parsing pipeline
├── pyproject.toml             # Project dependencies and build configuration
└── uv.lock                    # Dependency lock file

## Setup and Installation

1.  **Install Dependencies:**

    ```bash
    uv pip sync pyproject.toml
    ```
    *(Ensure you have `uv` installed. If not, install it with `pip install uv`)*

2.  **Configure Logfire (Optional):**

    *   If you intend to use Logfire for detailed logging, ensure you have set up a Logfire project and have your `LOGFIRE_TOKEN` available.
    *   Set the `LOGFIRE_TOKEN` environment variable in your `.env` file:
        ```env
        LOGFIRE_TOKEN=your_logfire_write_token
        ```
    *   If you don't have Logfire set up, you can still run the pipeline; logging will be output to the console based on the YAML configuration.

3.  **Configuration via YAML:**

    *   The parsing pipeline is **fully configured using `src/Processing/pdf_parser_config.yaml`**.
    *   **Modify this file to customize parsing behavior and logging verbosity without changing the code.**
    *   **Key Configuration Sections and Parameters:**
        *   **`pdf_parsing_module`:**
            *   `log_level`:  Sets the minimum log level for the `PDFParsingModule` itself. Choose from: `TRACE`, `DEBUG`, `INFO`, `NOTICE`, `WARN`, `ERROR`, `FATAL`. (Default: `INFO`).
        *   **`text_extraction_module`:**
            *   `text_blocks_strategy`:  Selects the text extraction strategy using `Page.get_text()`. Options: `blocks_sorted`, `words`, `dict`, `rawdict`, `html`, `xml`, `xhtml`, `text`. (Default: `blocks_sorted`).
            *   `text_formatting`:
                *   `bold_style`:  Markdown style for bold text (e.g., `**`, `__`). (Default: `**`).
                *   `italic_style`: Markdown style for italic text (e.g., `_`, `*`). (Default: `_`).
        *   **`table_extraction_module`:**
            *   `strategy`: Table detection strategy for `Page.find_tables()`. Options: `lines`, `lines_strict`, `text`. (Default: `lines`).
            *   `snap_tolerance`, `join_tolerance`, `intersection_tolerance`, `text_tolerance`, `edge_min_length`: Fine-tune table detection parameters (refer to PyMuPDF documentation for details).
        *   **`image_extraction_module`:**
            *   `image_format`: Output image format. Options: `png`, `jpeg`. (Default: `png`).
            *   `image_quality`: Image quality for JPEG (0-100, ignored for PNG). (Default: `90`).
            *   `output_subdirectory`: Subdirectory within the output folder to save images. (Default: `assets/images`).
        *   **`math_notation_module`:**
            *   `latex_display_delimiter`: Markdown delimiter for display LaTeX equations. (Default: `$$`).
            *   `latex_inline_delimiter`: Markdown delimiter for inline LaTeX equations. (Default: `$`).
        *   **`code_snippet_module`:**
            *   `code_fence_style`: Markdown code fence style. Options: ` ``` `, `~~~`. (Default: ` ``` `).
        *   **`logging_module`:**
            *   `console_log_level`:  Minimum log level for console output. Choose from: `TRACE`, `DEBUG`, `INFO`, `NOTICE`, `WARN`, `ERROR`, `FATAL`. (Default: `INFO`). **Use uppercase strings for log levels in YAML.**
            *   `logfire_enabled`: Enable sending logs to the Logfire platform (true/false). (Default: `true`).
        *   `output_module`:
            *   `markdown_filename_suffix`: Suffix appended to the output Markdown filename. (Default: `_parsed`).
            *   `asset_subdirectory`: Root subdirectory name for storing assets. (Default: `assets`).
    *   **Example Configuration Adjustments:**
        *   **To increase console log verbosity for debugging:** Change `logging_module.console_log_level` to `"DEBUG"`.
        *   **To experiment with table detection:** Modify parameters under `table_extraction_module` (e.g., `strategy`, `snap_tolerance`).
        *   **To change Markdown formatting:** Adjust `bold_style`, `italic_style`, or `code_fence_style` in `text_extraction_module` and `code_snippet_module`.

## How to Run the Pipeline

1.  **Place PDF Documents:** (Same as before)

2.  **Run `main.py`:** (Same as before)

3.  **Output Location:** (Same as before)

## Code Structure and Modules

*   **`main.py`:** Orchestration script that loads YAML configuration, initializes logging, and drives the PDF parsing process.
*   **`src/Processing/pdf_to_markdown.py`:** (Same as before, modular pipeline)
*   **`src/Utils/Logger/logfire.py`:** **Generic Logfire logging template (copy-paste ready) for use in any Python project.**
*   **`src/Processing/pdf_parser_config.yaml`:** YAML configuration file that **centrally controls all aspects of the parsing pipeline.**

## Observability with Logfire

*   (Same as before, Logfire integration details)
*   **YAML Configuration for Logging:** Log levels and Logfire platform integration are now configurable via the `logging_module` section in `pdf_parser_config.yaml`.

## Troubleshooting - KeyError: 'INFO'

If you encounter a `KeyError: 'INFO'` error, it indicates an issue with how the console log level is being configured within Logfire.

**Cause:**

The Logfire library's console exporter expects the `min_log_level` parameter in `ConsoleOptions` to be an **integer representation of the log level** (e.g., `logging.INFO`), not a string like `"INFO"`.

**Solution:**

1.  **Verify YAML Configuration:** Ensure that the `console_log_level` parameter in your `src/Processing/pdf_parser_config.yaml` file under the `logging_module` section is set to a **valid uppercase string representing a Python logging level**.  Valid options are: `"TRACE"`, `"DEBUG"`, `"INFO"`, `"NOTICE"`, `"WARN"`, `"ERROR"`, `"FATAL"`. **Make sure to use uppercase strings.**

    ```yaml
    logging_module:
      console_log_level: "INFO"  # Correct: Uppercase string
      logfire_enabled: true
    ```

2.  **Updated `logfire.py` Template:** The provided `src/Utils/Logger/logfire.py` template now includes logic to correctly handle string log levels from the YAML configuration and convert them to their integer equivalents using `logging` library constants. **Ensure you are using the updated `logfire.py` template.**

By following these steps and using the updated code and YAML configuration, you should resolve the `KeyError: 'INFO'` and have a fully functional and YAML-configurable PDF parsing pipeline with Logfire observability.

---

These are the updated files. Please replace your existing files with these new versions. After that, run `main.py` again to test if the `KeyError` is resolved and the pipeline is working as expected. Let me know how it goes!