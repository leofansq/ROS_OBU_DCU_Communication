# coding=UTF-8

from websocket_server import WebsocketServer
import json

import time
from collections import OrderedDict


# When new client connected
def new_client(client, server):
    print("new connection:%s" % client['id'])
    # # server.send_message_to_all("Hey all, a new client has joined us")
    # for i in range(3):
    #     server.send_message_to_all(js_info)
    #     time.sleep(1)
 
 
# When client disconnected
def client_left(client, server):
    print("client%sdisconnected" % client['id'])
 

last_time = 0.0
# Recieve msg from client
def message_received(client, server, message):
    global last_time
    print("Client(%d) said" % (client['id']))
    print (message)
    # server.send_message_to_all(message)
    print (time.time()-last_time)
    last_time = time.time()
    
 
if __name__ == '__main__':
 
    server = WebsocketServer(8205, 'localhost')
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()
