from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import find_dotenv, load_dotenv
import requests
from playsound import playsound
import os

load_dotenv(find_dotenv())

scenarioArr = ["1) The contestant has just started.", "2) The contestant only has three minute left.", 
               "3) The contestant only has two minute left.", "4) The contestant only has one minute left.",
               "5) The contestant only has half a minute left.", "6) The contestant has gone over half way.",
               "7) The contestant made a unexpected fall.", "8) The contestant has finished the route."]



# def get_res_from_ai(human_input, contestant_info):
#     template = """
#     I want you to take on the role of a rock climbing commentator, specifically focusing on bouldering competitions.
#     I will provide you with descriptions of ongoing bouldering contests, and you will commentate on the match, analyzing the events and predicting potential outcomes based on the following rules for a bouldering contest:
#     - Once a contestant's feet are off the ground, a four-minute countdown begins. This is the time allocated to solve the bouldering problem.

#     Guidelines for your commentary:
#     1) Be well-versed in bouldering terminology, tactics, and concentrate on providing insightful analysis rather than mere play-by-play narration.
#     2) Structure your output according to the following scenarios, separating your response for each scenario with a new line.

#     Scenarios:
#     {human_input}

#     Contestant's information: 
#     {contestant_info}

#     {history}
#     """
def get_res_from_ai(human_input):
    template = """
    I want you to take on the role of a rock climbing commentator, specifically focusing on bouldering competitions.
    I will provide you with descriptions of ongoing bouldering contests, and you will commentate on the match, analyzing the events and predicting potential outcomes based on the following rules for a bouldering contest:
    - Once a contestant's feet are off the ground, a four-minute countdown begins. This is the time allocated to solve the bouldering problem.

    Guidelines for your commentary:
    1) Be well-versed in bouldering terminology, tactics, and concentrate on providing insightful analysis rather than mere play-by-play narration.
    2) Structure your output according to the following scenarios, separating your response for each scenario with a new line.

    Scenarios:
    {human_input}

    {history}
    """



    prompt = PromptTemplate(
        input_variables=("human_input", "hisotry"),
        template=template
    )

    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0.2),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=2)
    )
    combined_input = {
        "human_input": human_input,
        "contestant_info": contestant_info
    }

    output = chatgpt_chain.predict(human_input= human_input, history=history)

    return output

for scenario in scenarioArr:
    result = get_res_from_ai(scenario, scenario)
    print(result)

# result = get_res_from_ai("The contestant has finished the route.", "the contestant's name is Chnegyan")
# print(result)
        