# Agent Data Platform: PDF Parsing Pipeline

## Overview

This document outlines the PDF parsing pipeline, a component of the Agent Data Platform, designed to extract structured information from PDF documents and convert it into Markdown format. This pipeline is built using PyMuPDF for PDF processing and Logfire for comprehensive observability. It is configured via a YAML file, allowing for easy customization of parsing behavior.

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
│   │       └── logfire.py   # Simplified Logfire logging module
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

    *   The parsing pipeline is configured using `src/Processing/pdf_parser_config.yaml`.
    *   **Modify this file to customize parsing behavior without changing the code.**
    *   **Key Configuration Sections:**
        *   `pdf_parsing_module`:  General logging level for the PDF parsing process.
        *   `text_extraction_module`:  Controls text extraction strategies and Markdown formatting for text.
        *   `table_extraction_module`:  Configures table detection parameters for PyMuPDF's table finder.
        *   `image_extraction_module`:  Sets image output format, quality, and subdirectory.
        *   `math_notation_module`:  Defines delimiters for LaTeX mathematical notations.
        *   `code_snippet_module`:  Controls code block formatting.
        *   `logging_module`:  Configures console logging level and Logfire integration.
        *   `output_module`:  Sets output filename suffixes and asset subdirectory names.
    *   **Refer to the comments within `src/Processing/pdf_parser_config.yaml` for detailed descriptions of each parameter and available options.**

## How to Run the Pipeline

1.  **Place PDF Documents:**

    *   Put the PDF documents you want to parse into the `Uploads/samples/` directory or create new subdirectories within `Uploads/` for better organization (e.g., `Uploads/beginner/`, `Uploads/advanced/`).

2.  **Run `main.py`:**

    ```bash
    python main.py
    ```

    *   Currently, `main.py` is configured to process the sample PDF: `Uploads/samples/monolith_realtime_recommend.pdf`.
    *   To process a different PDF, modify the `pdf_path` variable in the `main()` function of `main.py`.
    *   *(Future Enhancement: Command-line argument to specify PDF path directly)*

3.  **Output Location:**

    *   Parsed Markdown files and extracted assets will be saved in the `.output` directory.
    *   For each PDF processed, a new folder will be created in `.output/`, named after the PDF file (without extension).
    *   The Markdown file (`[pdf_filename]_parsed.md`) will be located directly in this folder.
    *   Extracted images will be placed in the `assets/images/` subdirectory within the PDF-specific output folder.

## Code Structure and Modules

*   **`main.py`:** Orchestration script that loads configuration, initializes logging, and drives the PDF parsing process.
*   **`src/Processing/pdf_to_markdown.py`:** Contains the core PDF parsing pipeline, modularized into classes for different functionalities:
    *   `PDFParsingModule`: Orchestrates the overall parsing workflow.
    *   `MetadataExtractionModule`: Extracts document-level metadata and TOC.
    *   `PageParsingModule`: Parses individual pages and coordinates element extraction.
    *   `TextExtractionModule`: Extracts text content from pages.
    *   `TableExtractionModule`: Extracts tables from pages.
    *   `ImageExtractionModule`: Extracts images from pages.
    *   `MarkdownOutputModule`: Assembles and saves the final Markdown output.
    *   `MathNotationModule`: Formats LaTeX notations in Markdown.
    *   `CodeSnippetModule`: Formats code snippets in Markdown.
*   **`src/Utils/Logger/logfire.py`:**  Encapsulates Logfire logging functionalities for consistent and structured logging throughout the pipeline. **SIMPLIFIED TEMPLATE - Project and service identification now external.**
*   **`src/Processing/pdf_parser_config.yaml`:** YAML configuration file that controls the behavior of the parsing pipeline, allowing users to customize parameters without modifying the code.

## Observability with Logfire

*   The pipeline is instrumented with Logfire for detailed logging and tracing.
*   Log messages are output to the console and, if configured, sent to the Logfire platform.
*   Spans are used to track the execution flow of the pipeline, providing insights into processing time and potential bottlenecks.
*   Log levels and Logfire integration are configurable via the `logging_module` section in `pdf_parser_config.yaml`.
*   Utilize the Logfire Web UI (if enabled) to explore traces, analyze performance, and debug issues.

## YAML Configuration for Customization

*   **Edit `src/Processing/pdf_parser_config.yaml` to customize the pipeline.**
*   **No Code Changes Required for Configuration Adjustments.**
*   **Example Customizations:**
    *   Change text extraction strategy (`text_extraction_module.text_blocks_strategy`).
    *   Adjust table detection parameters (`table_extraction_module` section).
    *   Modify image output format and quality (`image_extraction_module` section).
    *   Control console log verbosity and enable/disable Logfire cloud logging (`logging_module` section).
    *   Customize Markdown output styles (e.g., bold/italic styles, code fence style in `text_extraction_module` and `code_snippet_module`).

## Next Steps

*   Run the pipeline with the sample `monolith_realtime_recommend.pdf` document and examine the output in the `.output` directory.
*   Experiment with different configurations by modifying `src/Processing/pdf_parser_config.yaml` and observe the changes in parsing behavior and output.
*   Explore the Logfire Web UI (if enabled) to analyze the logs and traces generated during pipeline execution.
*   Begin integrating the parsed Markdown output into your multi-agent system and knowledge base.
*   Continuously refine and extend the pipeline by adding new features, modules, and configurations as needed.

This README provides a starting point for understanding and using the YAML-configurable PDF parsing pipeline. Remember to consult the comments within `src/Processing/pdf_parser_config.yaml` for detailed parameter descriptions and customization options.