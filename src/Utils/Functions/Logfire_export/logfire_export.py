import requests
import yaml
import os
import json
from dotenv import load_dotenv

def load_config(config_path="C:/Users/Anand/Documents/Code Projects/agent_data_platform/experiments/agent_pdf_pipeline/src/Utils/Functions/Logfire_export/logfire_export_config.yaml"):
    """
    Loads configuration from a YAML file.

    Args:
        config_path (str, optional): Path to the YAML configuration file.
                                     Defaults to "logfire_export_config.yaml".

    Returns:
        dict: Configuration dictionary, or None if loading fails.
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            print(f"Configuration loaded from: {config_path}")
            return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found at: {config_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML configuration: {e}")
        return None

def export_logfire_errors(config):
    """
    Exports Logfire error logs to a JSON file based on the provided configuration.

    Args:
        config (dict): Configuration dictionary containing Logfire API details and query parameters.
    """

    load_dotenv() # Load environment variables from .env file
    logfire_read_token = os.environ.get("LOGFIRE_READ_TOKEN") # Get token from environment variable
    
    # Set default output directory to .notes
    default_output_dir = "C:/Users/Anand/Documents/Code Projects/agent_data_platform/experiments/agent_pdf_pipeline/.notes"
    output_dir = config.get("output_directory", default_output_dir).replace("\\", "/") # Default output directory
    
    # If the config specifies a relative path, make it relative to the .notes directory
    if not os.path.isabs(output_dir):
        output_dir = os.path.join(default_output_dir, output_dir).replace("\\", "/")
        
    output_filename = config.get("output_filename", "logfire_errors.json") # Default output filename
    log_level_filter = config.get("log_level_filter", "error") # Default log level filter

    if not logfire_read_token:
        print("Error: Logfire read token is missing. Please set the LOGFIRE_READ_TOKEN environment variable.")
        return

    output_path = os.path.join(output_dir, output_filename)
    os.makedirs(output_dir, exist_ok=True) # Create output directory if it doesn't exist

    api_url = "https://logfire-api.pydantic.dev/v1/query"
    headers = {
        "Authorization": f"Bearer {logfire_read_token}",
        "Accept": "application/json", # Request JSON response - Defaulting to JSON for now
    }

    # --- SIMPLIFIED SQL QUERY (Time range removed for now) ---
    sql_query = f"""
    SELECT *
    FROM records
    WHERE level >= level_num('{log_level_filter}')
    LIMIT 100  -- Limiting to 100 errors for now
    """

    params = {"sql": sql_query}

    print(f"Querying Logfire API for the latest 100 {log_level_filter} or higher level logs...") # Updated message
    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        errors_data = response.json()


        with open(output_path, 'w') as outfile:
            json.dump(errors_data, outfile, indent=4) # Pretty JSON output

        print(f"Successfully exported Logfire errors to: {output_path}")


    except requests.exceptions.RequestException as e:
        print(f"Error querying Logfire API: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response from Logfire API: {e}")
        print(f"Response text: {response.text}") # Print the raw response text for debugging

if __name__ == "__main__":
    config = load_config()
    if config:
        export_logfire_errors(config)
    else:
        print("Aborting Logfire export due to configuration error.")