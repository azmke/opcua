import os
import time

from netfilterqueue import NetfilterQueue

from scapy.all import *
from struct import *

from random import randint

SERVICE_ID = 829

INTERVAL = 1000

DELAY_0 = 30
DELAY_1 = 60

last_time = -1

print("[*] Adding iptables rule")
os.system("iptables -A INPUT -p tcp --sport 53530 -j NFQUEUE")

def callback(packet):

	global last_time

	print(packet)

	pkt = IP(packet.get_payload())
	tcp = pkt[TCP]
	data = raw(tcp.payload)
	
	if len(data) >= 104:

		message_type = data[0:4]
		service_id = unpack("<H", data[26:28])[0]

		if message_type == b"MSGF":

			if service_id == SERVICE_ID:

				if last_time > 0:
					
					delay = (pkt.time - last_time) * 1000 - INTERVAL
					print("Delay: {:.2f} ms".format(delay))

					if delay > DELAY_1:
						print("Detected: 1")
					elif delay > DELAY_0:
						print("Detected: 0")
				
				last_time = pkt.time
					
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
