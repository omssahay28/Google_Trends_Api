import pandas as pd
import matplotlib.pyplot as plt
import io
import os

def save_csv_and_plot(all_values, filename, plt, flag):
    output_folder = 'outputs'
    os.makedirs(output_folder, exist_ok=True)
    excel_filename = os.path.join(output_folder, filename.replace('.csv', '_with_plot.xlsx'))
    writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')
    df = pd.DataFrame(all_values)
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    if flag:
        plt.show()
    buf.seek(0)
    worksheet = writer.sheets['Sheet1']
    worksheet.insert_image('C2', 'a', options={'image_data':buf})
    writer._save()
    buf.close()
    print(f'Plot and Data Saved to {excel_filename}')


