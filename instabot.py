from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import selenium
import platform
import random
import os


def randomize_list(arg_list):
	new_list = []
	for count in range(0, len(arg_list) - 1):
		random_index = random.randint(0, len(arg_list) - 1)
		while arg_list[random_index] in new_list:
			random_index = random.randint(0, len(arg_list) - 1)
		new_list.append(arg_list[random_index])
	return new_list


class InstaBot():
	def __init__(self, ident, password):
		os.system("clear")
		self.ident = ident
		self.password = password
		self.driver = webdriver.Firefox()
		self.driver.get("https://www.instagram.com/")
		self.driver.maximize_window()
		sleep(6)
		print("Log-in with username: " + ident + ", password: " + password + "...")
		username_field = self.driver.find_element_by_xpath("//input[@name=\"username\"]")
		sleep(random.randint(1, 3))
		for letter in ident:
			username_field.send_keys(letter)
			sleep(random.random())
		password_field = self.driver.find_element_by_xpath("//input[@name=\"password\"]")
		sleep(1)
		for letter in password:
			password_field.send_keys(letter)
			sleep(random.random())
		sleep(0.8)
		login_button = self.driver.find_element_by_xpath('//button[@type="submit"]').click()
		sleep(8)
		print("Sucessfully logged in !")
		notifiaction_deny = self.driver.find_element_by_xpath('//button[@class="aOOlW   HoLwm "]').click()
		sleep(3)
		profile_button = self.driver.find_element_by_xpath('//a[@class="gmFkV"]').click()
		sleep(5)


	def delete_message(self, c_list, index):
		attempt = 0
		comment_scroll_box = self.driver.find_element_by_class_name('XQXOT')
		for count in range(0, len(c_list) * 10):
			self.driver.execute_script("arguments[0].scrollBy(0, -100)", comment_scroll_box)

		if not c_list[index].is_displayed:
			self.driver.execute_script("arguments[0].scrollBy(0, 100)", comment_scroll_box)

		self.driver.execute_script("arguments[0].click();", c_list[index])
		sleep(5)
		action_buttons = self.driver.find_elements_by_class_name("aOOlW")
		# action_buttons[1].click()
		sleep(1)
		if action_buttons[1].is_displayed():
			attempt += 1
			print("Trying to quit the action menu... attempt N° " + str(attempt) + "...", end="\n")
			self.driver.execute_script("arguments[0].click();", action_buttons[2])
			sleep(2)

		sleep(2)


	def send_del_messages(self):
		nbPosts = WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, '//span[@class="g47SY "]')))
		for count in range(0, int(nbPosts.text) + 1):
			print("Scroll N°" + str(count))
			self.driver.execute_script("window.scrollBy(0, 100);")
			sleep(.025)
		sleep(2)
		self.driver.execute_script("window.scrollTo(0, 10);")
		sleep(8)
		all_posts = self.driver.find_elements_by_xpath('//div[@class="v1Nh3 kIKUG  _bz0w"]')
		count = 0
		comment_section_count = 0
		for post in all_posts:
			if count == 0:
				post.click()
				print("Click")
			else:
				try:
					self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
					print("Next")
				except selenium.common.exceptions.NoSuchElementException:
					break
			WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="eo2As "]')))
			comment_section = self.driver.find_element_by_class_name('eo2As')
			comment_element = comment_section.find_elements_by_class_name('Mr508')
			if len(comment_element) < 1:
				print("There isn't any comment... Skipping...")
				self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
				count += 1
				continue
			else:
				print("There is " + str(len(comment_element)) + " comments in this section!")
			for count in range(0, len(comment_element)):
				self.driver.execute_script("document.getElementsByClassName('_4l6NB')[" + str(count) + "].style.display = 'block';")
			comment_count = 0
			for comment in comment_element:
				sleep(0.2)
				comment_count += 1
				print("Scaning comment N°" + str(comment_count) + "...")
				comment_msg = comment.find_element_by_xpath(".//span")
				tag_count = 0
				print(comment_msg.text)
				print(len(comment_msg.text))
				for letter in comment_msg.text:
					if letter == "#":
						tag_count += 1
				if tag_count >= 10:
					comment_action_button = comment.find_elements_by_class_name("wpO6b")
					tags_list = comment_msg.text.split(" ")
					random_tag_list = randomize_list(tags_list)
					for tag in random_tag_list:
						print(tag, end=" ")
					self.delete_message(comment_action_button, 0)
					sleep(random.randint(2*60, 3*60))
					textarea = self.driver.find_element_by_class_name("Ypffh")
					textarea.click()
					textarea_visible = self.driver.find_element_by_class_name('Ypffh')
					try:
						for tag in random_tag_list:
							textarea_visible.send_keys(tag)
							textarea_visible.send_keys(" ")
							sleep(random.random())
					except selenium.common.exceptions.ElementNotInteractableException:
						self.driver.save_screenshot('screen.png')
					sleep(1)
					self.driver.find_element_by_xpath('//button[@type="submit"]').click()
					sleep(2)
			count += 1
		layout = self.driver.find_element_by_class_name("qJPeX")
		layout.find_element_by_class_name("wpO6b").click()
		self.driver.execute_script("window.scrollTo(0, 10)")


username = input("username ------> ")
password = input("password ------> ")

bot = InstaBot(username, password)

# bot = InstaBot("loup_swann", "#Phoenix@INSTA")

while True:
	bot.send_del_messages()
