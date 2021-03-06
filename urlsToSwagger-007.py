#!/usr/bin/env python3

import json,os
import argparse
from termcolor import colored

def getArguments():
	parser = argparse.ArgumentParser("Converts List Of URLS to Swagger 2.0 Format")
	parser.add_argument('-i','--input',dest='inputFile',help="File Having list of URL with its HttpMethod (METHOD:URL)")
	parser.add_argument('-t','--title',dest='title',help="Postman Collection Title")
	parser.add_argument('-u','--host',dest='host',help="HostName Without http/https")
	parser.add_argument('-f','--fullUrl',dest='isUrlWithProtocol',action='store_true',help="If URL includes protocol (Ex: http://test.com/api/ping)")
	parser.add_argument('-d','--delimiter',dest='delimiter',help="Delimiter (Default: colon)")
	parser.add_argument('-p','--protocol',dest='protocol',help="Protocol/Scheme [Default: https]")
	parser.add_argument('-o','--output',dest='outputDir',help="Output Filename")
	parser.add_argument('-v','--verbose',dest='verbose',action='store_true',help="Don't Print on Terminal [Default: False]")
	args = parser.parse_args()
	return args

def getAPIList(urlFile,delimiter,isUrlWithProtocol):
	try:
		with open(urlFile, "r") as file:
			lines = file.readlines()
	except FileNotFoundError:
		print(colored("[-]Input File Not Found:","red"),urlFile)
		exit(0)


	API_List = []
	for line in lines:                                     #FileFormat: HttpMethod:URL

		#Modify Logic Here
		line = line.split(delimiter,1)
		httpMethod = line[0].strip().lower()
		if isUrlWithProtocol:
			apiPath = "/" + line[1].strip().split("/",3)[3]   #If format: http://test.com/api/v2/sayHello
		else:
			apiPath = line[1].strip().lower()                  #If format: /api/v2/sayHello
		API_List.append((httpMethod,apiPath))                      #APIList = [(GET,/api/v2/sayHello)]
	
	return API_List


def convertToSwagger(API_List,title,host,protocol):
	pathDict = {}
	otherDict = {"Description": "Killer007","responses":{},"consumes":["application/json"]}

	for httpMethod,apiPath in API_List:
		pathDict[apiPath] = {httpMethod:otherDict}

	swaggerDict = {"swagger":"2.0","host":host,"info": {"title": title,"version": "v2"},"schemes": [protocol],"consumes":["application/json"],"paths":pathDict}
	return json.dumps(swaggerDict)    #Convert to Json

def saveOutput(swaggerJson,outputDir):
	with open(outputDir,"w") as file:
		file.write(swaggerJson)


def main():
	#Hardcode these or Pass as Arguments	
	inputFile = "urls.txt"
	title = "MyProject_APIs"
	host = "x.x.x.x"            #Without Https
	protocol = "https"
	outputDir = "swagger-007.json"
	verbose = True
	delimiter = ":"

	args = getArguments()
	if args.inputFile:
		inputFile = args.inputFile
	if args.title:
		title = args.title
	if args.host:
		host = args.host
	if args.protocol:
		protocol = args.protocol
	if args.outputDir:
		outputDir = args.outputDir
	if args.verbose:
		verbose = False
	if args.delimiter:
		delimiter=args.delimiter
	isUrlWithProtocol = args.isUrlWithProtocol or False


	if os.path.exists(outputDir):
		print(colored("[-] File Already Exists: "+ outputDir,"red"))
		exit(0)

	API_List = getAPIList(inputFile,delimiter,isUrlWithProtocol)
	swaggerJson = convertToSwagger(API_List,title,host,protocol)
	saveOutput(swaggerJson,outputDir)
	print(colored("[-]Output Saved To: "+ outputDir,"cyan"))

	if verbose:
		print(colored("[-]Swagger 2.0 \n","yellow") + swaggerJson)

if __name__ == '__main__':
	main()
	#https://mulesoft.github.io/oas-raml-converter/ --> For Further Conversion
