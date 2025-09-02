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
        DeclareLaunchArgument("odom_topic_name", default_value="odom"),
        DeclareLaunchArgument("publish_odom_tf", default_value="true"),
        DeclareLaunchArgument("use_rviz", default_value="true"),
        DeclareLaunchArgument("use_simple_urdf", default_value="false")
    ]

    port_name = LaunchConfiguration("port_name")
    robot_model = LaunchConfiguration("robot_model")
    odom_frame = LaunchConfiguration("odom_frame")
    base_frame = LaunchConfiguration("base_frame")
    update_rate = LaunchConfiguration("update_rate")
    odom_topic_name = LaunchConfiguration("odom_topic_name")
    publish_odom_tf = LaunchConfiguration("publish_odom_tf")
    use_rviz = LaunchConfiguration("use_rviz")
    use_simple_urdf = LaunchConfiguration("use_simple_urdf")

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

    # Robot description (URDF) - choose between simple and full
    ranger_description_path = get_package_share_path('ranger_description')
    
    # Use full URDF (simple URDF option available but not implemented in this version)
    robot_description_content = Command([
        'cat ', str(ranger_description_path / 'urdf' / 'ranger_mini3_v3.urdf')
    ])

    # Robot state publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[{'robot_description': robot_description_content,
                     'publish_frequency': 15.0}]
    )

    # Custom joint state publisher for ranger
    joint_state_publisher_node = Node(
        package='ranger_description',
        executable='ranger_joint_state_publisher',
        name='ranger_joint_state_publisher',
        output='screen',
    )
    
    # RViz node (optional)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', str(ranger_description_path / 'rviz' / 'show_ranger.rviz')],
        condition=IfCondition(use_rviz)
    )

    return LaunchDescription(declare_args + [
        ranger_base_node, 
        robot_state_publisher_node, 
        joint_state_publisher_node, 
        rviz_node
    ])
