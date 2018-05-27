#!/usr/bin/env python

import array
import sys
from ola.ClientWrapper import ClientWrapper

class pixel_multiplier(object):

	class universe_listener(object):
		
		class universe_sender(object):
			
			def __init__(self, universe, pixel_groups):
				self.universe = universe
				self.pixel_groups = [group for group in pixel_groups if group.destination_universe == universe]
				self.pixel_groups.sort()

			def __lt__(self, other):
				return self.universe < other.universe

			def generate_frame(self, received_frame):
				new_frame = array.array('B')
				for group in self.pixel_groups:
					new_frame.extend((group.destination_offset - len(new_frame)) * [0])
					pixel = received_frame[group.source_offset : group.source_offset + 3]
					new_frame.extend(pixel * group.number_of_pixels)
				return new_frame

		def __init__(self, universe, pixel_groups, ola_client):
			self.universe = universe
			self.ola_client = ola_client
			self.pixel_groups = [group for group in pixel_groups if group.source_universe == universe]
			self.destination_universes = {group.destination_universe for group in self.pixel_groups}
			self.senders = [self.universe_sender(u, self.pixel_groups) for u in self.destination_universes]
			self.senders.sort()
			ola_client.RegisterUniverse(universe, ola_client.REGISTER, self.frame_received)

			def __lt__(self, other):
				return self.universe < other.universe

		def frame_received(self, received_frame):
			
			def frame_sent(state):
				pass

			for sender in self.senders:
				new_frame = sender.generate_frame(received_frame)
				self.ola_client.SendDmx(sender.universe, new_frame, frame_sent)

	class pixel_group(object):

		def __init__(self, source_universe, source_channel, destination_universe, destination_channel, number_of_pixels):
			self.source_universe = source_universe
			self.source_offset = source_channel - 1
			self.destination_universe = destination_universe
			self.destination_offset = destination_channel - 1
			self.number_of_pixels = number_of_pixels

		def __lt__(self, other):
			return self.destination_offset < other.destination_offset

	def __init__(self, groups):
		self.pixel_groups = [self.pixel_group(group[0], group[1], group[2], group[3], group[4]) for group in groups]
		self.source_universes = {group.source_universe for group in self.pixel_groups}
		self.ola_client_wrapper = ClientWrapper()
		self.ola_client = self.ola_client_wrapper.Client()
		self.listeners = [self.universe_listener(u, self.pixel_groups, self.ola_client) for u in self.source_universes]
		self.listeners.sort()

	def run(self):
		self.ola_client_wrapper.Run()

	def stop(self):
		self.ola_client_wrapper.Stop()

def main():
	config_file_path = sys.argv[1]
	
	with open(config_file_path) as config_file:
		config_file_text = config_file.readlines()
	
	config_file_text = [line for line in [line.strip() for line in config_file_text] if line and not line.startswith('#')]
	
	pixel_groups = [[int(number) for number in line.split()] for line in config_file_text]
	
	multiplier = pixel_multiplier(pixel_groups)
	
	try:
		multiplier.run()
	except:
		multiplier.stop()

if __name__ == '__main__':
	main()