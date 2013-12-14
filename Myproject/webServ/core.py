# -*- coding: 'utf-8' -*-
import socket
import datetime
import os
import os.path
import subprocess
import re
import sqlite3
import configparser
import base64
class Server():
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def runServer(self,port=80):
        arrClient=[]
        request=""
        self.conn=sqlite3.connect("Student.db")
        self.sock.bind(('',int(port)))
        self.method=""
        self.url=""
        self.proto=""
        while True:
            self.sock.listen(1)
            conn,addr = self.sock.accept()
            print(addr)
            while True:
                data=conn.recv(1024)
                if not data:
                    break
                request=data.decode('utf-8')
                print(request)
                self.method,self.url,self.proto=self.validReq(request)
                cgiRE=re.compile('/cgi-bin/')
                isCGI=cgiRE.search(self.url)
                if self.url!=None:

                    if self.url=='/':
                        msg="""
                    <!DOCTYPE html>
                    <html>
                     <head>
                      <meta charset="utf-8">
                      <title>Текстовое поле</title>
                     </head>
                     <body>
                     <form action="student" name="myform" method="get">
                     <p><strong>Номер студента в журнале:</strong></p>
                       <input type="text" name="mytext" size="50">
                        <input name="Submit" type=submit value="Send data">
                    </form>
                     </body>
                    </html>
                        """
                        self.sendHTMLResponse(msg,conn)
                        #self.sendResponse(msg,conn)
                    #if self.url=="/sign":


                    elif self.url=="/register":
                        match=re.compile('Authorization: \w+ \w+')
                        auth=match.findall(request)
                        if auth.__len__()==0:
                            self.sendUnAuthresponse(conn)
                        if auth.__len__()!=0:
                            userInfo=auth[0].split(" ")[2]
                            userInfo+='=='
                            decUserInfo= base64.b64decode(userInfo.encode('ascii'))
                            decUserInfo=decUserInfo.decode("utf-8")
                            loginw=decUserInfo.split(":")[0]
                            passw=decUserInfo.split(":")[1]
                            cur=self.conn.cursor()
                            cur.execute("SELECT * FROM Users WHERE login='"+loginw+"'")
                            if cur.fetchone()!=None:
                               self.sendResponse('This login is already in use',conn)
                            else:
                                sql="INSERT INTO Users (login, pass) VALUES ('"+loginw+"','"+passw+"')"
                                cur.execute(sql)
                                self.conn.commit()
                                self.sendResponse('Registration completed successfully',conn)
                            cur.close()
                    elif self.url=="/time":
                        dt=datetime.datetime.now()
                        msg="now date:  "+str(dt)
                        self.sendResponse(msg,conn)
                    elif self.url=="/ya":
                        self.sendResponsewitnCockie(conn)

                    elif self.url=="/help":
                        ROOT_PATH=os.path.dirname(__file__)
                        ROOT_PATH+='/cgi-bin'
                        arrCmd=os.listdir(ROOT_PATH)
                        i=0
                        cmdLine="List of cgi-scripts:"+'\r\n'
                        while i<arrCmd.__len__():
                           cmdLine+=arrCmd[i]+'\r\n'
                           i+=1
                        self.sendResponse(cmdLine,conn)
                    elif isCGI:
                        req=self.url.split('/')
                        script=req[2]
                        name=script.split('?')[0]
                        try:
                            param=script.split('?')[1]
                            arrParam=param.split('&')
                            for i in range(len(arrParam)):
                                arrParam[i]=arrParam[i].split("=")[1]

                        except:
                            param=""
                            arrParam=[]
                        ROOT_PATH=os.path.dirname(__file__)
                        ROOT_PATH+='/cgi-bin/'+name
                        try:
                            open(ROOT_PATH)
                            res=self.startScript(name,arrParam)
                            res=res.decode("utf-8")
                            self.sendResponse(res,conn)
                        except:
                            self.sendBadResponse('Not found this Script',conn)
                    elif self.url=="/help":
                        ROOT_PATH=os.path.dirname(__file__)
                        ROOT_PATH+='/cgi-bin/'
                    elif self.url.startswith("/student"):
                        param=self.getParam(self.url)
                        id=param[0].split("=")[1] # take value without name
                        cur=self.conn.cursor()
                        cur.execute("SELECT surname FROM VM09 WHERE numb="+id)
                        mes="Фамилия студента:  "
                        name=cur.__next__()[0]
                        mes+=name
                        self.sendResponse(mes,conn)
                    else:
                        ROOT_PATH=os.path.dirname(__file__)
                        ROOT_PATH+=self.url
                        f=open(ROOT_PATH,'rb').read()
                        self.sendMsg("HTTP/1.0 200 OK\r\n",conn)
                        self.sendMsg("Server: OwnHands/0.1\r\n",conn)
                        self.sendMsg("Content-Type: */*\r\n",conn)
                        self.sendMsg("\r\n",conn)
                        conn.send(f)
                    conn.close()
                    break
    def startScript(self,name,arrParam):
        ROOT_PATH=os.path.dirname(__file__)
        ROOT_PATH+='/cgi-bin/'
        str=','.join(arrParam)
        cmd = 'python '+ROOT_PATH+name+" "+str
        PIPE = subprocess.PIPE
        p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE,
                stderr=subprocess.STDOUT)
        res=p.stdout.read()
        return res
    def validReq(self,req):
        try:
            req=req.split('\r\n')
            method, url, proto= req[0].split(" ", 2)
        except:
            return None,None,None
        return method,url,proto
    def getParam(self,url):
        req=url.split("?")
        param=req[1].split("&")
        return  param

    def sendResponsewitnCockie(self,conn):
        self.sendMsg("HTTP/1.0 200 OK\r\n",conn)
        self.sendMsg("Server: OwnHands/0.1\r\n",conn)
        self.sendMsg("Content-Type: text/plain;charset=utf-8\r\n",conn)
        self.sendMsg("Set-Cookie: idSess=1\r\n",conn)
        self.sendMsg("\r\n",conn)
        self.sendMsg(str,conn)
    def sendResponse(self,str,conn):
        self.sendMsg("HTTP/1.0 200 OK\r\n",conn)
        self.sendMsg("Server: OwnHands/0.1\r\n",conn)
        self.sendMsg("Content-Type: text/plain;charset=utf-8\r\n",conn)
        self.sendMsg("\r\n",conn)
        self.sendMsg(str,conn)
    def sendHTMLResponse(self,str,conn):
        self.sendMsg("HTTP/1.0 200 OK\r\n",conn)
        self.sendMsg("Server: OwnHands/0.1\r\n",conn)
        self.sendMsg("Content-Type: text/html;charset=utf-8\r\n",conn)
        self.sendMsg("\r\n",conn)
        self.sendMsg(str,conn)
    def sendUnAuthresponse(self,conn):
        self.sendMsg("HTTP/1.0 401 Unauthorized\r\n",conn)
        self.sendMsg("Server: OwnHands/0.1\r\n",conn)
        self.sendMsg("WWW-Authenticate: Basic realm='DB'\r\n",conn)
        self.sendMsg("Content-Type: text/plain;charset=utf-8\r\n",conn)
        self.sendMsg("\r\n",conn)
    def sendBadResponse(self,str,conn):
        self.sendMsg("HTTP/1.0 404 Not Found\r\n",conn)
        self.sendMsg("Server: OwnHands/0.1\r\n",conn)
        self.sendMsg("Content-Type: text/plain;charset=utf-8\r\n",conn)
        self.sendMsg("\r\n",conn)
        self.sendMsg(str,conn)
    def sendMsg(self,str,conn):
        conn.send(str.encode('utf-8'))
    def stopServer(self):
        self.sock.close()
        self.conn.close()

config = configparser.ConfigParser()
config.read('config.ini')
nport=config['Web-Server']['port']
serv=Server()
serv.runServer(nport)


