import time
import json
import requests
import http.client
import chainlit as cl


def get_public_ip_of_this_server():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        data = response.json()
        public_ip = data["ip"]
        return public_ip
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


backend_URL = "http://" + get_public_ip_of_this_server() + ":8000"



# when the user starts a chat, this will be called
@cl.on_chat_start
async def start():
    # Your logic will be here
    content = "Welcome to the meta-llama/Llama-2-7b-chat-hf chatbot!"
    await cl.Message(content=content).send()


# continously on a loop
# the @on_message decorator to tell Chainlit to run the main function each time a user sends a message. Then, we send back the answer to the UI with the Message class.
@cl.on_message
async def main(message: str):
    # Invode the generateText API from the FastAPI server
    prompt = {
        "prompt": message,
    }
    # Get the task_id from the API
    task_id = requests.post(
        url=f"{backend_URL}/generateText", data=json.dumps(prompt)
    ).json()["task_id"]

    while True:
        response = requests.get(url=f"{backend_URL}/task/{task_id}").json()
        if "status" in response.keys() and "Task Pending" in response["status"]:
            time.sleep(2)
        else:
            break

    # send a response back to the user all the time
    await cl.Message(
        content=f"The answer from meta-llama/Llama-2-7b-chat-hf: \n"
        + "\n\n".join([f"{key}: {value}" for key, value in response.items()])
    ).send()
