#!/usr/bin/env python3

import struct

f = open("Linearity.dat","rb")
b = f.read()
s = struct.unpack('d'*101,b)

print(s)
