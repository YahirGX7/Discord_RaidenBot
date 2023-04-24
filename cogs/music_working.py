import discord
from discord.ext import commands
import random
import json
from support_classes import *
import os

#This cog is for play music, pause it, resume it, play another song, and kick the bot of the voice channel
class music_working(commands.Cog):
    def __init__(self, client: commands.Bot):

        #Initialize all we need, the config file, the database, cursor and the music numbers for choosing
        self.path_file = os.path.join(r"C:\Users\wearethewarriors\Downloads\Proyectos_personales\Bot de curiosidades\discord music bot\cogs", "config.json")
        self.file = open(self.path_file, "r")
        self.config = json.load(self.file)
        self.DB = DB_pymysql()
        self.cursor = self.DB.cur()
        self.client = client
        self.music = self.config["values_choose"]["musica"]

    #This command, gets the path from database and stores it in variable "audio", then plays it with ffmpeg
    @commands.command()
    async def play(self, ctx):
  
        #If the user is in a voice channel, gets a random path and plays it
        if ctx.author.voice:
            choose = random.randint(self.music["min"], self.music["max"])
            self.cursor.execute("select musicpath from musicpaths where id = (%s);", (choose))
            result = self.cursor.fetchone()
    
            audio = os.path.join(self.config["paths_music"], result[0])
            channel = ctx.author.voice.channel
            voice = await channel.connect()

            #Plays the music with FFmpegPCMAudio
            voice.play(discord.FFmpegPCMAudio(source=audio, executable="C:/ffmpeg/bin/ffmpeg.exe"))

        #Else, it tolds the user that they have to connect a voice channel
        else:
            answer = Crear_Respuesta("Conectate a voz primero brou", None)
            await ctx.reply(embed=answer.enviar)

    @commands.command()
    #This command kick the bot from the voice channel
    async def salir(self, ctx):
        await ctx.voice_client.disconnect()

    #This pause the song that is already playing
    @commands.command()
    async def pausar(self, ctx):
        await ctx.voice_client.pause()

    #This resumes it 
    @commands.command()
    async def reanudar(self, ctx):
        await ctx.voice_client.resume()

    #And this is for playing another song, staying in the voice channel
    @commands.command()
    async def po(self, ctx):
        choose = random.randint(self.music["min"], self.music["max"])

        self.cursor.execute("select musicpath from musicpaths where id = (%s);", (choose))
        result = self.cursor.fetchone()

        audio = os.path.join(self.config["paths_music"], result[0])
        voice = ctx.guild.voice_client
        
        #If the user is in the voice channel, plays another song
        if voice != None:
            voice.stop()
            voice.play(discord.FFmpegPCMAudio(source=audio, executable="C:/ffmpeg/bin/ffmpeg.exe"))

        #Else, it tolds the user that they have to connect a voice channel
        else:
            answer = Crear_Respuesta("Conectate a voz primero brou", None)
            await ctx.reply(embed=answer.enviar)

#This is the setup for loading the cog in the bot
async def setup(client: commands.Bot) -> None:
    await client.add_cog(music_working(client))



        