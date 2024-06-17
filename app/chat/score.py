from app.chat.redis import client
import random


def random_component_by_score(component_type, component_map):
    #Make sure component type is 'llm', retriever, memory
    if component_type not in ["llm", "retriever", "memory"]:
        raise ValueError("Invalid component_type")
        
    #From redis, get the hash containing the sum total scores for given component_type
    values = client.hgetall(f"{component_type}_score_values")
    
    #From redis, get the hash containing the number of times each component has been voted on
    counts = client.hgetall(f"{component_type}_score_counts")
    
    #Get all the valid component names from the component map
    names = component_map.keys()
    
    #Loop over those valid names and use them to calculate the average score for each
    #Add average scores and store into a dictionary
    avg_scores = {}
    for name in names:
        score = int(values.get(name, 1))
        count = int(counts.get(name, 1))
        avg = score / count
        avg_scores[name] = max(avg, 0.1)
    
    #Do a weighted random selection
    #sum all the avg scores 
    sum_scores = sum(avg_scores.values())
    #pick a random number from 0 to the sum_scores
    random_val = random.uniform(0,sum_scores)
    cummulative = 0
    #pick up each score from avg_scores and add it into cummulative
    #If the scores for the random_val is less than cummulative use that component; return name
    for name, score in avg_scores.items():
        cummulative += score
        if random_val <= cummulative:
            return name
    

def score_conversation(
    conversation_id: str, score: float, llm: str, retriever: str, memory: str
) -> None:
    score = min(max(score, 0), 1)
    #Stores data at the particular hashes, increments the number stored at particular hash by score 
    #Sets dictionary, look at key of either llm, memory, or retriever, then the score
    client.hincrby("llm_score_values", llm, score)
    client.hincrby("llm_score_counts", llm, 1)
    
    client.hincrby("retriever_score_values", retriever, score)
    client.hincrby("retriever_score_counts", retriever, 1)
    
    client.hincrby("memory_score_values", memory, score)
    client.hincrby("memory_score_counts", memory, 1)


def get_scores():
    #summary of all scores
    #displays the scores in the scores tab of the website
    #stores all the avgerages into a dictionary called aggregate
    aggergate = {"llm": {}, "memory": {}, "retriever": {}}
    
    for component_type in aggergate.keys():
        values = client.hgetall(f"{component_type}_score_values")
        counts = client.hgetall(f"{component_type}_score_counts")
        
        names = values.keys()
        for name in names:
            score = int(values.get(name, 1))
            count = int(counts.get(name, 1))
            avg = score / count
            #updates the component_type at whatever name is, puts it into a list that calculates one number with the avg
            aggergate[component_type][name] = [avg]
    
    return aggergate
