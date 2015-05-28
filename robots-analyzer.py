#!/usr/bin/python

import socket
import sys
import os

#declaracao variaveis
port = 80
dominio  = socket.gethostbyname(sys.argv[1])
enter = "\r\n\r\n"
urls = ""

#Interface
print ("[+] - CONNECTING TO IP: %s" %dominio)
print ("[+] - PORT COMUNICATION: %d"%port)

#Conexao robots.txt
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((dominio, port))
s.send("GET /robots.txt HTTP/1.0\r\n")
s.send("HOST:%s%s" %(sys.argv[1],enter))
data = (s.recv(1000000))
s.close()
if data.find('200 OK')!= -1:
        print ("[+] - FILE robots.txt FOUND - [+]")
        f = open('robots.txt', 'w')
        f.write(data)
        f.close()
        #NAO ESTA FUNCIONANDO PASSAR ESSE COMANDO DE SISTEMA
        os.system('cat robots.txt | grep -E "Disallow|Allow" | cut -d " " -f2 > novo.txt')
        nf = open('novo.txt','r')
        for line in nf.readlines():
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((dominio, port))
                s.send("GET /%s HTTP/1.0\r\n" %line)
                s.send("HOST:%s%s" %(sys.argv[1],enter))
                data = (s.recv(1000000))
                s.close()
                if data.find("200 OK")!= -1:
                        print ("[+] - URL http://www.%s%s FOUND"%(sys.argv[1],line))
                else:
                        print ("[+] - URL http://www.%s%s NOT FOUND"%(sys.argv[1],line))

else:
        print ("[+] - FILE robots.txt NOT FOUND - [+]")


s.close()
