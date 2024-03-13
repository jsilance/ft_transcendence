from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

# initialize the client but point it to TGI
client = OpenAI(
  base_url="https://api-inference.huggingface.co/v1",
  api_key= os.getenv('HUGGINGFACE_TOKEN')
)

class GenAI:
    def description():
        prompt = "write a short 15 words description warrior for a video game. Answer directly and without formatting the text."
        chat_completion = client.chat.completions.create(
            model="google/gemma-7b-it",
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=True,
            max_tokens=200
        )
        answer = ""
        for message in chat_completion:
            msg = message.choices[0].delta.content
            if "eos" not in msg:
                answer += msg
        answer
        return answer

import random

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
