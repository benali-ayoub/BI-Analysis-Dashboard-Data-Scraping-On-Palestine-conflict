import asyncio
import pandas as pd
from pyppeteer import launch
import nest_asyncio
from datetime import datetime
from constants import live_statistics_urls

nest_asyncio.apply()


async def scrape_data(url):
    browser = await launch()
    page = await browser.newPage() 

    page.setDefaultNavigationTimeout(0)   
    await page.goto(url, waitUntil='domcontentloaded')
    await asyncio.sleep(5)
    
    data = await page.evaluate('''() => {
        const items = Array.from(document.querySelectorAll('.portfolio-items .work-item'));

        return items.map(item => {
            const id = item.querySelector('p.display-4').id;
            const count = parseInt(item.querySelector('p.display-4').innerText);
            const category = item.querySelector('p:not(.display-4)').innerText;

            return { 'id': id, 'count': count, 'category': category };
        });
    }''')

    await browser.close()
    return data

async def get_stats_data():
    all_data = []
    urls = live_statistics_urls

    for url in urls:
        data = await scrape_data(url)
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        for entry in data:
            entry['timestamp'] = timestamp
        all_data.extend(data)
    
    df = pd.DataFrame(all_data)
    df.replace({'Male':'Total Displaced male',
                  'Femal':'Total Displaced female',
                  'Kids':'Total Displaced kids'}, inplace=True)
    df.drop(columns=['id'], inplace=True, errors='ignore')
    df.dropna(axis=0, inplace=True)
    
    df.to_csv('../Data/stats_data.csv')
    
    print('############################################################')
    print('Live Statistics data update finished successfully!')
    print('############################################################')
    
    