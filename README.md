# Reinforcement training for hightorque minipi via video input
## Overview
This repository adapts the GVHMR + GMR + BeyondMimic framework for half-body humanoid robotics. The page uses hightorque_minipi as robot model but can be adapted to other half robots. Any changes made to the original code will be documented as reference for other half body robots.

## GVHMR
Please refer to the [GVHMR](https://github.com/zju3dv/GVHMR) repository for environment setup and usage

An example can be downloaded [here]() and imported into `GVHMR/outputs/demo/{exercise}` folder

```bash
cd GVHMR
python tools/demo/demo.py --video=outputs/demo/{exercise}/{exercise}.mp4 -s
```
To play the outputted video:
```bash
ffplay outputs/demo/{exercise}/{exercise}_3_incam_global_horiz.mp4
```

The output will give you a hmr4d file a video like this.




## GMR
[GMR](https://github.com/YanjieZe/GMR)

## BeyondMimic
[BeyondMimic](https://github.com/HybridRobotics/whole_body_tracking)


## Third-party projects (credits)

This repository provides MiniPi-specific integration code and configs and depends on the following open-source projects:

- **GVHMR** (used for human motion reconstruction): https://github.com/zju3dv/GVHMR  
- **GMR** (used for retargeting): https://github.com/YanjieZe/GMR (MIT License)
- **whole_body_tracking / BeyondMimic** (used for RL tracking in IsaacLab): https://github.com/HybridRobotics/whole_body_tracking (MIT License)

These projects are installed separately and remain under their respective licenses. Users must comply with upstream licenses and any model/dataset licenses (e.g., SMPL/SMPL-X).
