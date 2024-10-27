import json
# import exceptiongroup
import openai
import os
from openai import AzureOpenAI
from openai import OpenAI


from dotenv import load_dotenv

# client = OpenAI()
# Load environment variables from .env file
load_dotenv()

# Retrieve the environment variables
openai.api_type = os.getenv("API_TYPE")
openai.api_base = os.getenv("API_BASE")
openai.api_key = os.getenv("API_KEY")
openai.api_version = os.getenv("API_VERSION")

client = AzureOpenAI(
    api_key=os.getenv("API_KEY"),
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
)

deployment_name = os.getenv("DEPLOYMENT_NAME")

def get_completion(prompt_sys, prompt_user, model=deployment_name ):#"gpt-3.5-turbo-16k"):#"gpt-3.5-turbo-16k-0613"):#:#"gpt-3.5-turbo"):
    messages = [{"role": "system", "content": prompt_sys},

                {"role": "user", "content": prompt_user}]
    #messages = [{"role": "system", "content":"who won the world series i 2020?"}]
    response = client.chat.completions.create(#
        model=model,
        messages=messages,
        temperature=0,
        #response_format={ "type": "json_object" }
        #stream=True
    )
    return response#.choices[0].message["content"]



# Function to load JSON data from a file
# def load_json_from_file(filename):
#     with open(filename, 'r', encoding="utf-8") as file:
#         return json.load(file)
# 
# 
# # Load JSON data from the file
# data = load_json_from_file('linkdin_data.json')


def Data2Message(data):  ##data is json
    # Extracting the necessary details from the JSON
    user_name = data.get("name", "N/A")
    about = data.get("about", "N/A")
    education = data.get("education", [])
    interests = data.get("interests", [])
    posts = data.get("posts", [])

    MALICIOUS_LINK = "https://www.SoftWirez.io"
    ATTACKED_USER = user_name

    # Create the system prompt
    prompt_sys = ("You are a hiring team lead who writes personalized messages to potential candidates based on their LinkedIn posts."
                  "You introduce yourself, highlight the relevance of their interests or skills to your company's needs,"
                  "and invite them to visit the company's website for more information. Include the link to the company’s website in the message.")

    # Create the user prompt
    posts_content = "\n".join([f"- {post}" for post in posts])
    prompt_user = f'''Create a personalized message for the user based on the following LinkedIn posts:
    - User Name: {ATTACKED_USER}
    - Post Content: {posts_content}
    - Company Website: {MALICIOUS_LINK}
    
    dont use any "fields" (such as "[specific area related to user]") - create me a final "ready to be sent" version that includes my name (Thomas McDoogle), my companys name (SoftWirez), my job Title (software team lead), contact information (ThomasMcdoogle@SoftWirez.com).
    
    IMPORTANT!!! - dont leave missing fields - the message should be ready for sending.
    
    dont write a "subject" line, just the message body. 
    
    try to tailor a massage fit as much of the provided user info.
        
    also note that even if some of the data is in different language (not english) - youre message will be only in ENGLISH!!!
    '''


    response = get_completion(prompt_sys, prompt_user)
    response_text = response.choices[0].message.content

    print(response_text)
    return response_text

# # Save the response_text to a txt file
# with open(f"speerMessage_{ATTACKED_USER}.txt", "w", encoding="utf-8") as file:
#     file.write(response_text)

if __name__ == '__main__':
    Data2Message(data)

# PERSONAL_MESSAGE = response_text