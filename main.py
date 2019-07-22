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
import logging

class Whatsapp:

	def __init__(self):
		self.driver = self.create_driver_session()
		self.url = "http://web.whatsapp.com"
		self.driver.get(self.url)

	## Initializing the session or reuse a existing
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

	## Open a specify box chat
	def open_box(self, box):
		box.click()
		time.sleep(0.3)
		box.click()
		print('[+] Box oppened with success...')
	
	## Need to be executed after open box to sucess
	def get_contact_name(self):
		try:
			return self.get_xpath('.//span[@class = "_19RFN"]')[-1].text
		except:
			return None

	def send_message(self, msg):
		text_box = self.get_elem_class("_13mgZ")[-1]
		text_box.send_keys(msg)
		submit = self.get_elem_class("hnQHL")[-1]
		submit.click()
		#text_box.send_keys(Keys.ENTER)
		print("[+] Message send with sucess.")

	## Return all unread messages
	def get_unread_msgs(self):
		return self.get_xpath('//*[@class="_2UaNq _2ko65"]')
	
	def get_qrcode(self):
		qr_code = self.get_elem_class("_1pw2F _2VkjG")
		if(len(qr_code) > 0):
			try:
				os.remove("./data/screenshot.png")
				print("[+] Removed a QR Code SS.")
			except:
				pass
			self.driver.save_screenshot("./data/screenshot.png")
			print("[+] Saved a new screen shot from QR Code.")

	# Shortcuts to selenium
	def get_elem_class(self, class_name):
		return self.driver.find_elements_by_class_name(class_name)
	
	def get_xpath(self, xpath):
		return self.driver.find_elements_by_xpath(xpath)
	
	############################################

def main():
	Whats = Whatsapp()
	## Get the QR Code from browser
	time.sleep(5)
	Whats.get_qrcode()
	msgs = Whats.get_unread_msgs()
	print(len(msgs))
	for msg in msgs:
		Whats.open_box(msg)
		#Whats.get_contact_name()
		Whats.send_message("test1")
		Whats.send_message("test2")
		Whats.send_message("test3")

if __name__ == "__main__":
    main()