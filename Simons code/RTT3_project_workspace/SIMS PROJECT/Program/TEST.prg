1 Servo On
2 C_Com(2)="ETH:127.0.0.1,10002"  'Setting the configrations of the communication line 2 (com2)
3 Open "COM2:" As #1              'Open the Com2
4 Dly 1                           'Delay in seconds
5 Ovrd 30
6 Accel 1,1                        '
7 Servo On                        'Setting Servo on
8 *loopStart
9 Input #1, P1.X,P1.Y,P1.Z        'Getting needed data through com2                   'Sending p1 through com2, reciveing it in py
10 Mov P1                         'Apply p1 as movment
11 Print #1, "MOVE COMPLETED"
12 GoSub *loopStart
13 End
P1=(+270.00,+0.00,+504.00)(,)
