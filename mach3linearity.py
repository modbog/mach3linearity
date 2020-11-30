#!/usr/bin/env python3

import csv
import math
import struct
import sys
import getopt

''' 
read our csv file and output list of ratios to binary
'''
def read_write(inputfile,outputfile):
    # import csv as a list of tuples
    with open(inputfile) as f:
        csv_data = [tuple(line) for line in csv.reader(f)]

    # cast values into int and create a tuple of (index,requested,observed)
    observed_min = 0
    observed_max = 0
    num_observations = 0
    requested_vs_observed=[]
    for line in csv_data: 
        (requested,observed) = line
        observed = int(observed)
        requested = int(requested)
        requested_vs_observed.append((num_observations,requested,observed))
        num_observations += 1

    if (observed < observed_min):
        observed_min=observed

    if (observed > observed_max):
        observed_max=observed

    '''
    we're not going to use the actual values measured..
    rather, we'll use the measured values as a basis for interpolation into 101 evenly distributed observations.
    first and last are already covered as min and max observations.
    so we need to calculate the other 99 evenly distributed observations based on our measurements
    '''

    observed_increment=(observed_max-observed_min)/99.0    
    # print(observed_increment)

    print("interpolating observed values")
    interpolated_values = [(0,observed_min,observed_min)]
    current_interpolation = observed_min
    interpolated_index = 0
    for entry in requested_vs_observed:
        (index,requested,observed) = entry
        next_index = index+1

        if (next_index >= num_observations):
            next_index = index

        (_ni,next_requested,next_observed) = requested_vs_observed[next_index]

        # compute the slope between this observation and the next one
        rise = (next_observed-observed)
        run = (next_requested-requested)
        if (run == 0):
            run = 1
        slope = rise / run
        # print("{5}: slope {0} ({3} / {4}) between {1} and {2}".format(slope,entry,requested_vs_observed[next_index],rise,run,index))

        # now that we know the slope between us and the next entry we can interpolate
        for i in range(math.ceil(run/observed_increment)+1):

            if (current_interpolation+observed_increment < next_requested):
                current_interpolation += observed_increment

                # we interpolate using the slope between observed and next_observed values
                interpolated_observation = observed+((current_interpolation-requested)*slope)
                # print("{0}: {1}, {2} to {3} [{4}]".format( i, current_interpolation, observed, next_observed, interpolated_observation ))
                # then append to interpolated_values our interpolated requested,observed values
                interpolated_index += 1
                interpolated_values.append( (interpolated_index, current_interpolation, interpolated_observation) )
            else:
                break

    interpolated_values.append( (interpolated_index+1, observed_max, observed_max) )

    print("creating linearity data")
    # massage data into one last list 
    linearity_data = []
    for (index, requested, observed) in interpolated_values:
        # print("{}: {}, {}".format(index, requested, observed))
        # find index of largest observed value _smaller_ than (<) requested value at current index
        _index = 0
        observed_value = 1
        next_observed_value = 1
        ratio = 1
        for (_i,_r,_o) in interpolated_values:
            # print("\t{}: looking for observed value [{}] < requested value [{}]".format(_i,_o,_r))
            if (_o > 0 and _o >= requested and _o >= observed):
                break
            # print("observed value {} _smaller_ than (<) requested value {}".format(_o,requested))
            if (_o < requested):
                observed_value = _o
                _index = _i
                (next_i,next_r,next_o) = interpolated_values[_i+1]
                next_observed_value=next_o
                next_value_delta = (next_observed_value - observed_value)
                if (next_value_delta == 0):
                    next_value_delta = 1
                ratio = (requested - observed_value) / next_value_delta
            # print("\tfinding request value {} that is smaller than {} (index:{})".format(r,_o,_i))

        linearity_data.append( (_index+ratio)/100 )
    
    # last entry should be at max
    # with some input the length of interpolated_values may be 100 instead of 101 (and possibly other numbers)
    # this could likely be improved with some tweaks of the interpolation code
    if (len(linearity_data) == 100):
        linearity_data.append(1.0)
    else:
        linearity_data[100] = 1.0

    # pack our linearity_data list into a .dat file as double precision
    print("writing {}".format(outputfile))
    out_file = open(outputfile,"wb")
    s = struct.pack('d'*len(linearity_data), *linearity_data)
    out_file.write(s)
    out_file.close()


def main(argv):
   inputfile = 'observed.csv'
   outputfile = 'Linearity.dat'
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('mach3_linearity.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('mach3linearity.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   print ("input csv file: {} output .dat file: {}".format(inputfile,outputfile))
   read_write(inputfile,outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
