# Matthew Bond
# Mar 25, 2010
# node.py

import car

class Node:
	# Assumes that every link connected to this node is
	# a two lane road, and that every lane exiting this
	# node can be reached by every lane entering this node.
	def __init__(self, id):
		self.id =  id
		self.links = []

	def transferCar(car, orig_link, dest_link, dest_offset):
		assert dest_link in self.links
		assert orig_link in self.links

		if orig_link.dest_node_id == self.id:
			orig_link.car_queues[0].pop(car)
		else:
			orig_link.car_queues[1].pop(car)

		if dest_link.orig_node_id == self.id:
			car.offset = dest_offset
			assert car.offset <= dest_link.length
		else:
			car.offset = dest_link.length - dest_offset
			assert car.offset <= dest_link.length

