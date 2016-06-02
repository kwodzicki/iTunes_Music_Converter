#!/usr/bin/env python
def get_int_list(input, little=False):
	# input  : list of bytes to convert to bit string format
	# little : set if bytes are in little endian ordering
	if (little is True): 
		input = map( bin, bytearray(input[::-1]) )
	else:
		input = map( bin, bytearray(input) );
	return [int(i, 2) for i in input];
	
def get_last_bits(input, n, offset=0):
	# input  : one byte to get bits from
	# n      : Number of bits to get
	# offset : start point from left, i.e., 2^0 bit
	n = n + offset;
	return (input - ( (input >> n) << n)) >> offset;

def get_int(bits):
	# bits : list of bit strings to combine. 
	# Only works if last element is full 8-bits
	x = bits[0];                        # Initialize x
	for i in range(0,len(bits)-1):
		x = (x << 8) + bits[i+1];         # Shift x over 8 bits and add next 8 bits
	return x;                           # Return the number


def get_bit(int, size=None, little=False):
	# int  : integer to convert to bytes set by size 
	# size : Optional, set the number of bytes to be in the returned list
	if (int < 2**8):
		x = [int];
	elif (int < 2**16):
		x = [255, int >> 8];
	elif (int < 2**24):
		x = [255, 255, int >> 16];
	elif (int < 2**32):
		x = [255, 255, 255, int >> 24];
	if (size is not None):
		x.extend( [0]*(size - len(x)) );
	if (little is True):
		return x;
	else:
		return x[::-1];