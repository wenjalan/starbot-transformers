from transformers import pipeline
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
generator = pipeline(
  "text-generation", 
  model="wenjalan/starbot-transformers", 
  tokenizer=tokenizer,
)

def generate_message(prompt):
  output = generator(
    f"<msg>{prompt}</msg><msg>",
    max_length=100,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    temperature=0.9,
  )
  response = output[0]["generated_text"].split("</msg>")[1][10:]
  # if response is empty try again
  if response == "":
    return generate_message(prompt)
  return response

import discord
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  # skip messages from bots
  if message.author.bot:
    return

  # if the message mentions the bot
  if client.user in message.mentions:
    print(f"Message from {message.author}: {message.content}")
    response = generate_message(message.content)
    print(f"Response: {response}")
    await message.channel.send(response)

client.run(os.environ.get("BOT_TOKEN"))
