import EP.galaxydata as galaxydata
import EP.galaxy as galaxy
import time
import random


def get_coords(coords):
    c = coords.split(":")
    return {"x": int(c[0]), "y": int(c[1]), "z": int(c[2])}


def get_closest_asteroid(coords_dir, min_time_mins): 
    coords = get_coords(coords_dir["coords"])

    print('searching left...')
    y_left = search_for_asteroid(coords["x"], coords["y"], 'left', coords_dir["max_left"], min_time_mins)

    
    print('searching right...')
    y_right = search_for_asteroid(coords["x"], coords["y"], 'right', coords_dir["max_right"], min_time_mins)
    
    if abs(y_left-coords["y"]) <= (y_right-coords[y]):
        return y_left
    else:
        return y_right


def search_for_asteroid(x, y, direction, max_value, min_time_mins):  # searching for asteroid in one direction 
    if direction == 'left':
        direction_num = -1
    elif direction == 'right':
        direction_num = 1
    else:
        raise ValueError('spierdalaj')
        
    _, referal_url = galaxy.get_galaxy_html() # only for referal_url purposes (anti_bot?)

    for i in range(y, max_value, direction_num):
        time.sleep(random.uniform(0.25, 0.5))

        is_asteroid, url, time_left, referal_url = galaxydata.get_asteroid(referal_url, x, i)
        if is_asteroid:
            minutes_left = int(time_left.strip("()").split(":")[0]) 
            if minutes_left > min_time_mins:
                return i

    return None
