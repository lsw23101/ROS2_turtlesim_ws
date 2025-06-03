from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    config_file = os.path.join(
        get_package_share_directory('enc_turtle_cpp'),
        'config',
        'fastdds_config.xml'
    )
    
    # FastDDS 설정 환경 변수
    env = {
        'FASTRTPS_DEFAULT_PROFILES_FILE': config_file
    }

    return LaunchDescription([
        Node(
            package='enc_turtle_cpp',
            executable='enc_turtle_plant',
            name='enc_turtle_plant',
            output='screen',
            env=env
        ),
        Node(
            package='enc_turtle_cpp',
            executable='enc_turtle_controller',
            name='enc_turtle_controller',
            output='screen',
            env=env
        )
    ]) 