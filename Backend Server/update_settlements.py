from pyppeteer import launch
import pandas as pd
import nest_asyncio
from datetime import datetime
from constants import settlements_data_url

# 👇️ call apply()
nest_asyncio.apply()

async def scrape_settlements_data(year):
    browser = await launch(headless=True)
    page = await browser.newPage()

    url = f'{settlements_data_url}{year}.html'

    response = await page.goto(url)
    
    if response.status == 200:
        await page.waitForSelector('table.xl9319476')

        data = await page.evaluate('''() => {
            const tableRows = document.querySelectorAll('table.xl9319476 tbody tr');
            const extractedData = [];

            tableRows.forEach((row) => {
                const cells = row.querySelectorAll('td');
                if (cells.length === 2) { // Assuming you want to skip the "Click Here to Download Excel File" row
                    const cell1Text = cells[0].textContent.trim();
                    const cell2Text = cells[1].textContent.trim();
                    extractedData.push({ cell1: cell1Text, cell2: cell2Text });
                }
            });

            return extractedData;
        }''')

        await browser.close()

        df = pd.DataFrame(data)

        df.columns = df.iloc[0].str.replace('\n', '')
        df = df[1:]

        return True, df
    else:
        await browser.close()
        return False, None

async def get_settlements_data():
    current_year = datetime.now().year
    set_df = pd.DataFrame()


    while current_year >= 2000:
        success, df = await scrape_settlements_data(current_year)
        if success:
            set_df = df
            break
        else:
            current_year -= 1
    
    set_df.to_csv('../Data/settlements_data.csv')

    print('############################################################')
    print('Settlements data update finished successfully!')
    print('############################################################')
