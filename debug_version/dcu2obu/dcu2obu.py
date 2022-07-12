# leofansq 2022.1.14
import rospy
from std_msgs.msg import String

import time

from ClientSocket import ClientSocket


HEADER_KEYS = ["timestamp", "msg_type"]
BODY_KEYS = ["ts", "gps_time", "status", "pos_type", "lat", "lon", "ele", "heading", "speed", "accel", "pos_quality", "hdop",\
             "sats_num", "brake", "steer", "gear", "door", "light", "epb", "power", "vevent", "driver_id", "obstacles"]
OBSTACLE_KEYS = ["obs_id", "type", "sub_type", "ttl", "lat", "lon", "heading", "speed", "length", "width", "height"]


ADDR = "ws://localhost:8205"

rospy.init_node("dcu2obu", anonymous=True)
rospy.loginfo("dcu2obu ...")
pub_self = rospy.Publisher('/dcu2obu_status', String, queue_size=10)

CliSock = ClientSocket(ADDR, pub_self)

last_time = 0.0

def callback(status):
    
    report = status.data
    report = report.split(";")

    header_dict = {}
    for i in range(2):
        header_dict["timestamp"] = report[0]
        header_dict["msg_type"] = "report"
    
    body_dict = {}
    ilen=len(report)
    for i in range(ilen):
        temp = report[i]
        try:
            temp = float(temp)
        except:
            pass
        body_dict[BODY_KEYS[i]] = temp if i>2 else report[i]
    
    ob_report = report[-1].split("|")
    ob_list = []
    ob_report = []
    for ob in ob_report:
        ob_dict = {}
        ob = ob.split(",")
        for i in range(len(OBSTACLE_KEYS)):
            temp = ob[i]
            try:
                temp = float(temp)
            except:
                pass
            ob_dict[OBSTACLE_KEYS[i]] = temp
        ob_list.append(ob_dict)   
    body_dict[BODY_KEYS[-1]] = ob_list

    js_report = {}
    js_report["header"] = header_dict
    js_report["body"] = body_dict

    print (js_report)

    CliSock.send(js_report)

    global last_time
    print (time.time()-last_time)
    last_time = time.time()


def dcu2obu():

    rospy.Subscriber("reports_to_obu", String, callback)

    rospy.spin()


if __name__ == '__main__':
    dcu2obu()

