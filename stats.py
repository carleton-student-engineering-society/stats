import subprocess
from datetime import datetime

def rr(string: str) -> str:
    while "  " in string:
        string = string.replace("  ", " ")
    return string


host = subprocess.run(['hostname'], stdout=subprocess.PIPE).stdout.decode("utf-8").replace('\n','')

storage = subprocess.run(['df', '-h'], stdout=subprocess.PIPE)
first = True
cur = datetime.now()
timestamp = cur.strftime('%Y/%m/%d %H:%M:%S')

out = open("/var/backups/stats.csv", "a")

for line in storage.stdout.decode("utf-8").split('\n'):
    if first:
        first = False
        continue
    if not line:
        continue
    # time,hostname,DF,FS,size,used,avail,use%,mount
    out.write(timestamp + "," + host +",DF," + ",".join(rr(line).split(" ")) + "\n")

ram = subprocess.run(['free', '-h'], stdout=subprocess.PIPE)
rdata = rr(ram.stdout.decode("utf-8").split('\n')[1]).split(" ")
rdata[0] = "MEM"
# time,hostname,MEM,total,used,free,shared,cache,available

out.write(timestamp + "," + host + "," + ",".join(rdata) + "\n")

cpu = subprocess.run(['/root/stats/cpuusage.sh'], stdout=subprocess.PIPE).stdout.decode("utf-8").replace('\n','')
# time,hostname,CPU,percentage
out.write(timestamp + "," + host + ",CPU," + cpu + "%\n")

status = subprocess.run(['systemctl', 'status'], stdout=subprocess.PIPE).stdout.decode("utf-8").split('\n')[1]

# time,hostname,SERV,status (running,degraded,etc)
out.write(timestamp + "," + host + ",SERV," + status.split(":")[1][1:] + "\n")

out.close()

