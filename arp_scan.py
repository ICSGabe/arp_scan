from scapy.all import ARP, Ether, srp
from mac_vendor_lookup import MacLookup
import pyfiglet

ascii_banner = pyfiglet.figlet_format("ICS_Gabe")
print(ascii_banner)


#IP Address for the destination subnet. 
#print("Enter subnet: ") 
#target_ip = input()

target_ip = input("Enter Subnet or IP Address: ")
print("Let's see what's lurking on this network :)")

# you can modify this to preset the IP address
#target_ip = '192.168.0.0/24'

# creation of ethernet broadcast packet ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
arp = ARP(pdst=target_ip)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")

# stack layers 
packet = ether/arp

# you can increase timeout value for more accurate results. The srp() method in scapy returns a (sent_packet, received_packet) pair
result = srp(packet, timeout=3)[0]

# create an empty list to populate with clients
clients = []
try:
    for sent, received in result:
        # for each response, append the dictionary of ip, mac, and vendor to clients list
        clients.append({'ip': received.psrc, 'mac': received.hwsrc,'vendors': MacLookup().lookup(received.hwsrc)})

# the MacLookup module throws a KeyError if it does not recognize the mac address of some vendors. go here if you want to more info on the solution: https://github.com/bauerj/mac_vendor_lookup/issues/3
# this except just keeps the program trucking along when the KeyError rears its ugly head and output Vendor Unknownm for the host
except KeyError:
    clients.append({'ip': received.psrc, 'mac': received.hwsrc,'vendors':'Vendor Unknown'})
    pass
    
print("Available devices in the network:")
print("IP" + " "*18+"MAC" + " "*18+"VENDOR")
for client in clients:
    print("{:16}    {}    {}".format(client['ip'], client['mac'], client['vendors']))


