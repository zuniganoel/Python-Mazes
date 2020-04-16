def rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)

def hex_to_rgb(value):
    value = value.lstrip('#')
    length = len(value)
    return tuple(int(value[i:i+length//3], 16) for i in range(0, length, length//3))