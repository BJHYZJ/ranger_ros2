from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_path

def generate_launch_description():
    declare_args = [
        DeclareLaunchArgument("port_name", default_value="can0"),
        DeclareLaunchArgument("robot_model", default_value="ranger"),
        DeclareLaunchArgument("odom_frame", default_value="odom"),
        DeclareLaunchArgument("base_frame", default_value="base_link"),
        DeclareLaunchArgument("update_rate", default_value="50"),
        DeclareLaunchArgument("odom_topic_name", default_value="ranger/odom"),
        DeclareLaunchArgument("publish_odom_tf", default_value="false"),
    ]

    port_name = LaunchConfiguration("port_name")
    robot_model = LaunchConfiguration("robot_model")
    odom_frame = LaunchConfiguration("odom_frame")
    base_frame = LaunchConfiguration("base_frame")
    update_rate = LaunchConfiguration("update_rate")
    odom_topic_name = LaunchConfiguration("odom_topic_name")
    publish_odom_tf = LaunchConfiguration("publish_odom_tf")

    # Ranger base node
    ranger_base_node = Node(
        package="ranger_base",
        executable="ranger_base_node",
        name="ranger_base_node",
        output="screen",
        parameters=[{
            "port_name": port_name,
            "robot_model": robot_model,
            "odom_frame": odom_frame,
            "base_frame": base_frame,
            "update_rate": update_rate,
            "odom_topic_name": odom_topic_name,
            "publish_odom_tf": publish_odom_tf,
        }],
    )


    joint_state_publisher_node = Node(
        package='ranger_base',
        executable='ranger_joint_state_publisher',
        name='ranger_joint_state_publisher',
        output='screen',
    )

    return LaunchDescription(declare_args + [
        ranger_base_node, 
        joint_state_publisher_node
    ])
