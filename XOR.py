from time import time
def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

class XOR_Crypt:
    def __init__(self,keyfile):
        self.keyfile=keyfile
    def encrypt(self,bytestream):
        CHUNKSIZE=1024
        out=b""
        file=open(self.keyfile,'rb')
        while 1:
            if len(bytestream)<CHUNKSIZE:
                #last chunk
                chunk=file.read(len(bytestream))
                out+=byte_xor(chunk,bytestream)
                return out
            else:
                chunk=file.read(CHUNKSIZE)
                out+=byte_xor(chunk,bytestream)
    def encryptfile(self,filename,outputname=None):
        if outputname==None:
            outputname=filename+"_encrypted"
        ##Key File must be larger than the Input File
        CHUNKSIZE=1024
        file=open(self.keyfile,'rb')
        infile=open(filename,'rb')
        outfile=open(outputname,'wb')
        while 1:
            #load file 1024 bytes at a time.
            bytestream=infile.read(CHUNKSIZE)
            if len(bytestream)<CHUNKSIZE:
                #last chunk
                chunk=file.read(len(bytestream))
                outfile.write(byte_xor(chunk,bytestream))
                outfile.flush()
                break
            else:
                chunk=file.read(CHUNKSIZE)
                outfile.write(byte_xor(chunk,bytestream))
                outfile.flush()
"""                
#Initialise the crypter class with your key. It must be larger than what you're encrypting.
a=XOR_Crypt("./Keys/Keyname.key")
#record the current time
t=time()
#encrypt a file with the initialised crypter class
a.encryptfile("ImageIn.png","outcrypt")
#use the same crypter to decrypt the encrypted file, it will return your original
a.encryptfile("outcrypt","decrypted.png")
#record the time upon completion
t2=time()
#print the total ellapsed time.
print("Took %s seconds" %round(t2-t,4))
"""
