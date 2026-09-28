import sys,re
from collections import Counter

f  =  sys.argv[1]  if len(sys.argv)>1  else  "/var/log/auth.log"

try :
    d  =  open(f , errors="ignore").read().split("\n")
except :
    print("cant open",f)
    sys.exit()

bad  =  Counter()
users  =  Counter()
inv  =  Counter()
sudo  =  Counter()
good  =  []

for l in d :
    m  =  re.search(r"Failed password for (?:invalid user )?(\S+) from (\S+)",l)
    if m :
        users[m.group(1)]  +=  1
        bad[m.group(2)]  +=  1
    m  =  re.search(r"Invalid user (\S+) from (\S+)",l)
    if m :
        inv[m.group(1)]  +=  1
    m  =  re.search(r"Accepted (\S+) for (\S+) from (\S+)",l)
    if m :
        good.append( l[:15]+"  "+m.group(2)+" from "+m.group(3)+" ("+m.group(1)+")" )
    m  =  re.search(r"sudo:\s+(\S+) : .*COMMAND=(.*)",l)
    if m :
        sudo[m.group(1)+"  ran  "+m.group(2)]  +=  1

print("file:",f)
print("lines:",len(d))
print()

print("== failed logins:",sum(bad.values()),"==")
for k,v in bad.most_common(5) :
    print("  ",k,"-",v)

print()
print("== usernames they tried ==")
for k,v in users.most_common(5) :
    print("  ",k,"-",v)

print()
print("== invalid users ==")
for k,v in inv.most_common(5) :
    print("  ",k,"-",v)

print()
print("== good logins:",len(good),"==")
for g in good[-5:] :
    print("  ",g)

print()
print("== sudo stuff ==")
for k,v in sudo.most_common(5) :
    print("  ",k,"-",v,"times")
