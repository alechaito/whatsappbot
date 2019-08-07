from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from db import Database

DB    = Database()

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
	
	def open_box_from_user(self, user):
		divs = self.get_by_xpath('.//span[@class = "_19RFN"]')
		for div in divs:
			if(div.text == user):
				div.click()
				time.sleep(0.3)
				div.click()
				print('[+] Box from {} oppened with success...'.format(div.text))
	

	# PARAM AS NUMBER OR NAME OF CONTACT
	def search_contact(self, param):
		#search_bar = self.get_by_class("ZP8RM")[-1]
		#time.sleep(2)
		## Find the icon chat to find search box of contacts
		actions = ActionChains(self.driver)
		chat_icon = self.get_by_xpath('.//span[@data-icon = "chat"]')[-1]
		actions.move_to_element(chat_icon).click().perform()
		time.sleep(0.3)
		x_arg = "//*[@class='_183ES']"
		wait = WebDriverWait(self.driver, 5)
		wait.until(EC.presence_of_element_located((
			By.XPATH, x_arg
		)))
		## Find the search bar after find the icon chat
		search_bar = self.get_by_xpath(x_arg)[0]
		actions.move_to_element(search_bar).click().perform()
		## Writing based on the param gived
		input_text = self.get_by_class("eiCXe")[0]
		#print(len(input_text))
		input_text.send_keys(param)
		
		## Open first box when appear after the search param
		contacts_box = self.get_by_xpath('.//span[@title = '+param+']')
		print(len(contacts_box))

		'''for contact in contacts_box:
			try:
				print(contact.text)
				if(param == contact.text):
					print(contact.text)
					print("entrei")
					actions.move_to_element(contact)
					actions.click().perform()
					#actions.click().perform()
			except:
				pass'''

	def sent_messages_in_stack(self):
		msgs = DB.get_messages_to_sent()
		for msg in msgs:
			contact 		= DB.get_contact_by_id(msg['contact_id'])
			try:
				self.search_contact(contact['number'])
			except:
				self.search_contact(contact['name'])
	## Need to be executed after open box to sucess
	def get_contact_name(self):
		try:
			return self.get_by_xpath('.//span[@class = "_19RFN"]')[-1].text
		except:
			return None

	def get_details(self):
		## Open header from contact to get details
		header = self.get_by_class('_19vo_')[-1]
		header.click()
		time.sleep(1)

		try:
			## Get details if not is a saved contact
			name 		= self.get_by_xpath('.//span[@class = "_2he9-"]')[-1].text
			number 		= self.get_by_xpath('.//span[@class = "_1drsQ"]')[-1].text
		except:
			## Get details if in contact of celphone
			name 		= self.get_by_xpath('.//span[@class = "_1drsQ"]')[-1].text
			number 		= self.get_by_xpath('//*[@class="_2kUhl"]')[-1].text

		picture 		= self.get_by_xpath('//*[@class="jZhyM _13Xdg"]')[-1].get_attribute('src')
		## Contact instance
		contact = {
			"user_id": 1,
			"name":name,
			"number": number,
			"picture": picture
		}
		## Closing header of details to get text msg
		close_header 	= self.get_by_class('qfKkX')[-1]
		close_header.click()
		time.sleep(0.3)
		## Check new message received
		last_msg 		= self.get_by_xpath('//*[@class="_12pGw EopGb"]')[-1].text
		last_msg_hour	= self.get_by_xpath('//*[@class="_3fnHB"]')[-1].text
		## Message instance
		msg = {
			"content": last_msg,
			"hour": last_msg_hour
		}
		return contact, msg

	

	def update_messages(self):
		msgs = self.get_unread_msgs()
		print("[+] Total de mensagens novas: {}".format( len(msgs) ) )
		for msg in msgs:
			self.open_box(msg)
			contact, msg = self.get_details()
			data = DB.get_contact(contact['number'])
			if(data == None):
				DB.insert_contact(contact)
				data = DB.get_contact(contact['number'])
			msg.update({"contact_id": data['id']})
			DB.insert_message(msg)

	def send_message(self, msg):
		text_box = self.get_by_class("_13mgZ")[-1]
		text_box.send_keys(msg)
		submit = self.get_by_class("hnQHL")[-1]
		submit.click()
		#text_box.send_keys(Keys.ENTER)
		print("[+] Message send with sucess.")

	## Return all unread messages
	def get_unread_msgs(self):
		return self.get_by_xpath('//*[@class="_2UaNq _2ko65"]')
	
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
	def get_by_class(self, class_name):
		return self.driver.find_elements_by_class_name(class_name)
	
	def get_by_xpath(self, xpath):
		return self.driver.find_elements_by_xpath(xpath)
	
	def get_by_css(self, css):
		return self.driver.find_element_by_css_selector(css)
	############################################
