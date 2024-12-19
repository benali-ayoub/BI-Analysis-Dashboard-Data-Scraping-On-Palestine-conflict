import os
import requests
import zipfile
import csv
import shutil
from datetime import datetime
from constants import refugees_data_url

def get_refugees_data():
    base_url = refugees_data_url

    current_year = datetime.now().year

    url = base_url.format(current_year)

    local_folder = os.path.expanduser("~") + "/Downloads"

    # Set the custom folder where you want to save the updated CSV file
    custom_folder =  "../Data"
    os.makedirs(custom_folder, exist_ok=True)

    # Create a temporary folder in the Downloads folder
    temp_folder = os.path.join(local_folder, "temp")
    os.makedirs(temp_folder, exist_ok=True)

    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        filename = 'refugees_data.zip'

        zip_file_path = os.path.join(temp_folder, filename)

        with open(zip_file_path, "wb") as file:
            file.write(response.content)

        print(f"Zip file downloaded and saved to: {zip_file_path}")

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_folder)

        print(f"Zip file extracted to: {temp_folder}")

        unrwa_csv_path = os.path.join(temp_folder, "unrwa.csv")

        with open(unrwa_csv_path, 'r') as file:
            csv_data = list(csv.reader(file))

        csv_data = csv_data[14:]

        updated_csv_path = os.path.join(custom_folder, "refugees_data.csv")

        with open(updated_csv_path, 'w', newline='') as file:
            csv.writer(file).writerows(csv_data)

        print(f"Updated CSV file saved to: {updated_csv_path}")

        # Clean up: Delete the temporary folder and its contents
        shutil.rmtree(temp_folder)
        print("Temporary folder deleted.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
