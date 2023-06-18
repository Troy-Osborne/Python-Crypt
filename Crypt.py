from Key import RecursiveHashtoFile
from XOR import XOR_Crypt
from variablesizeheader import *
import os
#salt="Personal Salt Here".encode('UTF-8')  #use this salt for anything personal
##If you change the salt your version will be incompatible with any other that doesn't use the same salt
salt="Special Salt".encode('UTF-8')      #####use this salt for anything public
def make_not_exist(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
        return True
    else:
        return False
def encrypt_files(filelist,password,outname="outcrypt"):
    password=password.encode('UTF-8')
    ib=open('inputbytes','wb')
    ###make bytestream from files
    #alternatively do this by tar or 7zip
    KeySize=0
    for filename in filelist:
        #open file
        f=open(filename,'rb')
        #load bytes
        filebytes=f.read()
        ##Remove directories from filename
        raw_filename=os.path.basename(filename)
        towrite=pack("B",len(raw_filename))+raw_filename.encode('UTF-8')+pack_bytes_with_header(filebytes)
        ib.write(towrite)
        KeySize+=len(towrite)
    ib.close()
    print(KeySize)
    #KeySize=256*1024**2 #256 Mebibyte limit
    #KeySize=1024**2*4
    Keyfile="temp.key"
    RecursiveHashtoFile(password,password+salt,length=KeySize,filename="temp.key")
    a=XOR_Crypt("Keys/"+Keyfile)
    a.encryptfile('inputbytes',outname)
    #delete the keyfile
    del a
    os.remove("Keys/"+Keyfile)
    os.remove("inputbytes")
def split_bytesfile(file,unpack_directory='Unpack'):
    #check that unpack directory exists
    make_not_exist(unpack_directory)
        #if not make it

    f=open(file,'rb')
    while 1:
        try:
            namelen=unpack("B",f.read(1))[0]
        except:
            print("success")
            break
        name=f.read(namelen)
        print(name)
        head=f.read(8)
        length=unpack(">Q",head)[0] ##how many bytes did it take to write down the length of the data (8 bytes, big endian, max size larger than exibyte)
        lib=0#length_in_bytes
        mag=1
        for i in range(length): ##load that many bytes, magnitude of byte increases by 256 each time, smallest first.
            test=unpack("B",f.read(1))[0]
            lib+=test*mag
            mag*=256
        outfile=open(unpack_directory+"/"+name.decode('UTF-8'),"wb")
        outfile.write(f.read(lib))
        outfile.close()

def decrypt_files(crypt,password,unpack_directory='Unpack'):
    password=password.encode('UTF-8')
    ###update to make keysize proportional to cryptsize
    #KeySize=256*1024**2 #256 Mebibyte Key
    KeySize=os.stat(crypt).st_size
    Keyfile="temp.key"
    RecursiveHashtoFile(password,password+salt,length=KeySize,filename="temp.key")
    a=XOR_Crypt("Keys/"+Keyfile)
    outname="temp_decomp"
    a.encryptfile(crypt,outname)
    del a #free memory
    #split tempory file into separate files
    split_bytesfile("temp_decomp",unpack_directory)
    #delete tempory files
    os.remove("temp_decomp")
    os.remove("Keys/"+Keyfile)


def test(FileList):
    print("Enter Key")
    PW=input()
    outname="My_Test_Crypt"
    print ("test encryppting")
    encrypt_files(FileList,PW,outname)
    print ("test decrypting")
    decrypt_files(outname,PW)

def encrypt_directory(directory,password,outname=None):
    ##get filelist
    FileList=[directory+"\\"+i for i in os.listdir(directory)]
    if outname==None:
        outname=directory+"_crypt"
    encrypt_files(FileList,password,outname)

def UI(Caption,options):
        print(Caption)
        for i in options:
            print("%s : %s"%(i,options[i]))
        inp=''
        while not inp in options:
            inp=input()
        return inp

###If file is run directly open REPL
if __name__=='__main__':
    while 1:
        Task=UI("Choose a task:",{"0":"Encrypt File","1":"Encrypt Directory","2":"Decrypt","3":"Test","4":"Quit"})
        if Task=="4":
            quit()        
        elif Task=="3":
            print("runnning test")
            FileList=['ImageIn.png',"Key.py","Crypt.py"]  ###files to encrypt
            test(FileList)
        elif Task=="2":
            print("input key")
            PW=input()
            ####Decrypt
            print("Decrypt Which File")
            inname=input()
            decrypt_files(inname,PW)
        elif Task=="1":
            print("input key")
            PW=input()
            ####Encrypt
            print("Select a name for your output or leave blank for Test.Crypt")
            outname=input()
            if outname=="":
                outname="Test.Crypt"
            dirinp=None
            while dirinp==None or not os.path.exists(dirinp):
                print("Encrypt which file")
                dirinp=input()
            encrypt_directory(dirinp,PW,outname)
            inp=""
            while not (inp =="y" or inp=="n"):
                print("Run decryption test")
                inp=input()
            if inp.lower()=="y":
                decrypt_files(outname,PW)
        elif Task=="0":
            fileinp=None
            while fileinp==None or not os.path.exists(fileinp):
                print("Encrypt which file")
                fileinp=input()
            FileList=[fileinp]
            print("Enter Key")
            PW=input()
            outname=fileinp+".Crypt"
            encrypt_files(FileList,PW,outname)
            print ("Done")
