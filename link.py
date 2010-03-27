# Matthew Bond
# Mar 25, 2010
# link.py

import car
import lane

class Link:
	def __init__(self, length, num_lanes=1):
		self.length
		for count in range(num_lanes):
			self._lanes = (lane.Lane() in range(num_lanes))
	
	# Updates the link.
	def update_link(self):
		for lane in self._lanes:
			lane.update_lane()

	# Print out all of the car's id, offset, and vel
	def print_link(self):
		for lane in self._lanes:
			lane.print_lane()
