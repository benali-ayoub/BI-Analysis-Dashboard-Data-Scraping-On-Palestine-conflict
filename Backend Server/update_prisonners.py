import asyncio
import pandas as pd
import nest_asyncio
from pyppeteer import launch
from constants import month_mapping, prisonners_data_url

df_final = pd.DataFrame()

# 👇️ call apply()
nest_asyncio.apply()

async def get_prisoners_data():
    browser = await launch({'headless': True})
    page = await browser.newPage()

    await page.goto(prisonners_data_url)

    await page.waitForSelector('a[href="#Notes"]')

    await asyncio.sleep(5)

    data = await page.evaluate('''async () => {
            const tables = Array.from(document.querySelectorAll('.table-responsive'));
            const rowData = [];

            for (const table of tables) {
                let h3Element = table.previousElementSibling;

                // Find the previous h3 element
                while (h3Element && h3Element.tagName !== 'H3') {
                    h3Element = h3Element.previousElementSibling;
                }

                const currentYear = h3Element ? h3Element.textContent.trim().replace('Year ', '') : '';

                const rows = Array.from(table.querySelectorAll('tbody tr'));

                for (const row of rows) {
                    const columns = Array.from(row.querySelectorAll('td'));

                    const month = getValue(columns[0]);
                    const date = getValue(columns[1]);
                    const prisonFacility = getValue(columns[2]);
                    const total = getValue(columns[3]);
                    const servingSentence = getValue(columns[4]);
                    const detainees = getValue(columns[5]);
                    const illegalCombatants = getValue(columns[6]);
                    const legalProceedings = getValue(columns[7]);
                    const adminDetainees = getValue(columns[8]);

                    rowData.push({
                        'Year': currentYear,
                        'Month': month,
                        'Date': date,
                        'Prison Facility': prisonFacility,
                        'Total': total,
                        'Serving Sentence': servingSentence,
                        'Detainees': detainees,
                        'Illegal Combatants': illegalCombatants,
                        'Legal Proceedings': legalProceedings,
                        'Admin Detainees': adminDetainees
                    });
                }

            }

            function getValue(column) {
                return column ? column.textContent.trim() : 'N/A';
            }

            return rowData;
        }''')
    

    df = pd.DataFrame(data)

    numeric_columns = ['Total','Serving Sentence','Detainees','Illegal Combatants','Legal Proceedings','Admin Detainees']

    df[numeric_columns] = df[numeric_columns].replace({',': ''}, regex=True)

    df = df[df['Month'] != 'Month']
    
    df.reset_index()

    combined_mask = (df['Month'] == 'IDF') | (df['Month'] == 'IPS')  | (df['Month'] == 'iDF')
    combined_mask1 = (df['Date'] == 'IPS') | (df['Date'] == 'IDF')

    df.loc[combined_mask, 'Month':'Admin Detainees'] = df.loc[combined_mask,'Month':'Admin Detainees'].shift(2, axis=1)
    df.loc[combined_mask1,'Month':'Admin Detainees'] = df.loc[combined_mask1,'Month':'Admin Detainees'].shift(1, axis=1)

    df.drop(columns=['Date'], axis=1, inplace=True)

    df['Month'] = df['Month'].replace(month_mapping)

    df['Month'] = df['Month'].fillna(method='ffill')

    df = df.replace('*', None)
    df = df.replace('N/A', None)
    df = df.replace('iDF', 'IDF')



    df.to_csv('../Data/prisoners_data.csv')
    
    print('############################################################')
    print('Prosiners data update finished successfully!')
    print('############################################################')

    await browser.close()



    