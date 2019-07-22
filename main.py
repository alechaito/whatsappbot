from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
from PIL import Image
from io import BytesIO

class Whatsapp:

	def __init__(self):
		self.driver = self.create_driver_session()
		self.url = "http://web.whatsapp.com"
		self.driver.get(self.url)

	def create_driver_session(self):
		arch = open('drive.txt', 'r')
		session_id = arch.readline().strip()
		executor_url = arch.readline()
		arch.close()

		# Save the original function, so we can revert our patch
		org_command_execute = RemoteWebDriver.execute

		def new_command_execute(self, command, params=None):
			if command == "newSession":
				# Mock the response
				return {'success': 0, 'value': None, 'sessionId': session_id}
			else:
				return org_command_execute(self, command, params)

		# Patch the function before creating the driver object
		RemoteWebDriver.execute = new_command_execute

		new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
		new_driver.session_id = session_id

		# Replace the patched function with original function
		RemoteWebDriver.execute = org_command_execute
		return new_driver

	def get_new_msgs(self):
		unread = self.get_elem_class("_1ZMSM") # The green dot tells us that the message is new
		#unread = self.driver.find_elements_by_class_name("OUeyt")
		#element = self.get_elem_class("X7YrQ")
		name, message  = '', ''
		print(len(unread))
		print(unread[-1])
		# click submit button
		submit_button = self.driver.find_elements_by_xpath('//*[@class="_1ZMSM"]')[-1]
		submit_button.click()

		try:
			action.click()
			action.perform()
			time.sleep(3)
			action.click()
			action.perform()
			print("nem vi")
		except:
			pass
		#name = self.get_elem_class("_1wjpf")[0].text  # Contact name
		#msgs = self.drive.get_elem_class("vW7d1") # the message content
		#last_msg = msgs[-1]
		#prev_msg = msgs[-2]
		#print(name)

	def get_elem_class(self, class_name):
		return self.driver.find_elements_by_class_name(class_name)

def main():
	Whats = Whatsapp()
	## Get the QR Code from browser
	qr_code = Whats.get_elem_class("_1pw2F")
	#img = Whats.driver.find_element_by_tag_name('img')
	time.sleep(5)
	#img = Whats.driver.save_screenshot("./data/screenshot.png")
	Whats.get_new_msgs()
	#im = Image.open(BytesIO(img))

if __name__ == "__main__":
    main()