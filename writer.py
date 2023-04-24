from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import re
import urllib.request, urllib.error

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

counter = 3297
#counter = 4003
#counter = 3299

driver.get('https://p-town.dmm.com/machines/'+str(counter))
try: 
    #get name
    name = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/main/section[1]/div[1]/div[1]/h1').text
    nameArray = name.split('\n')
    print(nameArray[0])

    #get image
    img = driver.find_element(By.XPATH, '//*[@id="to-pagetop"]/body/div[2]/div/div[2]/main/section[1]/div[3]/div/div[1]/div/img')
    url = img.get_attribute('src')
    with urllib.request.urlopen(url=url)as rf:
        img_data = rf.read()
    with open('/Users/toshiakitakahashi/Downloads/machine.png', mode='wb')as wf:
        wf.write(img_data)


    #get date and probability
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
    probabilityArray.append('placeholder')
    print(probabilityArray[1])

    #averageMY 
    divs = driver.find_elements(By.CLASS_NAME, 'wysiwyg-box')
    for i in range(0, len(divs)):
        try:
            #if divs[i].find_element(By.CSS_SELECTOR, '.title _ellipsis').text.__contains__('初当り1回あたりの期待出玉'):
            #    print('gotit')
            #print(title)
            paragraphs = divs[i].find_elements(By.TAG_NAME, 'p')
            for j in range(0, len(paragraphs)):
                if paragraphs[j].text.__contains__('※電サポ中の出玉増減-10%、通常時10万回転から算出'):
                    paragraphsArray = re.split('玉|\n', paragraphs[j].text)
                    print(paragraphsArray[0])
        except NoSuchElementException:
            nothing = 'nothing'
    driver.quit()

except NoSuchElementException:
    print(str(counter) + ' ' + nameArray[0] + ' did not match the format so it was skipped')
    driver.quit()

except ListIndexOutOfRabgeException: 
    print('aaa')