# Matthew Bond
# Jun 22, 2010
# config.py

import ConfigParser

config = ConfigParser.RawConfigParser()

config.add_section('Section1')
config.set('Section1', 'int', '15')
config.set('Section1', 'bool', 'true')
config.set('Section1', 'float', '3.1415')
config.set('Section1', 'baz', 'fun')
config.set('Section1', 'bar', 'Python')
config.set('Section1', 'foo', '%(bar)s is %(baz)s!')

config.add_section('Global')
config.set('Global', 'prt', '%(bar)s is %(baz)s!')
config.set('Global', 'max_accel', '%(bar)s is %(baz)s!')
config.set('Global', 'incoming_vel', '%(bar)s is %(baz)s!')
config.set('Global', 'desired_vel', '%(bar)s is %(baz)s!')
config.set('Global', 'veh_length', '%(bar)s is %(baz)s!')
config.set('Global', 'max_brake', '%(bar)s is %(baz)s!')
config.set('Global', 'obs_brake', '%(bar)s is %(baz)s!')
config.set('Global', 'duration', '%(bar)s is %(baz)s!')

# Writing our configuration file to 'example.cfg'
with open('../config', 'wb') as configfile:
    config.write(configfile)

