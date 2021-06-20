import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
import async_cse
from SwSpotify import spotify
import json
import time

def info_song():
    nome, artista = spotify.current()
    return nome, artista

def get_key():
    with open("./customsarchgoogleapi.json", "r") as unloaded:
        coso = json.load(unloaded)
        key = coso["key"]
        return key
        
def nome_decente(nome):
    try: 
        final = nome.split()[:2]
        if "feat" in nome.split()[1]:
            str[1]
    except:
        final = nome.split()[:1]
    finally:
        final = " ".join(final)
    return final

async def cerca_link(nome, artista):
    final_name = nome_decente(nome)
    client = async_cse.Search(get_key()) # create the Search client (uses Google by default!)
    ricerca = f"beelyrics {final_name}, {artista}"
    results = await client.search(ricerca, safesearch=False) # returns a list of async_cse.Result objects
    first_result = results[0] # Grab the first result
    await client.close()
    return first_result.url

async def lyrics(link):
    async with aiohttp.ClientSession() as request:
        async with request.get(link) as content:
            soup = BeautifulSoup(await content.text(), 'html.parser')
            lyrics = soup.select_one('div[class^="lyric-body"]').get_text(strip=True, separator='\n')
            lyrics = re.sub("[\[].*?[\]]", "", lyrics)
            return lyrics
