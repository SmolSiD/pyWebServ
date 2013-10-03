import socket
import datetime
class Server():
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def runServer(self,port=80):
        str=""
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
                str=data.decode('utf-8')
                self.method,self.url,self.proto=self.validReq(str)
                if self.url!=None:
                    if self.url=="/":
                       self.welcome(conn)
                    if self.url=="/time.html":
                        self.time(conn)
                    conn.close()
                    break
    def validReq(self,req):
        try:
            req=req.split('\r\n')
            method, url, proto = req[0].split(" ", 2)
        except:
            return None,None,None
        return method,url,proto

    def welcome(self,conn):
        self.sendMsg("HTTP/1.0 200 OK\r\n",conn)
        self.sendMsg("Server: OwnHands/0.1\r\n",conn)
        self.sendMsg("Content-Type: text/plain\r\n",conn)
        self.sendMsg("\r\n",conn)
        self.sendMsg("Welcome to Python Web Server",conn)
    def time(self,conn):
        dt=datetime.datetime.now()
        self.sendMsg("HTTP/1.0 200 OK\r\n",conn)
        self.sendMsg("Server: OwnHands/0.1\r\n",conn)
        self.sendMsg("Content-Type: text/plain\r\n",conn)
        self.sendMsg("\r\n",conn)
        self.sendMsg("now date:  "+str(dt),conn)
    def sendMsg(self,str,conn):
        conn.send(str.encode('utf-8'))

    def stopServer(self):
        self.sock.close()
serv=Server()
serv.runServer()
