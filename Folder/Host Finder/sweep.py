import subprocess,sys,socket,ipaddress,platform
from concurrent.futures import ThreadPoolExecutor

if len(sys.argv)<2 :
    print("use it like:  python sweep.py 192.168.1.0/24")
    sys.exit()

try :
    n  =  ipaddress.ip_network(sys.argv[1],strict=False)
except :
    print("bad network, try something like 192.168.1.0/24")
    sys.exit()

if platform.system()  ==  "Windows" :
    c  =  ["ping","-n","1","-w","1000"]
else :
    c  =  ["ping","-c","1","-W","1"]

up  =  []

def check(ip) :
    ip  =  str(ip)
    r  =  subprocess.run(c+[ip] , stdout=subprocess.DEVNULL , stderr=subprocess.DEVNULL)
    if r.returncode  ==  0 :
        try :
            name  =  socket.gethostbyaddr(ip)[0]
        except :
            name  =  ""
        up.append( (ipaddress.ip_address(ip),name) )

print("sweeping",n,"...")

with ThreadPoolExecutor(100) as x :
    x.map(check , n.hosts())

up.sort()

for ip,name in up :
    print("[+]",ip,"is up   ",name)

print("done,",len(up),"hosts up")
