from micropython import const
# 音符与对应的的频率
B0 = const(31)
C1 = const(33)
CS1 = const(35)
D1 = const(37)
DS1 = const(39)
E1 = const(41)
F1 = const(44)
FS1 = const(46)
G1 = const(49)
GS1 = const(52)
A1 = const(55)
AS1 = const(58)
B1 = const(62)
C2 = const(65)
CS2 = const(69)
D2 = const(73)
DS2 = const(78)
E2 = const(82)
F2 = const(87)
FS2 = const(93)
G2 = const(98)
GS2 = const(104)
A2 = const(110)
AS2 = const(117)
B2 = const(123)
C3 = const(131)
CS3 = const(139)
D3 = const(147)
DS3 = const(156)
E3 = const(165)
F3 = const(175)
FS3 = const(185)
G3 = const(196)
GS3 = const(208)
A3 = const(220)
AS3 = const(233)
B3 = const(247)
C4 = const(262)
CS4 = const(277)
D4 = const(294)
DS4 = const(311)
E4 = const(330)
F4 = const(349)
FS4 = const(370)
G4 = const(392)
GS4 = const(415)
A4 = const(440)
AS4 = const(466)
B4 = const(494)
C5 = const(523)
CS5 = const(554)
D5 = const(587)
DS5 = const(622)
E5 = const(659)
F5 = const(698)
FS5 = const(740)
G5 = const(784)
GS5 = const(831)
A5 = const(880)
AS5 = const(932)
B5 = const(988)
C6 = const(1047)
CS6 = const(1109)
D6 = const(1175)
DS6 = const(1245)
E6 = const(1319)
F6 = const(1397)
FS6 = const(1480)
G6 = const(1568)
GS6 = const(1661)
A6 = const(1760)
AS6 = const(1865)
B6 = const(1976)
C7 = const(2093)
CS7 = const(2217)
D7 = const(2349)
DS7 = const(2489)
E7 = const(2637)
F7 = const(2794)
FS7 = const(2960)
G7 = const(3136)
GS7 = const(3322)
A7 = const(3520)
AS7 = const(3729)
B7 = const(3951)
C8 = const(4186)
CS8 = const(4435)
D8 = const(4699)
DS8 = const(4978)

# 第一首，超级马里奥乐谱
mario = [
    E7, E7, 0, E7, 0, C7, E7, 0,
    G7, 0, 0, 0, G6, 0, 0, 0,
    C7, 0, 0, G6, 0, 0, E6, 0,
    0, A6, 0, B6, 0, AS6, A6, 0,
    G6, E7, 0, G7, A7, 0, F7, G7,
    0, E7, 0, C7, D7, B6, 0, 0,
    C7, 0, 0, G6, 0, 0, E6, 0,
    0, A6, 0, B6, 0, AS6, A6, 0,
    G6, E7, 0, G7, A7, 0, F7, G7,
    0, E7, 0, C7, D7, B6, 0, 0,
]

# 第二首，jingle bells
jingle = [
    E7, E7, E7, 0,
    E7, E7, E7, 0,
    E7, G7, C7, D7, E7, 0,
    F7, F7, F7, F7, F7, E7, E7, E7, E7, D7, D7, E7, D7, 0, G7, 0,
    E7, E7, E7, 0,
    E7, E7, E7, 0,
    E7, G7, C7, D7, E7, 0,
    F7, F7, F7, F7, F7, E7, E7, E7, G7, G7, F7, D7, C7, 0
]