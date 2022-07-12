import rospy
from std_msgs.msg import String

def callback_self(status):
    
    info = status.data
    print (info)
    # info = info.split(";")
    # print (info)

def status_rcv():

    rospy.init_node("dcu_rcv", anonymous=True)
    rospy.loginfo("pseudo dcu_rcv...")

    rospy.Subscriber("dcu2obu_status", String, callback_self)

    rospy.spin()


if __name__ == '__main__':
    status_rcv()

