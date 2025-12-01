# tree.py

from structures import TreeNode

#arbre (quizz hockey)

root = TreeNode(content="Aimes-tu le hockey sur glace ?")
yes_1 = TreeNode(content="Préféres-tu jouer ou regarder des matchs ?")
no_1 = TreeNode(content="Tu préfères un autre sport ?")

root.add_child("oui", yes_1)
root.add_child("non", no_1)

yes_2 = TreeNode(content="Tu joues plutôt attaquant ?")
no_2 = TreeNode(content="Ton équipe préférée est-elle en NHL ?")

yes_1.add_child("jouer", yes_2)
yes_1.add_child("regarder", no_2)

yes_2.add_child("oui", TreeNode(content="Tu es un attaquant ! ok c'est cool", is_result=True))
yes_2.add_child("non", TreeNode(content="Défenseur ! tu es la pour protéger tonéquipe gg.", is_result=True))

no_2.add_child("oui", TreeNode(content="Fan de NHL! Les Canadiens sont les meilleurs !", is_result=True))
no_2.add_child("non", TreeNode(content="Supporter son équipe c'est important bravo !", is_result=True))

no_1.add_child("oui", TreeNode(content="Le foot c'est de la merde vient faire du Hockey un sport Homme !", is_result=True))
no_1.add_child("non", TreeNode(content="Alala après ta game de LOL faut aller prendre une douche !", is_result=True))

conversation_tree = root
user_pos = {}

# focntion de arbre 

def start_discussion(user_id):
    user_pos[str(user_id)] = conversation_tree
    return conversation_tree.content

def answer(user_id, choice):
    uid = str(user_id)
    if uid not in user_pos:
        return "Commence avec /quizz_hockey"

    current_node = user_pos[uid]
    next_node = current_node.get_child(choice)

    if not next_node:
        return "Réponse non valide pour cette question. Veuillez choisir parmi les options."
    
    user_pos[uid] = next_node

    if next_node.is_result:
        del user_pos[uid]
        return next_node.content
    else:
        return next_node.content

def reset_tree(user_id):
    user_pos[str(user_id)] = conversation_tree
    return "Discussion réinitialisée."

def contains_topic(node, topic):
    topic_lower = topic.lower()
    
    if topic_lower in node.content.lower():
        return True
    
    if topic_lower in node.get_available_keys():
        return True
        
    for child in node.children.values():
        if contains_topic(child, topic):
            return True
            
    return False

def get_tree_stats(node):
    if not node:
        return 0, 0, set()
    
    num_questions = 1 if not node.is_result else 0
    num_results = 1 if node.is_result else 0
    results_set = {node.content} if not node.is_result else {node.content}

    for child in node.children.values():
        q, r, s = get_tree_stats(child)
        num_questions += q
        num_results += r
        results_set.update(s)
        
    return num_questions, num_results, results_set

def get_stats():
    num_q, num_r, results = get_tree_stats(conversation_tree)
    unique_conclusions = {r for r in results if r.startswith(("Tu es un attaquant", "Défenseur !", "Fan de NHL!", "Supporter son équipe", "Le foot c'est de la merde", "Alala après ta game de LOL"))}
    
    return {
        "total_nodes": num_q + num_r,
        "total_questions": num_q,
        "unique_conclusions": len(unique_conclusions)
    }