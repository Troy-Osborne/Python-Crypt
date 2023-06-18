from math import log,ceil,pi,sqrt
from struct import pack,unpack
def make_dynamic_length_header(Length_In_Bytes=10240):
    number_of_characters=ceil(log(Length_In_Bytes+1,256))
    packedhead=pack(">Q",number_of_characters)  #first eight bytes encode how many more bytes would be needed to write down the length of your stream. (Packed big endian)
    remainder=Length_In_Bytes
    while remainder:#loop to write down the length of the stream, in base_256
        test=pack("B",remainder%256)
        packedhead+=test
        remainder=int(remainder/256)
    return packedhead

def read_dynamic_length_header(inbytes):
    head=inbytes[0:8]
    length=unpack(">Q",inbytes[0:8])[0] ##how many bytes did it take to write down the length of the data (8 bytes, big endian, max size larger than exibyte)
    lib=0#length_in_bytes
    mag=1
    for i in range(length): ##load that many bytes, magnitude of byte increases by 256 each time, smallest first.
        test=unpack("B",inbytes[8+i:9+i])[0]
        lib+=test*mag
        mag*=256
    return length,inbytes[9+i:]

def pack_bytes_with_header(b):
    return make_dynamic_length_header(len(b))+b
def unpack_bytes_with_header(b):
    return read_dynamic_length_header(b)

def random_megabyte():
    from random import random
    b=b""
    for i in range(1024**2):
        b+=pack("B",int(random()*256))
    return b

"""
KB=1024
MB=1024**2
GB=1024**3
TB=1024**4

####TESTS#######
TestSize1=1*KB
TestSize2=1*MB+50*KB
TestSize3=1*TB+50*GB
a=make_dynamic_length_header(TestSize1)
b=make_dynamic_length_header(TestSize2)
c=make_dynamic_length_header(TestSize3)

print(a)
print(read_dynamic_length_header(a))

testin=random_megabyte()
packed=pack_bytes_with_header(testin)
#print(packed)
unpacked=unpack_bytes_with_header(packed)
#print(unpacked)
print(testin==unpacked[1])
##################
"""
