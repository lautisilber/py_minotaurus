import numpy as np
from PIL import Image
import os

GOAL_B  = np.array([0, 0, 0xFF, 0xFF - 0b1000], dtype=np.uint8)
START_B = np.array([0, 0, 0xFF, 0xFF - 0b0100], dtype=np.uint8)
GOAL_R  = np.array([0xFF, 0, 0, 0xFF - 0b1000], dtype=np.uint8)
START_R = np.array([0xFF, 0, 0, 0xFF - 0b0100], dtype=np.uint8)
GOAL_G  = np.array([0, 0xFF, 0, 0xFF - 0b1000], dtype=np.uint8)
START_G = np.array([0, 0xFF, 0, 0xFF - 0b0100], dtype=np.uint8)
GOAL_R  = np.array([0xFF, 0xFF, 0, 0xFF - 0b1000], dtype=np.uint8)
START_R = np.array([0xFF, 0xFF, 0, 0xFF - 0b0100], dtype=np.uint8)
MINOTAUR = np.array([0, 0, 0, 0xFF - 0b0010], dtype=np.uint8)
HEDGE    = np.array([0, 0, 0, 0xFF - 0b0001], dtype=np.uint8)
WALL     = np.array([0, 0, 0, 0xFF - 0b0011], dtype=np.uint8)
GRASS     = np.array([0, 0, 0, 0xFF - 0b0000], dtype=np.uint8)

def compare_1d_arrays(a1: np.ndarray, a2: np.ndarray) -> bool:
    if len(a1) != len(a2): return False
    for i in range(len(a1)):
        if a1[i] != a2[i]:
            return False
    return True

def create_visualizer(arr: np.ndarray) -> np.ndarray:
    mapping = [
        (MINOTAUR, np.array([0, 0, 0, 0xFF], dtype=np.uint8)),
        (HEDGE, np.array([54, 99, 66, 0xFF], dtype=np.uint8)),
        (GRASS, np.array([50, 168, 82, 0xFF], dtype=np.uint8)),
        (WALL, np.array([110, 110, 110, 0xFF], dtype=np.uint8)),
    ]

    arr2 = np.zeros_like(arr)
    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            color = arr[x,y]

            for orig, chng in mapping:
                if compare_1d_arrays(color, orig):
                    color = chng
                    break

            arr2[x,y] = color

    return arr2

def create_image_from_array(arr: np.ndarray, fname: str, visualize_fname: str|None) -> None:
    assert(arr.dtype == np.uint8) # assert right type
    assert(len(arr.shape) == 3) # assert 2D image (and an extra dim for colors)
    assert(arr.shape[2] == 4) # assert RGBA image

    dirname = os.path.dirname(fname)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    im = Image.fromarray(arr)
    im.save(fname)

    if visualize_fname:
        visualize_arr = create_visualizer(arr)
        create_image_from_array(visualize_arr, visualize_fname, None)

# 20 x 20
BOARD_2P_1 = np.array([
    [*[START_R]*2, *[GRASS]*18],
    [START_R, *[GRASS]*19],
    [*[GRASS]*2, *[HEDGE]*2, *[GRASS]*2, HEDGE, *[GRASS]*2, *[HEDGE]*2, *[GRASS]*5, *[HEDGE]*2, *[GRASS]*2],
    [*[GRASS]*2, HEDGE, *[GRASS]*3, HEDGE, *[GRASS]*9, *[HEDGE]*2, *[GRASS]*2],
    [*[GRASS]*13, HEDGE, *[GRASS]*6],
    [*[GRASS]*10, HEDGE, *[GRASS]*2, HEDGE, *[GRASS]*6],
    [*[GRASS]*2, *[HEDGE]*2, *[GRASS]*2, *[HEDGE]*5, *[GRASS]*2, *[HEDGE]*3, *[GRASS]*4],
    [*[GRASS]*6, HEDGE, *[GRASS]*13],
    [*[GRASS]*6, HEDGE, GRASS, *[GOAL_R]*2, *[GRASS]*10],
    [*[GRASS]*2, HEDGE, *[GRASS]*3, HEDGE, GRASS, GOAL_R, *[HEDGE]*2, *[GRASS]*2, *[HEDGE]*2, *[GRASS]*2, HEDGE, *[GRASS]*2],
    [*[GRASS]*2, HEDGE, *[GRASS]*2, *[HEDGE]*2, *[GRASS]*2, *[HEDGE]*2, GOAL_B, GRASS, HEDGE, *[GRASS]*3, HEDGE, *[GRASS]*2],
    [*[GRASS]*10, *[GOAL_B]*2, GRASS, HEDGE, *[GRASS]*6],
    [*[GRASS]*13, HEDGE, *[GRASS]*6],
    [*[GRASS]*4, *[HEDGE]*3, *[GRASS]*2, *[HEDGE]*5, *[GRASS]*2, *[HEDGE]*2, *[GRASS]*2],
    [*[GRASS]*6, HEDGE, *[GRASS]*2, HEDGE, *[GRASS]*10],
    [*[GRASS]*6, HEDGE, *[GRASS]*13],
    [*[GRASS]*2, *[HEDGE]*2, *[GRASS]*9, HEDGE, *[GRASS]*3, HEDGE, *[GRASS]*2],
    [*[GRASS]*2, *[HEDGE]*2, *[GRASS]*5, *[HEDGE]*2, *[GRASS]*2, HEDGE, *[GRASS]*2, *[HEDGE]*2, *[GRASS]*2],
    [*[GRASS]*19, START_B],
    [*[GRASS]*18, *[START_B]*2]
], dtype=np.uint8)

create_image_from_array(BOARD_2P_1, "./maps/classic2p.png", "./maps/classic2p_visualize.png")
