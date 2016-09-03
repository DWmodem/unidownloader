#!/bin/python

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os.path
import requests

def main():

	baseURL = 'http://www.seas.upenn.edu/~bcpierce/unison/download/releases/'
	urlpath = urlopen(baseURL)
	string = urlpath.read().decode('utf-8')

	unisonVersions = getAllUnisonVersions(string)
	createDir(os.getcwd() + "/unison")
	os.chdir("unison")

	for version in unisonVersions:
		
		versionURL = baseURL + version
		versionURLpath = urlopen(versionURL)
		versionPage = versionURLpath.read().decode('utf-8')
		
		files = getFileNamesInPage(versionPage)
		print("Current dir: " + os.getcwd())
		print("Files: ")
		print(files)

		# create directory for version
		createDir(os.getcwd() + "/" + version)
		os.chdir(version)

		for file in files:

			fileURLPath = baseURL + version + "/" + file
			fileLocalPath = os.getcwd() + "/" + file
			
			if not os.path.exists(fileLocalPath):
				downloadAs(baseURL,file)
				print("Downloaded: " + fileLocalPath)
			else:
				print(fileLocalPath + " already exists. Skipping.")

		os.chdir("..")

def getAllUnisonVersions(string):
	
	unisonVersions = []
	soup = BeautifulSoup(string, "html.parser");
	for link in soup.find_all('a'):
		
		linkHref = link.get('href')
		if "unison" in linkHref:
			unisonVersions.append(linkHref)
	
	return unisonVersions

def getFileNamesInPage(string):

	files = []
	soup = BeautifulSoup(string, "html.parser");

	for link in soup.find_all('a'):
		linkHref = link.get('href')
		files.append(linkHref)
	
	return files

#creates if doesnt exist
def createDir(dirName):

	if not os.path.exists(dirName):
		os.makedirs(dirName)

def downloadAs(url, file_name):

	with open(file_name, "wb") as file:
		response = requests.get(url)
		file.write(response.content)


main();