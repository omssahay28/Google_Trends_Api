from dotenv import load_dotenv
import matplotlib.pyplot as plt
from datetime import datetime
import os
#from serpapi import GoogleSearch
import serpapi
from helper_helper import save_csv_and_plot
import pandas as pd
load_dotenv()

api_key = os.getenv("serp_api_key")


def get_graph(q, l, filename, flag):
    params = {
            "engine": "google_trends",
            "q": q,
            "location": l,
            "date":"all",
            "api_key": api_key
        }
    search = serpapi.search(params)
    r = search.as_dict()
    interest_over_time_data = r['interest_over_time']
    
    
    all_values = []
    for entry in interest_over_time_data.get('timeline_data', []):
        date = entry.get('date', '')
        timestamp = entry.get('timestamp', '')
        datetime_obj = datetime.utcfromtimestamp(int(timestamp))
        for value_entry in entry.get('values', []):
            query = value_entry.get('query', '')
            value = value_entry.get('value', '')
            extracted_value = value_entry.get('extracted_value', '')
            all_values.append({
                'date': datetime_obj.strftime('%Y-%m-%d %H:%M:%S'),
                'extracted_value': extracted_value
            })
    dates = [datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S') for entry in all_values]
    extracted_values = [entry['extracted_value'] for entry in all_values]
    filename_without_extension = filename[:-4]  # Remove the ".csv" extension
    filename_without_extension += f"_{q}_{l}"
    filename = filename_without_extension + ".csv"
    plt.figure(figsize=(10, 6))
    plt.plot(dates, extracted_values, marker='o', linestyle='-')
    plt.xlabel('Date and Time')
    plt.ylabel('Extracted Value')
    plt.title(f'Interest Over Time for "{q}" in "{l}"')
    save_csv_and_plot(all_values, filename, plt, flag);
    