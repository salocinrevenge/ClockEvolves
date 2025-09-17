from pymunk.vec2d import Vec2d
import copy


def aprox(value, key, hard):
    if hard:
        APROXITORS = {"rotation": 0.1, "position": 0.1, "linear_velocity": 1, "angular_velocity": 0.1 }
    else:
        APROXITORS = {"rotation": 0.1, "position": 0.1, "linear_velocity": 5, "angular_velocity": 0.1 }
    if key not in APROXITORS:
        raise ValueError("Key of hash not found")
    if isinstance(value, Vec2d):
        return Vec2d(round(value.x / APROXITORS[key]) * APROXITORS[key], round(value.y / APROXITORS[key]) * APROXITORS[key])
    else:
        return round(value / APROXITORS[key]) * APROXITORS[key]

def scale(value, key, hard):
    if hard:
        SCALERS = {"rotation": 1*10000, "position": 1*1000000, "linear_velocity": 1*100, "angular_velocity": 1*1 }
    else:
        SCALERS = {"rotation": 10*10000, "position": 10*1000000, "linear_velocity": 1*100, "angular_velocity": 100*1 }
    if key not in SCALERS:
        raise ValueError("Key of hash not found")
    if isinstance(value, Vec2d):
        return Vec2d(value.x * SCALERS[key], value.y * SCALERS[key])
    else:
        return value * SCALERS[key]
    
def limitar(value, key):
    LIMITER = {"rotation": 360, "position": 1000, "linear_velocity": 6, "angular_velocity": 360 }
    if key not in LIMITER:
        raise ValueError("Key of hash not found")
    if isinstance(value, Vec2d):
        return Vec2d(max(min(value.x, LIMITER[key]), -LIMITER[key]), max(min(value.y, LIMITER[key]), -LIMITER[key]))
    else:
        return max(min(value, LIMITER[key]), -LIMITER[key])

def hash(objects, hard = False):
    objects = copy.deepcopy(objects)
    # aprox
    hash = 0
    for object in objects:
        for key in object:
            if key == "name":
                continue
            object[key] = aprox(object[key], key, hard)

            object[key] = limitar(object[key], key)

            object[key] = scale(object[key], key, hard)

    

    for object in objects:
        for key in object:
            if key == "name":
                continue
            sum = int(object[key].x)+int(object[key].y) if isinstance(object[key], Vec2d) else int(object[key])
            hash ^= sum
    return objects, hash