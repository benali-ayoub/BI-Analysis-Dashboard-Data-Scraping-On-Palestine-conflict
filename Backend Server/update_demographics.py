import os
import zipfile
import pandas as pd
import urllib
from constants import demographics_data_url

def get_demographics_data():
    download_folder = os.path.expanduser("~") + "\Downloads"
    temp_folder = os.path.join(download_folder, 'temp')

    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    api_endpoint = demographics_data_url

    file_name = os.path.join(temp_folder, 'data.zip')

    with urllib.request.urlopen(api_endpoint) as url:
        with open(file_name, 'wb') as f:
            f.write(url.read())

    print(f"File downloaded and saved to: {file_name}")

    temp_file = os.path.join(temp_folder, os.path.basename(file_name))
    os.rename(file_name, temp_file)

    with zipfile.ZipFile(temp_file, 'r') as zip_ref:
        csv_file = next((name for name in zip_ref.namelist() if "Metadata" not in name), None)
        
        if csv_file:
            zip_ref.extract(csv_file, temp_folder)
            
            csv_file_path = os.path.join(temp_folder, csv_file)

            with open(csv_file_path, 'r') as file:
                lines = file.readlines()
            with open(csv_file_path, 'w') as file:
                file.writelines(lines[4:])

            df = pd.read_csv(csv_file_path)

            df.drop(columns=['Unnamed: 67'], inplace=True, errors='ignore')

            df.to_csv('../Data/demographics_data.csv')


            print('############################################################')
            print('Demographics data update finished successfully!')
            print('############################################################')
        else:
            print("No CSV file found in the ZIP archive without 'Metadata' in the name.")
