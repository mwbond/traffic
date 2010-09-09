# Matthew Bond
# Mar 25, 2010
# car.py

class Car:
	def __init__(self, id, max_accel, vel, desired_vel, length, prt,
					max_brake, obs_brake):
		self.id = id
		self.max_accel = max_accel 
		self.vel = vel
		self.desired_vel = desired_vel
		self.length = length
		self.prt = prt
		self.max_brake = max_brake
		self.obs_brake = obs_brake
		self.offset = 0
	
	def update_car(self, ninfo, einfo, winfo):
		vel = self.step_vel(*ninfo)
		evel = self.step_vel(*einfo)
		wvel = self.step_vel(*winfo)
		if vel < 0.01:
			vel = 0
		self.vel = vel
		self.offset = self.offset + self.vel * self.prt
		assert self.vel >= 0

	def step_vel(self, lead_dist=None, lead_vel=0):
		"""Get the new velocity depending on the lead car using the Gipps Model.
		Brake limit is ignored by the leaing vehicle if its lead is None."""
		accel_limit = (self.vel + 2.5 * self.max_accel * self.prt *
						(1 - self.vel / self.desired_vel) *
						(0.025 + self.vel / self.desired_vel) ** 0.5)
		if lead_dist == None:
			brake_limit = accel_limit
		else:
			brake_limit = (self.max_brake * self.prt +
							((self.max_brake ** 2) * (self.prt ** 2) -
							self.max_brake *
							(2 * lead_dist - self.vel * self.prt -
							 (lead_vel ** 2) / self.obs_brake)) ** 0.5)
		# I am unsure if vel(t) was used from vel(t-1) to vel(t) or from
		# vel(t) to vel(t+1).
		if accel_limit < brake_limit:
			return accel_limit
		else:
			return brake_limit
