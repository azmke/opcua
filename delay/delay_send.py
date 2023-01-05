import os
import time

from netfilterqueue import NetfilterQueue

from scapy.all import *
from struct import *

from random import randint

SERVICE_ID = 829

DELAY_0 = 30
DELAY_1 = 60

MESSAGE = "1101011011101111011111000011010110100000111110111000101110101110011011001101"

def generator():
	for c in MESSAGE:
		yield(c)

message_gen = generator()
next_char = next(message_gen, "")

wait = False

print("[*] Adding iptables rule")
os.system("iptables -A OUTPUT -p tcp --sport 53530 -j NFQUEUE")

def callback(packet):

	global wait
	global next_char

	print(packet)

	pkt = IP(packet.get_payload())
	tcp = pkt[TCP]
	data = raw(tcp.payload)
	
	if len(data) >= 104:

		message_type = data[0:4]
		service_id = unpack("<H", data[26:28])[0]

		if message_type == b"MSGF":

			if service_id == SERVICE_ID:

				if wait:
					print("{}: Waiting")
					wait = False

				elif next_char == "0":
					print("{}: Packet service id {} - Delay {} ms".format(next_char, SERVICE_ID, DELAY_0))

					next_char = next(message_gen, "")
					wait = True
					time.sleep(DELAY_0 / 1000)

				elif next_char == "1":
					print("{}: Packet service id {} - Delay {} ms".format(next_char, SERVICE_ID, DELAY_1))

					next_char = next(message_gen, "")
					wait = True
					time.sleep(DELAY_1 / 1000)

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
