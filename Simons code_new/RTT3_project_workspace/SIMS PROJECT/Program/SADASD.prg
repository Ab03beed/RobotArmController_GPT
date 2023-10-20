1 Close #1
2 Dly 1
3 Open "COM2:" As #1 ' Open as communication lne COM3
4 *StateLoop
5 Input #1,DATA,DATA1
6 If DATA=20 Then GoSub *ServoOn'
7 GoTo *StateLoop
8 *ServoOn
9 Servo On
10 Dly 1
11 If M_Svo=1 Then
12 Print #1,"22"
13 Print #1,"ServoOn"
14 EndIf
15 Return
