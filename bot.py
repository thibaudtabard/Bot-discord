
import discord
from discord.ext import commands
from discord.ui import Button, View
import tree
import history
import game 
from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents) 

# iamge
GOAL_IMAGE_USER_FILE = "goal.png"
GOAL_IMAGE_BOT_FILE = "goal_bot.png"
VICTORY_IMAGE_USER_FILE = "victoire.png"
VICTORY_IMAGE_BOT_FILE = "victoire_bot.png"


# Command pour que le slash focntionne

@bot.event
async def on_ready():
    history.load_history()
    await bot.tree.sync() 
    print(f"Connecté en tant que {bot.user}")

@bot.event
async def on_disconnect():
    history.save_history()
    

#focntion "o" et "ok"

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()
    
    # "o" k
    if content == "o":
        await message.channel.send("k")
        
    #"ok" hockey
    elif content == "ok":
        await message.channel.send("EH!!! RESPECTE LE SPORT LE HOCKEY SUR GLACE EST SUPER !!!")
    await bot.process_commands(message)

# /nombre pour compter de 1 a 10
@bot.tree.command(name="nombre", description="Compte de 1 à 10.")
async def nombre_slash(interaction: discord.Interaction):
    numbers = [str(i) for i in range(1, 11)]
    output_message = "\n".join(numbers)
    
    await interaction.response.send_message(f"**Comptage de 1 à 10 :**\n{output_message}")
    history.add_command(interaction.user.id, "nombre")

# derniere commande effectuer
@bot.tree.command(name="derniere_commande", description="Affiche votre dernière commande enregistrée.")
async def last_slash(interaction: discord.Interaction):
    cmd = history.get_last(interaction.user.id)
    await interaction.response.send_message(f"Dernière commande enregistrée : **/{cmd}**" if cmd else "Aucune commande enregistrée.")
    history.add_command(interaction.user.id, "derniere_commande")

# pour voir historique
@bot.tree.command(name="historique", description="Affiche l'historique complet de toutes vos commandes (Fonctionnalité Supp. 1: Embed).")
async def allcmd_slash(interaction: discord.Interaction):
    cmds = history.get_all(interaction.user.id)
    
    if not cmds:
        await interaction.response.send_message("Aucune commande enregistrée dans votre historique.", ephemeral=True)
        return
        
    cmd_list = [f"**{i+1}.** `/{cmd}`" for i, cmd in enumerate(cmds)]
    
    embed = discord.Embed(
        title=f"📜 Historique des Commandes de {interaction.user.display_name}",
        description="\n".join(cmd_list),
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Total: {len(cmds)} commandes.")
    await interaction.response.send_message(embed=embed)
    history.add_command(interaction.user.id, "historique")

#supprimer historique
@bot.tree.command(name="clearhistory", description="Vide votre historique de commandes.")
async def clearhistory_slash(interaction: discord.Interaction):
    history.clear_history(interaction.user.id)
    await interaction.response.send_message("Historique des commandes vidé.")
    history.add_command(interaction.user.id, "clearhistory")
    
    #afficher jsute le nombre de commande effectuer
@bot.tree.command(name="total_commande", description="Affiche le nombre total de commandes exécutées (Fonctionnalité Supp. 2: Compteur).")
async def mycount_slash(interaction: discord.Interaction):
    count = history.get_command_count(interaction.user.id)
    await interaction.response.send_message(f"Vous avez exécuté **{count}** commandes depuis votre première connexion.")
    history.add_command(interaction.user.id, "total_commande")


# tree pour le quizz hockey
@bot.tree.command(name="quizz_hockey", description="Lance le questionnaire sur vos préférences de hockey.")
async def help_hockey_slash(interaction: discord.Interaction):
    q = tree.start_discussion(interaction.user.id)
    current_node = tree.user_pos[str(interaction.user.id)] 
    view = create_quizz_view(interaction.user.id, current_node)
    
    await interaction.response.send_message(f"**Question :** {q}", view=view)
    history.add_command(interaction.user.id, "quizz_hockey") 

# reset 
@bot.tree.command(name="reset", description="Réinitialise votre discussion en cours avec le bot.")
async def reset_slash(interaction: discord.Interaction):
    res = tree.reset_tree(interaction.user.id)
    await interaction.response.send_message(res)
    history.add_command(interaction.user.id, "reset")

# sujet quizz
@bot.tree.command(name="sujet_quizz", description="Vérifie si un sujet existe dans l'arbre de discussion.")
async def speak_about_slash(interaction: discord.Interaction, topic: str):
    exists = tree.contains_topic(tree.conversation_tree, topic)
    await interaction.response.send_message("Oui, ce sujet existe dans l'arbre." if exists else "Non, ce sujet n'existe pas.")
    history.add_command(interaction.user.id, "sujet_quizz")

# stats du quizz
@bot.tree.command(name="stats_quizz", description="Affiche les statistiques de l'arbre de conversation.")
async def treestats_slash(interaction: discord.Interaction):
    stats = tree.get_stats()
    
    embed = discord.Embed(
        title=" Statistiques de l'Arbre de Discussion",
        description="Aperçu de la complexité de l'arbre de conversation.",
        color=discord.Color.green()
    )
    embed.add_field(name="Nombre Total de Nœuds", value=stats["total_nodes"], inline=True)
    embed.add_field(name="Nombre de Questions", value=stats["total_questions"], inline=True)
    embed.add_field(name="Conclusions Uniques", value=stats["unique_conclusions"], inline=True)
    
    await interaction.response.send_message(embed=embed)
    history.add_command(interaction.user.id, "stats_quizz")

# match de hockey
@bot.tree.command(name="hockey_match", description="Lance un match de hockey interactif avec des choix de jeu.")
async def hockey_match_slash(interaction: discord.Interaction):
    start_info = game.start_match(interaction.user.id)
    match_state = game.current_matches[str(interaction.user.id)]
    view = create_match_view(interaction.user.id, match_state.actions_available)
    
    await interaction.response.send_message(f"🚨 **Match lancé !**\n{start_info['message']}", view=view)
    history.add_command(interaction.user.id, "hockey_match")



#bouton du Quizz
def create_quizz_view(user_id, current_node):
    view = View(timeout=300) 
    options = current_node.get_available_keys()

    for opt in options:
        btn = Button(label=opt.capitalize(), style=discord.ButtonStyle.primary)

        async def callback(interaction: discord.Interaction, choice=opt):
            if interaction.user.id != user_id:
                await interaction.response.send_message("Ce n'est pas votre session ! Lancez `/quizz_hockey` pour commencer votre propre discussion.", ephemeral=True)
                return

            response = tree.answer(user_id, choice)
            
            is_result = any(keyword in response for keyword in ["attaquant", "Défenseur", "Fan de NHL", "Supporter", "Le foot", "Alala après"])

            if is_result:
                await interaction.response.edit_message(content=f"**Réponse :** {choice.capitalize()}\n\n**Conclusion :** {response}", view=None)
            else:
                next_node = tree.user_pos.get(str(user_id))
                if next_node:
                    next_view = create_quizz_view(user_id, next_node)
                    await interaction.response.edit_message(content=f"**Réponse :** {choice.capitalize()}\n\n**Nouvelle Question :** {response}", view=next_view)
                else:
                    await interaction.response.edit_message(content=f"**Réponse :** {choice.capitalize()}\n\n**Conclusion :** {response}", view=None)


        btn.callback = callback
        view.add_item(btn)
        
    cancel_btn = Button(label="Fermer la discussion", style=discord.ButtonStyle.danger)
    async def cancel_callback(interaction: discord.Interaction):
        if interaction.user.id == user_id:
            tree.reset_tree(user_id) 
            await interaction.response.edit_message(content="Discussion fermée. Utilisez `/quizz_hockey` pour recommencer.", view=None)
        else:
            await interaction.response.send_message("Ce n'est pas votre session !", ephemeral=True)
    cancel_btn.callback = cancel_callback
    view.add_item(cancel_btn)

    return view

# bouton du Match de Hockey
def create_match_view(user_id, options):
    view = View(timeout=None)

    for opt in options:
        btn = Button(label=opt, style=discord.ButtonStyle.success if "Tir" in opt or "Passe" in opt else discord.ButtonStyle.primary)

        async def callback(interaction: discord.Interaction, choice=opt):
            await interaction.response.defer() 
            
            if interaction.user.id != user_id:
                await interaction.followup.send("Ce n'est pas votre match !", ephemeral=True)
                return

            res_dict = game.process_choice(user_id, choice)
            
            if res_dict["scored_goal_user"]:
                await interaction.followup.send("GOALLLL pour vous !", file=discord.File(GOAL_IMAGE_USER_FILE))
            
            if res_dict["scored_goal_bot"]:
                await interaction.followup.send("BUT adverse !", file=discord.File(GOAL_IMAGE_BOT_FILE))

            if res_dict["user_won"]:
                await interaction.followup.send(" INCROYABLE VICTOIRE !", file=discord.File(VICTORY_IMAGE_USER_FILE))
            elif res_dict["bot_won"]:
                await interaction.followup.send(" DOMMAGE, le bot a gagné !", file=discord.File(VICTORY_IMAGE_BOT_FILE))
            
            match_state = game.current_matches.get(str(user_id))
            
            if not match_state or match_state.status == "finished":
                await interaction.message.edit(content=f"**Votre action :** {choice}\n\n{res_dict['message']}", view=None)
            else:
                next_view = create_match_view(user_id, match_state.actions_available)
                await interaction.message.edit(content=f"**Votre action :** {choice}\n\n{res_dict['message']}", view=next_view)

        btn.callback = callback
        view.add_item(btn)

    return view

# Lancer le bot
bot.run(TOKEN)