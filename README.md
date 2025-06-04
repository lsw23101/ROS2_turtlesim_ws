![image](https://github.com/user-attachments/assets/8ac3d6a4-9617-4b49-b13f-b977f1c6da56)

<rqt_graph >

bgv 테스트 용

```
 cd ~/ROS2_turtlesim_ws && colcon build --packages-select enc_turtle_cpp && source install/setup.bash && ros2 run enc_turtle_cpp bgv_test

```


OpenFHE 파이썬은 동형암호 스킴이 지원이 안되는 것으로 보임 
C++ 패키지로 완성

현재 : 
암호화 된 터틀봇 1의 x,y 값을 보냄 => x+y 계산 후 전송 => 복호화 후 프린트

암호화 -> cereal 라이브러리를 통한 직렬화 -> string msg 을 통해 통신 

이때 xml 파일로 QoS 설정을 통해 fast DDS의 데이터 max size를 2MB로 변경하여 사용
(현재 P = 65537 일때, N = 16384 (2^14) 정도이며 이때 데이터 크기는 1050103 약 1MB 사이즈)


# open fhe scheme 속도
```
// N사이즈 : 2^14 16384 일때 뎁스: 2

sangwon@STEIECDSL-P04:~/ROS2_turtlesim_ws/install/enc_turtle_cpp/lib/enc_turtle_cpp$ ./bgv_test
========== BGV 암호화 성능 테스트 시작 ==========
컨텍스트 생성 시간: 11.551 ms
키 생성 시간: 74.051 ms

암호화 시간 (두 개의 값): 15.028 ms
직렬화 시간 (두 개의 값): 3.508 ms
직렬화된 데이터 크기: 1050103 bytes

역직렬화 시간 (두 개의 값): 5.607 ms
복호화 시간 (두 개의 값): 4.623 ms

복호화된 결과:
X: 5544
Y: 5544

========== 성능 요약 ==========
컨텍스트 생성: 11.551 ms (10.1%)
키 생성: 74.1 ms (64.7%)
암호화: 15.0 ms (13.1%)
직렬화: 3.5 ms (3.1%)
역직렬화: 5.6 ms (4.9%)
복호화: 4.6 ms (4.0%)
총 시간: 114.4 ms (100%)
==============================

```


// N 사이즈가 2^13 일때 뎁스: 1

![image](https://github.com/user-attachments/assets/931f0fdd-07e8-4626-a2b3-fceb73d74fc5)


// N 사이즈 2^12 일때 뎁스: 0 일때 65537 플레인 텍스트 크기에 대해서 이게 마지노선


![image](https://github.com/user-attachments/assets/780c3537-c846-4351-b90b-a6b4ba0f4394)

// 



# 질문거리

1. 시나리오 설정을 어떻게 해야 좋을지
   - 어떤 노드가 원격으로 제어함과 동시에 신뢰하지 못해서 제어 연산을 암호화 된 처리를 해야하는지와 같은 상황 설정
   - topic 메세지를 암호문으로 보내는 게 될 것 같다는 생각이 드는데 이를 어떻게 처리 하는지
   - 조금 practical 하게 실제 ROS2 환경의 실험 장비에서 무선 혹은 유선 통신이 어떻게 진행되는지
   - 지금 해야하는 제어 상황 ? 제어기가 수행해야하는 연산 ? 이 무엇인지
     \\ ex. 자유도 1짜리 로봇 팔의 PD + G 제어
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

OR 단축어 설정 해놨으면

rosfoxy 
```

2. 런치파일 실행
   
```
ros2 launch enc_turtle_cpp enc_turtle_demo.launch.py
```

# ToDo

# Reference



https://github.com/roboticvedant/ROS2_turtlesim_PID_demo
