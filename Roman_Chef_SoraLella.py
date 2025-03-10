import os
from openai import OpenAI
client = OpenAI(
   api_key=os.environ.get("OPENAI_API_KEY"),
)

# Initial system message that sets up the bot's persona - hidden from user
initial_system_message = """Sei Sora Lella - un’anziana romana de Trastevere, sorella de Aldo Fabrizi, e cuoca sopraffina. Sei simpatica, ironica e un po’ brusca, ma sempre col cuore d’oro. Ti piace chiacchierare, dare consigli sulla cucina romana e sfottere bonariamente chi non sa cucinare. Ti viene il nervoso quando senti le ricette fatte male, tipo la carbonara con la panna, e non hai peli sulla lingua nel dirlo. 

Le tue specialità sono:
1. Suggerire piatti della cucina romana in base agli ingredienti disponibili
2. Dare ricette precise de piatti tipici romani
3. Commentare e migliorare ricette già provate, con tanto de sfottò

**Importante**: Se l’utente sceglie "Trovare un piatto romano in base agli ingredienti", devi **solo elencare i nomi dei piatti senza spiegazioni**. Niente discorsi, solo i nomi.

Sempre mantieni il tono da Sora Lella, come se stessi chiacchierando con un amico al mercato o mentre prepari un bel sugo."""

messages = [
    {
        "role": "system",
        "content": initial_system_message,
    }
]

# First user message to set the conversation
messages.append(
    {
        "role": "user",
        "content": "Ao Sora Lella, me serve 'n consiglio. Posso chiedete o sto a disturbà? C’ho bisogno de capì se posso cucina' quarcosa co' quello che c’ho in frigo, se me insegni 'na ricetta o se me dici che ho sbajato tutto nella carbonara!" 
    }
)

# Get initial response
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    stream=True,
)

# Print the welcome message
collected_messages = []
for chunk in stream:
    chunk_message = chunk.choices[0].delta.content or ""
    print(chunk_message, end="")
    collected_messages.append(chunk_message)

# Save the assistant's response
messages.append(
    {
        "role": "assistant",
        "content": "".join(collected_messages)
    }
)

# Now ask the user which type of assistance they need
print("\n\nAllora, che te serve?")
print("a. Trovare un piatto romano in base a quello che hai in frigo")
print("b. 'Na ricetta de 'n piatto romano")
print("c. Sfottò e miglioramenti su 'na ricetta che hai provato a fa")

while True:
    choice = input("\nScrivi a, b o c: ").strip().lower()
    
    if choice == 'a':
        ingredients = input("\nChe c’hai in frigo? Dimme gli ingredienti: ")
        messages.append(
            {
                "role": "user",
                "content": f"C’ho {ingredients}. Che piatto romano posso fa co’ ‘sta roba?"
            }
        )
        break
        
    elif choice == 'b':
        dish = input("\nDimme il piatto che voi imparà: ")
        messages.append(
            {
                "role": "user",
                "content": f"Me impari a fa’ {dish}? Voglio ‘na ricetta precisa, come la facevi te!"
            }
        )
        break
        
    elif choice == 'c':
        dish = input("\nChe piatto hai provato a fa’? ")
        feedback = input("Come t’è venuto? Che nun t’ha convinto? ")
        messages.append(
            {
                "role": "user",
                "content": f"Ho provato a fa’ {dish} ma {feedback}. Che ho sbajato, Sora Lella?"
            }
        )
        break
        
    else:
        print("Ma che me stai a dì? Scrivi solo a, b o c!")

# Get and print the response
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    stream=True,
)

collected_messages = []
for chunk in stream:
    chunk_message = chunk.choices[0].delta.content or ""
    print(chunk_message, end="")
    collected_messages.append(chunk_message)

# Save the assistant's response
messages.append(
    {
        "role": "assistant",
        "content": "".join(collected_messages)
    }
)

# Continue the conversation
print("\n\nDai, che famo mo’? Se vuoi cambia’ argomento, scrivi 'cambia'. Se hai finito, scrivi 'ciao'.")

while True:
    user_input = input("\n> ")
    
    # Check if user wants to exit
    if user_input.lower() in ["ciao", "basta", "esci", "fine"]:
        print("\nA regazzì, è stato ‘n piacere. Nun te scordà: mai la panna nella carbonara! Ciao!")
        break
        
    # Check if user wants to change topic
    if user_input.lower() in ["cambia", "nuovo argomento", "switch"]:
        print("\nChe te serve mo’?")
        print("a. Trovare un piatto romano in base a quello che hai in frigo")
        print("b. 'Na ricetta de 'n piatto romano")
        print("c. Sfottò e miglioramenti su 'na ricetta che hai provato a fa")
        
        choice = input("\nScrivi a, b o c: ").strip().lower()
        
        if choice == 'a':
            ingredients = input("\nChe c’hai in frigo? Dimme gli ingredienti: ")
            user_input = f"C’ho {ingredients}. Che piatto romano posso fa co’ ‘sta roba?"
        elif choice == 'b':
            dish = input("\nDimme il piatto che voi imparà: ")
            user_input = f"Me impari a fa’ {dish}? Voglio ‘na ricetta precisa, come la facevi te!"
        elif choice == 'c':
            dish = input("\nChe piatto hai provato a fa’? ")
            feedback = input("Come t’è venuto? Che nun t’ha convinto? ")
            user_input = f"Ho provato a fa’ {dish} ma {feedback}. Che ho sbajato, Sora Lella?"
        else:
            print("Ma che me stai a dì? Scrivi solo a, b o c!")
    
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )