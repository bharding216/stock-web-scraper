import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import asyncio
import aiohttp
import time

# Tutorial: https://oxylabs.io/blog/asynchronous-web-scraping-python-aiohttp


stock_df = pd.DataFrame()

def clean_up(stock_df):
    stock_df[['Name', 'Current price', 'Change(%)', 'Open','High', 'Low']] = \
    stock_df[['Name', 'Current price', 'Change(%)', 'Open', 'High', 'Low']] \
    .astype(str)

    stock_df.replace({'Current price': {',':'', '-':'1'},
                    'Change(%)': {',':'', '-':'1', '%':''},
                    'Open': {',':'', '-':'1'},
                    'High': {',':'', '-':'1'},
                    'Low': {',':'', '-':'1'},
                    'Volume': {',':'', '-':'1'}
    }, regex=True, inplace=True)

    stock_df[['Current price', 'Change(%)', 'Open', 'High', 'Low', 'Volume']] = \
        stock_df[['Current price', 'Change(%)', 'Open', 'High', 'Low', 'Volume']]. \
        apply(pd.to_numeric)

    stock_df = stock_df.sort_values(by=['Volume'], ascending=False)


async def scrape(page, stock_df):
    async with aiohttp.ClientSession() as session:
        async with session.get(page) as resp:
            body = await resp.text()

            soup = bs(body, 'html.parser')


            if soup.find('table'):
                stock_table = soup.find('table', class_='tabMini tabQuotes')
                tr_tag_list = stock_table.find_all('tr')

                for each_tr_tag in tr_tag_list[1:]:
                    td_tag_list = each_tr_tag.find_all('td')

                    row_values = []
                    for each_td_tag in td_tag_list[0:7]:
                        new_value = each_td_tag.text.strip()
                        row_values.append(new_value)

                    stock_df.loc[len(stock_df)] = row_values
    
        clean_up(stock_df)


async def main():
    global stock_df
    global start_time
    start_time = time.time()
    pages = []

    for page_number in range(1, 50):
        # https://www.centralcharts.com/en/price-list-ranking/ALL/asc/ts_19-us-nasdaq-stocks--qc_1-alphabetical-order?p=1
        url_start = 'https://www.centralcharts.com/en/price-list-ranking/'
        url_end = 'ALL/asc/ts_19-us-nasdaq-stocks--qc_1-alphabetical-order?p='
        url = url_start + url_end + str(page_number)
        pages.append(url)

    webpage = requests.get(pages[0])
    soup = bs(webpage.text, 'html.parser')
    stock_table = soup.find('table', class_='tabMini tabQuotes')
    th_tag_list = stock_table.find_all('th')

    headers = []
    for each_tag in th_tag_list:
        title = each_tag.text
        headers.append(title)

    headers[0] = 'Name'

    new_headers = []
    for header in headers:
        if header not in ('Cap.', 'Issued Cap.', ''):
            new_headers.append(header)
    headers = new_headers

    stock_df = pd.DataFrame(columns = headers)


    tasks = []
    for page in pages:
        task = asyncio.create_task(scrape(page, stock_df))
        tasks.append(task)

    await asyncio.gather(*tasks)        

    # The (*) operator unpacks the task list into separate
    # expressions. 
    # asyncio.gather returns a 'future object' that represents
    # the group of tasks. 
    # Wait until all pages are scraped. 


asyncio.run(main())

time_difference = time.time() - start_time
print(stock_df)
print(time_difference)

