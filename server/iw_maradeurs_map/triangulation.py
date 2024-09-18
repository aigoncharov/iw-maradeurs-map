import sympy as sp
from sympy.solvers import solve

def process_request(request):
    for i in range(len(request['sensors'])):
        idx = request['sensors'][i]['id']
        request['sensors'][i]['lat'] = sensors_positions[idx]['lat']
        request['sensors'][i]['long'] = sensors_positions[idx]['long']

    return triangulate(request['sensors'])

def apply_curve(signal, alpha=1):
    pass

def get_distance(signal):
    return signal + 127 + 100

def triangulate(signals):
    assert len(signals) >= 2, "Should be at least 2 signals"

    signals.sort(key = lambda x : -x['signal'])
    
    x1 = signals[0]['lat']
    y1 = signals[0]['long']
    dist1 = get_distance(signals[0]['signal'])

    x2 = signals[1]['lat']
    y2 = signals[1]['long']
    dist2 = get_distance(signals[1]['signal'])

    if len(signals) == 2:
        coef1 = dist2 / (dist1 + dist2) / (((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)) ** 0.5)
        coef2 = dist1 / (dist1 + dist2) / (((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)) ** 0.5)
        res_x1 = x1 * coef1 + x2 * coef2
        res_y1 = y1 * coef1 + y2 * coef2
        return res_x1, res_y1

    x3 = signals[2]['lat']
    y3 = signals[2]['long']
    dist3 = get_distance(signals[2]['signal'])

    coef1 = dist2 / (dist1 + dist2) / (((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)) ** 0.5)
    coef2 = dist1 / (dist1 + dist2) / (((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)) ** 0.5)
    res_x1 = x1 * coef1 + x2 * coef2
    res_y1 = y1 * coef1 + y2 * coef2

    coef1 = dist3 / (dist2 + dist3) / (((x2 - x3) * (x2 - x3) + (y2 - y3) * (y2 - y3)) ** 0.5)
    coef2 = dist2 / (dist2 + dist3) / (((x2 - x3) * (x2 - x3) + (y2 - y3) * (y2 - y3)) ** 0.5)
    res_x2 = x2 * coef1 + x3 * coef2
    res_y2 = y2 * coef1 + y3 * coef2

    coef1 = dist3 / (dist1 + dist3) / (((x1 - x3) * (x1 - x3) + (y1 - y3) * (y1 - y3)) ** 0.5)
    coef2 = dist1 / (dist1 + dist3) / (((x1 - x3) * (x1 - x3) + (y1 - y3) * (y1 - y3)) ** 0.5)
    res_x3 = x1 * coef1 + x3 * coef2
    res_y3 = y1 * coef1 + y3 * coef2

    res_x = (res_x1 + res_x2 + res_x3) / 3
    res_y = (res_y1 + res_y2 + res_y3) / 3
    return res_x, res_y

sensors_positions = {
    "bantik_scene": {
        "lat": 1,
        "long": 1
    },
    "bantik_india_door": {
        "lat": 0,
        "long": 1,
    },
    "bantik_flags": {
        "lat": 1,
        "long": 0,
    },
}

request = {
    "sensors": [
        {
            "id": "bantik_scene",
            "signal": 100,
        },
        {
            "id": "bantik_india_door",
            "signal": -10,
        },
        {
            "id": "bantik_flags",
            "signal": -20,
        },
    ]
}

print(process_request(request))
