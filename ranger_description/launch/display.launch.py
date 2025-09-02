from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.substitutions import Command

from launch_ros.actions import Node


def generate_launch_description():
    ranger_description_path = get_package_share_path('ranger_description')
    robot_description_content = Command(['xacro ',
                                         str(ranger_description_path / 'urdf' / 'ranger_mini3_v3_simple.urdf')])

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[{'robot_description': robot_description_content,
                     'publish_frequency': 15.0}]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', str(ranger_description_path / 'rviz' / 'show_ranger.rviz')]
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node,
    ])
