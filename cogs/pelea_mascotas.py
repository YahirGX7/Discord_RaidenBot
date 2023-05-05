from discord.ext import commands
from support_classes import *

#This cog is for a primitive "mascot fighting" and for "talk" with the bot 
class pelea_mascotas(commands.Cog):
    def __init__(self, client: commands.Bot):

        #Initialize all we need, like the database, cursor and the object for "talking"
        self.client = client
        self.RaidenTalk = RaidenTalk()
        self.db = DB_pymysql()
        self.cursor = self.db.cur()
    
    #This command first checks if user is already registered with the id of the user, if yes, equips the mascot (that are in a MySQL table), else it tolds the user to register
    @commands.command()
    async def equipar(self, ctx, mascot):
        try:
            id = ctx.author.id
            self.cursor.execute("select user from users where user = (%s);", (id))
            user_result = self.cursor.fetchone()

            if user_result is not None:
                self.cursor.execute("select mascota from mascotasDisponibles where mascota = (%s);", (mascot))
                mascot_result = self.cursor.fetchone()

                if mascot_result is not None: 
                    self.cursor.execute("update users set mascotaEquipada = (%s) where user = (%s);", (mascot, id))
                    self.db.comm()
                
                    ans = Crear_Respuesta(f"Haz equipado a {mascot}!", None)
                    await ctx.reply(embed=ans.enviar)
            
                else:
                    ans = Crear_Respuesta("Esa mascota no existe!", None)
                    await ctx.reply(embed=ans.enviar)
            
            else:
                ans = Crear_Respuesta("Aun no te haz registrado!", None)
                await ctx.reply(embed=ans.enviar)

        except Exception as e:
            await ctx.send(e)

    #Command that shows the mascot the user had equiped, else it tolds they don't already equiped a mascot
    @commands.command()
    async def mascota(self, ctx):
        try:
            id = ctx.author.id
            self.cursor.execute("select mascotaEquipada from users where user = (%s);", (id))
            mascot_result = self.cursor.fetchone()

            if mascot_result is not None:
                answer = Crear_Respuesta(f"Tienes equipado a {mascot_result[0]}!", None)
                await ctx.reply(embed=answer.enviar)

            else:
                answer = Crear_Respuesta("No tienes equipada ninguna mascota!", None)
                await ctx.reply(embed=answer.enviar)

        except Exception as e:
            await ctx.send(e)

    #This commands takes the text of the user and send the answer (using Open AI api)
    @commands.command()
    async def talk(self, ctx, *message):
        try:
            response = self.RaidenTalk.generate_text(message)
            await ctx.send(response)

        except Exception as e:
            await ctx.send(e)

#This is the setup for loading the cog in the bot        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(pelea_mascotas(client)) 
        

    

           
          