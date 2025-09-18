#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from ranger_msgs.msg import ActuatorStateArray
import math

class RangerJointStatePublisher(Node):
    def __init__(self):
        super().__init__('ranger_joint_state_publisher')
        
        # Publisher for joint states
        self.joint_state_pub = self.create_publisher(JointState, '/ranger/joint_states', 10)
        
        # Subscriber for actuator data
        self.actuator_sub = self.create_subscription(
            ActuatorStateArray, 
            '/ranger/actuator_state', 
            self.actuator_callback, 
            10
        )
        
        # Timer to publish joint states regularly
        self.timer = self.create_timer(0.02, self.publish_joint_states)  # 50Hz
        
        # Joint state message template
        self.joint_state = JointState()
        self.joint_state.name = [
            'fr_steering_joint', 'rr_steering_joint', 'rl_steering_joint', 'fl_steering_joint',
            'fr_wheel',          'rr_wheel',          'rl_wheel',          'fl_wheel'
        ]
        self.joint_state.position = [0.0] * 8
        self.joint_state.velocity = [0.0] * 8
        self.joint_state.effort = [0.0] * 8
        
        # Store latest actuator data
        self.latest_actuator_data = None
        
        self.get_logger().info('Ranger Joint State Publisher started.')

    def actuator_callback(self, msg):
        """Callback for actuator state - contains motor angles and speeds"""
        self.latest_actuator_data = msg

    def publish_joint_states(self):
        """Publish joint states based on actuator data"""
        # Update timestamp
        self.joint_state.header.stamp = self.get_clock().now().to_msg()
        
        if self.latest_actuator_data is None:
            # No data yet, publish zeros
            self.joint_state_pub.publish(self.joint_state)
            return
        
        # === Steering joints (positions from motor_angles) ===
        steering_angles = [
            self.latest_actuator_data.motor_angles.angle_5,
            self.latest_actuator_data.motor_angles.angle_6,
            self.latest_actuator_data.motor_angles.angle_7,
            self.latest_actuator_data.motor_angles.angle_8 
        ]
        
        # Set steering positions directly (indices 0-3)
        for i in range(4):
            self.joint_state.position[i] = -steering_angles[i]
        
        # === Wheel joints (speeds and positions) ===
        # Raw wheel data (no sign processing here)
        wheel_speeds = [
            self.latest_actuator_data.motor_speeds.speed_1,
            self.latest_actuator_data.motor_speeds.speed_2,
            self.latest_actuator_data.motor_speeds.speed_3,
            self.latest_actuator_data.motor_speeds.speed_4
        ]
        
        # Unified sign processing for front/rear wheels
        wheel_signs = [1, 1, -1, -1]  # FR, FL normal; RR, RL inverted
        
        # Set wheel velocities (indices 4-7)
        for i in range(4):
            self.joint_state.velocity[i + 4] = wheel_speeds[i] * wheel_signs[i]
        
        # Set wheel positions from pulse counts
        wheel_pulses_per_radian = 1000.0  # Adjust based on encoder resolution
        for i in range(4):
            if len(self.latest_actuator_data.states) > i:
                pulse_count = self.latest_actuator_data.states[i].motor.pulse_count
                wheel_angle = pulse_count / wheel_pulses_per_radian * wheel_signs[i]
                self.joint_state.position[i + 4] = wheel_angle % (2 * math.pi)
        
        # === Optional: Set steering velocities from RPM ===
        rpm_to_rad_per_sec = 2 * math.pi / 60
        for i in range(4):
            if len(self.latest_actuator_data.states) > i + 4:
                steering_rpm = self.latest_actuator_data.states[i + 4].motor.rpm
                self.joint_state.velocity[i] = steering_rpm * rpm_to_rad_per_sec
        
        # Publish the joint state
        self.joint_state_pub.publish(self.joint_state)

def main(args=None):
    rclpy.init(args=args)
    node = RangerJointStatePublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
