# SNN_Project_code
code for the project
SNN DVS unsupervised

8.12
14 single3_1
15 single3_2
16 single3_4 time /10000 with max 1.4 can turn down max when reduce more time
17
18
19 change init -> 0.5 ideal training must keep! try to change th to 6 to see what will happen 

2
continue 19


3 th=6
32 3_4 0.4 1.5
33/34 3_4 25 more stable
35 3_5 seem that lane 1 more weak
36 3_5
40 3_10
50 3_17 th=7
51 3_16 th=6
60 sp 10
70 
71
tauPlus = 40
tauMinus = 30
aPlus = 0.02
aMinus = 0.010 
wMax = 0.4
wMaxInit = 0.07

'cm': 1,
'i_offset': 0.0,
'tau_m': 20.0,
'tau_refrac': 20.0,
'tau_syn_E': 2.0,
'tau_syn_I': 10.0,
'v_reset': -70.0,
'v_rest': -65.0,
'v_thresh': -50.0
72 73
aPlus = 0.024
wMaxInit = 0.08
74
tauPlus = 30
75
0.24 0.12
0.4 0.08
inhi -1

 cancel inhibtory at test max 1.0

sp different speed
th=7
0
trylabel=0
__delay__ = 1
tauPlus = 40
tauMinus = 20
aPlus = 0.024  
aMinus = 0.012 
wMax = 0.4
wMaxInit = 0.08
wMin = 0
inhibWeight = -1

trylabel=76
#def parameters
__delay__ = 1#0.250 # (ms) 
tauPlus = 40#25 #20 # 15 # 16.8 from literature
tauMinus = 20# #20 # 30 # 33.7 from literature
aPlus = 0.024  #tum 0.016 #9 #3 #0.5 # 0.03 from literature
aMinus = 0.012 #255 #tum 0.012 #2.55 #2.55 #05 #0.5 # 0.0255 (=0.03*0.85) from literature 
wMax = 0.36#1 #1 # G: 0.15 1
wMaxInit = 0.065#0.5#0.1#0.100
wMin = 0
nbIter = 5
testWeightFactor = 1#0.05177
x = 3 # no supervision for x first traj presentations
y = 0# for inside testing of traj to see if it has been learned /!\ stdp not disabled




11
0.6 0.3
0.4 1


13 0.6 0.3 
0.1 0.05
14 

trylabel=14
#def parameters
__delay__ = 1#0.250 # (ms) 
tauPlus = 100#25 #20 # 15 # 16.8 from literature
tauMinus = 300# #20 # 30 # 33.7 from literature
aPlus = 0.1 #tum 0.016 #9 #3 #0.5 # 0.03 from literature
aMinus = 0.1 #255 #tum 0.012 #2.55 #2.55 #05 #0.5 # 0.0255 (=0.03*0.85) from literature 
wMax = 0.6#1 #1 # G: 0.15 1
wMaxInit = 0.4#0.5#0.1#0.100
wMin = 0
nbIter = 5
testWeightFactor = 1#0.05177
x = 3 # no supervision for x first traj presentations
y = 0# for inside testing of traj to see if it has been learned /!\ stdp not disabled

input_len=32#y 30
input_class=32#x 3
input_size=input_len*input_class
output_size=9
inhibWeight = -1
stimWeight = 20

15 do not use

#trylabel=53
trylabel=15
#def parameters
__delay__ = 1#0.250 # (ms) 
tauPlus = 150#25 #20 # 15 # 16.8 from literature
tauMinus = 1000# #20 # 30 # 33.7 from literature
aPlus = 0.1 #tum 0.016 #9 #3 #0.5 # 0.03 from literature
aMinus = 0.1 #255 #tum 0.012 #2.55 #2.55 #05 #0.5 # 0.0255 (=0.03*0.85) from literature 
wMax = 0.4#1 #1 # G: 0.15 1
wMaxInit = 0.15#0.5#0.1#0.100
wMin = 0
nbIter = 5
testWeightFactor = 1#0.05177
x = 3 # no supervision for x first traj presentations
y = 0# for inside testing of traj to see if it has been learned /!\ stdp not disabled

input_len=32#y 30
input_class=32#x 3
input_size=input_len*input_class
output_size=9
inhibWeight = -0.1


cell_params_lif = {'cm': 1,#70
                   'i_offset': 0.0,
                   'tau_m': 200.0,#20
                   'tau_refrac': 150.0,#2 more that t inhibit#10
                   'tau_syn_E': 2.0,#2
                   'tau_syn_I': 100.0,#5
                   'v_reset': -70.0,
                   'v_rest': -65.0,
                   'v_thresh': -55.0
                   }
16



real
th=5
10 init 0.5
11 init 0.4
12 1 0.3
13 50 0.7 0.3
14 15 
45 0.7 0.3
16
t re 40
t in 20
muldependence
1.5 0.35
17

20190823 record AER data 
20-22 two way
24 four lanes
25 three lanes clear?


twoway
th=9
0.36 0.12
2
th=8
0.36 0.12
3
th=7
0.11

6
th=7
0.36 0.12
55
7
th=7
0.1 0.05
0.36 0.12
52.5
8
0.04 0.02
0.24 0.12
52.5
9
th=8
10
55

2019-08-12 18:02:21 WARNING: The delays in the connector AllToAllConnector from outputspikes to outputspikes was clipped to 1.0 a total of 72 times.  This can be avoided by reducing the timestep or increasing the minimum delay to one timestep
2019-08-12 18:02:21 WARNING: No multicast packets were sent by supersignal:0:8.  If you expected packets to be sent this could indicate an error
2019-08-12 18:02:21 WARNING: The reinjector on 0, 0 has detected that 25 packets were dumped from a core failing to take the packet. This often occurs when the executable has crashed or has not been given a multicast packet callback. It can also result from the core taking too long to process each packet. These packets were reinjected and so this number is likely a overestimate.
2019-08-12 18:46:01 WARNING: The last entry in the STDP exponential lookup table for the tau_plus parameter of the SpikePairRule between inputspikes:0:1023 and outputspikes:0:8 was 0.00146484375 rather than 0, indicating that the lookup table was not big enough at this timestep and value.  Try reducing the parameter value, or increasing the timestep