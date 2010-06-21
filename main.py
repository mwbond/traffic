# Matthew Bond
# Mar 25, 2010
# main.py

import car
import intersection
import lane
import stream

max_accel = 2
vel = 0
desired_vel =  20
length = 6.5
prt = 1	#2/3.0
max_brake = -3
obs_brake = -3.5

streams = []
in_lanes = []
x_lanes = []
out_lanes = []
for x in range(4):
	in_lanes.append(lane.Lane(1000))
	x_lanes.append(lane.Lane(5))
	out_lanes.append(lane.Lane(1000))
	streams.append(stream.Stream(x, in_lanes[x], out_lanes[x], x_lanes[x]))

inter = intersection.Intersection(in_lanes, x_lanes, out_lanes, streams)

for step in range(500):
	if (step % 20) == 0:
		for index in range(4):
			in_lanes[index].add_car(car.Car(index, max_accel, vel, desired_vel,
											length, prt, max_brake, obs_brake))
	print "***** STEP", step, "*****"
	in_lanes[1].print_lane()
	print
	x_lanes[1].print_lane()
	print
	out_lanes[1].print_lane()

	inter.calc_updates()
	inter.fix_offsets()
	inter.commit_queues()
	print
