from tqdm import tqdm
import os
import time
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

suffix = '_Ralph_Lauren'
urls = [
    {f'Big&Tall{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/big-tall/10102?webcat=men%7Cclothing%7CBig%20%26%20Tall'},
    {f'Blazers{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/blazers/10209?webcat=men%7Cclothing%7CBlazers'},
    {f'Casual_Shirts{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/casual-shirts/10202?webcat=men%7Cclothing%7CCasual%20Shirts'},
    {f'Coats&Jackets{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/coats-jackets/10205?webcat=men%7Cclothing%7CCoats%20%26%20Jackets'},
    {f'Formal_Shirts{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/formal-shirts/10207?webcat=men%7Cclothing%7CFormal%20Shirts'},
    {f'Hoodies&Sweatshirts{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/hoodies-sweatshirts/10204?webcat=men%7Cclothing%7CHoodies%20%26%20Sweatshirts'},
    {f'Jeans{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/jeans/102010?webcat=men%7Cclothing%7CJeans'},
    {f'Jumpers&Cardigans{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/jumpers-cardigans/10206?webcat=men%7Cclothing%7CJumpers%20%26%20Cardigans'},
    {f'Lounge&Sleepwear{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/lounge-sleepwear/102012?webcat=men%7Cclothing%7CLounge%20%26%20Sleepwear'},
    {f'Polo_Shirts{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/polo-shirts/10201?webcat=men%7Cclothing%7CPolo%20Shirts'},
    {f'Shorts{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/shorts/102013?webcat=men%7Cclothing%7CShorts'},
    {f'Suits{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/suits/102019?webcat=men%7Cclothing%7CSuits'},
    {f'T-Shirts{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/t-shirts/10203?webcat=men%7Cclothing%7CT-Shirts'},
    {f'Tracksuits{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/tracksuits/102011?webcat=men%7Cclothing%7CTracksuits'},
    {f'Trousers{suffix}': 'https://www.ralphlauren.eu/pt/en/men/clothing/trousers/102015?webcat=men%7Cclothing%7CTrousers'}
]
raspBerry = False
headless = False
driverVersion = '78'
exception_limit = 5

def OS():
    os.system('cls' if os.name == 'nt' else 'clear')

def error_handler():
    try:
        browser.find_elements_by_xpath('/html/body/div[9]/div/div[1]/a')[0].click()
    except:
        time.sleep(60)

def browser_config():
    global browser

    # Set driver options
    OS()
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_extension('Driver/Extension/anticaptcha.zip')
    if headless == True:
        options.add_argument('--headless')

    # Check if its using rapsberry Pi
    if raspBerry == True:
        # Start browser
        print('Staring browser ...')
        browser = webdriver.Chrome(executable_path=f'/usr/lib/chromium-browser/chromedriver', options=options)
        print('Browser started')
    else:
        # Start browser
        print('Staring browser ...')
        browser = webdriver.Chrome(executable_path=f'Driver/chromedriver-{driverVersion}', chrome_options=options)
        print('Browser started')

    # Set browser window position to the left
    browser.set_window_position(1920, 1080, windowHandle='current')
    # Set browser size to 1920x540
    browser.set_window_size(960, 1080, windowHandle='current')
    browser.maximize_window()

def get_total_items_in_page(exception_count):
    # Get quantity of items in web page.
    # For example if there is 10 shirts it will output 10
    try:
        items = browser.find_elements_by_xpath('//*[@id="search-result-items"]/li')
        items = len(items)
        return items
    except:
        if exception_count != exception_limit:
            exception_count = exception_count + 1
            get_total_items_in_page(exception_count)
        else:
            error_handler()

def get_num_pages(exception_count):
    # Get number of pages
    # The input will be something like 1/5 so we need to remove 1 and the /
    # giving an output of 5 in this case
    try:
        total_pages = browser.find_elements_by_xpath('/html/body/div[3]/div[3]/div[2]/div[3]/div/div[2]/ul/li[2]')[0].text
        total_pages = total_pages.replace('1', '')
        total_pages = total_pages.replace('/', '')
        total_pages = total_pages.replace(' ', '')
        return int(total_pages)
    except:
        if exception_count != exception_limit:
            exception_count = exception_count + 1
            get_num_pages(exception_count)
        else:
            error_handler()

def change_page(exception_count):
    try:
        value = browser.find_elements_by_xpath('/html/body/div[3]/div[3]/div[2]/div[1]/div[3]/div[1]/div/div[2]/ul/li[3]/a')[0].get_attribute('href')
        browser.get(value)
    except:
        if exception_count != exception_limit:
            exception_count = exception_count + 1
            change_page(exception_count)
        else:
            error_handler()

def get_items(file, exception_count):
    try:
        for x in tqdm(range(1, (get_total_items_in_page(exception_count=0)+1)), desc='Getting items', smoothing=1, total=get_total_items_in_page(exception_count=0)):
            name = browser.find_elements_by_xpath(f'/html/body/div[3]/div[3]/div[2]/div[2]/div[1]/div[1]/ul/li[{x}]/div/div[3]')[0].text
            price = browser.find_elements_by_xpath(f'/html/body/div[3]/div[3]/div[2]/div[2]/div[1]/div[1]/ul/li[{x}]/div/div[4]')[0].text
            picture_link = browser.find_elements_by_xpath(f'/html/body/div[3]/div[3]/div[2]/div[2]/div[1]/div[1]/ul/li[{x}]/div/div[1]/a')[0].get_attribute("href")
    
            data = {'Name': [name],
                    'Price': [price],
                    'Picture link': [picture_link]
                    }
    
            df = DataFrame(data, columns=['Name', 'Price', 'Picture link'])
            df.to_csv(f'Data/{file}.csv', mode='a', header=False, index=False)
    except:
        if exception_count != exception_limit:
            exception_count = exception_count + 1
            get_items(file, exception_count)
        else:
            error_handler()

try:
    exception_count = 0
    browser_config()
    OS()
    for i in tqdm(range(0, (len(urls)+1)), desc='Scraping pages', smoothing=1, total=len(urls)):
        for file, url in urls[i].items():
            browser.get(url)
            num_pages = get_num_pages(exception_count)
            for x in tqdm(range(0, num_pages), desc='Scraping levels', smoothing=1, total=num_pages):
                get_items(file, exception_count)
                if x < num_pages:
                    change_page(exception_count)
            OS()
    browser.quit()
except KeyboardInterrupt:
    browser.quit()
