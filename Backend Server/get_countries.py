import os
import requests

def download_countries_data():
    url = 'https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/raw/master/all/all.csv'
    new_file_name = 'countries_data.csv'
    new_directory = '../Data/'

    response = requests.get(url)

    if response.status_code == 200:
        os.makedirs(new_directory, exist_ok=True)

        new_file_path = os.path.join(new_directory, new_file_name)

        with open(new_file_path, 'wb') as file:
            file.write(response.content)
        print(f'File downloaded successfully to: {new_file_path}')
    else:
        print(f'Failed to download file. Status code: {response.status_code}')
