from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'ranger_base'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='TODO',
    maintainer_email='contact@westonrobot.com',
    description='Control Nodes for Mobile Robots from Weston Robot/AgileX Robotics Ranger',
    license='BSD',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ranger_joint_state_publisher = ranger_base.ranger_joint_state_publisher:main',
        ],
    },
)
