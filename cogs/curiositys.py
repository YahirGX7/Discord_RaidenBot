import discord
from discord.ext import commands
import random
import json
import os
from support_classes import *

#This class is for a RockPaperScissors minigame with discord buttons
class RPS(discord.ui.View, commands.Cog):
    def __init__(self):
        super().__init__()
        #The choices that bot can do
        self.choices = {1: "Piedra", 2: "Papel", 3: "Tijera"}

    #Button for "Stone", shows different answer if you win, loose or tie
    @discord.ui.button(label="Piedra", style=discord.ButtonStyle.gray)
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        bot_choice = random.choice([1, 2, 3])

        #Loose answer
        if bot_choice == 2:
            await interaction.response.send_message("Perdiste! por malo ehe, pero de chill.")

        #Win answer    
        elif bot_choice == 3:
            await interaction.response.send_message("Ganaste, re falso ehe.")

        #Tie answer    
        else:
            await interaction.response.send_message("Empate! Tambien elegi piedra pa.")

    #Button for "Paper", shows different answer if you win, loose or tie
    @discord.ui.button(label="Papel", style=discord.ButtonStyle.green)
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        bot_choice = random.choice([1, 2, 3])

        #Loose answer
        if bot_choice == 3:
            await interaction.response.send_message("Perdiste! Metete a un curso de esto pa que te reviento.")

        #Win answer    
        elif bot_choice == 1:
            await interaction.response.send_message("Ganaste, pero sigues sin saberle.")

        #Tie answer
        else:
            await interaction.response.send_message("Empate! Pero como? no se vale.")

    #Button for "Scissors", shows different answer if you win, loose or tie
    @discord.ui.button(label="Tijera", style=discord.ButtonStyle.blurple)
    async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        bot_choice = random.choice([1, 2, 3])

        #Loose answer
        if bot_choice == 1:
            await interaction.response.send_message("Perdiste! Como Francia contra Argentina ehe.")

        #Win answer    
        elif bot_choice == 2:
            await interaction.response.send_message("Ganaste, pero porque no le heche ganas.")

        #Tie answer    
        else:
            await interaction.response.send_message("Empate! Reñido eh.")

#This cog is for register the user to an "economy", show they coins, play RockPapersScissors and send a random curiosity using a config file and a MySQL database
class curiositys(commands.Cog):
    def __init__(self, client: commands.Bot):

        #Initializing everything we need, the config file, the database, cursor and curiositys numbers
        self.client = client
        self.path_file = os.path.join(r"C:\Users\wearethewarriors\Downloads\Proyectos_personales\Bot de curiosidades\discord music bot\cogs", "config.json")
        self.file = open(self.path_file, "r")
        self.config = json.load(self.file)
        self.DB = DB_pymysql()
        self.cursor = self.DB.cur()
        self.curi = self.config["values_choose"]["curiosidades"]

    #This register the user id in the "economy" with 50 free coins
    @commands.command(help="Registro en la economia!")
    async def registrar(self, ctx):
        id = ctx.author.id
        self.cursor.execute("SELECT user from users where user = (%s);", (id))
        result = self.cursor.fetchone()
        
        if result is None:
            self.cursor.execute("INSERT INTO users (user,coins) VALUES (%s,%s);", (id, 50))
            self.DB.comm()

            respuesta = Crear_Respuesta("Registrado!, con 50 monedas de regalo :3", None)
            await ctx.reply(embed=respuesta.enviar)
           
        else:
            respuesta = Crear_Respuesta("¡Ya te haz registrado!", None)
            await ctx.reply(embed=respuesta.enviar)

    #This shows the user coins using the id
    @commands.command(help="Checar tu saldo!")
    async def coins(self, ctx):
        id = ctx.author.id
        
        self.cursor.execute("SELECT coins from users where user = (%s);", (id))
        result = self.cursor.fetchone()
        
        if result is None:
            answer = Crear_Respuesta("Aun no te haz registrado!", None)
            await ctx.reply(embed=answer.enviar)
           
        else:
            name = ctx.author
            answer = Crear_Respuesta(f"{name}, tienes {result[0]} monedas!", None)
            await ctx.reply(embed=answer.enviar)   

    #Command that display the RockPaperScissors minigame    
    @commands.command()
    async def rck(self, ctx):
        view = RPS()
        await ctx.reply(view=view)

    #This sends a random curiosity from the database
    @commands.command()
    async def curiosidad(self, ctx):
        choose = random.randint(self.curi["min"], self.curi["max"])

        self.cursor.execute("SELECT curiosity from curiositys where id = (%s);", (choose))
        result = self.cursor.fetchone()
        
        answer = Crear_Respuesta(f"Sabias que... {result[0]}", None)
        await ctx.reply(embed=answer.enviar)

#This is the setup for loading the cog in the bot        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(curiositys(client))

    