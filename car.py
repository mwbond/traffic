# Matthew Bond
# Mar 25, 2010
# car.py

class Car:
	def __init__(self, stream_id, max_accel, vel, desired_vel, length, prt,
					max_brake, obs_brake):
		self.stream_id = stream_id
		self.max_accel = max_accel
		self.vel = vel
		self.desired_vel = desired_vel
		self.length = length
		self.prt = prt
		self.max_brake = max_brake
		self.obs_brake = obs_brake
		self.offset = 0

	def update_car(self, gap_length, lead_vel, stop_dist=None):
		"""Get the new velocity depending on the lead car using the Gipps Model.
		Brake limit is ignored by the leading vehicle if its lead is None."""
		accel_limit = (self.vel + 2.5 * self.max_accel * self.prt *
						(1 - self.vel / self.desired_vel) *
						(0.025 + self.vel / self.desired_vel) ** 0.5)
		if gap_length is None:
			brake_limit = accel_limit
		else:
			brake_limit = (self.max_brake * self.prt +
							((self.max_brake ** 2) * (self.prt ** 2) -
								self.max_brake *
									(2 * gap_length - self.vel * self.prt -
									(lead_vel ** 2) / self.obs_brake)) ** 0.5)
		if stop_dist is None:
			stop_brake_limit = accel_limit
		elif (self.vel ** 2) / (-2 * self.max_brake) > stop_dist:
			stop_brake_limit = accel_limit
		else:
			stop_brake_limit = (self.max_brake * self.prt +
								((self.max_brake ** 2) * (self.prt ** 2) -
									self.max_brake * (2 * stop_dist -
										self.vel * self.prt)) ** 0.5)
		# I am unsure if vel(t) was used from vel(t-1) to vel(t) or from
		# vel(t) to vel(t+1).
		self.vel = min(brake_limit, accel_limit, stop_brake_limit)

		if self.vel < 0.1:
			self.vel = 0
		self.offset = self.offset + self.vel * self.prt
		assert self.vel >= 0
