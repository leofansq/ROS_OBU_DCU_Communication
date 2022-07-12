# leofansq 2021.1.14

import json
from collections import OrderedDict
import time
import thread
import rospy

from websocket import create_connection
from std_msgs.msg import String

class ClientSocket:
    """
    Class for client of the WebSocket
    """
    def __init__(self, address, pub, is_alive_period=5):
        """
        Init the connection
        
        Paramaters:
            address
            pub: ROS Publisher for self-status publishment
            is_alive_period(s): period to publish the alive status to ROS, defalut=5
        """
        self.ws = None
        self.address = address
        self.is_alive_period = is_alive_period
        self.pub = pub
        self.pub_data = String()

        # try to create connection
        while not self.ws:
            try:
                self.ws = create_connection(self.address)
            except:
                print ("Failed to create connection ... still trying to connect ...")
                self._ros_pub("Failed to create connection")
                time.sleep(2)

        print ("Connected")
        self._ros_pub("Connected")

        # Start the self-alive pub
        thread.start_new_thread(self._alive, (self.is_alive_period,))

    def send(self, message):
        """
        Send Message
        Send the message, and try to reconnect the server if failed. 
        """
        try:
            self.ws.send(json.dumps(message))
            print ("Send Successfully")
            self._ros_pub("Send Successfully")
        except:
            print ("Send Failed")
            self._ros_pub("Send Failed")
            self.ws = None
            while not self.ws:
                try:
                    self.ws = create_connection(self.address)
                except:
                    print ("Failed to connect ... trying ...")
                    self._ros_pub("Failed to connect")
                    time.sleep(2)

            print ("Connected")
            self._ros_pub("Connected")

            # Start the self-alive pub
            thread.start_new_thread(self._alive, (self.is_alive_period,))
    
    def recv(self):
        """
        Receive Message
        Receive the message, and try to reconnect the server if failed.
        """
        try:
            recv_message = self.ws.recv()
            print ("Received Message:")
            self._ros_pub("Received Message")
            print (recv_message)
            print ()
            recv_message = json.loads(recv_message, object_pairs_hook=OrderedDict)
            return recv_message
        except:
            self.ws = None
            while not self.ws:
                try:
                    self.ws = create_connection(self.address)
                except:
                    print ("Failed to connect ... trying ...")
                    self._ros_pub("Failed to connect")
                    time.sleep(2)

            print ("Connected")
            self._ros_pub("Connected")

            # Start the self-alive pub
            thread.start_new_thread(self._alive, (self.is_alive_period,))

    def quit(self):
        """
        Close the socket
        """
        self.ws.close()
    
    def _alive(self, is_alive_peroid):
        """
        Publish the ALIVE status to ROS if alive
        """
        while self.ws:
            self._ros_pub("Alive")
            time.sleep(is_alive_peroid)
    
    def _ros_pub(self, data):
        """
        Publish the status to ROS
        """
        self.pub_data.data = data
        self.pub.publish(self.pub_data)
        
