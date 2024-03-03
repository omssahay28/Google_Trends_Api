from pytrends.request import TrendReq
from datetime import datetime, timedelta
import pandas as pd
import os
import shutil
from tqdm import tqdm
import time
pytrends = TrendReq(hl='en-US', tz=360)

with open("INPUT.txt", "r") as file:
    kw_list = file.read().split(",")
kw_list = [kw.strip() for kw in kw_list]
print("Keywords:", kw_list)

end_date = datetime.now()
output_dir = "output"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

# Create the directory
os.makedirs(output_dir)

for kw in kw_list:
    timeframe = {}
    start_date = datetime(2023, 1, 1)
    result_dict = None

    with tqdm(total=int((end_date - start_date).days / 30)) as pbar:
        while start_date < end_date:
            time.sleep(60)
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
            pbar.update(1)

    timeframe.update(result_dict)
    df = pd.DataFrame(timeframe)
    excel_file_path = os.path.join(output_dir, f"{kw}.xlsx") 
    if os.path.exists(excel_file_path):
        os.remove(excel_file_path)
    
    df.to_excel(excel_file_path, index=False)
    
    print(f"Excel file saved for keyword: {kw}")
