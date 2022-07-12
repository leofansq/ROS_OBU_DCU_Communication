import rospy
from std_msgs.msg import String

from planning_msg.msg import planning, keypoints

def callback(status):
    print (status)
    # info = status.data
    # print (info)
    # info = info.split(";")
    # print (info)

def callback_self(status):
    
    info = status.data
    print (info)
    # info = info.split(";")
    # print (info)



def dcu2obu():

    rospy.init_node("dcu", anonymous=True)
    rospy.loginfo("pseudo dcu...")

    rospy.Subscriber("obu_planning", planning, callback)
    rospy.Subscriber("obu_uwb", keypoints, callback)
    rospy.Subscriber("obu2dcu_status", String, callback_self)

    rospy.spin()





if __name__ == '__main__':
    dcu2obu()

