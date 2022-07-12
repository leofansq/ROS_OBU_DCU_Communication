import rospy
from planning_msg.msg import planning, keypoints, trail

class PlanningMSG():
    def __init__(self):
        self.data = planning()
        self.data.ts = ""
        self.data.area_id = ""
        self.data.level = ""
        self.data.reason = ""
        self.data.dest = ""
        self.data.option = ""
        self.data.last_ret = ""
        self.data.key_points = []
        self.data.trail = []


class KeypointsMSG():
    def __init__(self):
        self.data = keypoints()
        self.data.type = ""
        self.data.lat = 0.0
        self.data.lon = 0.0
        self.data.heading = -1


class TrailMSG():
    def __init__(self):
        self.data = trail()
        self.data.lat = 0.0
        self.data.lon = 0.0



