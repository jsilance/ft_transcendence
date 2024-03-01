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
        prompt = "write a unique and short 15 words description warrior for a video game. Answer directly and without formatting the text. be creative"
        chat_completion = client.chat.completions.create(
            model="google/gemma-7b-it",
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=True,
            max_tokens=50
        )
        answer = ""
        for message in chat_completion:
            msg = message.choices[0].delta.content
            if "eos" not in msg:
                answer += msg
        answer
        return answer