# mach3linearity
Generates the Mach3 spindle control macro "Linearity.dat" based on measured spindle speeds. This file can then be copied to the macros folder in the Mach3 profile being used.

Script takes two parameters, one for input .csv and one for output .dat:
`./mach3linearity.py -i observed.csv -o Linearity.dat`

To use the script, first create a comma separate values file that contains two columns. The first column should be requested RPMs in ascending order. And the second column should be the observed speed of the spindle for each input.

Below is an example using a 2.2kw spindle with a max speed of 24K RPM. For this example, PWM is translated to analog voltage input by the circuity in a Leadshine MX4660 drive (note that this calibration was required because the IC voltage drop of ~1.1V does not allow a full 10V signal so the max speed attained is 21,600 RPM. or 90% of 24,000)

I used a digital tachometer and the MDI controls in Mach3 to step through in intervals of 1000 from 1000 to the max of 21600 (e.g. `S1000 M3, S2000 M3, S3000 M3`) then recorded the values the tachometer displayed. 

observed.csv:

```
0,0
1000,0
2000,1456
3000,2480
4000,4095
5000,5419
6000,6745
7000,8076
8000,9411
9000,10745
10000,12080
11000,13416
12000,14748
13000,16088
14000,17416
15000,18756
16000,20100
17000,21443
18000,21555
19000,21555
20000,21555
21000,21555
21555,21555
```

You can use any interval you like, 1000 was plenty accurate for my machine. The observations after "Linearity.dat" was copied to macros folder in Mach3 were very close to the requested values.

**NB:** The last entry in your csv file should be the max observed spindle speed e.g. `24000,24000` or in the example above `21555,21555` **Without this entry you may see an IndexError.**

calibrated.csv

```
0,0
1000,0
1500,1505
2000,2006
3000,2998
4000,3993
5000,4991
6000,5999
7000,7003
8000,7992
9000,8998
10000,9993
11000,10992
12000,11993
13000,12998
14000,13998
15000,14992
16000,15998
17000,17000
18000,17998
19000,18990
20000,19996
21000,21299
21561,21584
```
