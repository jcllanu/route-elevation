import geometrical_utilities as geom
import math
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt


EARTH_ROTATION_AXIS_ANGLE_RAD =geom.degree2radian(23.44)

def position(latitude, longitude, t):
    
    (x0, y0, z0) = geom.spherical2cartesian(1,latitude,longitude)
    # (x1, y1, z1) = geom.rot_fix_y(EARTH_ROTATION_AXIS_ANGLE_RAD, x0, y0, z0)
    (r0, alpha0) = geom.cartesian2polar(x0,y0)
    (x2, y2) = geom.polar2cartesian(r0, alpha0 + angle_rotation_earth(t))
    (x3, y3, z3) = geom.rot_fix_y(-EARTH_ROTATION_AXIS_ANGLE_RAD, x2, y2, z0)
    return (x3,y3,z3)

def angle_sun_earth(t): #t en días
    return (t-172) *2*math.pi/365.25 # June 21st

def angle_rotation_earth(t): # t en días
    return 2*math.pi*t+ math.pi + (t-172) *2*math.pi/365.25

def get_time_in_days(month, day, hour, minute):
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return sum(month_days[:month-1]) + day + (hour + minute/60)/24

def init_function():
    return

def plot_shadow_day(t, month, day, latitude_rad, longitude_rad, ax):
    
    hours=t*24
    hour = math.floor(hours)
    minute = math.floor((hours-hour)*60)

    print(hour, minute)

    t = get_time_in_days(month, day, hour, minute)

    months = ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August','September', 'October', 'November', 'December']
    

    normal_vector = np.array(position(latitude_rad, longitude_rad, t))

    angle_sun = angle_sun_earth(t)
    sun_ray = np.array((-math.cos(angle_sun), -math.sin(angle_sun), 0))
    rotation_axis_vector = np.array((math.sin(EARTH_ROTATION_AXIS_ANGLE_RAD), 0, math.cos(EARTH_ROTATION_AXIS_ANGLE_RAD)))

    north = np.dot(normal_vector,rotation_axis_vector)*normal_vector + rotation_axis_vector
    east = np.cross(rotation_axis_vector, normal_vector)

    dot_product = np.dot(normal_vector,sun_ray)
    if dot_product >=0:
        # Night
        pass
    else:
        shadow_vector = normal_vector - sun_ray / dot_product
        shadow_east_component = float(np.dot(shadow_vector, east))
        shadow_north_component = float(np.dot(shadow_vector, north))
        (r, angle) = geom.cartesian2polar(shadow_east_component, shadow_north_component)

        ax.plot([0, shadow_east_component], [0,shadow_north_component], linestyle='-', color='black')

        # Plot the point
        ax.scatter(shadow_east_component, shadow_north_component, color='blue')

        label = 'x = ' + str(round(shadow_east_component, 2)) + ' y = ' + str(round(shadow_north_component, 2)) + '\n' +\
                'r = ' + str(round(r,2)) + ' angle = '+ str(round(geom.radian2degree(angle),2)) + '°'

        # Add a label
        ax.text(shadow_east_component + 0.1, shadow_east_component + 0.1, label, fontsize=12)

        # print('x =', round(shadow_east_component, 2))
        # print('y = ',round(shadow_north_component, 2))
        # print('r = ', round(r,2))
        # print('angle = ', str(round(geom.radian2degree(angle),2)) + '°')

    L = 4
    ax.set_ylim(-L, L)
    ax.set_xlim(-L, L)
    time_label = months[month-1] + str(day) + ' UTC '+str(hour).rjust(2,'0')+':'+str(minute).rjust(2,'0')
    ax.set_title(time_label)
    ax.set_xlabel('WEST - EAST')
    ax.set_ylabel('SOUTH - NORTH')
    position_label = 'Latitude: ' + str(round(latitude_deg,2))+'° ' +'Longitude:'+ str(round(longitude_deg,2))+'°'
    plt.suptitle(position_label)    

figure, ax = plt.subplots()


latitude_deg = 39.67410949332963
longitude_deg = -0.20563175459619165
latitude_rad = geom.degree2radian(latitude_deg)
longitude_rad = geom.degree2radian(longitude_deg)
month = 7
day = 30

ani = animation.FuncAnimation(
        figure,
        func = plot_shadow_day,
        frames=np.linspace(0, 1, 24 + 1),
        fargs=(month, day, latitude_rad, longitude_rad, ax),
        init_func=init_function
    )

ani.save("Shadow.gif", writer='pillow', fps=100) 