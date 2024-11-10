from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlretrieve

options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Path to your Chrome installation
chrome_driver_binary = "C:\chromedriver\chromedriver.exe" # Path to Chrome Driver
driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

driver.get("http://www.ieeeuvce.in/posts/")

img = driver.find_element_by_xpath('/html/body/main/main/section/div/div/div[2]/div[1]/div[1]/a/img')
src = img.get_attribute('src')
print(src)

# download the image
urlretrieve(src, "ieee-pic.jpg")

driver.get("https://web.whatsapp.com/")
input("Scan QR code")
person = driver.find_element_by_css_selector('span[title="Nimitha"]')  # Name of the contact. In this implementation, the contact has to be visible. You can also search for it in the search bar, and hit the enter key via code
person.click()

textbox = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')
textbox.send_keys('This was sent from the ieee website by a bot')
send = driver.find_element_by_class_name('_1E0Oz')
send.click()

attach = driver.find_element_by_css_selector('span[data-testid="clip"]')
attach.click()
driver.find_element_by_css_selector('input[type="file"]').send_keys(r'C:\Users\anamx\ieee-pic.jpg')  # Attach saved image

try:
    element = WebDriverWait(driver, 10).until( # We wait until the element comes into view, in this case, the send button
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-testid="send"]'))
    )
except:
    driver.quit()

element.click()


print('Success')


