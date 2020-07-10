
try:
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support import expected_conditions
	from tkinter import messagebox as tkMessageBox
	from selenium.webdriver.common.by import By
	from selenium import webdriver
	from time import sleep
	from tkinter import *
	import datetime
	import selenium
	import platform
	import getpass
	import sqlite3
	import random
	import distro
	import base64
	import sys
	import os

except ImportError:
	print("You need to run the script named 'dependencies.py' before running this one !")

window_size = "600x250"

input_color = "#339966"

background = "#6A9A71"

insta_ver = "1.0"

random_tags = ["#instagram", "#instagramer", "#heythere", "#hi", "#stopreadingthetagslol", "#followme"]

def remove_twice(arg_list):
	new_list = []
	for tag in arg_list:
		if not tag in new_list:
			new_list.append(tag)
		else:
			print("Removing " + tag + " from the list yay...")
			continue
	return new_list


def randomize_list(arg_list):
	new_list = []
	notwice_list = remove_twice(arg_list)

	while len(notwice_list) < 10:
		tag = random.choice(random_tags)
		if not tag in notwice_list:
			print("Adding random tag: " + tag + " !")
			notwice_list.append(tag)
		else:
			continue

	for count in range(0, len(notwice_list)):
		random_index = random.randint(0, len(notwice_list) - 1)
		while notwice_list[random_index] in new_list:
			random_index = random.randint(0, len(notwice_list) - 1)
		new_list.append(notwice_list[random_index])
	print("OLD: " + str(len(arg_list)) + " tags...")
	print("NEW: " + str(len(new_list)) + " tags...")
	return new_list


class InstaBot():
	def __init__(self, ident, password, sleep_from, sleep_to, log_file):
		self.ident = ident
		self.password = password
		self.sleep_from = sleep_from
		self.sleep_to = sleep_to
		self.driver = webdriver.Firefox()
		self.driver.get("https://www.instagram.com/")
		self.driver.maximize_window()
		self.log_file = log_file
		f = open("logs/logs.txt", "w")
		OS = platform.system()
		if OS == "Linux":
			os.system("clear")
			data = distro.linux_distribution()
			print("[OS DETECTION] You're using " + data[0].capitalize() + " " + str(data[1]) + "...")
			f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "[OS DETECTION] You're using " + data[0].capitalize() + " " + str(data[1]) + "...\n")

		else:
			os.system("cls")

		sleep(6)
		print("Log-in with username: " + ident + ", password: " + "*" * int(len(password) - 1) + "...")
		f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "Log-in with username: " + ident + ", password: " + "*" * int(len(password) - 1) + "...\n")
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
		f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "Sucessfully logged in !\n")
		WebDriverWait(self.driver, 9999).until(expected_conditions.presence_of_element_located((By.XPATH, '//button[@class="aOOlW   HoLwm "]'))).click()
		sleep(3)
		profile_button = self.driver.find_element_by_xpath('//a[@class="gmFkV"]').click()
		sleep(5)


	def delete_message(self, c_list, f):
		attempt = 0
		comment_scroll_box = self.driver.find_element_by_class_name('XQXOT')
		for count in range(0, len(c_list) * 10):
			self.driver.execute_script("arguments[0].scrollBy(0, -100)", comment_scroll_box)

		if not c_list[0].is_displayed:
			self.driver.execute_script("arguments[0].scrollBy(0, 100)", comment_scroll_box)

		self.driver.execute_script("arguments[0].click();", c_list[0])
		sleep(5)
		action_buttons = self.driver.find_elements_by_class_name("aOOlW")
		action_buttons[1].click()
		sleep(2)
		action_buttons = self.driver.find_elements_by_class_name("aOOlW")
		if not len(action_buttons) < 2:
			attempt += 1
			print("Trying to quit the action menu... attempt N° " + str(attempt) + "...")
			f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "Trying to quit the action menu... attempt N° " + str(attempt) + "...\n")
			action_buttons[2].click()
			sleep(2)

		sleep(2)


	def send_del_messages(self, f):
		try:
			self.driver.refresh()
			sleep(3)
			nbPosts = WebDriverWait(self.driver, 9999).until(expected_conditions.presence_of_element_located((By.XPATH, '//span[@class="g47SY "]')))
			for count in range(0, int(nbPosts.text) + 1):
				print("Scroll N°" + str(count))
				f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "Scrolling\n")
				self.driver.execute_script("window.scrollBy(0, 100);")
				sleep(.025)
			sleep(2)
			self.driver.execute_script("window.scrollTo(0, 10);")
			sleep(8)
			all_posts = self.driver.find_elements_by_xpath('//div[@class="v1Nh3 kIKUG  _bz0w"]')
			count = 0
			comment_section_count = 0
			for post in all_posts:
				sleep(2)
				if count == 0:
					post.click()
					print("Click")
					f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "Click\n")
				else:
					try:
						self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
						print("Next")
						f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "Next\n")
					except selenium.common.exceptions.NoSuchElementException:
						print("OOF ?")
						break
				comment_section = WebDriverWait(self.driver, 9999).until(expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="eo2As "]')))
				comment_element = comment_section.find_elements_by_xpath(".//ul[@class='Mr508']")
				if len(comment_element) < 1:
					print("There isn't any comment... Skipping...")
					f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "There isn't any comment... Skipping...\n")
					self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
					count += 1
					continue
				else:
					print("There is " + str(len(comment_element)) + " comments in this section!")
					f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "There is " + str(len(comment_element)) + " comments in this section!\n")
				for count in range(0, len(comment_element)):
					self.driver.execute_script("document.getElementsByClassName('_4l6NB')[" + str(count) + "].style.display = 'block';")
				comment_count = 0
				for comment in comment_element:
					sleep(0.1)
					comment_msg = comment.find_elements_by_xpath(".//span")[1]
					print(comment_msg.text)
					comment_author = comment.find_element_by_xpath('.//a[@class="sqdOP yWX7d     _8A5w5   ZIAjV "]').text
					comment_count += 1
					print("Scaning comment N°" + str(comment_count) + " | Author: " + comment_author + "...")
					f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "Scaning comment N°" + str(comment_count) + " | Author: " + comment_author + "...\n")
					tag_count = 0
					for letter in comment_msg.text:
						if letter == "#":
							tag_count += 1
					if tag_count >= 10:
						comment_action_button = comment.find_elements_by_xpath(".//button[@class='wpO6b ']")
						if str(comment_author) != self.ident:
							print("The author of the comment is not the owner of this account... skipping")
							f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "The author of the comment is not the owner of this account... skipping\n")
							continue
						tags_list = comment_msg.text.split(" ")
						random_tag_list = randomize_list(tags_list)
						print("Deleting the comment: " + comment_msg.text)
						f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "Deleting the comment: " + comment_msg.text + "\n")
						print("New tags order :", end=" ")
						f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "New tags order : ")
						for tag in random_tag_list:
							print(tag, end=" ")
							f.write(tag + " ")
						f.write("\n")
						print()
						self.delete_message(comment_action_button, f)
						waiting_time = random.randint(self.sleep_from * 60, self.sleep_to * 60)
						print("Waiting " + str(waiting_time) + "s before reposting the tags...")
						f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "Waiting " + str(waiting_time) + "s before reposting the tags...\n")
						sleep(waiting_time)
						print("Writing the comment...")
						f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "Writing the comment...\n")
						textarea = self.driver.find_element_by_class_name("Ypffh")
						textarea.click()
						textarea_visible = self.driver.find_element_by_class_name('Ypffh')
						try:
							for tag in random_tag_list:
								textarea_visible.send_keys(tag)
								textarea_visible.send_keys(" ")
								sleep(random.random())
						except selenium.common.exceptions.ElementNotInteractableException as error:
							print("[CRITICAL ERROR] SHUT DOWNING THE BOT (comment can't be write)")
							f.write("[ERROR] [" + str(datetime.datetime.now()) + "] " + "[CRITICAL ERROR] SHUT DOWNING THE BOT (comment can't be write)\n")
							self.driver.save_screenshot('screen_posting.png')
							sys.exit()
						sleep(1)
						print("Posting the comment...")
						f.write("[INFO] [" + str(datetime.datetime.now()) + "] " + "Posting the comment...\n")
						try:
							self.driver.find_element_by_xpath('//button[@type="submit"]').click()
						except selenium.common.exceptions.ElementNotInteractableException:
							print("[CRITICAL ERROR] SHUT DOWNING THE BOT (comment can't be posted)")
							f.write("[ERROR] [" + str(datetime.datetime.now()) + "] " + "[CRITICAL ERROR] SHUT DOWNING THE BOT (comment can't be posted)\n")
							self.driver.save_screenshot('screen_submiting.png')
							sys.exit()
						sleep(5)
				count += 1
			layout = self.driver.find_element_by_class_name("qJPeX")
			layout.find_element_by_class_name("wpO6b").click()
			self.driver.execute_script("window.scrollTo(0, 10)")
		except Exception as e:
			raise e
			f.write("[ERROR] [" + str(datetime.datetime.now()) + "] " + str(e) + "\n")
			sys.exit()




# Instancing the main frame...
root = Tk()

# Properties of the main frame called 'root'...
root.geometry(window_size)
root.config(bg=background)
root.title("InstaBot {}".format(insta_ver))


# Function called when the button 'login_button' is pressed...
def loginInsta():
	username = login_username.get()
	password = login_password.get()
	sleep_from = sleep_slider_from.get()
	sleep_to = sleep_slider_to.get()
	if not len(username) > 2 or not len(password) > 2:
		tkMessageBox.showerror('InstaBot ERROR.', 'Your username or password is invalid !')
		return

	tkMessageBox.showinfo('InstaBot INFO.', 'Launching the browser !')

	root.destroy()

	log_file = open("logs/logs.txt", "w")

	bot = InstaBot(username, password, sleep_from, sleep_to, log_file)


	while True:
		bot.send_del_messages(log_file)


def insert_logins():
	connection = sqlite3.connect("logins.db")
	cursor = connection.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS logins(login text, password text)""")
	cursor.execute("SELECT * FROM logins")
	data = cursor.fetchall()

	if len(data) < 1:
		print(data)
		return
	else:
		username = data[0][0]
		password_encoded = data[0][1]
		password_encoded = base64.b64decode(password_encoded.encode("UTF-8"))
		password_decoded = password_encoded.decode("UTF-8")

		login_username.insert(0, username)
		login_password.insert(0, password_decoded)





def save_logins():
	# Connection to database & creation of a cursor
	connection = sqlite3.connect("logins.db")
	cursor = connection.cursor()

	# Creating a table "logins" if not existing
	cursor.execute("""CREATE TABLE IF NOT EXISTS logins(login text, password text)""")

	cursor.execute("DELETE FROM logins")

	username = login_username.get()

	password_decoded = login_password.get()

	password_decoded = base64.b64encode(password_decoded.encode('UTF-8'))

	pasword_encoded = password_decoded.decode('utf-8')

	cursor.execute('INSERT INTO logins(login, password) VALUES (?, ?)',(username, pasword_encoded))

	connection.commit()

	connection.close()

	print("Log-in's sucessfully saved and stocked in the database !")



def reset_saved_logins():
	connection = sqlite3.connect("logins.db")
	cursor = connection.cursor()

	# Creating a table "logins" if not existing
	cursor.execute("""CREATE TABLE IF NOT EXISTS logins(login text, password text)""")

	cursor.execute("DELETE FROM logins")

	print("Sucessfully deleted saved log-in's !")

	login_username.delete(0, "end")

	login_password.delete(0, "end")

	connection.commit()

	connection.close()
	



# Creating entries widgets and showing them...
login_username = Entry(root, bg=input_color, highlightbackground="#27870d", borderwidth=0)
login_username.place(x=220, y=10)

login_password = Entry(root, show="*", highlightbackground="#27870d", bg=input_color, borderwidth=0)
login_password.place(x=220, y=40)

# the login_button who call loginInsta function...
login_button = Button(root, text="Log-in", bg=input_color,highlightbackground="#27870d" ,bd=0,command=loginInsta, pady=5)
login_button.place(x=265, y=70)

# Creating sliders to change values...
sleep_slider_from = Scale(root, from_= 0, to=60,fg="#000000",bd=0,borderwidth=0,sliderlength=8, bg=background, highlightbackground=background,orient=HORIZONTAL)
sleep_slider_from.place(x=25, y=200)

sleep_slider_to = Scale(root, from_= 0, to=60,fg="#000000",bd=0,borderwidth=0,sliderlength=8, bg=background, highlightbackground=background,orient=HORIZONTAL)
sleep_slider_to.place(x=145, y=200)

# Creating a 'save_logins_button' woh calls save_logins function...
save_logins_button = Button(root, text="Save Logins", bg=input_color, highlightbackground="#27870d", bd=0, command=save_logins, pady=5)
save_logins_button.place(x=150, y=70)

# Creating a 'reset_saved_logins_button' woh calls save_logins function...
reset_logins_button = Button(root, text="Reset Logins", bg=input_color, highlightbackground="#27870d", bd=0, command=reset_saved_logins, pady=5)
reset_logins_button.place(x=342, y=70)

insert_logins()


# Creating a new Text Widgets in root...
"""
credits = Label(root, text="By Louswan")

# Showing it...
credits.pack()
"""
# Main app loop
root.mainloop()
