

# a bunch of formula to evenly space and center a collection of objects in a gui.
def spacing(dimension, num_objs, obj_dim, obj_gap):
    return [i for i in range(((dimension - ((num_objs * obj_dim) + ((num_objs - 1) * obj_gap)))//2), dimension -
            ((dimension - ((num_objs * obj_dim) + ((num_objs - 1) * obj_gap)))//2) + 1, (obj_dim + obj_gap))]
