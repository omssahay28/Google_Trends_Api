Overview
This script analyzes the trending of keywords over a specific timeframe using Google Trends API. It retrieves and processes data for multiple keywords, saving the results in separate Excel files.

Requirements
To run this script, you need to have the following installed:

•	Python 3.10
•	pandas library (pip install pandas)
•	tqdm library (pip install tqdm)
•	pytrends library (pip install pytrends)
•	datetime and os libraries (built-in Python)

Usage

•	Save the script as a .py file.
•	Install the required libraries if not already installed.
•	Create a text file named INPUT.txt and add your keywords, one per line.
•	Run the script using the Python interpreter.

How it works
The script performs the following steps:

1.	Reads keywords from INPUT.txt and prints them for reference.
2.	Sets the start and end dates for the analysis (defaulting to the current date and January 1, 2023, respectively).
3.	Creates an output directory named output if it doesn't exist.
4.	For each keyword:
      	Initializes an empty dictionary to store timeframe data.
      	Sets the initial start date.
      	Enters a loop that runs for approximately the number of months between the start and end dates.
           o	Sleeps for 60 seconds to avoid excessive API requests.
           o	Generates the next month's end date.
           o	Constructs a timeframe payload for Google Trends API.
           o	Retrieves data for the keyword and current timeframe using pytrends library.
           o	Updates the timeframe dictionary with the current payload and data.

      	Combines the timeframe data with the keyword data.
      	Converts the combined data into a pandas DataFrame.
      	Saves the DataFrame as an Excel file in the output directory with the keyword as the file name.
5.	Prints a success message for each keyword with the corresponding Excel file saved.


Limitations
This script is designed to work with the US region and Google Trends data. It may require modifications to support different regions or data sources.
