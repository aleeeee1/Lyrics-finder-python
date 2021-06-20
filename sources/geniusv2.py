import aiohttp
from bs4 import BeautifulSoup
import re
import async_cse
import json

from win32gui import PostThreadMessage
from utils import spotifyAPI



def info_song():
    nome, artista = spotifyAPI.song_info()
    return nome, artista

def get_key():
    with open(r"./utils/customsarchgoogleapi.json", "r") as unloaded: #https://developers.google.com/custom-search/v1/overview#api_key
        coso = json.load(unloaded)
        key = coso["key"]
        return key
        

async def cerca_link(nome, artista):
    client = async_cse.Search(get_key())
    ricerca = f"site:https://genius.com {nome}, {artista} lyrics"
    print(ricerca)
    results = await client.search(ricerca, safesearch=False)
    await client.close()
    ok = False
    index = 0
    while not ok:
        final = results[index]
        if "lyrics" in final.url:
            if "translation" not in final.url or "translations" in final.url:
                ok = True
        if index == 10:
            break
        index += 1
    return final.url

async def get_content(link):
    async with aiohttp.ClientSession() as request:
        async with request.get(link) as content:
            text = await content.text()
            await request.close()
            return text
                

async def lyrics(link):

    tries = 10
    error = True

    while tries != 0:
        if not error:
            break
        content = await get_content(link)
        soup = BeautifulSoup(content, 'html.parser')
        try:
            lyrics = soup.select_one('div[class^="lyrics"]').get_text(strip=True, separator='\n')
            # lyrics = re.sub("[\[].*?[\]]", "", lyrics)
            error = False
        except AttributeError as e :
            # with open ("./repo.html", "w", encoding='utf-8') as file:
            #     file.write(str(soup))
            if tries == 1:
                lyrics = "10 tentativi effettuati, c'è qualcosa che non va :/"
            tries -= 1
            pass
        


    return lyrics
