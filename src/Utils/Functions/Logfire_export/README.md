# Logfire Error Log Export Utility

## Overview

This utility, `logfire_export.py`, is a Python script designed to export error logs from your Logfire project using the Logfire Query API. It allows you to retrieve structured error data from Logfire and save it to a JSON file for local analysis and debugging.

**Note:** This version of the utility uses a simplified SQL query that **does not include time range filtering**. Time range filtering is temporarily disabled to ensure basic error log export functionality. We will investigate and re-enable time range filtering in a later iteration.

## Files

*   **`logfire_export.py`**: The main Python script that performs the Logfire API query and data export.
*   **`logfire_export_config.yaml`**: A YAML configuration file containing settings for the script, such as output directory, and log level filter. **Important: This file should NOT contain your Logfire Read Token directly.  See "Security: API Token" below.**
*   **`README.md`**: This documentation file, providing instructions on how to use the utility.

## Prerequisites

*   **Python 3.x**:  Make sure you have Python 3.x installed on your system.
*   **`requests` library**: Install the `requests` library for making HTTP requests. You can install it using pip:
    ```bash
    pip install requests
    ```
*   **`PyYAML` library**: Install the `PyYAML` library for parsing YAML configuration files. You can install it using pip:
    ```bash
    pip install pyyaml
    ```
*   **Logfire Read Token**: You need a Logfire Read Token to authenticate with the Logfire API. You can create one from your Logfire project settings in the Logfire web UI (see previous instructions on generating read tokens).

## Security: API Token

**IMPORTANT SECURITY NOTE:**

**Do NOT store your Logfire Read Token directly in the `logfire_export_config.yaml` file!**  API tokens, even read-only ones, should be treated as sensitive credentials and kept out of version control.

**Instead, set your Logfire Read Token as an environment variable named `LOGFIRE_READ_TOKEN`.**

**How to set environment variables (examples):**

*   **Linux/macOS:**
    *   Open your terminal's configuration file (e.g., `.bashrc`, `.zshrc`, `.bash_profile`).
    *   Add the following line, replacing `<YOUR_LOGFIRE_READ_TOKEN>` with your actual token:
        ```bash
        export LOGFIRE_READ_TOKEN="<YOUR_LOGFIRE_READ_TOKEN>"
        ```
    *   Save the file and source it in your terminal: `source ~/.bashrc` (or the name of your config file).

*   **Windows (Command Prompt):**
    ```bash
    setx LOGFIRE_READ_TOKEN "<YOUR_LOGFIRE_READ_TOKEN>"
    ```
    (Note: This command may require administrative privileges.  You may need to restart your command prompt for the variable to be available.)

*   **Windows (PowerShell):**
    ```powershell
    $env:LOGFIRE_READ_TOKEN = "<YOUR_LOGFIRE_READ_TOKEN>"
    ```
    (Note: This command sets the variable for the current session only. To make it persistent, use `setx` from Command Prompt or set it via System Environment Variables in Control Panel.)

**After setting the environment variable, leave the `logfire_read_token` line in `logfire_export_config.yaml` commented out or remove it entirely.**

## Configuration

Before running the script, you need to configure it using the `logfire_export_config.yaml` file.

1.  **Open `src/Utils/Functions/logfire_export/logfire_export_config.yaml` in a text editor.**

2.  **Edit the following parameters:**

    *   **`output_directory`**: (Optional)  Specify the directory where you want to save the exported JSON file. The default value is `"logfire_export_output"`, which will create a directory named `logfire_export_output` in the same location where you run the script.
    *   **`output_filename`**: (Optional)  Specify the filename for the exported JSON file. The default value is `"logfire_errors.json"`.
    *   **`time_range`**: (Parameter currently disabled) Time range for querying errors from Logfire.  **Note:** This parameter is currently not used in the simplified SQL query in `logfire_export.py`. Time range filtering will be re-enabled in a future version.
    *   **`log_level_filter`**: (Optional)  Set the minimum log level to filter for.  The script will export logs with this level and above (more severe levels).  Valid values are (case-insensitive):
        *   `"error"`:   Exports only error and fatal logs (default).
        *   `"warn"`:    Exports warning, error, and fatal logs.
        *   `"notice"`:  Exports notice, warn, error, and fatal logs.
        *   `"info"`:    Exports info, notice, warn, error, and fatal logs.
        *   `"debug"`:   Exports debug, info, notice, warn, error, and fatal logs.
        *   `"trace"`:   Exports all log levels (trace, debug, info, notice, warn, error, fatal).

3.  **Save the `logfire_export_config.yaml` file.**

## How to Run the Utility

1.  **Ensure you have set the `LOGFIRE_READ_TOKEN` environment variable** as described in the "Security: API Token" section above.

2.  **Open your terminal or command prompt.**

3.  **Navigate to the `src/Utils/Functions/logfire_export` directory** where you saved the `logfire_export.py` and `logfire_export_config.yaml` files.

4.  **Run the script using the Python interpreter:**
    ```bash
    python logfire_export.py
    ```

5.  **Check the output:**
    *   The script will print messages to the console indicating the configuration file being loaded, the Logfire API query being executed, and the output file being created.
    *   If successful, it will print a message like:  `Successfully exported Logfire errors to: logfire_export_output/logfire_errors.json` (or your configured output path).
    *   If there are errors (e.g., missing read token, API errors), error messages will be printed to the console.

6.  **Locate the output file:**
    *   The exported Logfire error logs will be saved in a JSON file named `logfire_errors.json` (or your configured `output_filename`) within the `logfire_export_output` directory (or your configured `output_directory`).

## Analyzing the Output JSON File

The exported JSON file (`logfire_errors.json`) will contain a structured representation of your Logfire error logs. You can open this file with a text editor, JSON viewer, or programmatically process it in Python or other tools.

The JSON data will be a list of dictionaries, where each dictionary represents a single log entry (or span, as Logfire uses a unified table). Each dictionary will contain keys corresponding to the columns in your Logfire `records` table, including:

*   `start_timestamp`: Timestamp when the event started.
*   `created_at`: Timestamp when the event was recorded.
*   `trace_id`:  Trace ID for correlating related events.
*   `span_id`:  Span ID for the specific operation.
*   `parent_span_id`:  Parent Span ID (for nested operations).
*   `level`:  Log level (e.g., 17 for "error").
*   `span_name`:  Name of the span or log.
*   `message`:  The log message text.
*   `attributes`:  A JSON object containing structured attributes associated with the log/span, providing valuable context.
*   `is_exception`: Boolean indicating if an exception occurred in the span.
*   `otel_status_code`: OpenTelemetry status code.
*   `otel_status_message`: OpenTelemetry status message.
    ... (and other columns from the `records` table).

By examining this structured JSON data, you can gain a more detailed understanding of the errors occurring in your PDF pipeline.

---

**Regarding alternative output formats and token efficiency:**

*   **Logfire API Response Formats:**  Yes!  The Logfire Query API *does* support other output formats besides JSON, as you can see in the documentation!  It supports:
    *   **JSON (default):**  You are currently using this. It's very readable and flexible for programmatic processing in Python, but can be verbose and less token-efficient.
    *   **Apache Arrow (`application/vnd.apache.arrow.stream`):** This is a **highly efficient, binary format** designed for columnar data and data analysis. It's excellent for performance and reducing data size, and is ideal if you intend to process the logs programmatically using tools that understand Arrow (like Pandas or Polars DataFrames, which Logfire also supports in its Python client!).  **This would be the most token-efficient option.**
    *   **CSV (`text/csv`):**  Comma-Separated Values format.  This is a plain text, tabular format, also more compact than JSON and easily readable by many tools.

*   **Token Efficiency:**  **Apache Arrow is definitely the most token-efficient format.** It's a binary format, so it's much smaller than text-based formats like JSON or CSV. If you are concerned about token usage when feeding the exported logs to a language model, Arrow would be the best choice. CSV would be a step up from JSON in terms of token efficiency, but still not as good as Arrow.

**To use Apache Arrow output format:**

1.  **Install `pyarrow`:** You'll need the `pyarrow` Python library to work with Arrow data in Python. If you don't have it already, install it:
    ```bash
    pip install pyarrow
    ```

2.  **Modify `logfire_export.py`:**
    *   **Change the `Accept` header:**  In the `headers` dictionary in `logfire_export.py`, change the `Accept` header to:
        ```python
        "Accept": "application/vnd.apache.arrow.stream", # Request Arrow response
        ```
    *   **Update the response processing:**  You'll need to change how you handle the API response because it will no longer be JSON.  You'll receive binary Arrow data.  You can use `pyarrow` and `polars` (which you already have installed) to read and process this data.  Here's an example of how to modify the `try` block in `export_logfire_errors` to handle Arrow output and load it into a Polars DataFrame (which is very efficient for tabular data):

        ```python
        try:
            response = requests.get(api_url, headers=headers, params=params, stream=True) # <-- Add stream=True for binary data
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            import pyarrow as pa
            import pyarrow.flight
            import polars as pl

            # Read Arrow stream from response content
            arrow_data_stream = pa.ipc.open_stream(response.content)
            errors_data_df = pl.read_ipc(arrow_data_stream) # Load into Polars DataFrame

            # Now you have a Polars DataFrame 'errors_data_df' containing your log data in Arrow format
            print("\nExported Logfire errors (Arrow format, Polars DataFrame):")
            print(errors_data_df) # Print DataFrame (optional - remove for large datasets)


            output_path_arrow = os.path.splitext(output_path)[0] + ".arrow" # Change output extension to .arrow
            pl.write_ipc(errors_data_df, output_path_arrow, compression="lz4") # Save as Arrow file
            print(f"Successfully exported Logfire errors to: {output_path_arrow} (Arrow format)")


        except requests.exceptions.RequestException as e:
            print(f"Error querying Logfire API: {e}")
        except Exception as e: # Catch other potential errors (Arrow parsing, etc.)
            print(f"Error processing Logfire API response: {e}")
            if 'response' in locals(): # Check if response object exists before accessing .text
                print(f"Response text: {response.text}") # Print raw response text for debugging

        ```

        **Important Notes for Arrow Implementation:**

        *   **`stream=True` in `requests.get()`:**  When dealing with binary data like Arrow, it's important to add `stream=True` to your `requests.get()` call. This tells `requests` to stream the response content instead of loading it all into memory at once, which is more efficient for potentially large Arrow datasets.
        *   **Error Handling:** I've added a more general `except Exception as e:` block to catch potential errors during Arrow parsing or DataFrame creation.  I've also included a check to print `response.text` in case of errors, which can be helpful for debugging API response issues.
        *   **Output Filename Extension:** I've changed the output filename extension to `.arrow` to indicate that you are now saving an Arrow file.
        *   **`pl.write_ipc(...)`:**  I'm using `pl.write_ipc()` from the `polars` library to efficiently save the Arrow DataFrame to an Arrow file.  I've added `compression="lz4"` for potential file size reduction (LZ4 is a fast compression algorithm).

**To switch back to JSON output:** Simply revert the changes to the `Accept` header and the response processing code in `logfire_export.py`.

**Choose Your Output Format:**

*   **For immediate debugging and human-readability: Stick with JSON.** It's easier to inspect the `logfire_errors.json` file directly in a text editor or JSON viewer.
*   **For token efficiency and programmatic processing (e.g., feeding to a language model): Use Apache Arrow.**  This will generate a `.arrow` file which is smaller and more efficient to parse programmatically using Polars or other Arrow-compatible tools.

Let me know if you want to proceed with implementing the Arrow output format. If you just want to get the error logs exported in *any* format right now to debug the PyMuPDF issue, sticking with the simplified JSON output is perfectly fine for now!