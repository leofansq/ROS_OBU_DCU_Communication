# leofansq 2022.1.14

import rospy
import json
import time
import os
from std_msgs.msg import String
from planning_msg.msg import planning, keypoints

from ClientSocket import ClientSocket
from msg_init import PlanningMSG, KeypointsMSG, TrailMSG

ADDR = "ws://localhost:8204"
IS_SUBCRIBE_PLANNING = True
IS_SAVING_LOG = False

# ROS Setup
rospy.init_node("obu2dcu", anonymous=True)
pub_hw_planning = rospy.Publisher('/obu_planning', planning, queue_size=10)
pub_hw_uwb = rospy.Publisher('/obu_uwb', keypoints, queue_size=10)
pub_self = rospy.Publisher('/obu2dcu_status', String, queue_size=10)

# WebSocket-Client Setup
CliSock = ClientSocket(ADDR, pub_self)

# Send the Sub Message: Select the message to subcribe
import json
with open('{}/SelectMsg.json'.format(os.path.abspath(os.path.dirname(__file__))), 'r') as js_file:
    js_info = json.load(js_file)
    print ("########################### Subcribe Message ###########################")
    print (json.dumps(js_info))
    print ("########################################################################")
    CliSock.send(js_info)

# Listening
while True:
    if IS_SUBCRIBE_PLANNING:
        with open('{}/Ask4Planning.json'.format(os.path.abspath(os.path.dirname(__file__))), 'r') as js_file:
            js_info = json.load(js_file)
            print ("########################### Subcribe Message ###########################")
            print (json.dumps(js_info))
            print ("########################################################################")
            CliSock.send(js_info)

    # JSON Listener
    hw_json = CliSock.recv()

    # JSON Saver
    if IS_SAVING_LOG:
        with open("{}/msg_log/{}.json".format(os.path.abspath(os.path.dirname(__file__)), time.strftime("%Y%m%d-%H%M%S",time.localtime())), 'a') as hw_save:
            hw_save.write(json.dumps(hw_json))

    # JSON Decoder
    try:
        # Decode the Planning Message & Transfer to ROSMSG
        if hw_json["header"]["msg_type"] == "planning":
            hw_body = hw_json["body"]
            planning_msg = PlanningMSG()
            # If the "Planning" message is success
            if hw_body["ts"]:
                planning_msg.data.ts = hw_body["ts"]
                planning_msg.data.area_id = hw_body["area_id"]
                planning_msg.data.level = hw_body["level"]
                planning_msg.data.reason = hw_body["reason"]
                planning_msg.data.dest = hw_body["dest"]
                planning_msg.data.option = hw_body["option"]
                planning_msg.data.last_ret = hw_body["last_ret"]

                hw_keypoints = hw_body["key_points"]
                hw_trail = hw_body["trail"]

                for kp in hw_keypoints:
                    kp_msg = KeypointsMSG()
                    kp_msg.data.lat = float(kp["lat"])
                    kp_msg.data.lon = float(kp["lon"])
                    try:
                        kp_msg.data.type = kp["type"]
                    except:
                        pass

                    try:
                        kp_msg.data.heading = int(kp["heading"])
                    except:
                        pass

                    planning_msg.data.key_points.append(kp_msg.data)
                
                for tr in hw_trail:
                    tr_msg = TrailMSG()
                    tr_msg.data.lat = float(tr["lat"])
                    tr_msg.data.lon = float(tr["lon"])

                    planning_msg.data.trail.append(tr_msg.data)

            else:
                # If the "Planning" message is fail
                try:
                    planning_msg.data.last_ret = hw_body["last_ret"]
                # If the "Planning" message is NONE
                except:
                    pass
        
            pub_hw_planning.publish(planning_msg.data)
        
        elif hw_json["header"]["msg_type"] == "notify":
            uwb_msg = KeypointsMSG()
            uwb_msg.data.lat = float(hw_json["body"]["lat"])
            uwb_msg.data.lon = float(hw_json["body"]["lon"])
            uwb_msg.data.heading = float(hw_json["body"]["heading"])
            uwb_msg.data.type = "uwb_pos"

            pub_hw_uwb.publish(uwb_msg.data)
            is_subcribe_planning = True
    except:
        pass
