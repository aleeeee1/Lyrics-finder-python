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
    with open("./customsarchgoogleapi.json", "r") as unloaded: #https://developers.google.com/custom-search/v1/overview#api_key
        coso = json.load(unloaded)
        key = coso["key"]
        return key
        

async def cerca_link(nome, artista):
    client = async_cse.Search(get_key()) 
    ricerca = f"site:https://genius.com {nome}, {artista}"
    results = await client.search(ricerca, safesearch=False) 
    await client.close()
    final = results[0]
    index = 1
    print(final.url)
    while "-lyrics" not in final.url:
        final = results[index]
        index += 1
        if index == 10:
            break
    return final.url

async def lyrics(link):
    async with aiohttp.ClientSession() as request:
        async with request.get(link) as content:
            soup = BeautifulSoup(await content.text(), 'html.parser')
            try:
                lyrics = soup.select_one('div[class^="lyrics"]').get_text(strip=True, separator='\n')
                lyrics = re.sub("[\[].*?[\]]", "", lyrics)
            except Exception as e:
                with open ("./repo.html", "w", encoding='utf-8') as file:
                  file.write(str(soup))                
                lyrics = "Qualcosa è andato storto :/\nProva a ricaricare (anche più volte)"
            return lyrics
