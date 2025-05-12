import os
import requests
from backend.conexion.dataBase import supabase


# downloaded txt files will be stored here
CACHE_FOLDER = "cache_texts"
os.makedirs(CACHE_FOLDER, exist_ok=True)

def get_text_from_url(url: str, filename: str):
    local_path = os.path.join(CACHE_FOLDER, filename)

    if os.path.exists(local_path):
        with open(local_path, "r", encoding="utf-8") as file:
            return file.read()

    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        return response.text
    else:
        return f"Error: Could not retrieve {filename}"

def get_knowledge_data():
    response = supabase.table("base_conocimiento").select("*").execute()
    data = response.data
    knowledge = {}

    for entry in data:
        consulta = entry["consulta"]
        url = entry["informacion"]
        filename = url.split("/")[-1].split("?")[0]
        text_content = get_text_from_url(url, filename)
        knowledge[consulta] = text_content
    return knowledge

# example test
if __name__ == "__main__":
    knowledge = get_knowledge_data()
    for question, content in knowledge.items():
        print(f"\n{question}: {content[:200]}...\n")
