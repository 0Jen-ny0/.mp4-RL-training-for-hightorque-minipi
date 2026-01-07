import pathlib

HERE = pathlib.Path(__file__).parent
IK_CONFIG_ROOT = HERE / "ik_configs"
ASSET_ROOT = HERE / ".." / "assets"

ROBOT_XML_DICT = {
    # Add robot model
    "hightorque_minipi": ASSET_ROOT / "hightorque_minipi" / "urdf" / "hightorque_minipi.urdf",
}

IK_CONFIG_DICT = {
    # offline data
    "smplx":{
        # Add robot model
        "hightorque_minipi": IK_CONFIG_ROOT / "smplx_to_hightorque_minipi.json",
    },
}


ROBOT_BASE_DICT = {
    # Add robot model
    "hightorque_minipi": "base_link",
}

VIEWER_CAM_DISTANCE_DICT = {
    # Add robot model
    "hightorque_minipi": 2.0,
}