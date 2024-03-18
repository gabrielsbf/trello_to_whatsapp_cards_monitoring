from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from utils.env_p import *

class Selenium_Manager:

	def __init__(self, url_post_3w):
		self.url = "https://" + url_post_3w
		self.options = webdriver.ChromeOptions()
		s = Service(ChromeDriverManager().install())
		self.options.add_argument(CHROME_DATA_PATH)
		self.driver = webdriver.Chrome(options=self.options,
									   service=s)

	def access_url(self):
		self.driver.get(self.url)
		
	def access_field(self, type : By, elem, time_to_wait):
		self.driver.implicitly_wait(time_to_wait)
		elem = self.driver.find_element(type, elem)
		return elem

	def do_action(self, target, action, message=None, press_return=False):

		if action == "click":
			target.click()
		elif action == "send_keys":
			target.send_keys(message)
			if (press_return == True):
				target.send_keys(Keys.RETURN)

	def do_presskeys(self, first_key, second_key):
		action = ActionChains(self.driver)
		action.key_down(first_key).send_keys(second_key).key_up(first_key).perform()
