import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


URL = "https://subway.com.my/find-a-subway"
LOCATION = "kuala lumpur"
SLEEP_TIME = 2

def enterSearchBox(input: str) -> None:
    '''Enter value into search box'''
    
    filter = driver.find_element(By.XPATH, value="/html/body/div[2]/div[2]/div/div/div[2]/div/div/div/div/div/div[1]/div[2]/div[2]/form/div[1]/input")
    filter.send_keys(input)
    filter.send_keys(Keys.ENTER)

def getSoupElements(driver):
    '''Yields scraped web elements containing necessary information using selenium'''
    
    # could be a better way to select elements
    #
    # elements = driver.find_elements(by= By.XPATH, value="//div[@class='fp_listitem fp_list_marker']")
    elements = driver.find_elements(by= By.CSS_SELECTOR, value="div[class^='fp_listitem fp_list_marker']:not(div[style*=' display: none;'])")
    for WebElement in elements:
        elementHTML = WebElement.get_attribute('outerHTML')
        elementSoup = BeautifulSoup(elementHTML,'html.parser')
        yield elementSoup
    pass

def extractData(soupElements) -> list:
    
    data_vector = []
    
    for elements in soupElements:
        
        try:
            location_name = elements.find("h4")
            location_address = elements.select('div.infoboxcontent p')[0]
            operating_hours = elements.select('div.infoboxcontent p')[2]
            waze_link = elements.select('div.directionButton a')[1]['href']
            
            latitude = elements.find("div")['data-latitude']
            longitude = elements.find("div")['data-longitude']
            
            print(f"Outlet Name: {location_name.text}")
            print(f"Outlet Address: {location_address.text}")
            print(f"Operation Hours: {operating_hours.text}")
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
            print(f"Waze Link: {waze_link}")
            
            data_list = [location_name.text, location_address.text, operating_hours.text, latitude, longitude, waze_link]

            # data_dict = {
            #     "Outlet Name": [location_name.text],
            #     "Outlet Address": [location_address.text],
            #     "Operation Hours": [operating_hours.text],
            #     "Latitude": [latitude],
            #     "Longitude": [longitude],
            #     "Waze Link": [waze_link] ,
            # }
            
            data_vector.append(data_list)
        except:
            pass
        
    return data_vector

if __name__ == "__main__":
    
    driver = webdriver.Edge()
    driver.get(URL)
        
    try:
        # sleep to let pages load
        time.sleep(SLEEP_TIME)

        enterSearchBox(LOCATION)
        
        # needs to sleep, else selerium scrapes web before filtering location
        time.sleep(SLEEP_TIME)
            
        soupElements = getSoupElements(driver)
        # print(f"Element datatype: {type(webElements)}")
        
        data = extractData(soupElements)
        print(data)
        
        df = pd.DataFrame(data, columns=['Outlet Name', 'Outlet Address', 'Operating Hours', 'Latitude', 'Longitude', 'Waze Link'])
        
        df.head()
        
        # for element in soupElements:
        #     print(element)
        #     print("\n")

    except Exception as e:
        print(f"There is an exception: {e}")
        
    finally:
        # terminates web driver
        driver.quit()

    #     elements = driver.find_elements(by= By.CSS_SELECTOR, value="div[class^='fp_listitem fp_list_marker']:not(div[style*=' display: none;'])")
    #     for WebElement in elements:
    #         elementHTML = WebElement.get_attribute('outerHTML')
    #         elementSoup = BeautifulSoup(elementHTML,'html.parser')
            
    #         try:
    #             location_name = elementSoup.find("h4")
    #             location_address = elementSoup.select('div.infoboxcontent p')[0]
    #             operating_hours = elementSoup.select('div.infoboxcontent p')[2]
    #             waze_link = elementSoup.select('div.directionButton a')[1]['href']
                
    #             latitude = elementSoup.find("div")['data-latitude']
    #             longitude = elementSoup.find("div")['data-longitude']
                
    #             try:
    #                 df = pd.DataFrame(
    #                     {
    #                         "Outlet Name": [location_name.text],
    #                         "Outlet Address": [location_address.text],
    #                         "Operation Hours": [operating_hours.text],
    #                         "Latitude": [latitude],
    #                         "Longitude": [longitude],
    #                         "Waze Link": [waze_link] ,
    #                     }
    #                 )
    #                 print(df.head())
    #             except Exception as e:
    #                 print(f"Error {e}")
                
                
    #             print(f"Outlet Name: {location_name.text}")
    #             print(f"Outlet Address: {location_address.text}")
    #             print(f"Operation Hours: {operating_hours.text}")
    #             print(f"Latitude: {latitude}")
    #             print(f"Longitude: {longitude}")
    #             print(f"Waze Link: {waze_link}")
                
    #         except:
    #             pass
    #             # print(elementSoup)
                
    #         print("\n")

    # finally:
    #     driver.quit()