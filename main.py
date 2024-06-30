import discord
import os
import json
import asyncio
import requests
from utils import Utils
from mail_listener import EmailListener
from mail_sender import EmailSender
from discord.ext import commands
from discord.ext import tasks
from html2image import Html2Image
from EmailObject import Email
from PIL import Image, ImageDraw

bot = discord.Bot()
configs = json.load(open('config.json'))
utils = Utils()
emailList = []
emailListener = EmailListener(configs['email'], configs['password'])
emailSender = EmailSender(configs['email'], configs['password'])
category = None


@bot.event
async def on_ready():
    print('Bot is ready.')
    
    email_Listner.start()



@bot.command(
    debug_guilds = [configs['guild_id']]
)
async def setup(ctx):
    print(emailListener.isSetup())
    if emailListener.isSetup() == True:
        await ctx.respond("Bot is already setup.")
        return
    else:
        emailListener.setupBot()
        #create category
        global category
        category =  await ctx.guild.create_category(name="Emails")
        await ctx.respond("Bot is ")        

@tasks.loop(seconds=30)
async def email_Listner():
    if emailListener.isSetup():
        emails = emailListener.listen()
        counter = 0
        for email in emails:
            print(counter)
            counter += 1
            channel = await category.create_text_channel(name = email['subject'])
            emailList.append(Email(sender=email['sender'], subject=email['subject'], body=email['body'], attachments=email['attachments'], channel=channel.id))
            await channel.send(f"From: {email['sender']}")
            await channel.send(f"Subject: {email['subject']}")
            try:
                if utils.isHTML(email['body']):      
                    hti = Html2Image()
                    with open('email.html', 'w') as f:
                            f.write(email['body'])
                    hti.screenshot(html_file='email.html', save_as='email.png')
                    os.remove('email.html')
                    await channel.send(file=discord.File('email.png'))
                    os.remove('email.png')
                else:
                    email_data = []
                    print(email['body'])
                    string = ''
                    if len(email['body']) > 1990:
                        for char in email['body']:
                            if (len(string) == 1990):
                                email_data.append(string)
                                string = ''
                            else:
                                string+= char
                    else:
                        email_data.append(email['body'])
                    for data in email_data:
                        await channel.send(data)
                        
                
                for attachment in email['attachments']:
                    await channel.send(file=discord.File(attachment.get_payload(decode=True), filename=attachment.get_filename()))
                    os.remove(attachment.get_filename())
            except Exception as e:
                print(e)
                await channel.send("Error: Could not parse this email.")
                await channel.send("This channel will be deleted in 5 minutes.")
                await asyncio.sleep(300)
                await channel.delete() 
        

@bot.command(
    debug_guilds = [configs['guild_id']]
)
async def prune(ctx):
    for channel in ctx.guild.channels:
        await channel.delete()



@bot.command(
    debug_guilds = [configs['guild_id']]
)
async def confirm(ctx):
    await ctx.defer()
    channel = ctx.channel
    messages = await channel.history(limit=100).flatten()
    _email = None
    _subject = ''
    _to = ''
    for email in emailList:
        if email.channel == channel.id:
            _email = email
            _subject = 'Re: ' + email.subject
            _to = email.sender
            if _subject == '':
                _subject = 'No Subject'


    fianlMessage = ''
    files = []
    for message in messages:
        if not message.author.bot:
            if message.attachments:
                for attachment in message.attachments:
                    print(attachment.filename)
                    requests.get(attachment.url)
                    files.append(attachment.filename)

                    with open(attachment.filename, 'wb') as f:
                            f.write(requests.get(attachment.url).content)     
                
                with open('message.txt', 'r') as f:
                        fianlMessage = f.read()
                
    _email.setResponse(fianlMessage)
    utils.text2png(text=fianlMessage, fullpath='image.png', fontsize=20, width=1200)
    emebed = discord.Embed(
        color= discord.Color.green(),
        title = "Email",
    )
    emebed.add_field(name="To", value=_to)
    emebed.add_field(name="Subject", value=_subject)
    print(fianlMessage)
    emebed.add_field(name="Body", value= fianlMessage[0:10]+ "........", inline=False)
    emebed.set_image(url="attachment://image.png")
    emebed.add_field(name="Attachments", value= str(files))
    await ctx.respond(embed=emebed)
    os.remove('image.png')
    
@bot.command( debug_guilds = [configs['guild_id']])
async def send(ctx):
    await ctx.respond("Email sent.")
    for email in emailList:
        if email.channel == ctx.channel.id:
            emailSender.send_email(recipient=email.sender, subject=email.subject, body=email.response, attachments=email.attachments)            
            emailList.remove(email)
            break


@bot.command(
    debug_guilds = [configs['guild_id']]
)
async def getmessages(ctx):
    await ctx.respond("Printing")
    messages = await ctx.channel.history(limit=20).flatten()
    for message in messages:
        if not message.author.bot:
            if message.attachments:
                for attachment in message.attachments:
                    requests.get(attachment.url)
                    print(attachment.filename)
   

bot.run(configs['token'])



