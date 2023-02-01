import argparse
import sys
import os

import json
import numpy as np
import matplotlib.pyplot as plt

from object_ids import object_ids

def get_packets_num(packets):
	return len(packets)

# Packet lenght

def get_packet_lengths(packets):
	return np.array([packet["_source"]["layers"]["frame"]["frame.len"] for packet in packets], dtype=int)

def get_length_min(packets):
	arr = get_packet_lengths(packets)
	return np.min(arr)

def get_length_max(packets):
	arr = get_packet_lengths(packets)
	return np.max(arr)

def get_length_avg(packets):
	arr = get_packet_lengths(packets)
	return np.average(arr)

def get_length_var(packets):
	arr = get_packet_lengths(packets)
	return np.var(arr)

def get_length_std(packets):
	arr = get_packet_lengths(packets)
	return np.std(arr)

def show_length_hist(packets):
	arr = get_packet_lengths(packets)
	plt.hist(arr, bins=20)
	plt.title("Packet lenghts")
	plt.show()

# Packet delay

def get_packet_delays(packets):
	timestamps = np.array([packet["_source"]["layers"]["frame"]["frame.time_epoch"] for packet in packets], dtype=float)
	delays = np.diff(timestamps)
	# convert to milliseconds
	delays = np.multiply(delays, 1000)
	return delays

def get_delay_min(packets):
	arr = get_packet_delays(packets)
	return np.min(arr)

def get_delay_max(packets):
	arr = get_packet_delays(packets)
	return np.max(arr)

def get_delay_avg(packets):
	arr = get_packet_delays(packets)
	return np.average(arr)

def get_delay_var(packets):
	arr = get_packet_delays(packets)
	return np.var(arr)

def get_delay_std(packets):
	arr = get_packet_delays(packets)
	return np.std(arr)

def show_delay_hist(packets):
	arr = get_packet_delays(packets)
	plt.hist(arr, bins=20)
	plt.title("Packet delays")
	plt.show()

def get_bandwidth_min(packets):
	# 1 Bit / Packet
	# Result: Bytes/s
	return 1 / (get_delay_max(packets) or 1) * 1000 / 8

def get_bandwidth_max(packets):
	# 1 Bit/Packet
	# Result: Bytes/s
	return 1 / (get_delay_min(packets) or 1) * 1000 / 8

# OPC UA Services

def get_services(packets):
	service_ids = []

	for packet in packets:
		layers = packet["_source"]["layers"]

		if "opcua" in layers:
			if "OpcUa Service : Encodeable Object" in layers["opcua"]:
				if "TypeId : ExpandedNodeId" in layers["opcua"]["OpcUa Service : Encodeable Object"]:
					service_id = int(layers["opcua"]["OpcUa Service : Encodeable Object"]["TypeId : ExpandedNodeId"]["opcua.servicenodeid.numeric"])
					
					if service_id not in service_ids:
						service_ids.append(service_id)

	return service_ids

def process_json(file_name):

	# open json file
	file = open(file_name, "r")

	# convert json object to a python object
	packets = json.load(file)

	print("= [ Packet length ] =")
	print("Minimum:		{}".format(get_length_min(packets)))
	print("Maximum:		{}".format(get_length_max(packets)))
	print("Average:		{:.2f}".format(get_length_avg(packets)))
	print("Variance:		{:.2f}".format(get_length_var(packets)))
	print("Standard Deviation:	{:.2f}".format(get_length_std(packets)))
	print("")

	show_length_hist(packets)

	print("= [ Interpacket Times ] =")
	print("Minimum:		{:.0f} ms".format(get_delay_min(packets)))
	print("Maximum:		{:.0f} ms".format(get_delay_max(packets)))
	print("Average:		{:.2f} ms".format(get_delay_avg(packets)))
	print("Variance:		{:.2f}".format(get_delay_var(packets)))
	print("Standard Deviation:	{:.2f}".format(get_delay_std(packets)))
	print("")
	print("Min. Bandwidth:	{:.2f} B/s".format(get_bandwidth_min(packets)))
	print("Max. Bandwidth:	{:.2f} B/s".format(get_bandwidth_max(packets)))
	print("")

	show_delay_hist(packets)

	print("= [ OPC UA Services ] =")

	services = get_services(packets)
	for service in services:
		print("{}: {}".format(service, object_ids[service].replace("_Encoding_DefaultBinary", "")))

	# close file
	file.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='OPCUA Network Traffic Analysis (ONTA)')
	parser.add_argument('--file', metavar='<file name>',
						help='wireshark json export to parse', required=True)
	args = parser.parse_args()

	file_name = args.file
	if not os.path.isfile(file_name):
		print('"{}" does not exist'.format(file_name), file=sys.stderr)
		sys.exit(-1)

	process_json(file_name)
	sys.exit(0)