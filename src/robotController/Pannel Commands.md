| SR. NO. | TAG NAME                              | MODBUS ADDRESS | COMMAND TYPE     | TAG TYPE | SOFTWARE ACTION |
| ------- | ------------------------------------- | -------------- | ---------------- | -------- | --------------- |
| 1       | Mode Selection (JOG / Auto)           | 50             | Coil Status      | Bool     | Read            |
| 2       | Jog Type Slection (Inch / Continuous) | 51             | Coil Status      | Bool     | Read/Write      |
| 3       | "+X" Axis Push Button                 | 52             | Coil Status      | Bool     | Read/Write      |
| 4       | "-X" Axis Push Button                 | 53             | Coil Status      | Bool     | Read/Write      |
| 5       | "+Y" Axis Push Button                 | 54             | Coil Status      | Bool     | Read/Write      |
| 6       | "-Y" Axis Push Button                 | 55             | Coil Status      | Bool     | Read/Write      |
| 7       | "+Z" Axis Push Button                 | 56             | Coil Status      | Bool     | Read/Write      |
| 8       | "-Z" Axis Push Button                 | 57             | Coil Status      | Bool     | Read/Write      |
| 9       | "+A" Axis Push Button                 | 58             | Coil Status      | Bool     | Read/Write      |
| 10      | "-A" Axis Push Button                 | 59             | Coil Status      | Bool     | Read/Write      |
| 11      | X Axis Homming Push Button            | 60             | Coil Status      | Bool     | Read/Write      |
| 12      | Y Axis Homming Push Button            | 61             | Coil Status      | Bool     | Read/Write      |
| 13      | Z Axis Homming Push Button            | 62             | Coil Status      | Bool     | Read/Write      |
| 14      | A Axis Homming Push Button            | 63             | Coil Status      | Bool     | Read/Write      |
| 15      | Cycle Start Push Button               | 64             | Coil Status      | Bool     | Read/Write      |
| 16      | Cycle Pause Push Button               | 65             | Coil Status      | Bool     | Read/Write      |
| 17      | Cycle Stop Push Button                | 66             | Coil Status      | Bool     | Read/Write      |
| 18      | Emergency Stop Push Button            | 67             | Coil Status      | Bool     | Read            |
| 19      | Jog Speed                             | 150            | Holding Registor | Real     | Read/Write      |
| 20      | X Axis Ref Position                   | 158            | Holding Registor | Real     | Read            |
| 21      | Y Axis Ref Position                   | 160            | Holding Registor | Real     | Read            |
| 22      | Z Axis Ref Position                   | 162            | Holding Registor | Real     | Read            |
| 23      | A Axis Ref Position                   | 164            | Holding Registor | Real     | Read            |
| 24      | Jog Step X                            | 166            | Holding Registor | Real     | Read/Write      |
| 25      | Jog Step Y                            | 168            | Holding Registor | Real     | Read/Write      |
| 26      | Jog Step Z                            | 170            | Holding Registor | Real     | Read/Write      |
| 27      | Jog Step A                            | 172            | Holding Registor | Real     | Read/Write      |