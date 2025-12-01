import random

current_matches = {} 

class MatchState:
    def __init__(self):
        self.score_user = 0
        self.score_bot = 0
        self.period = 1
        self.status = "ongoing"
        self.message = "Le match commence ! Première période. Le score est 0 - 0."
        self.actions_available = ["Tir au but", "Passe", "Mise en échec"]
        
    def get_status_message(self):
        return f"🏒 Période {self.period}/3 | Score : VOUS {self.score_user} - BOT {self.score_bot}"

    def resolve_action(self, choice):
        scored_goal_user = False 
        scored_goal_bot = False  
        
        message_result = ""
        
        # le aleatoire 
        if random.random() < 0.35:
            self.score_bot += 1
            scored_goal_bot = True
        
        if choice == "Tir au but":
            if random.random() > 0.4:
                self.score_user += 1
                scored_goal_user = True
                message_result = "GOAL! Vous marquez un point avec un tir précis!"
            else:
                message_result = "Tir arrêté par le gardien adverse! Dommage."
                
        elif choice == "Passe":
            if random.random() > 0.7:
                self.score_user += 1
                scored_goal_user = True
                message_result = "Passe réussie et but sur la contre-attaque! Magnifique jeu d'équipe."
            else:
                message_result = "Passe interceptée! L'adversaire récupère le palet."

        elif choice == "Mise en échec":
            if random.random() > 0.8:
                message_result = "Mise en échec réussie! Vous récupérez la rondelle."
            elif random.random() > 0.6:
                message_result = " Pénalité ! Vous êtes envoyé au banc pour 2 minutes."
            else:
                message_result = "La mise en échec échoue, l'adversaire continue son action."
        
        self.period += 1
        
        if self.period > 3:
            final_res_dict = self.finalize() 
            return {
                "message": f"{message_result}\n\n{final_res_dict['message']}", 
                "status": self.status, 
                "scored_goal_user": scored_goal_user, 
                "scored_goal_bot": scored_goal_bot,
                "user_won": final_res_dict.get("user_won", False),
                "bot_won": final_res_dict.get("bot_won", False)
            }

        return {
            "message": f"{message_result}\n\n{self.get_status_message()}", 
            "status": self.status, 
            "scored_goal_user": scored_goal_user, 
            "scored_goal_bot": scored_goal_bot,
            "user_won": False, 
            "bot_won": False
        }

    def finalize(self):
        """Détermine le résultat final du match ou lance les tirs au but."""
        user_won = False 
        bot_won = False
        final_message = ""

        if self.score_user > self.score_bot:
            self.status = "finished"
            user_won = True
            final_message = f" VICTOIRE ! Score final : {self.score_user} - {self.score_bot}. Vous avez dominé la glace."
        elif self.score_user < self.score_bot:
            self.status = "finished"
            bot_won = True
            final_message = f" DÉFAITE ! Score final : {self.score_user} - {self.score_bot}. Le bot a été plus solide aujourd'hui."
        else:
            self.status = "penalty_shootout"
            self.message = "Égalité ! Nous allons aux tirs au but !"
            self.actions_available = ["Tirer à gauche", "Tirer au centre", "Tirer à droite"]
            final_message = f" ÉGALITÉ ! Le match se termine sur un score de {self.score_user} - {self.score_bot}.\n**Passons aux tirs au but !**"
        
        return {
            "message": final_message,
            "user_won": user_won,
            "bot_won": bot_won
        }


    def resolve_penalty(self, choice):
        scored_goal_user = False
        scored_goal_bot = False
        
        message_penalty = ""

        if (choice == "Tirer à gauche" and random.random() < 0.6) or \
           (choice == "Tirer au centre" and random.random() < 0.3) or \
           (choice == "Tirer à droite" and random.random() < 0.6):
            self.score_user += 1
            scored_goal_user = True
            message_penalty = "GOAL ! Le gardien a été déjoué !"
        else:
            message_penalty = "Arrêt du gardien adverse ! Tir manqué."
            
        if random.random() < 0.5:
            self.score_bot += 1
            scored_goal_bot = True
            message_penalty += "\nLe bot marque aussi. C'est serré !"
        else:
            message_penalty += "\nLe bot rate son tir ! C'est votre chance !"

        self.status = "finished" 
        final_res_dict = self.finalize() 
        
        return {
            "message": f"{message_penalty}\n\n**Tirs au but terminés.**\n{final_res_dict['message']}", 
            "status": self.status, 
            "scored_goal_user": scored_goal_user, 
            "scored_goal_bot": scored_goal_bot,
            "user_won": final_res_dict.get("user_won", False),
            "bot_won": final_res_dict.get("bot_won", False)
        }

def start_match(user_id):
    new_match = MatchState()
    current_matches[str(user_id)] = new_match
    return {"message": new_match.message, "status": new_match.status, "scored_goal_user": False, "scored_goal_bot": False, "user_won": False, "bot_won": False}

def process_choice(user_id, choice):
    uid = str(user_id)
    if uid not in current_matches or current_matches[uid].status == "finished":
        return {"message": "Match non trouvé. Utilisez `/hockey_match` pour commencer.", "status": "finished", "scored_goal_user": False, "scored_goal_bot": False, "user_won": False, "bot_won": False}

    match = current_matches[uid]
    
    if match.status == "penalty_shootout":
        res_dict = match.resolve_penalty(choice)
    else:
        res_dict = match.resolve_action(choice)

    if match.status == "finished":
        del current_matches[uid]

    return res_dict