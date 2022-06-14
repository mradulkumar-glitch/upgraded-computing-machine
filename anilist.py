from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from kaibot import Anibot, LOGGER, prefixes
from kaibot.helpers.search import *


# Anime Command
@Anibot.on_message(filters.private & filters.incoming & filters.command("anime", prefixes=prefixes))
async def user_anime(event, message):
   args = message.text
   if not " " in args:
    await message.reply_text("**Give Something To Search**.\n\nUse the format `/anime The Rising of the Shield Hero` or `/anime 11111`", quote=True, parse_mode="md")
   else:
    search = args.split(" ", 1)[-1]
    if search.isdigit():
       variables = {"id": int(search)}
    else:
       variables = {"search": search}
    json = requests.post(
        GRAPHQL, json={"query": anime_query, "variables": variables}
    ).json()
    if "errors" in json:
        return await message.reply_text("Can't Find Any Anime of This Name", quote=True)
    if json:
        json = json["data"]["Media"]
        id = json.get('id')
        mid = json.get('idMal')
        source = json['source'].capitalize()
        if "_" in source:
            source = source.replace("_", " ")
        adult = str(json['isAdult']).capitalize()
        name = f"**[🏳️]** `{json['title']['romaji']}`\n**[🇱🇷]** `{json['title']['english']}`\n**[🇯🇵]** `{json['title']['native']}`"
        type = json['format']
        status = json['status'].capitalize()
        eps = json.get('episodes', 'N/A')
        duration = f"{json.get('duration', 'N/A')} Per Ep."
        score = str(json['averageScore']/10)
        genre = ", ".join(json['genres'])
        siteurl = json["siteUrl"]
        season = json["season"]
        studio = ""
        for x in json["studios"]["nodes"]:
            studio += f"{x['name']}, "
        slen = len(studio) - 2
        studio = studio[0:slen]
        if json["trailer"] is not None:
           trailer = json["trailer"]
           if trailer['site'] == "youtube":
             trailer = f"[Trailer](https://youtu.be/{trailer['id']})"
           else:
             trailer = "N/A"
        else:
            trailer = "N/A"
        site = f"[Anilist]({json['siteUrl']})"
        
        hashtag = json["hashtag"] if json["hashtag"] != None else "N/A"
        image = f"https://img.anili.st/media/{id}"
        msg = f"""
{name}
**Id** | **Malid**: `{id}` | `{mid}`
**⋞ Type:** `{type}`
**⋞ IsAdult:** `{adult}`
**⋞ Status:** `{status}`
**⋞ Source:** `{source}`
**⋞ Score:** `{score}` ✨
**⋞ Season Type:** `{season}`
**⋞ Episodes:** `{eps}`
**⋞ Duration:** `{duration}`
**⋞ Genre:** `{genre}`
**⋞ Studio:** `{studio}`
**⋞ Trailer:** {trailer}
**⋞ SiteUrl:** {site}
**⋞ Hashtag:** {hashtag}"""
        await message.reply_photo(photo=image,
              caption=msg, parse_mode="md")
