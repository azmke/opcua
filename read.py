import argparse
import sys
import os

from scapy.all import *
from struct import *

def process_pcap(file_name):
	print('Opening {}...'.format(file_name))
	packets = rdpcap(file_name)

	for packet in packets:

		data = raw(packet[TCP].payload)

		print(data)

		# Message Header

		message_header = data[0:12]

		message_type        = message_header[0:3]
		is_final            = message_header[3:4]
		message_size        = unpack("<L", message_header[4:8])[0]
		secure_channel_id   = unpack("<L", message_header[8:12])[0]

		print("Message Type: {}".format(message_type))
		print("Is Final: {}".format(is_final))
		print(message_size)
		print(secure_channel_id)

		# Security Header

		security_header = data[12:16]

		token_id = unpack("<L", security_header[0:4])[0]

		print(token_id)

		# Sequence Header

		sequence_header = data[16:24]

		sequence_number = unpack("<L", sequence_header[0:4])[0]
		request_id = unpack("<L", sequence_header[4:8])[0]

		print(sequence_number)
		print(request_id)

		# Node id

		node_id = data[24:28]

		encoding_mask = unpack("B", node_id[0:1])[0]
		namespace_index = unpack("B", node_id[1:2])[0]
		identifier_numeric = unpack("<H", node_id[2:4])[0]

		print(encoding_mask)
		print(namespace_index)
		print(identifier_numeric)

		if identifier_numeric != 829:
			continue

		# insert new value
		new_value = pack("<L", 23)
		data = data[0:100] + new_value + data[104:]

		value = unpack("<L", data[100:104])[0]
		print("Value: {}".format(value))

		#break


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='PCAP reader')
	parser.add_argument('--pcap', metavar='<pcap file name>',
						help='pcap file to parse', required=True)
	args = parser.parse_args()

	file_name = args.pcap
	if not os.path.isfile(file_name):
		print('"{}" does not exist'.format(file_name), file=sys.stderr)
		sys.exit(-1)

	process_pcap(file_name)
	sys.exit(0)