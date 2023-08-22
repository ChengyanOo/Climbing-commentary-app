from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import find_dotenv, load_dotenv
import requests
from playsound import playsound
import os
import time

load_dotenv(find_dotenv())


def get_res_from_ai(human_input):
    template = """
    I want you to take on the role of a rock climbing commentator, specifically focusing on bouldering competitions.
    I will provide you with descriptions of ongoing bouldering contests, and you will commentate on the match, analyzing the events and predicting potential outcomes based on the following rules for a bouldering contest:
    - Once a contestant's feet are off the ground, a four-minute countdown begins. This is the time allocated to solve the bouldering problem.

    Guidelines for your commentary:
    1) Be well-versed in bouldering terminology, tactics, and concentrate on providing insightful analysis rather than mere play-by-play narration.
    2) Structure your output according to the following scenarios, separating your response for each scenario with a new line.
    3) Don't be boring, make some jokes if appropriate.
    4) Mention the contestant's personal information if appropriate, but dont mention it everytime! Make the commentary more vivid and realistic.

    Scenarios:
    {human_input}

    {history}
    """

    prompt = PromptTemplate(
        input_variables=("human_input", "history"),
        template=template
    )

    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0.2),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=2)
    )

    output = chatgpt_chain.predict(human_input=human_input)

    return output


file_path = '/Users/tonsonwang/Desktop/Climbing-commentary-app/Commentary/express_server/userInfo.txt'

with open(file_path, 'r') as file:
    myString = file.read().strip()


scenarioArr = [
    "The contestant has just started.",
    "The contestant only has three minute left.",
    "The contestant only has two minute left.",
    "The contestant only has one minute left.",
    "The contestant only has half a minute left.",
    "The contestant has gone over half way.",
    "The contestant made an unexpected fall.",
    "The contestant has finished the route."
]

output_file_path = 'scenariosResponse.txt'

# Open the output file for writing
with open(output_file_path, 'w') as out_file:
    for scenario in scenarioArr:
        human_input = scenario
        result = get_res_from_ai(
            human_input + "Contestant's info: " + myString)
        out_file.write(result + '\n')

print(f'Results written to {output_file_path}')



CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/TX3LPaxmHKxFdv7VOQHJ"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "eeced99bf38abc46b65ceef79ccfb274"
}

data = {
    "text": "",
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.3,
        "similarity_boost": 0.8
    }
}

# response = requests.post(url, json=data, headers=headers)
# with open('output.mp3', 'wb') as f:
#     for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
#         if chunk:
#             f.write(chunk)

time.sleep(3)

if not os.path.exists('audios'):
    os.mkdir('audios')

text_file_path = 'scenariosResponse.txt'

with open(text_file_path, 'r') as file:
    lines = file.readlines()

for index, line in enumerate(lines):
    line = line.strip() 
    data["text"] = line 

    response = requests.post(url, json=data, headers=headers)
    
    audio_file_path = f'audios/audio_{index}.mp3'
    with open(audio_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    
    print(f"Audio for line {index} saved to {audio_file_path}")