# !/usr/bin/python

import os
import hashlib
from datetime import datetime

#walks the file tree starting at the root directory
#returns a list of every file, exclusing those in the 'exclude' list
def walk():
	#list of directories to exclude from hashing:
	exclude = ["/dev", "/proc", "/run", "/sys", "/tmp", "/var/lib", "/var/run"]
	fileList = []
	#recursively walk through the file path and get files
	#os.walk() method usage from GeeksforGeeks
	for root, dirs, files in os.walk("/", topdown=True):
		for name in files:
			fullpath = os.path.join(root, name)
			if (fullpath[0:4] not in exclude) and (fullpath[0:5] not in exclude) and (fullpath[0:8] not in exclude):
				fileList.append(fullpath)
		'''
		for name in dirs:
			fullpath = os.path.join(root, name)
			if (fullpath[0:4] not in exclude) and (fullpath[0:5] not in exclude) and (fullpath[0:8] not in exclude):
				fileList.append(fullpath)
		'''
	return fileList

#take the list of files on the system and hash each one
def hashFiles(pathlist):
	hashDict = {}
	#hashlib usage from pythoncentral
	hasher = hashlib.sha256()
	for file in pathlist:
		try:
			with open(file, 'rb') as afile:
				buf = afile.read()
				hasher.update(buf)
				hash = hasher.hexdigest()
		except FileNotFoundError:
			pass
		timeInfo = datetime.now()
		# make datetime info readable
		# datetime usage from prgramiz.com
		time = timeInfo.strftime("%m/%d/%Y, %H:%M:%S")
		hashDict[file] = (hash, time)

	return hashDict

# write all the info to a file
def logFiles(dict):
	with open("changeLog.txt", "w") as log:
		for entry in dict:
			log.write(entry + ";" + dict[entry][0] + ";" + dict[entry][1] + "\n")

# import info from the log file to compare
def importLog():
	with open("changeLog.txt", "r") as log:
		hashDict = {}
		for line in log:
			lineSplit = line.split(";")
			hashDict[lineSplit[0]] = (lineSplit[1], lineSplit[2].replace("\n", ""))

	return hashDict

'''
# ONLY USED FOR TESTING
def testingLog():
	with open("changeLog.txt", "r") as log:
		hashDict = {}
		for line in log:
			lineSplit = line.split(";")
			hashDict[lineSplit[0]] = (lineSplit[1], lineSplit[2].replace("\n", ""))
		hashDict["/home/m220612/labs/lab5/hash.py"] = ("abcdef123456789", "22/2/2022 22:22:22:22")

	return hashDict
'''

# compare hash dictionaries to look for changes
# old hashes = dict1, new hashes = dict2
def compare(dict1, dict2):
	for entry in dict1:
		if dict1[entry][0] != dict2[entry][0]:
			print(entry + " changed: " + str(dict1[entry]) + " -> " + str(dict2[entry]) + "\n")
		if entry not in dict2.keys():
			print(entry + " changed location or was deleted.\n")
	for entry in dict2:
		if entry not in dict1.keys():
			print(entry + " changed location or was added.\n")

# walk the file system
print("Walking the filesystem.")
tree = walk()
# hash all the files, stored as dictionary
print("Hashing files.")
newHashes = hashFiles(tree)
# newHashes = testingLog() #FOR TESTING
# import old log to get dictionary of old hashes
print("Importing hash log.")
oldHashes = importLog()
# compare the two dictionaries
print("Comparing hashes.")
compare(oldHashes, newHashes)
# rewrite/update the log file
print("Logging new hashes.")
logFiles(newHashes)
