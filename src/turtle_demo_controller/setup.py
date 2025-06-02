from setuptools import find_packages, setup

package_name = 'turtle_demo_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', [
            'launch/two_turtle.launch.py',
            'launch/enc_two_turtle.launch.py'
        ]),
    ],
    install_requires=['setuptools'],
    zip_safe=False,
    maintainer='vedantknaik',
    maintainer_email='vnaik79014@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'turtle_plant = turtle_demo_controller.turtle_plant:main',
            'turtle_controller = turtle_demo_controller.turtle_controller:main',
            'enc_turtle_plant = turtle_demo_controller.enc_turtle_plant:main',
            'enc_turtle_controller = turtle_demo_controller.enc_turtle_controller:main',
        ],
    },
)


# from setuptools import find_packages, setup

# package_name = 'turtle_demo_controller'

# setup(
#     name=package_name,
#     version='0.0.0',
#     packages=find_packages(exclude=['test']),
#     data_files=[
#         ('share/ament_index/resource_index/packages',
#             ['resource/' + package_name]),
#         ('share/' + package_name, ['package.xml']),
#         ('share/turtle_demo_controller/launch', ['launch/two_turtle.launch.py']),
#     ],
#     install_requires=['setuptools'],
#     zip_safe=True,
#     maintainer='vedantknaik',
#     maintainer_email='vnaik79014@gmail.com',
#     description='TODO: Package description',
#     license='TODO: License declaration',
#     tests_require=['pytest'],
#     entry_points={
#         'console_scripts': [
#             'turt_controller = turtle_demo_controller.turtle_controller:main'
#         ],
#     },
# )