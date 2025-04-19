# Modbus command constants and functions for CNC machine control

# Command definitions based on Pannel Commands.md and Axis Data.md
COMMANDS = {
    "Mode Selection (JOG / Auto)": {"address": 50, "type": "coil", "action": "read", "tag": "mode"},
    "Jog Type Selection (Inch / Continuous)": {"address": 51, "type": "coil", "action": "read_write", "tag": "jog_type"},
    "+X Axis Push Button": {"address": 52, "type": "coil", "action": "read_write", "tag": "x_axis"},
    "-X Axis Push Button": {"address": 53, "type": "coil", "action": "read_write", "tag": "x_axis"},
    "+Y Axis Push Button": {"address": 54, "type": "coil", "action": "read_write", "tag": "y_axis"},
    "-Y Axis Push Button": {"address": 55, "type": "coil", "action": "read_write", "tag": "y_axis"},
    "+Z Axis Push Button": {"address": 56, "type": "coil", "action": "read_write", "tag": "z_axis"},
    "-Z Axis Push Button": {"address": 57, "type": "coil", "action": "read_write", "tag": "z_axis"},
    "+A Axis Push Button": {"address": 58, "type": "coil", "action": "read_write", "tag": "a_axis"},
    "-A Axis Push Button": {"address": 59, "type": "coil", "action": "read_write", "tag": "a_axis"},
    "X Axis Homming Push Button": {"address": 60, "type": "coil", "action": "read_write", "tag": "x_axis_homing"},
    "Y Axis Homming Push Button": {"address": 61, "type": "coil", "action": "read_write", "tag": "y_axis_homing"},
    "Z Axis Homming Push Button": {"address": 62, "type": "coil", "action": "read_write", "tag": "z_axis_homing"},
    "A Axis Homming Push Button": {"address": 63, "type": "coil", "action": "read_write", "tag": "a_axis_homing"},
    "Cycle Start Push Button": {"address": 64, "type": "coil", "action": "read_write", "tag": "cycle_start"},
    "Cycle Pause Push Button": {"address": 65, "type": "coil", "action": "read_write", "tag": "cycle_pause"},
    "Cycle Stop Push Button": {"address": 66, "type": "coil", "action": "read_write", "tag": "cycle_stop"},
    "Emergency Stop Push Button": {"address": 67, "type": "coil", "action": "read", "tag": "emergency_stop"},
    "Jog Speed": {"address": 150, "type": "holding", "action": "read_write", "tag": "jog_speed"},
    "X Axis Ref Position": {"address": 158, "type": "holding", "action": "read", "tag": "x_axis_ref"},
    "Y Axis Ref Position": {"address": 160, "type": "holding", "action": "read", "tag": "y_axis_ref"},
    "Z Axis Ref Position": {"address": 162, "type": "holding", "action": "read", "tag": "z_axis_ref"},
    "A Axis Ref Position": {"address": 164, "type": "holding", "action": "read", "tag": "a_axis_ref"},
    "Jog Step X": {"address": 166, "type": "holding", "action": "read_write", "tag": "jog_step_x"},
    "Jog Step Y": {"address": 168, "type": "holding", "action": "read_write", "tag": "jog_step_y"},
    "Jog Step Z": {"address": 170, "type": "holding", "action": "read_write", "tag": "jog_step_z"},
    "Jog Step A": {"address": 172, "type": "holding", "action": "read_write", "tag": "jog_step_a"},
    "X Axis Live Position": {"address": 0, "type": "holding", "tag_type": "Real", "action": "read"},
    "Y Axis Live Position": {"address": 2, "type": "holding", "tag_type": "Real", "action": "read"},
    "Z Axis Live Position": {"address": 4, "type": "holding", "tag_type": "Real", "action": "read"},
    "A Axis Live Position": {"address": 6, "type": "holding", "tag_type": "Real", "action": "read"},
    "Probe X Sense Bit": {"address": 100, "type": "coil", "tag_type": "Bool", "action": "read"},
    "Probe Y Sense Bit": {"address": 101, "type": "coil", "tag_type": "Bool", "action": "read"},
    "Probe Z Sense Bit": {"address": 102, "type": "coil", "tag_type": "Bool", "action": "read"},
    "Probe A Sensor Bit": {"address": 103, "type": "coil", "tag_type": "Bool", "action": "read"},
    "X Homed State": {"address": 104, "type": "coil", "tag_type": "Bool", "action": "read"},
    "Y Homed State": {"address": 105, "type": "coil", "tag_type": "Bool", "action": "read"},
    "Z Homed State": {"address": 106, "type": "coil", "tag_type": "Bool", "action": "read"},
    "A Homed State": {"address": 107, "type": "coil", "tag_type": "Bool", "action": "read"},
    # Add more Axis Data commands as needed...
    
    # Add missing G92 offsets
    "G92_X offset": {"address": 166, "type": "holding", "tag_type": "Real", "action": "read"},
    "G92_Y offset": {"address": 168, "type": "holding", "tag_type": "Real", "action": "read"},
    "G92_Z offset": {"address": 170, "type": "holding", "tag_type": "Real", "action": "read"},
    "G92_A offset": {"address": 172, "type": "holding", "tag_type": "Real", "action": "read"},
    
    # Add G5x offsets
    "G5x_X offset": {"address": 174, "type": "holding", "tag_type": "Real", "action": "read"},
    "G5x_Y offset": {"address": 176, "type": "holding", "tag_type": "Real", "action": "read"},
    "G5x_Z offset": {"address": 178, "type": "holding", "tag_type": "Real", "action": "read"},
    "G5x_A offset": {"address": 180, "type": "holding", "tag_type": "Real", "action": "read"},
    
    # Add G43 offsets
    "G43_X offset": {"address": 182, "type": "holding", "tag_type": "Real", "action": "read"},
    "G43_Y offset": {"address": 184, "type": "holding", "tag_type": "Real", "action": "read"},
    "G43_Z offset": {"address": 186, "type": "holding", "tag_type": "Real", "action": "read"},
    "G43_A offset": {"address": 188, "type": "holding", "tag_type": "Real", "action": "read"},
    
    # Add HAL version
    "HAL VERSION NO": {"address": 196, "type": "holding", "tag_type": "Real", "action": "read"},
}

def reset_bits(modbus_client):
    """Reset all command bits after sending a command."""
    for command in COMMANDS.values():
        if command["type"] == "coil":
            modbus_client.send_command(command["address"], False)

# Add helper functions for data type conversion
def convert_to_real(registers):
    """Convert two consecutive registers to a real number."""
    if len(registers) != 2:
        raise ValueError("Real numbers require two registers")
    return float(registers[0] | (registers[1] << 16))

def convert_to_int32(registers):
    """Convert two consecutive registers to a 32-bit integer."""
    if len(registers) != 2:
        raise ValueError("32-bit integers require two registers")
    return registers[0] | (registers[1] << 16)