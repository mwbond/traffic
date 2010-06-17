# Matthew Bond
# Jun 16, 2010
# stream.py

class Stream:
	def __init__(self, id, in_lane, out_lane, x_lane=None):
		self.id  = id
		self.in_lane = in_lane
		self.out_lane = out_lane
		self.x_lane = x_lane

	def dist_ahead(self, lane, offset):
		assert offset < lane.length
		assert offset >= 0
		dist = 0
		for seg in (self.in_lane, self.x_lane, self.out_lane):
			if (lane is seg) and (lane is not None):
				num_cars = len(lane.car_queue)
				for index in range(num_cars):
					if lane.car_queue[index].offset > offset:
						return dist + lane.car_queue[index].offset - offset
				dist += lane.length - offset
				if lane is self.in_lane:
					lane = self.x_lane
				if lane is self.x_lane:
					lane = self.out_lane
				offset = 0
		return dist

	def dist_behind(self, lane, offset):
		assert offset < lane.length
		assert offset >= 0
		dist = 0
		for seg in (self.out_lane, self.x_lane, self.in_lane):
			if (lane is seg) and (lane is not None):
				num_cars = len(lane.car_queue)
				for index in reversed(range(num_cars)):
					if lane.car_queue[index].offset < offset:
						return dist + offset - lane.car_queue[index].offset
				dist += offset
				if lane is self.out_lane:
					lane = self.x_lane
				if lane is self.x_lane:
					lane = self.in_lane
				offset = lane.length
		return dist

	def update_in(self):
		if self.in_lane.time == (time - 1):
			self.x_lane.update_lane
		self.out_lane.check_offsets(self.id)
		for car in out_cars:
			car.offset -= self.in_lane.length
			if car.offset > self.x_lane.length:
				car.offset -= self.x_lane.length
				if car.offset < self.out_lane.length:
					self.out_lane.add_car(car)
			else:
				self.x_lane.add_car(car)

	def update_x(self, time):
		if self.x_lane is None:
			return
		if self.x_lane.time == (time - 1):
			self.x_lane.update_lane
		out_cars = self.x_lane.check_offsets(self.id)
		for car in out_cars:
			car.offset -= self.x_lane.length
			if car.offset < self.out_lane.length:
				self.out_lane.add_car(car)

	def update_out(self):
		if self.out_lane.time == (time - 1):
			self.out_lane.update_lane
		self.out_lane.check_offsets(self.id)
