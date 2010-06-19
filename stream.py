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
		assert offset < lane.length
		assert offset >= 0
		dist = 0
		for seg in (self.in_lane, self.x_lane, self.out_lane):
			if (lane is seg) and (lane is not None):
				num_cars = len(lane.car_queue)
				for index in range(num_cars):
					if lane.car_queue[index].offset > offset:
						dist += lane.car_queue[index].offset - offset
						vel = lane.car_queue[index].vel
						length = lane.car_queue[index].length
						return (dist, vel, length)
				dist += lane.length - offset
				if lane is self.in_lane:
					lane = self.x_lane
				if lane is self.x_lane:
					lane = self.out_lane
				offset = 0
		return (None, 0, 0)

	def dist_behind(self, lane, offset):
		assert offset < lane.length
		assert offset >= 0
		dist = 0
		for seg in (self.out_lane, self.x_lane, self.in_lane):
			if (lane is seg) and (lane is not None):
				num_cars = len(lane.car_queue)
				for index in reversed(range(num_cars)):
					if lane.car_queue[index].offset < offset:
						dist += offset - lane.car_queue[index].offset
						vel = lane.car_queue[index].vel
						length = lane.car_queue[index].length
						return (dist, vel, length)
				dist += offset
				if lane is self.out_lane:
					lane = self.x_lane
				if lane is self.x_lane:
					lane = self.in_lane
				offset = lane.length
		return (None, 0, 0)

	def in_to_x(self, cars):
		if self.in_lane is None:
			return
		for car in cars:
			car.offset -= self.in_lane.length
			if car.offset > self.x_lane.length:
				car.offset -= self.x_lane.length
				if car.offset < self.out_lane.length:
					if self.out_lane is not None:
						self.out_lane.add_car(car)
			else:
				if self.x_lane is not None:
					self.x_lane.add_car(car)

	def x_to_out(self, time):
		if self.x_lane is None:
			return
		for car in out_cars:
			car.offset -= self.x_lane.length
			if car.offset < self.out_lane.length:
				if self.out_lane is not None:
					self.out_lane.add_car(car)
