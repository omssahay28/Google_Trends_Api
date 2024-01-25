### Project Readme

## Google Trends Data Visualization Project

### Overview

This project is designed to retrieve and visualize Google Trends data for specified keywords and locations. It utilizes the `serpapi` library to interact with the Google Trends API, and the results are presented in a time-series plot. Additionally, the data is saved in an Excel file along with the plot for further analysis.

### Prerequisites

1. Python 3.x
2. Required Python packages (install using `pip install -r requirements.txt`):
   - pandas
   - matplotlib
   - serpapi
   - python-dotenv

### Getting Started

1. Clone the repository to your local machine.
2. Create a virtual environment (optional but recommended).
3. Install the required packages using `pip install -r requirements.txt`.
4. Obtain a Google Trends API key and set it in the `.env` file. You can create a `.env` file in the project root with the following content:

   ```
   serp_api_key=your_google_trends_api_key
   ```

### Usage

Run the main script by executing the following command in your terminal:

```bash
python Script.py True
```

Replace `True` with `False` if you don't want to display the plots interactively. The script expects a CSV file named `Sheet.csv` in the project directory with columns `Keyword` and `Location`.

**Important:** Ensure to populate the `Sheet.csv` file with your desired keyword-location pairs before running the script. Each row should represent a unique pair of a keyword and its corresponding location.

### Project Structure

- **Script.py:** Main script that reads data from the CSV file, retrieves Google Trends data, and calls functions to save the plot and data.

- **helper.py:** Contains the `get_graph` function responsible for interacting with the Google Trends API and generating the plot.

- **helper_helper.py:** Includes the `save_csv_and_plot` function to save the data and plot to an Excel file.

- **outputs/:** Folder where the generated Excel files and plots are saved.

### File Descriptions

- **Script.py:** Main script to run the project.

- **helper.py:** Helper functions related to Google Trends API interaction and plot generation.

- **helper_helper.py:** Additional helper functions for saving data and plots.

### Important Notes

- Ensure that the `serp_api_key` in the `.env` file is valid and has access to the Google Trends API.

- The CSV file should be formatted with columns `Keyword` and `Location` for the script to work correctly.

- The project uses `serpapi` library, so an internet connection is required for API calls.

- Install the required packages using `pip install -r requirements.txt`.

### Acknowledgments

- The project uses the `serpapi` library for interacting with the Google Trends API. Visit [serpapi.com](https://serpapi.com/) for more information.

- Make sure to comply with Google's terms of service when using the Google Trends API.
