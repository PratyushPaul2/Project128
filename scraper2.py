from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Webdriver
browser = webdriver.Chrome("C:/Users/prita/OneDrive/Desktop/Project127/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

stars_data = []

def scrape():
    for i in range(1,2):
        while True:
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, "html.parser")

            # Check page number    
            current_page_num = int(soup.find_all("input", attrs={"star", "page_num"})[0].get("value"))

            if current_page_num < i:
                browser.find_element(By.XPATH, value='/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/table[4]/tbody/tr[1]/td[1]/a').click()
            else:
                break

        for ul_tag in soup.find_all("ul", attrs={"class", "star"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            # Get Hyperlink Tag
            hyperlink_li_tag = li_tags[0]

            temp_list.append("https://exoplanets.nasa.gov"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            
            stars_data.append(temp_list)

        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

        print(f"Page {i} scraping completed")


# Calling Method
scrape()

# Define Header
headers = ["Star", "Constellation", "Right Ascension", "Declination", "App. Mag.", "Distance (ly)","Spectral Type","Brown Dwarf","Mass","Radius"]

# Define pandas DataFrame 
planet_df_1 = pd.DataFrame(planets_data, columns=headers)

# Convert to CSV
planet_df_1.to_csv('updated_scraped_data.csv',index=True, index_label="id")