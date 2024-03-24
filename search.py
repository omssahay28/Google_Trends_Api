import asyncio
from pytrends.request import TrendReq
from datetime import datetime, timedelta
import pandas as pd
import os
import shutil
import random
from openpyxl import load_workbook

output_dir = "result"
pytrends = TrendReq(timeout=(10, 20))

async def fetch_data(kw, start_date, end_date, i):
    print(f"{start_date} -> {end_date}")
    timeframe = {}
    result_dict = None
    retries = 0
    max_retries = 10000  # Adjust the maximum number of retries as needed
    
    while start_date < end_date:
        try:
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
            print(e)
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
    
        if timeframe:
            timeframe.update(result_dict)
            df = pd.DataFrame(timeframe)
            print(df)
            excel_file_path = os.path.join(output_dir, f"{kw}_{i}.xlsx") 
            print(excel_file_path)
            df.to_excel(excel_file_path, index=False)
    # if os.path.exists(excel_file_path):
    #     # Read existing data from Excel file
    #     existing_df = pd.read_excel(excel_file_path, engine='openpyxl')
    #     # Concatenate existing data with new data
    #     combined_df = pd.concat([existing_df, df], ignore_index=True)
    #     # Save combined data to Excel file
    #     combined_df.to_excel(excel_file_path, index=False)
    #     print(f"Excel file updated for keyword: {kw}.xlsx")
    # else:
    #     # Save new data to Excel file
    #     df.to_excel(excel_file_path, index=False)
            print(f"New Excel file saved for keyword: {kw}_{i}.xlsx")


async def main():
    with open("INPUT.txt", "r") as file:
        kw_list = file.read().split(",")
    kw_list = [kw.strip() for kw in kw_list]
    print("Keywords:", kw_list)

    # output_dir = "output"
    # if os.path.exists(output_dir):
    #     shutil.rmtree(output_dir)

    # os.makedirs(output_dir)

    tasks = []
    for kw in kw_list:
        start_date = datetime(2004, 1, 1)
        i = 0
        while start_date.year < datetime.now().year:
            end_date_iteration = min(start_date.replace(year=start_date.year + 1) - timedelta(days=1), datetime.now())
            tasks.append(fetch_data(kw, start_date, end_date_iteration, i))
            i+=1
            start_date = end_date_iteration + timedelta(days=1)

    await asyncio.gather(*tasks)

asyncio.run(main())
