# Matthew Bond
# Jun 16, 2010
# stream.py

class Stream:
	def __init__(self, id, in_lane, out_lane, x_lane=None):
		self.id  = id
		self.in_lane = in_lane
		self.out_lane = out_lane
		self.x_lane = x_lane
		self.status = 0 # 0=red

	def change_status(self, change):
		self.status = change

	def info_ahead(self, lane, offset):
		gap_length = 0
		for seg in (self.in_lane, self.x_lane, self.out_lane):
			if (lane is seg) and (lane is not None):
				num_cars = len(lane.refrence_queue)
				for index in range(num_cars):
					lead = lane.refrence_queue[index]
					if lead.offset > offset:
						gap_length += lead.offset - offset - lead.length
						return (gap_length, lead.vel)
				gap_length += lane.length - offset
				if lane is self.in_lane:
					lane = self.x_lane
				if lane is self.x_lane:
					lane = self.out_lane
				offset = 0
		return (None, 0)

	def info_behind(self, lane, offset):
		assert offset < lane.length
		assert offset >= 0
		gap_length = 0
		for seg in (self.out_lane, self.x_lane, self.in_lane):
			if (lane is seg) and (lane is not None):
				num_cars = len(lane.refrence_queue)
				for index in reversed(range(num_cars)):
					lead = lane.refrence_queue[index]
					if lead.offset < offset:
						gap_length += offset - lead.offset - lead.length
						return (gap_length, lead.vel)
				gap_length += offset
				if lane is self.out_lane:
					lane = self.x_lane
				if lane is self.x_lane:
					lane = self.in_lane
				offset = lane.length
		return (None, 0)

	def in_to_x(self, cars):
		for car in cars:
			car.offset -= self.in_lane.length
			if self.x_lane is None:
				if car.offset < self.out_lane.length:
					self.out_lane.add_car(car)
			else:
				if car.offset < self.x_lane.length:
					self.x_lane.add_car(car)
				else:
					car.offset -= self.x_lane.length
					if car.offset < self.out_lane.length:
						self.out_lane.add_car(car)

	def x_to_out(self, cars):
		for car in cars:
			car.offset -= self.x_lane.length
			if car.offset < self.out_lane.length:
				if self.out_lane is not None:
					self.out_lane.add_car(car)
