import psutil
import os
import socket   
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)

IPAddr = IPAddr.split(".")
IPAddr = IPAddr[0]+"."+IPAddr[1]


print("""
   _____                ____  ___.__          __   
  /  _  \   ____ ___.__.\   \/  /|__| _______/  |_ 
 /  /_\  \ /    <   |  | \     / |  |/  ___/\   __\\
/    |    \   |  \___  | /     \ |  |\___ \  |  |  
\____|__  /___|  / ____|/___/\  \|__/____  > |__|  
        \/     \/\/           \_/        \/        
> python anydesk ip grabber for windows
> made by n0nexist
""")




logfile = "ip-grabbati.txt"
process_name = "anydesk"
pidlist = list()
hostlist = list()

print("Looking for anydesk..")

for proc in psutil.process_iter():
    if process_name in proc.name().lower():
        pidlist.append(proc.pid)

if len(pidlist) == 0:
    print("ERROR: no open anydesk found")
    exit()
else:
    print("ANYDESK found: listening for connections (CNTRL-C to stop)")

while True:
    try:
        for x in os.popen("netstat -n -a -o").read().split("\n"):
            for y in pidlist:
                if str(y) in x and ("SYN_SENT" in x or "ESTABILISHED" in x) and ("UDP" not in x):
                    hostandport = x.split(":")
                    host = hostandport[1].split(" ")[-1]
                    port = hostandport[2].split(" ")[0]
                    if host not in hostlist:
                        hostlist.append(host)
                        print("\n"+("#"*20))
                        flag = ""
                        if host.startswith(IPAddr):
                            flag = "!! this may be your local ip address"
                        print(f"""NEW CONNECTION FOUND!
{flag}
info:
ip -> {host}
port -> {port}

process id -> {str(y)}""")
                        f = open(logfile,"a")
                        f.write("INFO:\nip: "+host+"\nport: "+port+"\nPID: "+str(y)+"\n\n")
                        f.close()
    except KeyboardInterrupt:
        print("\nCONTROL-C detected, exiting")
        exit()
