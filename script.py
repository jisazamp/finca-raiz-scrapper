from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
import time

SEARCH_PARAM = "Bogotá"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get("https://www.fincaraiz.com.co/")

wait = WebDriverWait(driver, 10)

searchbox_selector = "div.location-search__container > div > input"
searchbox = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, searchbox_selector))
)
searchbox.send_keys(SEARCH_PARAM)
time.sleep(10)
searchbox.send_keys(Keys.ARROW_DOWN)
searchbox.send_keys(Keys.ENTER)

search_button_selector = "#home-container > section.home-first-section > div.home-cover.false > div.home-cover_content > form > div > div.ant-col.ant-col-order-5.big-input > div:nth-child(1) > div > div.search-button-container > button"
search_button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, search_button_selector))
)
search_button.click()
time.sleep(15)

search_api_url = "https://search-service.fincaraiz.com.co/api/v1/properties/search"
for request in driver.requests:
    if search_api_url in request.url:
        if request.response:
            print("Response Status Code:", request.response.status_code)
            try:
                if (
                    "content-encoding" in request.response.headers
                    and request.response.headers["content-encoding"] == "gzip"
                ):
                    import gzip

                    decompressed_body = gzip.decompress(request.response.body)
                    response_body = json.loads(decompressed_body)
                else:
                    response_body = json.loads(request.response.body)

                with open("search_response.json", "w", encoding="utf-8") as f:
                    json.dump(response_body, f, ensure_ascii=False, indent=4)
                print("Response successfully written to search_response.json")
            except json.JSONDecodeError:
                print("Response Body (raw):", request.response.body)
            except Exception as e:
                print(f"Error processing response: {str(e)}")
                print("Response Body (raw):", request.response.body)
        else:
            print("No response received")
        break
else:
    print(f"No requests to {search_api_url} were intercepted")

driver.quit()
