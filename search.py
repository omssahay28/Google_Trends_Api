from pytrends.request import TrendReq
from datetime import datetime, timedelta
import pandas as pd
import os
import shutil
from tqdm import tqdm
import time
import asyncio
import random

pytrends = TrendReq()

async def fetch_data(kw, start_date, end_date):
    timeframe = {}
    result_dict = None
    retries = 0
    max_retries = 10  # Adjust the maximum number of retries as needed
    
    while start_date < end_date:
        try:
            time.sleep(10)  # Introduce a delay between requests
            next_month = start_date.replace(day=28) + timedelta(days=4)
            end_of_month = next_month - timedelta(days=next_month.day)
            payload_timeframe = f'{start_date.strftime("%Y-%m-%d")} {end_of_month.strftime("%Y-%m-%d")}'
            
            pytrends.build_payload([kw], cat=0, 
                                    timeframe=payload_timeframe, 
                                    geo='US', gprop='')
            data = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
            
            payload_timeframe = f"{payload_timeframe.split(' ')[0]} - {payload_timeframe.split(' ')[1]}"
            
            if 'TimeStamp' not in timeframe.keys():
                timeframe['TimeStamp'] = [payload_timeframe]
            else:
                timeframe['TimeStamp'].append(payload_timeframe)
            
            r_dict = data.to_dict()
            
            if result_dict is None:
                result_dict = r_dict[kw]
                if isinstance(result_dict, int):
                    result_dict = {key: [result_dict] for key in r_dict[kw]}
                else:
                    for key in result_dict:
                        result_dict[key] = [result_dict[key]]
            else:
                for key in r_dict[kw]:
                    if key in r_dict[kw] and key in result_dict:
                        if isinstance(result_dict[key], int):
                            result_dict[key] = [result_dict[key], r_dict[kw][key]]
                        else:
                            result_dict[key].append(r_dict[kw][key])
            
            start_date = next_month
        
        except Exception as e:
            if hasattr(e, 'response') and e.response.status_code == 429:
                if retries < max_retries:
                    delay = 2 ** retries + random.uniform(0, 1) 
                    print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                    retries += 1
                else:
                    print("Max retries reached. Exiting...")
                    break
            else:
                print("An error occurred:", e)
                break
    
    timeframe.update(result_dict)
    df = pd.DataFrame(timeframe)
    excel_file_path = os.path.join(output_dir, f"{kw}.xlsx") 
    if os.path.exists(excel_file_path):
        os.remove(excel_file_path)
    
    df.to_excel(excel_file_path, index=False)
    
    print(f"Excel file saved for keyword: {kw}")

async def main():
    with open("INPUT.txt", "r") as file:
        kw_list = file.read().split(",")
    kw_list = [kw.strip() for kw in kw_list]
    print("Keywords:", kw_list)

    end_date = datetime.now()
    output_dir = "output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    os.makedirs(output_dir)

    tasks = []
    for kw in kw_list:
        start_date = datetime(2023, 1, 1)
        tasks.append(fetch_data(kw, start_date, end_date))

    await asyncio.gather(*tasks)

asyncio.run(main())
