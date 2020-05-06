import os
import sys
import time
import subprocess

def generate_modules_list(input_list):
	newlist = []
	for line in input_list:
		if len(line) < 2:
			continue
		newlist.append(line)
	return newlist

def list_to_str(input_list):
	output_str = ""
	for word in input_list:
		output_str.join(word)

	return output_str

def update():
	os.system("clear")

	pip_version = str(input("Do you want to use pip or pip3 ? (pip, pip3). \n>>>> "))

	if "pip3" not in pip_version:
		if "pip" not in pip_version:
			print("The only options are pip and pip3 !")
			time.sleep(3)
			update()
			return


	try:
		modules_file = open("modules.txt", "r")

	except FileNotFoundError:
		print("The file 'modules.txt' is not in the current directory !")
		return

	data = modules_file.read()

	lines = data.split("\n")

	modules = generate_modules_list(lines)

	modules_str = list_to_str(modules)

	if len(modules) < 1:
		print("There is not any dependencies to install !")
		return

	print("\nModules to install : " + modules_str)

	decision = input("\nDo you want to install " + str(len(modules)) + " modules ? (y/n) ").lower()

	if decision == "n":
		return

	for module in modules:
		print("\nInstalling " + module + "...\n")
		try:
			subprocess.call([pip_version,"install",module])
		except FileNotFoundError:
			print("You do not have " + pip_version + " installed !")
			return


	print("\nDependencies successfully installed !")


update()