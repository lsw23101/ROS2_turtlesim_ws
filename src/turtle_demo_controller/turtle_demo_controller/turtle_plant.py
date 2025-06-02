#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class TurtlePlant(Node):
    def __init__(self):
        super().__init__('turtle_plant')
        self.get_logger().info("Turtle Plant Node Started")
        
        # Subscribers (터틀심으로부터 데이터 수신)
        self.turtle1_pose_sub = self.create_subscription(
            Pose, 
            "/turtle1/pose", 
            self.turtle1_pose_handler, 
            10
        )
        self.turtle2_pose_sub = self.create_subscription(
            Pose, 
            "/turtle2/pose", 
            self.turtle2_pose_handler, 
            10
        )
        
        # Publishers (상태 정보 전송)
        self.turtle1_state_pub = self.create_publisher(
            Pose,
            "/turtle1/state",
            10
        )
        self.turtle2_state_pub = self.create_publisher(
            Pose,
            "/turtle2/state",
            10
        )
        
        # 제어 명령 수신 및 전달
        self.control_command_sub = self.create_subscription(
            Twist,
            "/turtle2/control_command",
            self.control_command_handler,
            10
        )
        
        # Publisher for turtle2 control
        self.turtle2_cmd_pub = self.create_publisher(
            Twist,
            "/turtle2/cmd_vel",
            10
        )

    def turtle1_pose_handler(self, msg: Pose):
        """터틀1의 위치 정보 처리"""
        self.turtle1_state_pub.publish(msg)
        self.get_logger().debug(f"Published turtle1 state: x={msg.x:.2f}, y={msg.y:.2f}")

    def turtle2_pose_handler(self, msg: Pose):
        """터틀2의 위치 정보 처리"""
        self.turtle2_state_pub.publish(msg)
        self.get_logger().debug(f"Published turtle2 state: x={msg.x:.2f}, y={msg.y:.2f}")

    def control_command_handler(self, msg: Twist):
        """제어 명령을 터틀2에게 전달"""
        self.turtle2_cmd_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    plant_node = TurtlePlant()
    rclpy.spin(plant_node)
    plant_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 