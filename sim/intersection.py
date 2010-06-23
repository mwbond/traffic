#.itervalues() Matthew Bond
# Jun 16, 2010
# intersection.py

import copy

import car
import lane
import stream

class Intersection:
	def __init__(self, in_lanes, x_lanes, out_lanes, streams, cycle, phases):
		self.in_lanes = in_lanes
		self.x_lanes = x_lanes
		self.out_lanes = out_lanes
		self.streams = streams
		self.cycle = cycle
		self.phases = phases
		self.time = 1

	def update(self):
		self.controller()
		self.calc_updates()
		self.fix_offsets()
		self.commit_queues()
		self.time += 1

	def controller(self):
		timing =  time % self.cycle
		if timing in self.phases:
			for stream_id in self.phases[timing]:
				self.streams[stream_id].switch_phase()

	def calc_updates(self):
		for stream in self.streams.itervalues():
			stream.update_stream()

	def fix_offsets(self):
		for lane in self.out_lanes:
			unbounded = lane.get_unbounded()

		for lane in self.x_lanes:
			unbounded = lane.get_unbounded()
			for stream_id in unbounded:
				self.streams[stream_id].x_to_out(unbounded[stream_id])

		for lane in self.in_lanes:
			unbounded = lane.get_unbounded()
			for stream_id in unbounded:
				self.streams[stream_id].in_to_x(unbounded[stream_id])

	def commit_queues(self):
		for lanes in (self.out_lanes, self.x_lanes, self.in_lanes):
			for lane in lanes:
				if lane is not None:
					lane.refrence_queue = copy.copy(lane.car_queue)
