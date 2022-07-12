# coding=UTF-8

from websocket_server import WebsocketServer
import json
import os

import time


# When new client connected
def new_client(client, server):
    print("New connection:%s" % client['id'])
    for f in os.listdir("./msg_log"):
        with open("./msg_log/"+f, 'r') as js_file:
            js_info = json.load(js_file)

            js_info = json.dumps(js_info)
            print (js_info)

            server.send_message_to_all(js_info)
            time.sleep(1)
 
 
# When client disconnected
def client_left(client, server):
    print("Client%sdisconnected" % client['id'])
     
last_time = 0.0
# Receive MSG from client
def message_received(client, server, message):
    global last_time
    print (time.time()-last_time)
    last_time = time.time()
 
 
if __name__ == '__main__':
 
    server = WebsocketServer(8204, 'localhost')
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()









