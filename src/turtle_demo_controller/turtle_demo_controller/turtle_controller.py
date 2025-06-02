#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.get_logger().info("Turtle Controller Node Started")
        
        # 위치 저장 변수
        self.target_x = 5.0
        self.target_y = 5.0
        
        # 상태 정보 구독
        self.turtle1_state_sub = self.create_subscription(
            Pose,
            "/turtle1/state",
            self.target_pose_callback,
            10
        )
        self.turtle2_state_sub = self.create_subscription(
            Pose,
            "/turtle2/state",
            self.current_pose_callback,
            10
        )
        
        # 제어 명령 발행
        self.control_command_pub = self.create_publisher(
            Twist,
            "/turtle2/control_command",
            10
        )

    def target_pose_callback(self, msg: Pose):
        """목표(터틀1)의 위치 업데이트"""
        self.target_x = msg.x
        self.target_y = msg.y
        self.get_logger().debug(f"Updated target position: x={msg.x:.2f}, y={msg.y:.2f}")

    def current_pose_callback(self, msg: Pose):
        """현재(터틀2) 위치를 받아 제어 명령 계산 및 발행"""
        # 위치 오차 계산
        err_x = self.target_x - msg.x
        err_y = self.target_y - msg.y
        err_dist = math.sqrt(err_x**2 + err_y**2)
        
        # 목표 방향 계산
        desired_theta = math.atan2(err_y, err_x)
        err_theta = desired_theta - msg.theta
        
        # 각도 정규화 (-π ~ π)
        while err_theta > math.pi:
            err_theta -= 2.0 * math.pi
        while err_theta < -math.pi:
            err_theta += 2.0 * math.pi
            
        # 제어 게인
        Kp_dist = 0.9
        Kp_theta = 2.0
        
        # 제어 명령 계산
        if err_dist < 0.1:  # 더 작은 임계값으로 수정
            linear_vel = 0.0
            angular_vel = 0.0
        else:
            linear_vel = Kp_dist * err_dist
            angular_vel = Kp_theta * err_theta
        
        # 제어 명령 발행
        self.publish_control_command(linear_vel, angular_vel)
        
    def publish_control_command(self, linear_vel, angular_vel):
        """계산된 제어 명령을 발행"""
        cmd = Twist()
        cmd.linear.x = linear_vel
        cmd.angular.z = angular_vel
        self.control_command_pub.publish(cmd)
        self.get_logger().debug(f"Published control command: linear={linear_vel:.2f}, angular={angular_vel:.2f}")

def main(args=None):
    rclpy.init(args=args)
    controller = TurtleController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 