from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class Browser:
	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument("user-data-dir=./data")
		options.add_argument("--start-maximized")
		self.chrome = webdriver.Chrome(executable_path="/home/chaito/centralmessenger/whats/bot/chromedriver",chrome_options=options)


	def write_sess(self):
		arch = open('drive.txt', 'w+')
		arch.write(self.chrome.session_id+"\n")
		arch.write(self.chrome.command_executor._url)
		arch.close()


def main():
	inst = Browser()
	inst.write_sess()
	
	print(inst.chrome.session_id)
	print(inst.chrome.command_executor._url)

	while True:
		time.sleep(20)



main()