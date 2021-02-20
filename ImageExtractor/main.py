from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.request
import random

# Please input in this list the webiste to extract images. Format - 'first_website', 'second_website', 'third_website'
path = ['https://unsplash.com/t/wallpapers', 'https://unsplash.com/t/textures-patterns', 'https://unsplash.com/t/nature','https://unsplash.com/t/current-events', 'https://unsplash.com/t/architecture', 'https://unsplash.com/t/business-work', 'https://unsplash.com/t/film', 'https://unsplash.com/t/animals']
# If you are using a raspberry please write True instead of false
RaspBerry = False
# Driver options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
if RaspBerry == True:
    browser = webdriver.Chrome(executable_path = f'/usr/lib/chromium-browser/chromedriver', chrome_options = chrome_options)
else:
    browser = webdriver.Chrome(executable_path = f'Driver/chromedriver-78', chrome_options = chrome_options)

x = 0
while x < len(path):
    browser.get(path[x])
    images = browser.find_elements_by_tag_name('img')
    for image in images:
        src = image.get_attribute('src')
        try:
            print(src)
            r = random.randrange(1, 100000000)
            urllib.request.urlretrieve(str(src), f'Images/{r}.jpg')
        except:
            pass
    x = x + 1
browser.quit()
