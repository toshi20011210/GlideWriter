from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import re
import requests
import urllib.request, urllib.error
import time

driver = webdriver.Chrome('./chromedriver')

#required input 

#name
#date
#probability 
#image
#averageMY

#P 37*20 741
# 32*20 + 
#S 
#3297 ~ 4324

driver.get('https://kitaichi.glideapp.io/dl/d8fc49')
time.sleep(2)
driver.execute_script("window.open()")


for counter in range(1000, 4366):
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://p-town.dmm.com/machines/'+str(counter))
    try: 
        nameArray = []
        #get name
        name = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/main/section[1]/div[1]/div[1]/h1').text
        nameArray = name.split('\n')
        print(nameArray[0])

        #get image
        try:
            img = driver.find_element(By.XPATH, '//*[@id="to-pagetop"]/body/div[2]/div/div[2]/main/section[1]/div[3]/div/div[1]/div/img')
            url = img.get_attribute('src')
            with urllib.request.urlopen(url=url)as rf:
                img_data = rf.read()
            with open('/Users/toshiakitakahashi/Downloads/machine.png', mode='wb')as wf:
                wf.write(img_data)
        except NoSuchElementException:
                nothing = 'nothing'


        #get date and probability
        dateArray = []
        probabilityArray = []
        table = driver.find_element(By.XPATH, '//*[@id="to-pagetop"]/body/div[2]/div/div[2]/main/section[1]/div[4]/table')
        trs = table.find_elements(By.TAG_NAME, 'tr')    
        for i in range(0, len(trs)):
            ths = trs[i].find_element(By.TAG_NAME, 'th').text
            tds = trs[i].find_element(By.TAG_NAME, 'td').text
            if ths.__contains__('導入開始日'):
                date = tds
            if ths.__contains__('大当り確率'):
                probability = tds
            
        dateArray = date.split('(')
        print(dateArray[0])

        probabilityArray = re.split('（|/|）', probability)
        probabilityArray.append('default')
        print(probabilityArray[1])

        #averageMY 
        paragraphsArray = []

        #---------------
        #divs = driver.find_elements(By.CLASS_NAME, 'wysiwyg-box')
        #for i in range(0, len(divs)):
        #    try:
        #        #if divs[i].find_element(By.CSS_SELECTOR, '.title _ellipsis').text.__contains__('初当り1回あたりの期待出玉'):
        #        #    print('gotit')
        #        #print(title)
        #        paragraphs = divs[i].find_elements(By.TAG_NAME, 'p')
        #        for j in range(0, len(paragraphs)):
        #            if paragraphs[j].text.__contains__('初当り1回あたりの期待出玉'):
        #                paragraphsArray = re.split('玉|\n', paragraphs[j].text)
        #                print('found it!!!!!!')
        #                print(paragraphsArray[0])
        #    except NoSuchElementException:
        #        nothing = 'nothing'
        #-----rewrite-----
        elements = driver.find_elements(By.TAG_NAME, 'p')
        for i in range (0, len(elements)):
            if elements[i].text == '初当り1回あたりの期待出玉':
                box = elements[i].find_element(By.XPATH, '../..')
                tempArray = box.find_elements(By.TAG_NAME, 'p')
                for j in range (0, len(tempArray)):
                    paragraphsArray = re.split('玉|\n', tempArray[j].text)
        paragraphsArray.append('default')
        #print(paragraphsArray)

        #Writing to Glide--------------------
        if probabilityArray[1] == 'default' or paragraphsArray[0] == 'default': 
            print(str(counter) + ' ' + nameArray[0] + ' did not match the format so it was skipped')
            with open('skipped.txt', 'a') as f:
                f.write(str(counter) + ' ' + nameArray[0] + '\n')
        else:
            #driver.quit()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(5)
            driver.find_element(By.XPATH, '//*[@id="app-root"]/div[2]/div[1]/div[3]/div/div[2]/div[2]/button').click()
            driver.find_element(By.XPATH, '//*[@id="screenScrollViewcab5cac14100c76b106d35067a77c24e"]/div/div[1]/div[2]/div/div/textarea').send_keys(nameArray[0])
            driver.find_element(By.XPATH, '//*[@id="screenScrollViewcab5cac14100c76b106d35067a77c24e"]/div/div[2]/div[2]/div/input').send_keys(paragraphsArray[0])
            driver.find_element(By.XPATH, '//*[@id="screenScrollViewcab5cac14100c76b106d35067a77c24e"]/div/div[3]/div[2]/div/input').send_keys(probabilityArray[1])
            driver.find_element(By.XPATH, '//*[@id="screenScrollViewcab5cac14100c76b106d35067a77c24e"]/div/div[5]/div[2]/div/div/textarea').send_keys(dateArray[0])
            driver.find_element(By.XPATH, '//*[@id="screenScrollViewcab5cac14100c76b106d35067a77c24e"]/div/div[6]/label/div[2]/label/input').send_keys('/Users/toshiakitakahashi/Downloads/machine.png')
            time.sleep(15)
            #let the image upload
            driver.find_element(By.XPATH, '//*[@id="app-root"]/div[2]/div[1]/div[3]/div/div[2]/div[2]/button').click()
            time.sleep(5)
            driver.switch_to.window(driver.window_handles[1])
            #driver.quit()
            

    except NoSuchElementException:
        print(str(counter) + ' ' + nameArray[0] + ' did not match the format so it was skipped')
        with open('skipped.txt', 'a') as f:
            f.write(str(counter) + ' ' + nameArray[0] + '\n')

driver.quit()