from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests, sys, concurrent.futures
import json, base64
import subprocess
from pyrogram import Client, client,  filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
import pyrogram
from pyrogram import Client, filters
import tgcrypto
from subprocess import getstatusoutput
import helper, format, StudyIQ
import logging
import time
import aiohttp
import asyncio
import aiofiles
from pyrogram.types import User, Message
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib.parse import parse_qs, urlparse
import googleapiclient.discovery

auth_users = int(1981702422) #[ int(chat) for chat in os.environ.get("AUTH_USERS").split(",") if chat != '']
api_id=14741990
bot = Client(
    "psbot",
    bot_token="6092166667:AAGj71k_GHRMz2YvChr1hAcTFkPfnAJNgyY",
    api_id=int(str(api_id)), #int(os.environ.get("API_ID")),
    api_hash="c2b4895438c1cc0e8a32cdd15363e26c"
)

logger = logging.getLogger()
links=[]
    

   
def linkdl(bot, m, url, name, ytf, res, fileno):
    os.makedirs(f"./downloads/{m.chat.id}", exist_ok=True)
    try:
     if ".pdf" in url:
        r = s.get(url, allow_redirects=True, stream=True, verify=False)
        open(f"./downloads/{m.chat.id}/{name}.pdf",'wb').write(r.content)
        
     else:
       cmd = f'yt-dlp --no-check-certificate -f "{ytf}" -o "./downloads/{m.chat.id}/file{fileno}.mp4" "{url}"'       
       download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
       os.system(download_cmd)
       
       
     
    except:
       pass
async def send_media(bot, m, raw_text, links, sn):

  caption = None
  for data in links:
   try:
     name, filename = data["name"], data["filename"]
     editable = await m.reply_text(f"**uploading:-**{name}")
     if ".pdf" in filename:    
        caption = f"**{sn}. {name}.pdf\n\nDescription-\n**{raw_text}"        
        await m.reply_document(f"./downloads/{m.chat.id}/{name}.pdf", caption=caption)       
        os.remove(f"./downloads/{m.chat.id}/{name}.pdf")
     else:
       chat_id, path = m.chat.id, f"./downloads/{m.chat.id}/{filename}"
       subprocess.run(f'ffmpeg -i "{path}" -ss 00:00:19 -vframes 1 "{path}.jpg"', shell=True)
       thumbnail = f"{path}.jpg"
       dur = int(helper.duration(path))
       caption = f"**{sn}. {name}.mkv**\n\n**Description-\n**{raw_text}"
       await bot.send_video(chat_id = chat_id, video=path, caption=caption, thumb=thumbnail, duration=dur, supports_streaming=True, height=720,width=1280)
       
       os.remove(path)
       os.remove(thumbnail)
     await editable.delete(True)
   except Exception as e:
     try:
       await bot.send_message(chat_id=chat_id, text=e)
       
       os.remove(path)
       os.remove(thumbnail)
     except:
       await m.reply_text(f"Video Downloading Failed \n{caption}")
       await m.reply_text(e)      
   sn+=1
def formatSL(format_id, resolution):
     try:
       print(format_id)
       if resolution == "low":          
             ytf = format_id[0] 
       elif resolution == "medium":
            ytf = format_id[len(format_id)//2]
       elif resolution == "high":
          if len(format_id) >= 3:
             ytf = format_id[len(format_id)-1]
               
       
       for data in ytf:
          ytf, res = (ytf[data]), data
          return ytf, res
     except Exception as e:
        print(e)
        ytf, res = "best", "best"
        return ytf, res
     
def download(i, arg, m, bot, resolution, content):
    try:
          
          rawName, fileno =  content[i].split(":")[0], 1+i 
          url = content[i].replace(f"{rawName}:","")    
         # url = "http"+str(url)
          
          name = (
            rawName.replace("/", "")
            .replace("|", "_")
            .replace("*", "")
            .replace("?", "")
            .replace("#", "")
            .replace("\t", "")
            .replace(":", "-")
            .replace(";", "")
            .replace("+", "")
            .replace("@", "")
            .replace("'", "")
            .replace('"', '')
            .replace("{", "(")
            .replace("}", ")")
            .replace("`", "")
            .replace("__", "_")
            .strip()
          )      
          #print(links)
          if url.startswith("http"):
             try:
              filename = f"file{fileno}.mp4" if ".pdf" not in url else f"{name}.pdf"
              links.append({"name":name, "filename":filename})
              if ".pdf" not in url:
               
                format_id = format.get_resolution(url)
                ytf, res = formatSL(format_id, resolution)
                
              else:
                ytf, res = "", ""
              
              if "manifest.prod.boltdns" in url:
                      ytf = f"{ytf}, bestvideo+bestaudio"
              elif "vimeo" in url:
                      ytf = f"{ytf}, bestvideo+bestaudio"
              else:
                      ytf = f"{ytf}, best"
              
              json3 = linkdl(bot, m, url, name, ytf, res, fileno)
              
             except Exception as e:
                print(f"{e}")
                
    except Exception as exception:
          print(exception)
@bot.on_message(filters.command(["download_txt"]))   
async def drm(bot: Client, m: Message):
   edit = await m.reply_text("Send .txt file.")
   @bot.on_message(filters.document)
   async def processdoc(bot:Client, m:Message):
    x = await m.download()
    resolution, raw_text, arg = "medium", "", 0
    
    if m.caption is not None:
       cap = m.caption.strip().replace(" :",":").replace(": ", ":").split("\n")
       for data in cap:
            
            if "resolution:" in data:
                 reso= data.split(":")[-1]
                 resolution = reso
            elif "sn:" in data:
                 arg1 = data.split(":")[-1]                             
                 arg = int(arg1)-1 if arg1!=0 else 0          
            else:
                 raw_text+=data+"\n"
               
            
       
    else: 
        arg = 0
    if resolution not in ["low", "medium", "high"]:
           resolution = "medium"
    print("arg:", arg) 
    sn=arg+1
    print("raw_text2:", raw_text)
    try:
       with open(x) as f:
           content = f.read().strip()
       content = content.replace(": http", ":http").split("\n")

       os.remove(x)
    except:
         await m.reply_text("fcuk! wrong input")
         os.remove(x)
         return
    print(content)
    total_links = len(content) + 1 - arg if arg!=0 else len(content)
    await m.reply_text(f"**total links found: {total_links}**")
    editable=await m.reply_text("Downloading all the links to cloud storage, you can rest or wait until completion of the process🙂")
    start_time=time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
          results = [executor.submit(download, i, arg, m, bot, resolution, content) for i in range(arg, len(content))]
    end_time=time.time()  
    await editable.edit(f"Downloading Completed😴\n\n\n\nUploading gonna starts now😋**")
    e_time=end_time-start_time
    hour, minute, seconds = int(e_time//3600), int(e_time%3600//60), int(e_time%3600%60)    
    await m.reply_text(f"Downloaded in **{hour} hours, {minute}minutes & {seconds}seconds**")
    print(links)
    await send_media(bot, m, raw_text, links, sn)
    await editable.delete(True)
    await m.reply_text(f"**completed!**")
@bot.on_message(filters.command(["stiq"]) & filters.chat(auth_users))  
async def stiq(bot: Client, m: Message):
     r = requests.Session()
     editable = m.text
     inpurl = editable.replace("/stiq ","")
     boturl = inpurl.split("?")[1].replace(".","\.").replace("-","\-").replace("=",":")
     try:
        course_title = await StudyIQ.extdata(inpurl)
        await m.reply_document(f"{course_title}.txt", caption=f"**{course_title}\n#BHAUKAL**")
        os.remove(f"{course_title}.txt") 
     except Exception as e:
        await m.reply_text(e)
        os.remove(f"{course_title}.txt")
                  
bot.run()                      
