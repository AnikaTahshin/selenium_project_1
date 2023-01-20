import csv
from selenium import webdriver
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome('./chromedriver')
driver.maximize_window()


Image_Source = []
Status_Code = []
pageName = []
count = 0

with open('webLink.csv')as file:
    csvFile = csv.reader(file)
    for row in csvFile:
        count += 1
        print("Loop to check: ", count)
        driver.get(row[1])

        def Image():
            try:
        # wait until property-tiles loaded
                WebDriverWait(driver, 80).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"img[id^='js-hero-image']")))
                print("Page is loaded within 60 seconds.")
            
        # scroll page from top to bottom
                
                last_height = driver.execute_script("return document.body.scrollHeight")
                time.sleep(8)
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(5)

                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                    # time.sleep(3)
                    
            # scroll end
        
            except:
                print("Timeout Exception: Page did not load within 60 seconds.")

            images = driver.find_elements(By.CSS_SELECTOR,"img[id^='js-hero-image']") #common variable
            sum = 0
            for img in images:
                sum += 1
                print("Total Images: ", sum)
                featured_image = img.get_attribute("src")
                requestCode = requests.get(featured_image)
                statusCode = requestCode.status_code
                
                pageName.append(row[0])
                Image_Source.append(featured_image)
                Status_Code.append(statusCode)
                
                
                dict = {'pageName':pageName,'ImageSource': Image_Source, 'StatusCode': Status_Code}
                df = pd.DataFrame(dict)
                print(df)
                df.to_csv('result.csv')
        Image()

    