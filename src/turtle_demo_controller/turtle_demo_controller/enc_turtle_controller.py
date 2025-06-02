#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtle_demo_controller.msg import EncryptedData
import openfhe
from openfhe import *
import json
import base64

class EncTurtleController(Node):
    def __init__(self):
        super().__init__('enc_turtle_controller')
        self.get_logger().info("Encrypted Turtle Controller Node Started")
        
        # FHE 설정 (복호화는 하지 않지만 직렬화를 위해 필요)
        self.cc = BinFHEContext()
        self.cc.GenerateBinFHEContext(MEDIUM)
        
        # 위치 저장 변수
        self.target_x = 5.0
        self.target_y = 5.0
        
        # 암호화된 값 저장
        self.encrypted_x = None
        self.encrypted_y = None
        
        # 상태 정보 구독 (기존 기능)
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
        
        # 암호화된 상태 정보 구독 (새로운 기능)
        self.encrypted_state_sub = self.create_subscription(
            EncryptedData,
            "/turtle1/encrypted_state",
            self.encrypted_state_handler,
            10
        )
        
        # 제어 명령 발행 (기존 기능)
        self.control_command_pub = self.create_publisher(
            Twist,
            "/turtle2/control_command",
            10
        )
        
        # 암호화된 합계 발행 (새로운 기능)
        self.encrypted_sum_pub = self.create_publisher(
            EncryptedData,
            "/encrypted_sum",
            10
        )

    def serialize_encrypted(self, ct) -> str:
        """암호화된 데이터를 문자열로 직렬화"""
        try:
            # 암호문 객체를 문자열로 변환
            serialized = ct.Serialize()
            # base64로 인코딩
            encoded = base64.b64encode(serialized).decode('utf-8')
            return encoded
        except Exception as e:
            self.get_logger().error(f"Serialization error: {str(e)}")
            raise

    def deserialize_encrypted(self, data_str: str):
        """문자열에서 암호화된 데이터로 역직렬화"""
        try:
            # base64 디코딩
            decoded = base64.b64decode(data_str)
            # 새 암호문 객체 생성
            ct = LWECiphertext()
            ct.Deserialize(decoded)
            return ct
        except Exception as e:
            self.get_logger().error(f"Deserialization error: {str(e)}")
            raise

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

    def encrypted_state_handler(self, msg: EncryptedData):
        """암호화된 상태 정보 처리"""
        try:
            # 문자열을 암호문으로 변환
            ct = self.deserialize_encrypted(msg.encrypted_data)
            
            # x 또는 y 값 저장
            if msg.data_type == "x":
                self.encrypted_x = ct
                self.get_logger().debug("Received encrypted x value")
            elif msg.data_type == "y":
                self.encrypted_y = ct
                self.get_logger().debug("Received encrypted y value")
            
            # 두 값이 모두 있으면 덧셈 수행
            if self.encrypted_x is not None and self.encrypted_y is not None:
                # 암호화된 상태에서 덧셈
                encrypted_sum = self.encrypted_x + self.encrypted_y
                
                # 결과 전송
                sum_msg = EncryptedData()
                sum_msg.encrypted_data = self.serialize_encrypted(encrypted_sum)
                sum_msg.data_type = "sum"
                self.encrypted_sum_pub.publish(sum_msg)
                
                self.get_logger().debug("Published encrypted sum")
                
                # 저장된 값 초기화
                self.encrypted_x = None
                self.encrypted_y = None
                
        except Exception as e:
            self.get_logger().error(f"Error in handling encrypted state: {str(e)}")

def main(args=None):
    rclpy.init(args=args)
    controller = EncTurtleController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 