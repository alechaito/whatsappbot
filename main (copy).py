from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import time

class Browser:
	def __init__(self):
		self.browser = webdriver.Chrome()
		self.url = "http://web.whatsapp.com" 	
class Whatsapp:

	def __init__(self):
		self.browser = webdriver.Chrome()
		self.url = "http://web.whatsapp.com"
		#STATE
		self.state = "HI"
		self.stack = []
		self.name = ""
		
		#MSG
		self.st0 = "Ola, sou assistente virtual :D. Vamos la? \n" # -- ESTADO b
		self.st1 = "Qual seu nome?" # -- ESTADO 2
		self.st2 = ''', o que voce deseja?
			1 - Efetuar Pedido
			2 - Andamento do Pedido \n
			3 - Falar com um atendente
		''' #ESTADO 3


	def elem_class(self, string):
		return self.browser.find_element_by_class_name(string)

	def main(self):
		self.browser.get(self.url)
		new_msg = self.check_new_msgs()

	
	def check_msgs(self):
		all_msg = self.browser.find_elements_by_class_name("vW7d1")
		#if(all_msg[-1] not in )

	def select_user(self, user):
		wait = WebDriverWait(self.browser, 5)
		x_arg = "//span[@title='ale']"
		try:
			wait.until(EC.presence_of_element_located((
				By.XPATH, x_arg
			)))
		except:
			# If contact not found, then search for it
			searBoxPath = '//*[@id="input-chatlist-search"]'
			wait.until(EC.presence_of_element_located((
				By.ID, "input-chatlist-search"
			)))
			inputSearchBox = self.browser.find_element_by_id("input-chatlist-search")
			time.sleep(0.5)
			# click the search button
			self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/div/button').click()
			time.sleep(1)
			inputSearchBox.clear()
			inputSearchBox.send_keys(target[1:len(user) - 1])
			print('Target Searched')
			# Increase the time if searching a contact is taking a long time
			time.sleep(4)

		# Select the target
		self.browser.find_element_by_xpath(x_arg).click()
		print("Target Successfully Selected")
		time.sleep(2)
		#SEDING FIRST CHOICE
		header = "o que voce deseja para hoje?"
		#strings = ["Make Order", "Support", "Contact"]
		#choices = self.new_choice(header, strings)

		#text_box = self.browser.find_element_by_class_name("_2S1VP")
		#text_box.send_keys(choices)
		#text_box.send_keys(Keys.ENTER)



	def check_new_msgs(self):
		unread = self.browser.find_elements_by_class_name("OUeyt") # The green dot tells us that the message is new
		name,message  = '',''
		if len(unread) > 0:
			ele = unread[-1]
			action = webdriver.common.action_chains.ActionChains(self.browser)
			action.move_to_element_with_offset(ele, 0, -20) # move a bit to the left from the green dot

			action.click()
			action.perform()
			action.click()
			action.perform()

			name = self.browser.find_element_by_class_name("_1wjpf").text  # Contact name
			last_msg = self.browser.find_elements_by_class_name("vW7d1")[-1]  # the message content
			prev_msg = self.browser.find_elements_by_class_name("vW7d1")[-2]
			#print("estado atual:"+self.state)
			if(name not in self.stack):
				text_box = self.browser.find_element_by_class_name("_2S1VP")
				text_box.send_keys("Bom dia, sou o assistente virtual que ira te atender.")
				text_box.send_keys("Antes de comecarmos qual seu nome?")
				text_box.send_keys(keys.ENTER)
			return name


def main():
	whats = Whatsapp()
	whats.main_loop()


if __name__ == "__main__":
    main()