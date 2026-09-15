## 50221 -> 9090 [PSH, ACK] 

Raw hex: 0000   18 00 00 00 60 0e 43 06 00 86 06 80 00 00 00 00   ....`.C.........
0010   00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00   ................
0020   00 00 00 00 00 00 00 00 00 00 00 01 c4 2d 23 82   .............-#.
0030   b6 4a 76 a9 81 93 50 be 50 18 00 ff 6a bc 00 00   .Jv...P.P...j...
0040   50 59 52 4f 01 f6 01 01 00 00 00 00 00 00 00 4a   PYRO...........J
0050   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0060   00 00 00 00 00 00 4d c5 23 20 73 65 72 70 65 6e   ......M.# serpen
0070   74 20 75 74 66 2d 38 20 70 79 74 68 6f 6e 33 2e   t utf-8 python3.
0080   32 0a 7b 27 68 61 6e 64 73 68 61 6b 65 27 3a 27   2.{'handshake':'
0090   68 65 6c 6c 6f 27 2c 27 6f 62 6a 65 63 74 27 3a   hello','object':
00a0   27 50 79 72 6f 2e 4e 61 6d 65 53 65 72 76 65 72   'Pyro.NameServer
00b0   27 7d                                             '}

Payload decoded : #serpant utf-8 python3.2 {'hand shake':'hello',' object' : 'Pyro.Na meServer'}

This is the Python dict with two keys: 'handshake' with value: 'hello' and 'object' 
as well as the value: 'Pyro.NameServer'.