from pymunk.vec2d import Vec2d


def aprox(value, key):
    APROXITORS = {"rotation": 0.1, "position": 0.1, "linear_velocity": 1, "angular_velocity": 0.01 }
    if key not in APROXITORS:
        raise ValueError("Key of hash not found")
    if isinstance(value, Vec2d):
        return Vec2d(round(value.x / APROXITORS[key]) * APROXITORS[key], round(value.y / APROXITORS[key]) * APROXITORS[key])
    else:
        return round(value / APROXITORS[key]) * APROXITORS[key]


def hash(objects):
    # aprox
    for object in objects:
        for key in object:
            if key == "name":
                continue
            object[key] = aprox(object[key], key)
    return objects