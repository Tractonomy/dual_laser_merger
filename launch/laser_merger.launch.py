from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, LogInfo
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
    ThisLaunchFile,
)
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")

    # params for the landmark averaging/tracking node
    config_prefix = get_package_share_directory("dual_laser_merger")
    config_wanted = LaunchConfiguration("laser_merger_params_file_name")
    config_path = LaunchConfiguration("laser_merger_params_file_path")

    return LaunchDescription(
        [
            GroupAction(
                [
                    LogInfo(msg=["Launching ", ThisLaunchFile()]),
                    DeclareLaunchArgument(
                        "laser_merger_params_file_name",
                        default_value="dual_laser_merger.yaml",
                        description=(
                            "Select the yaml file that has the landmark poses for your map."
                            "Use the files from dual_laser_merger/config/** ."
                        ),
                    ),
                    DeclareLaunchArgument(
                        "laser_merger_params_file_path",
                        default_value=PathJoinSubstitution(
                            [
                                PathJoinSubstitution([config_prefix, "config"]),
                                config_wanted,
                            ]
                        ),
                        description=(
                            "Specify a yaml file path that has dual_laser_merger parameters."
                            "The 'laser_merger_params_file_name' argument will be ignored if this value is set."
                        ),
                    ),
                    ComposableNodeContainer(
                        name="laser_merger_container",
                        namespace="",
                        package="rclcpp_components",
                        executable="component_container",
                        composable_node_descriptions=[
                            ComposableNode(
                                package="dual_laser_merger",
                                plugin="merger_node::MergerNode",
                                name="dual_laser_merger_node",
                                parameters=[
                                    config_path,
                                    {"use_sim_time": use_sim_time},
                                ],
                            )
                        ],
                        output="screen",
                    ),
                ]
            )
        ]
    )
