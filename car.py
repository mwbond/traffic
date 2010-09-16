# Matthew Bond
# Mar 25, 2010
# car.py

import copy

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
	
	def update_car(self, n_info, e_info, w_info):
		vel = self.step_vel(*n_info)
		if e_info is not None:
			print 'east', e_info, self.id, self.offset
			e_mobil, e_vel = self.mobil(vel, *e_info)
			print 'east', 'done'
		else:
			e_mobil = None
		if w_info is not None:
			print 'west', w_info, self.id, self.offset
			w_mobil, w_vel = self.mobil(vel, *w_info)
			print 'west', 'done'
		else:
			w_mobil = None
		delta = vel - self.vel
		decision = max(delta, e_mobil, w_mobil)
		if decision is e_mobil:
			vel = e_vel
			dir = 1
		if decision is w_mobil:
			vel = w_vel
			dir = -1
		else:
			dir = 0

		if vel < 0.01:
			vel = 0
		self.vel = vel
		self.offset = self.offset + self.vel * self.prt
		assert self.vel >= 0
		return dir

	def mobil(self, vel, n_dist, n_vel, s_dist, s_car):
		p = 0.0 #politeness factor
		a = 0.1 #threshold for lane changing
		new_vel = self.step_vel(n_dist, n_vel)
		delta = new_vel - vel
		if s_car is None:
			s_delta = 0
		else:
			dist = n_dist and (n_dist + s_dist)
			s_vel = s_car.step_vel(dist, n_vel)
			new_s_vel = s_car.step_vel(s_dist - self.length, self.vel)
			s_delta = s_vel - new_s_vel
			if -s_delta < s_car.max_brake:
				return None, 0
		return delta - p * s_delta - a, new_vel

	def step_vel(self, lead_dist=None, lead_vel=0):
		"""Get the new velocity depending on the lead car using the Gipps Model.
		Brake limit is ignored by the leaing vehicle if its lead is None."""
		#print self.id, lead_dist, lead_vel
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
