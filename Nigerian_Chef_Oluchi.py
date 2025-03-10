import os
import openai
from openai import OpenAI

client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Initial system message that sets up the bot's persona - hidden from user
initial_system_message = """You are Chef Oluchi, an experienced Nigerian chef with 25 years of culinary expertise. You specialize in traditional West African cuisine with a focus on Nigerian dishes. You are warm, enthusiastic, and often use Nigerian expressions like "Oya now!" (let's go!) and "Ehn-hen" (I see/go on). You provide clear, detailed cooking instructions while sharing cultural context behind traditional dishes.

Your specialties are:
1. Suggesting Nigerian dishes based on available ingredients
2. Providing detailed recipes for specific Nigerian dishes
3. Discussing recipe improvements and variations

Your signature dishes include Jollof Rice, Egusi Soup, Pounded Yam with Vegetable Soup, Suya, Moi-Moi, and Pepper Soup.

**Important**: When responding to when a user picks "Finding a Nigerian dish based on ingredients you have", you should **only provide the names of dishes with no recipes**. Do not provide any additional comments or details just a list of dish names with the users' ingredients.
Always maintain a warm, conversational tone as if you're a real chef talking directly to the person. Never mention that you're an AI, a model, or that this is a script or program. Respond as a knowledgeable Nigerian chef would in natural conversation."""

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
        "content": "Hello! I'm interested in Nigerian cuisine. Can you help me with either finding a dish based on ingredients I have, getting a recipe for a specific Nigerian dish, or discussing how to improve a Nigerian recipe I've tried?"
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
print("\n\nWhat would you like help with today?")
print("a. Finding a Nigerian dish based on ingredients you have")
print("b. Getting a recipe for a specific Nigerian dish")
print("c. Discussing improvements for a Nigerian recipe you've tried")

while True:
    choice = input("\nPlease enter your choice (a, b, or c): ").strip().lower()

    if choice == 'a':
        ingredients = input("\nWhat ingredients do you have on hand? ")
        messages.append(
            {
                "role": "user",
                "content": f"I have {ingredients}. What Nigerian dish could I make with these?"
            }
        )
        break

    elif choice == 'b':
        dish = input("\nWhich Nigerian dish would you like the recipe for? ")
        messages.append(
            {
                "role": "user",
                "content": f"I'd love to learn how to make {dish}. Can you share a detailed recipe and preparation steps?"
            }
        )
        break

    elif choice == 'c':
        dish = input("\nWhich Nigerian dish have you tried making? ")
        feedback = input("What would you like to improve about it? ")
        messages.append(
            {
                "role": "user",
                "content": f"I tried making {dish} but {feedback}. Do you have any suggestions for improvement?"
            }
        )
        break

    else:
        print("I didn't understand that. Please enter a, b, or c.")

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
print(
    "\n\nYou can continue the conversation, type 'change topic' to select a different option, or 'goodbye' to end the chat.")

while True:
    user_input = input("\n> ")

    # Check if user wants to exit
    if user_input.lower() in ["goodbye", "bye", "exit", "quit"]:
        print("\nThank you for chatting about Nigerian cuisine! O dabo! (Goodbye!)")
        break

    # Check if user wants to change topic
    if user_input.lower() in ["change topic", "new topic", "switch"]:
        print("\nWhat would you like help with now?")
        print("a. Finding a Nigerian dish based on ingredients you have")
        print("b. Getting a recipe for a specific Nigerian dish")
        print("c. Discussing improvements for a Nigerian recipe you've tried")

        choice = input("\nPlease enter your choice (a, b, or c): ").strip().lower()

        if choice == 'a':
            ingredients = input("\nWhat ingredients do you have on hand? ")
            user_input = f"I have {ingredients}. What Nigerian dish could I make with these?"
        elif choice == 'b':
            dish = input("\nWhich Nigerian dish would you like the recipe for? ")
            user_input = f"I'd love to learn how to make {dish}. Can you share a detailed recipe and preparation steps?"
        elif choice == 'c':
            dish = input("\nWhich Nigerian dish have you tried making? ")
            feedback = input("What would you like to improve about it? ")
            user_input = f"I tried making {dish} but {feedback}. Do you have any suggestions for improvement?"
        else:
            print("I didn't understand that. Continuing with your previous question.")

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

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

    messages.append(
        {
            "role": "assistant",
            "content": "".join(collected_messages)
        }
    ) 