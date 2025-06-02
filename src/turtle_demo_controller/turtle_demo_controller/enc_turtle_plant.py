#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtle_demo_controller.msg import EncryptedData
import openfhe
from openfhe import *
import json
import base64

class EncTurtlePlant(Node):
    def __init__(self):
        super().__init__('enc_turtle_plant')
        self.get_logger().info("Encrypted Turtle Plant Node Started")
        
        # FHE 설정
        self.cc = BinFHEContext()
        self.cc.GenerateBinFHEContext(MEDIUM)
        self.sk = self.cc.KeyGen()
        self.get_logger().info("FHE Context initialized")
        
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
        
        # 암호화된 데이터 발행자
        self.encrypted_pub = self.create_publisher(
            EncryptedData,
            "/turtle1/encrypted_state",
            10
        )
        
        # 암호화된 합계 수신
        self.encrypted_sum_sub = self.create_subscription(
            EncryptedData,
            "/encrypted_sum",
            self.encrypted_sum_handler,
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

    def encrypt_value(self, value: float) -> int:
        """실수값을 정수로 변환하여 암호화"""
        scaled_value = int(value * 100)  # 소수점 2자리까지 보존
        return self.cc.Encrypt(self.sk, scaled_value)

    def decrypt_value(self, ct) -> float:
        """암호화된 값을 복호화하여 실수로 변환"""
        decrypted = self.cc.Decrypt(self.sk, ct)
        return float(decrypted) / 100.0

    def turtle1_pose_handler(self, msg: Pose):
        """터틀1의 위치 정보 처리 및 암호화"""
        # 1. 일반 상태 정보 전송 (기존 기능)
        self.turtle1_state_pub.publish(msg)
        self.get_logger().debug(f"Published turtle1 state: x={msg.x:.2f}, y={msg.y:.2f}")
        
        # 2. 암호화된 데이터 전송 (새로운 기능)
        try:
            # x 좌표 암호화 및 전송
            enc_x = self.encrypt_value(msg.x)
            enc_msg_x = EncryptedData()
            enc_msg_x.encrypted_data = self.serialize_encrypted(enc_x)
            enc_msg_x.data_type = "x"
            self.encrypted_pub.publish(enc_msg_x)
            
            # y 좌표 암호화 및 전송
            enc_y = self.encrypt_value(msg.y)
            enc_msg_y = EncryptedData()
            enc_msg_y.encrypted_data = self.serialize_encrypted(enc_y)
            enc_msg_y.data_type = "y"
            self.encrypted_pub.publish(enc_msg_y)
            
            self.get_logger().debug("Published encrypted position data")
        except Exception as e:
            self.get_logger().error(f"Error in encryption: {str(e)}")

    def turtle2_pose_handler(self, msg: Pose):
        """터틀2의 위치 정보 처리"""
        self.turtle2_state_pub.publish(msg)
        self.get_logger().debug(f"Published turtle2 state: x={msg.x:.2f}, y={msg.y:.2f}")

    def control_command_handler(self, msg: Twist):
        """제어 명령을 터틀2에게 전달"""
        self.turtle2_cmd_pub.publish(msg)

    def encrypted_sum_handler(self, msg: EncryptedData):
        """암호화된 합계 수신 및 복호화"""
        try:
            ct = self.deserialize_encrypted(msg.encrypted_data)
            decrypted_sum = self.decrypt_value(ct)
            self.get_logger().info(f"Decrypted sum of x and y coordinates: {decrypted_sum}")
        except Exception as e:
            self.get_logger().error(f"Error in decryption: {str(e)}")

def main(args=None):
    rclpy.init(args=args)
    plant_node = EncTurtlePlant()
    rclpy.spin(plant_node)
    plant_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 