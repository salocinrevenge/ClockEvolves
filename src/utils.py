from pymunk.vec2d import Vec2d
import copy


def aprox(value, key, mode=0):
    if mode == 0:
        APROXITORS = {"rotation": 0.1, "position": 0.1, "linear_velocity": 5, "angular_velocity": 0.1 }
    elif mode == 1:
        APROXITORS = {"rotation": 0.1, "position": 0.1, "linear_velocity": 1, "angular_velocity": 0.1 }
    elif mode == 2:
        APROXITORS = {"rotation": 0.5, "position": 0.05, "linear_velocity": 0, "angular_velocity": 0 }
    if key not in APROXITORS:
        raise ValueError("Key of hash not found")
    if isinstance(value, Vec2d):
        if APROXITORS[key] == 0:
            return Vec2d(0,0)
        return Vec2d(round(value.x / APROXITORS[key]) * APROXITORS[key], round(value.y / APROXITORS[key]) * APROXITORS[key])
    else:
        if APROXITORS[key] == 0:
            return 0
        return round(value / APROXITORS[key]) * APROXITORS[key]

def scale(value, key, mode = 0):
    if mode == 0:
        SCALERS = {"rotation": 10*10000, "position": 10*1000000, "linear_velocity": 1*100, "angular_velocity": 100*1 }
    elif mode == 1:
        SCALERS = {"rotation": 1*10000, "position": 1*1000000, "linear_velocity": 1*100, "angular_velocity": 1*1 }
    elif mode == 2:
        SCALERS = {"rotation": 1*1000, "position": 1*1000000, "linear_velocity": 0, "angular_velocity": 0 }
    if key not in SCALERS:
        raise ValueError("Key of hash not found")
    if isinstance(value, Vec2d):
        return Vec2d(value.x * SCALERS[key], value.y * SCALERS[key]/2)
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

def hash(objects, mode = 0):
    objects = copy.deepcopy(objects)
    # aprox
    hash = 0
    for object in objects:
        for key in object:
            if key == "name":
                continue
            object[key] = aprox(object[key], key, mode)

            object[key] = limitar(object[key], key)

            object[key] = scale(object[key], key, mode)

    

    for object in objects:
        for key in object:
            if key == "name":
                continue
            sum = int(object[key].x)+int(object[key].y) if isinstance(object[key], Vec2d) else int(object[key])
            hash ^= sum
    return objects, hash

def colidindo_com_outra(peca_principal, space, ignorar_tipos):
    colidindo = False
    if type(peca_principal) not in ignorar_tipos:
        for shape in peca_principal.shapes:
            colisoes = space.shape_query(shape)
            for colisao in colisoes:
                if colisao.shape.body != peca_principal.body:
                    colidindo = True
    return colidindo