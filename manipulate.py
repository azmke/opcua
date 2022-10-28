import os

from netfilterqueue import NetfilterQueue

from scapy.all import *
from struct import *

from random import randint

print("[*] Adding iptables rule")
os.system("iptables -A OUTPUT -p tcp --sport 53530 -j NFQUEUE")

def callback(packet):

	print(packet)

	pkt = IP(packet.get_payload())
	
	tcp = pkt[TCP]
	
	data = raw(tcp.payload)
	
	if len(data) >= 104:

		message_type = data[0:4]
		service_id = unpack("<H", data[26:28])[0]
		
		if message_type == b"MSGF":
		
			if service_id == 829:
		
				print("[*] Patching value")
				
				value = unpack("<L", data[100:104])[0]
				print("Old value: {}".format(value))
				
				new_value = pack("<L", randint(0, 30))
				data = data[:100] + new_value + data[104:]
	
	tcp.load = data
	
	# recalculate checksum
	del pkt[TCP].chksum
	del pkt[IP].chksum
	
	packet.set_payload(bytes(pkt))

	packet.accept()
	return

print("[*] Binding NFQueue")
nfqueue = NetfilterQueue()
nfqueue.bind(0, callback)

try:
	print("[*] Waiting for data")
	nfqueue.run()
except KeyboardInterrupt:
	pass

print("[*] Unbinding NFQueue")
nfqueue.unbind()

print("[*] Flushing iptables")
os.system("iptables -F")
os.system("iptables -X")
