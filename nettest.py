# -*- coding: cp949 -*-
import socketserver
import random
import json

class MyTCPHandler(socketserver.BaseRequestHandler):
    1111client_data = {"order":None} ##dict
    server_data ={"ETH":None,"BTC":None,"SAND":None,"MANA":None} ##dict
 

    def handle(self):
        print("new connect") 
        while True:
          try:
            data = self.request.recv(8192)
            try:
                d = json.loads(data.decode('utf-8'))
            except Exception as e:
                print("error hear1 ",data)
                break

            if d.get("server") == True: 
                self.server_data[d["name"]] = d
                if self.client_data["order"] != None:
                    send_info = json.dumps(self.client_data["order"]).encode('utf-8')
                    self.request.sendall(send_info)
                    print("send ",self.client_data["order"])
                    self.client_data["order"] = None
                    

            elif d.get("client") == True:
               ##print("client")
               if d.get("order") != None:
                    self.client_data["order"] = d
                    print(self.client_data["order"])
               else:
                if self.server_data[d["name"]] != None:
                    send_info = json.dumps(self.server_data[d["name"]]).encode('utf-8')
                    self.request.sendall(send_info)
                else:
                    continue
          except Exception as e:
             print(e)
             print("close connect")
             break


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "192.168.35.175", 50007
    print("run")
    with ThreadedTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
