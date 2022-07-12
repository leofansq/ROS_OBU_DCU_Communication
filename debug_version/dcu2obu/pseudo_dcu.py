import rospy
from std_msgs.msg import String

import time

rospy.init_node("dcu", anonymous=True)
pub = rospy.Publisher('/reports_to_obu', String, queue_size=10)


pub_data = String()
pub_data.data = "123456789;;;;11.1111111;22.2222222;;;0.013579;;;;10;;0;N;;;;50;0;001"

for i in range(3):
# while True:
    # print (i)
    pub.publish(pub_data)

    time.sleep(0.1)




