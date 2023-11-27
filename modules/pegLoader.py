from modules.physicsObjects import Peg
import pygame
import random
import math
import json


# Import level data
with open("levels.json", "r") as file:
    level_data = json.load(file)
    peg_positions = level_data["level_0"]["peg_positions"]
    background = level_data["level_0"]["background"]


# Set how many special pegs there will be (special pegs = total pegs / 10, + 1 for purple peg)
num_of_special_pegs = math.trunc(len(peg_positions) / 10 + 1)

# Get random sample (no duplicate values) of number of peg positions
random_integers = random.sample(range(len(peg_positions) + 1), num_of_special_pegs)

# First random sample will be purple peg
purple_peg_num = random_integers.pop(0)

all_pegs = pygame.sprite.Group()
for peg_idx, peg_pos in enumerate(peg_positions):

    if purple_peg_num == peg_idx:
        peg = Peg(None, peg_pos, "purple")

    elif peg_idx in random_integers:
        peg = Peg(None, peg_pos, "red")

    else:
        peg = Peg(None, peg_pos, "blue")

    all_pegs.add(peg)


def replace_purple_peg():
    # If purple peg is removed, replace it in a random spot
    pass