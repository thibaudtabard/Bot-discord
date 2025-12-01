import json
import os
from structures import LinkedList

SAVE_FILE = "history.json"
history = {}  

# charge l'historique 
def load_history():
    global history
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            
        history = {}
        for user_id, cmd_list in data.items():
            ll = LinkedList()
            for cmd in cmd_list:
                ll.append(cmd)
            history[user_id] = ll


# sauvegarde l'historique 

def save_history():
    data_to_save = {}
    for user_id, ll in history.items():
        data_to_save[user_id] = ll.get_all()
        
    with open(SAVE_FILE, "w") as f:
        json.dump(data_to_save, f, indent=4)


# ajoute une commande dans l'hisstorique

def add_command(user_id, command_name):
    user_id = str(user_id)
    if user_id not in history:
        history[user_id] = LinkedList()
    history[user_id].append(command_name)

def get_last(user_id):
    user_id = str(user_id)
    if user_id in history:
        return history[user_id].get_last()
    return None

def get_all(user_id):
    user_id = str(user_id)
    if user_id in history:
        return history[user_id].get_all()
    return []


# clear historique  du joeuuer

def clear_history(user_id):
    user_id = str(user_id)
    if user_id in history:
        history[user_id].clear()
    

def get_command_count(user_id):
    user_id = str(user_id)
    if user_id in history:
        return history[user_id].size()
    return 0