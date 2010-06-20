# Matthew Bond
# Jun 16, 2010
# intersection.py

import car
import lane
import stream

class Intersection:
	def __init__(self, in_lanes, x_lanes, out_lanes, streams):
		self.in_lanes = in_lanes
		self.x_lanes = x_lanes
		self.out_lanes = out_lanes
		self.streams = streams


	def calc_updates(self):
		for lanes in (self.out_lanes, self.x_lanes, self.in_lanes):
			for lane in lanes:
				if lane is not None:
					car = lane.update_lane()
					stream = self.streams[car.stream_id]
					lead_info = stream.info_ahead(lane, car.offset)
					car.update_car(*lead_info)

	def fix_offsets(self):
		for lane in self.out_lanes:
			if lane is not None:
				unbounded = lane.get_unbounded(self)

		for lane in self.x_lanes:
			if lane is not None:
				unbounded = lane.get_unbounded(self)
				for stream_id in unbounded:
					self.streams[stream_id].update_x(unbounded[stream_id])

		for lane in self.in_lanes:
			if lane is not None:
				unbounded = lane.get_unbounded(self)
				for stream_id in unbounded:
					self.streams[stream_id].update_in(unbounded[stream_id])
