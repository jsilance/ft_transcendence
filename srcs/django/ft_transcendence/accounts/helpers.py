from dotenv import load_dotenv
import random
import os
load_dotenv()

warriors = [
    "Crimson Blade: A relentless warrior wielding a fiery sword, leaving enemies scorched in battle.",
    "Shadow Fang: A cunning assassin, striking swiftly from the darkness with deadly precision.",
    "Ironclad Sentinel: A towering behemoth clad in impenetrable armor, impervious to all attacks.",
    "Stormbringer: A tempestuous warrior harnessing the power of lightning, striking fear into foes.",
    "Serpent's Wrath: A nimble warrior skilled in dual-wielding blades, striking with venomous speed.",
    "Raging Bull: A hulking brute armed with a massive warhammer, causing devastation with every swing.",
    "Phoenix Fury: A mystical warrior capable of summoning flames, rising from ashes to conquer.",
    "Silent Reaper: A master of stealth armed with deadly daggers, leaving no trace behind.",
    "Frostbitten Slayer: A frosty warrior wielding a frost axe, freezing enemies in their tracks.",
    "Celestial Guardian: A celestial warrior harnessing divine energy, defending justice with heavenly might."
]

def pick_random_description():
    return random.choice(warriors)
