import asyncio
import os
import shutil
import pandas as pd
from datetime import datetime, timedelta
from pyppeteer import launch
from constants import fatalities_data_urls
import nest_asyncio

# 👇️ call apply()
nest_asyncio.apply()

async def get_fatalities_data():
    downloads_folder = os.path.expanduser("~") + "\Downloads"

    temp_folder = os.path.join(downloads_folder, "temp")
    os.makedirs(temp_folder, exist_ok=True)

    browser = await launch({'headless': True})
    page = await browser.newPage()

    await page._client.send('Page.setDownloadBehavior', {
        'behavior': 'allow',
        'downloadPath': downloads_folder
    })

    urls = fatalities_data_urls

    file_counter = 1  # Counter for appending numbers to downloaded files

    for url in urls:
        print(f'Navigating to the website: {url}')
        await page.goto(url, {'waitUntil': 'domcontentloaded'})
        await page.waitForSelector('.v-tabs.sub-tabs.v-tabs--grow.theme--light')
        print('Website loaded.')

        #await asyncio.sleep(12)

        cards = await page.querySelectorAll('.stats-card')
        for card in cards:
            title = await card.querySelectorEval('.v-card__title', '(element) => element.textContent')
            button = await card.querySelector('.v-btn')

            is_card_visible = await page.evaluate('(card) => card.offsetParent !== null', card)

            if not is_card_visible:
                print(f'Card titled {title} is not visible. Skipping...')
                continue

            print(f'Clicking download button for card titled {title}...')
            await button.click()

            # Wait for the download to start
            await asyncio.sleep(12)

            # Get the list of downloaded files
            all_files = os.listdir(downloads_folder)

            latest_file = None
            if all_files:
                latest_file = max(
                    [f for f in all_files if f.endswith(".xlsx") and f.startswith("data")],
                    key=lambda x: os.path.getctime(os.path.join(downloads_folder, x)),
                    default=None
                )

            if latest_file:
                # Move the file to the temp folder with an appended number
                source_path = os.path.join(downloads_folder, latest_file)
                destination_name = f"data_{file_counter}.xlsx"
                destination_path = os.path.join(temp_folder, destination_name)
                shutil.move(source_path, destination_path)

                file_counter += 1

                print(f'File for card titled {title} downloaded and moved to {destination_path}.')
            else:
                print(f'No files found for card titled {title}.')

    file_extension = ".xlsx"
    file_prefix = "data"

    one_hour_ago = datetime.now() - timedelta(hours=1)

    # Get a list of files in the Downloads folder
    all_files = os.listdir(downloads_folder)

    filtered_files = [
        file
        for file in all_files
        if file.endswith(file_extension)
        and file.startswith(file_prefix)
        and os.path.getmtime(os.path.join(downloads_folder, file)) > one_hour_ago.timestamp()
    ]

    for file in filtered_files:
        file_path = os.path.join(downloads_folder, file)
        destination_path = os.path.join(temp_folder, file)
        shutil.move(file_path, destination_path)

    temp_folder_link = os.path.abspath(temp_folder)

    # Print or use temp_folder_link as needed
    print("Temp Folder Link:", temp_folder_link)

    directory = temp_folder_link

    all_data = pd.DataFrame()

    for filename in os.listdir(directory):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(os.path.join(directory, filename))
            all_data = pd.concat([all_data, df], ignore_index=True)

    # remove duplicates based on the 'name' column
    all_data.drop_duplicates(subset ="Name", keep = 'last', inplace = True)

    all_data.to_csv('../Data/fatalities_data.csv')

    shutil.rmtree(temp_folder)
    print("Temporary folder deleted.")

    print('############################################################')
    print('Fatalities data update finished successfully!')
    print('############################################################')

    print('Closing the browser...')
    await browser.close()
    print('Browser closed.')

