#!/usr/bin/python

import socket
import sys
import os

#Checagem parametros
if len(sys.argv) < 2:
	print '[+] - Syntax Error'
	print '[+] - Usage: python '+sys.argv[0]+' host'
	print '[+] - Example:'
	print 'python '+sys.argv[0]+' www.facebook.com'
	exit()

#Funcao resolve host
def resolve(host):
	try:
		address = socket.gethostbyname(host)
		return address
	except:
		print '[+] - Impossivel resolver endereco'
		exit()


def connecta(path):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1)
	s.connect((ip, port))
	s.send("GET %s HTTP/1.0\r\n" %path)
	s.send("HOST:%s\r\n\r\n" %dominio)
	data = s.recv(100000000)
	s.close()	
	return data

def check_robots(ip,port,dominio):
	print ("[+] - CONNECTING TO IP: %s" %ip)
	print ("[+] - PORT COMUNICATION: %d"%port)
	data = connecta('/robots.txt')
	if data.find('200 OK')!= -1:
		print ("[+] - FILE FOUND - [+]")
		f = open('robots.txt', 'w')
		f.write(data)
		f.close()
		analisa()
	else:
        	print ("[+] - FILE NOT FOUND - [+]")
		exit()
def analisa():
	f = open('robots.txt')
	for paths in f:
		if 'Disallow:' in paths:
			paths = paths.strip()
			paths = paths.split(':')[1]
			data = connecta(paths)
			if "HTTP/1.0 200" in data:
				print ("[+] - URL http://www."+dominio+paths+" FOUND")
			elif "HTTP/1.0 401" in data:
				print ("[+] - URL http://www."+dominio+paths+" NOT ALLOWED")
			elif "HTTP/1.0 302" in data:
				print ("[+] - URL http://www."+dominio+paths+" MOVED TEMPORARILY")
			else:
				print ("[+] - URL http://www."+dominio+paths+" NOT FOUND")
	os.remove("robots.txt")
	
port    = 80
dominio = sys.argv[1]
try:
	ip = resolve(dominio)
	check_robots(ip,port,dominio)

except KeyboardInterrupt:
	print
	print 'Process Interrupt'
