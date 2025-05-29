# turtlebot_encrypted_control

# 질문거리

1. 시나리오 설정을 어떻게 해야 좋을지
   - 어떤 노드가 원격으로 제어함과 동시에 신뢰하지 못해서 제어 연산을 암호화 된 처리를 해야하는지와 같은 상황 설정
   - topic 메세지를 암호문으로 보내는 게 될 것 같다는 생각이 드는데 이를 어떻게 처리 하는지
   - 조금 practical 하게 실제 ROS2 환경의 실험 장비에서 무선 혹은 유선 통신이 어떻게 진행되는지
   - 지금 해야하는 제어 상황 ? 제어기가 수행해야하는 연산 ? 이 무엇인지
     ex. 자유도 1짜리 로봇 팔의 PD + G 제어
     - 이 부분에 대해서 정리가 될때
     - 센서 출력을 [a b theta] 이런게 있을 때 [a b thea theta^2 theta^3 ...] 이런식으로 추가해서 보낸다고 가정하면
     - 삼각함수가 들어간 제어기를 LTI로 표현이 가능해지지 않는지 (테일러 or 맥클로린 급수 활용)
       
   - look up table의 방식 cordic 이 흥미로워 보이고 혹시 설명을 한번 해주실수 있는지 (중간에 부호를 판별해야하는 부분이 존재...)
     


# git 다루기
https://shortcuts.tistory.com/8

# install
```
$ mkdir my_ws/src  
$ cd ~/my_ws/src  
$ git clone https://github.com/lsw23101/ROS2_turtlesim_ws

colcon build --symlink-install
```
git pull을 하면 폴더가 생성 x
# Requirement
ros2 (현:foxy)
turtlesim package

# Usage
1. 배쉬 실행
```
source /opt/ros/foxy/setup.bash

source install/setup.bash


rosfoxy / source ./install/setup.bash
```

2. 터틀봇 두개 소환하는 런치 파일 실행  
```
ros2 launch turtle_demo_controller two_turtle.launch.py
```

3. 터틀봇1을 움직일 노드파일 실행
new terminal:  
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap /cmd_vel:=/turtle1/cmd_vel
```

5. leader-follower 노드 실행
new terminal:  
```
ros2 run turtle_demo_controller leader_follower
```

# ToDo
- publisher subcriber 나눠서 plant contoller 파트 나누기
- 암호 적용하기
- 


# Reference

https://github.com/roboticvedant/ROS2_turtlesim_PID_demo
