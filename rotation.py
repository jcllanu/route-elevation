import geometrical_utilities as geom
import math
import numpy as np

EARTH_ROTATION_AXIS_ANGLE_RAD =geom.degree2radian(23.44)

def position(latitude, longitude, t):
    
    (x0, y0, z0) = geom.spherical2cartesian(1,latitude,longitude)
    # (x1, y1, z1) = geom.rot_fix_y(EARTH_ROTATION_AXIS_ANGLE_RAD, x0, y0, z0)
    (r0, alpha0) = geom.cartesian2polar(x0,y0)
    (x2, y2) = geom.polar2cartesian(r0, alpha0 + angle_rotation_earth(t))
    (x3, y3, z3) = geom.rot_fix_y(-EARTH_ROTATION_AXIS_ANGLE_RAD, x2, y2, z0)
    return (x3,y3,z3)

def angle_sun_earth(t): #t en días
    return (t-172) *2*math.pi/365.25 # June 

def angle_rotation_earth(t): # t en días
    return 2*math.pi*t



latitude = geom.degree2radian(39.67410949332963)
longitude = geom.degree2radian(-0.20563175459619165)
t = 75.58

normal_vector = np.array(position(latitude, longitude, t))

angle_sun = angle_sun_earth(75.58)
sun_ray = np.array((-math.cos(angle_sun), -math.sin(angle_sun), 0))
rotation_axis_vector = np.array((math.sin(EARTH_ROTATION_AXIS_ANGLE_RAD), 0, math.cos(EARTH_ROTATION_AXIS_ANGLE_RAD)))

north = np.dot(normal_vector,rotation_axis_vector)*normal_vector + rotation_axis_vector
east = np.cross(rotation_axis_vector, normal_vector)

dot_product = np.dot(normal_vector,sun_ray)
if dot_product >=0:
    print('Night')
else:
    shadow_vector = normal_vector - sun_ray / dot_product
    shadow_east_component = np.dot(shadow_vector, east)
    shadow_north_component = np.dot(shadow_vector, north)
    print((shadow_east_component, shadow_north_component))
    print(geom.cartesian2polar(shadow_east_component, shadow_north_component))
