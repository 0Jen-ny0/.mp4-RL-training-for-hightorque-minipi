import argparse
import pathlib
import os
import time
import pandas as pd
import glfw

import numpy as np

# Initialize GLFW
if not glfw.init():
    print("GLFW initialization failed!")
    raise Exception("GLFW could not be initialized")
else:
    print("GLFW initialized successfully.")
    

from general_motion_retargeting import GeneralMotionRetargeting as GMR
from general_motion_retargeting import RobotMotionViewer
from general_motion_retargeting.utils.smpl import load_gvhmr_pred_file, get_gvhmr_data_offline_fast

from rich import print



if __name__ == "__main__":
    
    HERE = pathlib.Path(__file__).parent

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gvhmr_pred_file",
        help="SMPLX motion file to load.",
        type=str,
        # required=True,
        default="/home/yanjieze/projects/g1_wbc/GMR/GVHMR/outputs/demo/tennis/hmr4d_results.pt",
    )
    
    parser.add_argument(
        "--robot",
        choices=["hightorque_minipi"],
        default="hightorque_minipi",
    )
    
    parser.add_argument(
        "--save_path",
        default=None,
        help="Path to save the robot motion.",
    )
    
    parser.add_argument(
        "--loop",
        default=False,
        action="store_true",
        help="Loop the motion.",
    )

    parser.add_argument(
        "--record_video",
        default=False,
        action="store_true",
        help="Record the video.",
    )

    parser.add_argument(
        "--rate_limit",
        default=False,
        action="store_true",
        help="Limit the rate of the retargeted robot motion to keep the same as the human motion.",
    )

    args = parser.parse_args()


    SMPLX_FOLDER = HERE / ".." / "assets" / "body_models"
    
    
    # Load SMPLX trajectory
    smplx_data, body_model, smplx_output, actual_human_height = load_gvhmr_pred_file(
        args.gvhmr_pred_file, SMPLX_FOLDER
    )
    
    # align fps
    tgt_fps = 30
    smplx_data_frames, aligned_fps = get_gvhmr_data_offline_fast(smplx_data, body_model, smplx_output, tgt_fps=tgt_fps)
    
    
   
    # Initialize the retargeting system
    retarget = GMR(
        actual_human_height=actual_human_height,
        src_human="smplx",
        tgt_robot=args.robot,
    )
    
    robot_motion_viewer = RobotMotionViewer(robot_type=args.robot,
                                            motion_fps=aligned_fps,
                                            transparent_robot=0,
                                            record_video=args.record_video,
                                            video_path=f"videos/{args.robot}_{args.gvhmr_pred_file.split('/')[-1].split('.')[0]}.mp4",)


    curr_frame = 0
    # FPS measurement variables
    fps_counter = 0
    fps_start_time = time.time()
    fps_display_interval = 2.0  # Display FPS every 2 seconds
    
    if args.save_path is not None:
        save_dir = os.path.dirname(args.save_path)
        if save_dir:  # Only create directory if it's not empty
            os.makedirs(save_dir, exist_ok=True)
        qpos_list = []
    
    # Start the viewer
    i = 0

    while True:
        if args.loop:
            i = (i + 1) % len(smplx_data_frames)
        else:
            i += 1
            if i >= len(smplx_data_frames):
                break
        
        # FPS measurement
        fps_counter += 1
        current_time = time.time()
        if current_time - fps_start_time >= fps_display_interval:
            actual_fps = fps_counter / (current_time - fps_start_time)
            print(f"Actual rendering FPS: {actual_fps:.2f}")
            fps_counter = 0
            fps_start_time = current_time
        
        # Update task targets.
        smplx_data = smplx_data_frames[i]

        # retarget
        qpos = retarget.retarget(smplx_data, offset_to_ground=True)


        # visualize
        robot_motion_viewer.step(
            root_pos=qpos[:3],
            root_rot=qpos[3:7],
            dof_pos=qpos[7:],
            human_motion_data=retarget.scaled_human_data,
            # human_motion_data=smplx_data,
            human_pos_offset=np.array([0.0, 0.0, 0.0]),
            show_human_body_name=True,
            rate_limit=args.rate_limit,
        )
        if args.save_path is not None:
            qpos_list.append(qpos)



    if args.save_path is not None:
        
        motion_data = {
            "root_pos_x": [],
            "root_pos_y": [],
            "root_pos_z": [],
            "root_rot_x": [],
            "root_rot_y": [],
            "root_rot_z": [],
            "root_rot_w": [],
            # MiniPi 12-DoF legs-only (adjust names if your URDF uses different joint names)
            "r_hip_pitch_joint": [],
            "r_hip_roll_joint": [],
            "r_thigh_joint": [],
            "r_calf_joint": [],
            "r_ankle_pitch_joint": [],
            "r_ankle_roll_joint": [],

            "l_hip_pitch_joint": [],
            "l_hip_roll_joint": [],
            "l_thigh_joint": [],
            "l_calf_joint": [],
            "l_ankle_pitch_joint": [],
            "l_ankle_roll_joint": [],
        }

        for i, qpos in enumerate(qpos_list):

            motion_data["root_pos_x"].append(qpos[0])
            motion_data["root_pos_y"].append(qpos[1])
            motion_data["root_pos_z"].append(qpos[2])

            motion_data["root_rot_x"].append(qpos[4])
            motion_data["root_rot_y"].append(qpos[5])
            motion_data["root_rot_z"].append(qpos[6])
            motion_data["root_rot_w"].append(qpos[3])

            motion_data["r_hip_pitch_joint"].append(qpos[7])
            motion_data["r_hip_roll_joint"].append(qpos[8])
            motion_data["r_thigh_joint"].append(qpos[9])
            motion_data["r_calf_joint"].append(qpos[10])
            motion_data["r_ankle_pitch_joint"].append(qpos[11])
            motion_data["r_ankle_roll_joint"].append(qpos[12])

            motion_data["l_hip_pitch_joint"].append(qpos[13])
            motion_data["l_hip_roll_joint"].append(qpos[14])
            motion_data["l_thigh_joint"].append(qpos[15])
            motion_data["l_calf_joint"].append(qpos[16])
            motion_data["l_ankle_pitch_joint"].append(qpos[17])
            motion_data["l_ankle_roll_joint"].append(qpos[18])

        # Remove the "frame" column from motion_data
        if "frame" in motion_data:
            del motion_data["frame"]

        # Convert motion_data dictionary to a DataFrame
        df = pd.DataFrame(motion_data)

        # Save the DataFrame to a CSV
        df.to_csv(args.save_path, header=False, index=False)


        print(f"Saved kinematic data to {args.save_path}")
            
    # Terminate GLFW at the end
    glfw.terminate()
    
    robot_motion_viewer.close()
