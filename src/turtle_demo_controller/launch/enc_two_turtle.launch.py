from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # 1. 터틀심 노드 실행
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen'
        ),
        
        # 2. 두 번째 터틀 생성 (터틀2)
        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn', 
                 '{x: 2.0, y: 2.0, theta: 0.0, name: "turtle2"}'],
            output='screen'
        ),
        
        # 3. 암호화된 플랜트 노드 실행
        Node(
            package='turtle_demo_controller',
            executable='enc_turtle_plant.py',
            name='enc_turtle_plant',
            output='screen'
        ),
        
        # 4. 암호화된 컨트롤러 노드 실행
        Node(
            package='turtle_demo_controller',
            executable='enc_turtle_controller.py',
            name='enc_turtle_controller',
            output='screen'
        ),
        
        # 5. 터틀1 제어를 위한 키보드 텔레옵 노드
        Node(
            package='teleop_twist_keyboard',
            executable='teleop_twist_keyboard',
            name='teleop',
            prefix='xterm -e',
            remappings=[
                ('/cmd_vel', '/turtle1/cmd_vel'),
            ],
            output='screen'
        )
    ]) 