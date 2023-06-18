from hashlib import sha256
from time import time
class distribution:
    def __init__(self,size=256):
        self.size=size
        self.occurances=[0 for i in range(size)]
        self.count=0
    def addbytes(self,bytestring):
        length=len(bytestring)
        while bytestring!=b"":
            self.occurances[bytestring[0]]+=1
            bytestring=bytestring[1:]
        self.count+=length
    def addints(self,int_list):
        length=len(int_list)
        while int_list!=[]:
            self.occurances[int_list[0]]+=1
            int_list=int_list[1:]
        self.count+=length
    def graph_distribution(self):
        from matplotlib import pyplot as plt
        plt.plot(self.occurances)
        plt.show()


def RecursiveHash(startVal,salt,length=4096):
    ###Only for small keys,
    #the whole thing will be stored in the memory
    #for large keys make a key file
    Sha=sha256(salt+startVal)
    val=Sha.digest()
    o=val
    while len(o)<length:
        Sha.update(val+salt)
        val=Sha.digest()
        o+=val
    return o[:length]

def RecursiveHashtoFile(startVal,salt,filename="test.key",length=4096,distributioninst=distribution()):
    #length isn't exact, and for efficiency it will be rounded up to the nearest 32 bits
    Sha=sha256(salt+startVal)
    val=Sha.digest()
    fileout=open("Keys/"+filename,"wb")
    fileout.write(val)
    distributioninst.addbytes(val)
    n=32
    while n<length:
        Sha.update(val+salt)
        val=Sha.digest()
        distributioninst.addbytes(val)
        fileout.write(val)
        fileout.flush()
        n+=32
    return distributioninst
