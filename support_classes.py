import discord
import pymysql
import openai
import json
import os

#This class allows us to show an answer with an discord embed 
class Crear_Respuesta():
        def __init__(self, title, content):
            self.title = title
            self.content = content

            self.respuesta = discord.Embed(
                title=self.title,
                description=self.content,
                colour=int("DC75FF", 16)
            )

        @property
        def enviar(self):
            return self.respuesta

#This class allows us to connect a MySQL database using a config file         
class DB_pymysql():
    def __init__(self):
        self.path_file = os.path.join(r"C:\Users\wearethewarriors\Downloads\Proyectos_personales\Bot de curiosidades\discord music bot\cogs", "config.json") 
        self.file = open(self.path_file, "r")
        self.config = json.load(self.file)
        self.connections = self.StartConnection()

    #Function that returns the connection object
    def StartConnection(self):
        connection = pymysql.connect(host=self.config["host"],
                                     password=self.config["password"],
                                     database=self.config["database"],
                                     port=self.config["port"],
                                     user=self.config["user"])
        return connection
    
    #Function that returns a cursor object
    def cur(self):
        return self.connections.cursor()
    
    #Function that commits thing like inserts, update, etc
    def comm(self):
        self.connections.commit()

#This class uses Open AI api to allow the users "talk" with the bot    
class RaidenTalk():
    def __init__(self):
        self.api_key = "Your_api_key_here"

    #Function that takes a text provided by user, process it and returns the response
    def generate_text(self, message):
        text = " ".join(message)
        openai.api_key = self.api_key
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.3,
        max_tokens=150)

        return response.choices[0].text