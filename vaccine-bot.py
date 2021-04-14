from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import os
from twilio.rest import Client
from decouple import config
import caffeine

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# Initiate the browser
def get_chrome_driver():
    """This sets up our Chrome Driver and returns it as an object"""
    path_to_chrome = "/Users/isabelbolger/Documents/Code/CVS-Vaccine-Bot/chromedriver"
    chrome_options = Options()
    # Keeps the browser open
    chrome_options.add_experimental_option("detach", True)
    
    # Removes the "This is being controlled by automation" alert / notification
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    #Chrome window won't open
    #chrome_options.headless = True
    return webdriver.Chrome(executable_path = path_to_chrome,
                            options = chrome_options)

def findVaccines():
	try:
		chrome_driver = get_chrome_driver()
	except Exception as e:
		print(e)
	while True:
		try:
			chrome_driver.get('https://www.cvs.com/immunizations/covid-19-vaccine?icid=cvs-home-hero1-link2-coronavirus-vaccine')
		except:
			print("failed to get web page")

		wait = WebDriverWait(chrome_driver, 5)
		try:
			wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"acsFocusFirst\"]")))
			chrome_driver.find_element_by_xpath("//*[@id=\"acsFocusFirst\"]").click()
			time.sleep(2)
			wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='Washington']]"))).click()
		except:
			wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='Washington']]"))).click()
		
		status = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='city' and contains(text(), \"seattle, WA\")]/parent::td/parent::tr//span[@class=\"status\"]"))).text
		if (status == "Available"):
			print("available")
			message = client.messages.create(
	              body="There is a CVS COVID vaccine available in Seattle",
	              from_='+15868001122',
	              to=config('MY_NUMBER')
	          )
			chrome_driver.close()
			break
		else:
			print("not available")
			
			#don't try again for another 5 min
			time.sleep(300)


if __name__ == "__main__":
	caffeine.on(display=False)
	findVaccines()
	caffeine.off()



