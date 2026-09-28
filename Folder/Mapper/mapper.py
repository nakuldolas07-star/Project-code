import subprocess,sys,socket,ipaddress,platform,re
from concurrent.futures import ThreadPoolExecutor

me  =  ""

if len(sys.argv)>1 :
    net  =  sys.argv[1]
else :
    k  =  socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    try :
        k.connect(("8.8.8.8",80))
        me  =  k.getsockname()[0]
    except :
        me  =  "127.0.0.1"
    k.close()
    net  =  me+"/24"

try :
    n  =  ipaddress.ip_network(net,strict=False)
except :
    print("bad network, try something like 192.168.1.0/24")
    sys.exit()

if platform.system()  ==  "Windows" :
    c  =  ["ping","-n","1","-w","1000"]
else :
    c  =  ["ping","-c","1","-W","1"]

ports  =  [21,22,23,53,80,139,443,445,3389,8080]
up  =  {}

def check(ip) :
    ip  =  str(ip)
    r  =  subprocess.run(c+[ip] , stdout=subprocess.DEVNULL , stderr=subprocess.DEVNULL)
    if r.returncode  !=  0 :
        return
    try :
        name  =  socket.gethostbyaddr(ip)[0]
    except :
        name  =  ""
    op  =  []
    for p in ports :
        k  =  socket.socket()
        k.settimeout(0.3)
        if k.connect_ex((ip,p))  ==  0 :
            op.append(p)
        k.close()
    up[ip]  =  [name,op]

print("mapping",n,"...")

with ThreadPoolExecutor(100) as x :
    x.map(check , n.hosts())

macs  =  {}

try :
    a  =  subprocess.run(["arp","-a"] , capture_output=True , text=True).stdout
    for l in a.split("\n") :
        i  =  re.search(r"(\d+\.\d+\.\d+\.\d+)",l)
        m  =  re.search(r"([0-9a-fA-F]{1,2}[:-]){5}[0-9a-fA-F]{1,2}",l)
        if i and m :
            macs[i.group(1)]  =  m.group(0)
except :
    pass

print()
print("IP               MAC                NAME                OPEN PORTS")
print("-----------------------------------------------------------------")

for ip in sorted(up , key=ipaddress.ip_address) :
    nm  =  up[ip][0]  or  "-"
    mc  =  macs.get(ip,"-")
    pt  =  ",".join(str(p) for p in up[ip][1])  or  "-"
    tag  =  "  (you)"  if ip==me  else  ""
    print(ip.ljust(16),mc.ljust(18),nm[:19].ljust(19),pt+tag)

print()
print("done,",len(up),"hosts found")
