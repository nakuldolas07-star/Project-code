import socket,sys
from concurrent.futures import ThreadPoolExecutor

if len(sys.argv)<2 :
    print("use it like:  python scan.py 127.0.0.1 1 1024")
    sys.exit()

t  =  sys.argv[1]
s  =  int(sys.argv[2])  if len(sys.argv)>2 else 1
e  =  int(sys.argv[3])  if len(sys.argv)>3 else 1024

try :
    ip  =  socket.gethostbyname(t)
except :
    print("cant find that host")
    sys.exit()

found  =  []

def scan(p) :
    k  =  socket.socket()
    k.settimeout(1)
    if k.connect_ex((ip,p))  ==  0 :
        b  =  b""
        try :
            b  =  k.recv(1024)
        except :
            pass
        if not b :
            try :
                k.send(b"HEAD / HTTP/1.0\r\n\r\n")
                b  =  k.recv(1024)
            except :
                pass
        b  =  b.decode(errors="ignore").strip().split("\n")[0]
        found.append( (p,b) )
    k.close()

print("scanning",ip,"ports",s,"to",e)

with ThreadPoolExecutor(100) as x :
    x.map(scan , range(s,e+1))

found.sort()

for p,b in found :
    print("[+]",p,"open   ",b)

print("done,",len(found),"open")
