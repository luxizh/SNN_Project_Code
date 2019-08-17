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



2019-08-12 18:02:21 WARNING: The delays in the connector AllToAllConnector from outputspikes to outputspikes was clipped to 1.0 a total of 72 times.  This can be avoided by reducing the timestep or increasing the minimum delay to one timestep
2019-08-12 18:02:21 WARNING: No multicast packets were sent by supersignal:0:8.  If you expected packets to be sent this could indicate an error
2019-08-12 18:02:21 WARNING: The reinjector on 0, 0 has detected that 25 packets were dumped from a core failing to take the packet. This often occurs when the executable has crashed or has not been given a multicast packet callback. It can also result from the core taking too long to process each packet. These packets were reinjected and so this number is likely a overestimate.
2019-08-12 18:46:01 WARNING: The last entry in the STDP exponential lookup table for the tau_plus parameter of the SpikePairRule between inputspikes:0:1023 and outputspikes:0:8 was 0.00146484375 rather than 0, indicating that the lookup table was not big enough at this timestep and value.  Try reducing the parameter value, or increasing the timestep