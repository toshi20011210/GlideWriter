from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome('./chromedriver')


name = ''
averageMY = ''
probability = ''
releaseDate = ''

#P 37*20 741
# 32*20 + 
#S 
#3297 ~ 4324

counter = 3297

browser.get('https://p-town.dmm.com/machines/'+str(counter))
name = browser.find_element(By.__class__, 'title').text
print(name)
