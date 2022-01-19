import kthread #pip install kthread
from time import sleep
import subprocess
import socket

def test():
    ip = []
    for ping in range(1, 10):
        address = "127.0.0." + str(ping)
        res = subprocess.call(['ping', '3', address])
        if res == 0:
            print("ping to", address, "OK")
            ip.add(address)
        elif res == 2:
            #print("no response from", address)
            pass
        else:
            pass
            #print("ping to", address, "failed!")
        return ip


def getips():
    ipadressen = {}
    def ping(ipadresse):
        try:
            outputcap = subprocess.run([f'ping', ipadresse, '-n', '1'], capture_output=True) #sends only one package, faster
            ipadressen[ipadresse] = outputcap
        except Exception as Fehler:
            print(Fehler)
    t = [kthread.KThread(target = ping, name = f"ipgetter{ipend}", args=(f'192.168.0.{ipend}',)) for ipend in range(255)] #prepares threads
    [kk.start() for kk in t] #starts 255 threads
    while len(ipadressen) < 255:
        print('Searching network')
        sleep(.3)
    alldevices = []
    for key, item in ipadressen.items():
        #print(ipadressen)
        if not 'unreachable' in item.stdout.decode('windows-1252') and 'failure' not in \
                item.stdout.decode('windows-1252') and 'perdus = 1' not in item.stdout.decode('windows-1252')\
                and item.returncode != 1: #checks if there wasn't neither general failure nor 'unrechable host'
            alldevices.append(key)
            print(item.returncode)
    return alldevices



def test2():
    print([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1])

#allips = getips() #takes 1.5 seconds on my pc
#allips = test()
#print(allips)

test2()