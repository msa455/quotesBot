# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 17:00:55 2021

@author: pmjum
"""

import discord
from discord.ext import commands
import os
import requests
import json
from replit import db
from keep_alive import keep_alive
import random

TOKEN = os.environ['TOKEN']

bot = commands.Bot(command_prefix="!")

def add_new_quote(homie, quote):
  if homie in db.keys():
    quotes = db[homie]
    quotes.append(quote)
    db[homie] = quotes
    return f'{quote} successfully added to {homie}\'s list of quotes'
  else:
    db[homie] = [quote]
    return f'"{quote}"" successfully added to {homie}\'s list of quotes'


def list_homie_quotes(homie):
  if homie in db.keys():
    return db[homie]
  else:
    return "This homie doesn't have any quotes saved yet"

def list_all_quotes():
  quotes = {}
  for key in db.keys():
    quotes[key] = db[key]
  return quotes

def delete_quote(homie, quoteToDelete):
  quotes_deleted = []
  if homie in db.keys():
    for x in range(len(db[homie])):
      if db[homie][x].startswith(quoteToDelete):
        quotes_deleted.append(db[homie][x])
        del db[homie][x]
        if len(db[homie]) == 0:
          del db[homie]
    return "Successfully deleted the following quotes: \n" + " \n ".join(quotes_deleted)
  else:
    return "Error: homie does not have any quotes to delete"

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')

@bot.command(name="test")
async def testFunction(ctx, arg):
  await ctx.send(arg)

@bot.command(name="addQuote", help="Adds a quote to the list of homie quotes")
async def addQuote(ctx, homie, quote):
  homie = homie.lower()
  result = add_new_quote(homie,quote)
  print("quote added")
  print(result)
  await ctx.send(result)

@bot.command(name="listQuotes", help="List all quotes for a specific homie")
async def listQuotes(ctx, homie):
  result = ""
  result += homie + "'s quotes: \n"
  quotes = list_homie_quotes(homie)
  for item in quotes:
    result += '"' + item + '"' + "\n"
  print(result)
  await ctx.send(result)

@bot.command(name="getQuote", help="Get a random quote from a specific homie")
async def getQuote(ctx, homie):
  quotes = list_homie_quotes(homie)
  quote = random.choice(quotes)
  result = homie + " said: " + quote
  await ctx.send(result)

@bot.command(name="randomQuote", help="Get a random quote from a random homie")
async def randomQuote(ctx):
  homie = random.choice(list(db.keys()))
  quote = random.choice(db[homie])
  result = homie + " said: " + quote
  await ctx.send(result)


@bot.command(name="listAllQuotes", help="List all quotes stored for the homies")
async def listAllQuotes(ctx):
  quotes = list_all_quotes()
  result = ""
  for key in quotes.keys():
    result += str(key) + ": \n"
    for quote in quotes[key]:
      result += '"' + quote + '"' + "\n"
    result += "\n"
  if result == "":
    await ctx.send("Oops, no messages have been stored yet")
  else: 
    await ctx.send(result)

@bot.command(name="deleteQuote", help="Removes a quote from the list of homie quotes")
async def removeQuote(ctx, homie, quote):
  result = delete_quote(homie,quote)
  await ctx.send(result)

keep_alive()

bot.run(TOKEN)