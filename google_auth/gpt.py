import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()
# api_key=os.environ["api_key"]

def gpt_response():    
    fr = "Aditya"
    to = "Roshni"
    body = "create a heartfelt message for my beautiful wife %s from %s. i want to send this message to her mail on everyday because my everyday is made special by %s. create a body response as a row string with fix format."%(to,fr,to)

    # body = "create various of prompt strings seperated by newline include 30 lines or prompts . the prompt is configured as Email body, the Email is sent by Aditya to Roshni to express his love to his wife and how she takes an important place in his life ."
    genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("gemini-1.5-flash")
    body_response = model.generate_content(body).text
    print(body_response)
    return body_response


# print(gpt_response())



# subject_pattern = r"Subject: (.+)"
# body_pattern = r"Subject: .+\n\n(.+)"
# subject_match = re.search(subject_pattern, body_response)
# subject = subject_match.group() if subject_match else None
# print(subject)
# body_match = re.findall(body_pattern, body_response, re.DOTALL)
# body_text = '\n'.join(body_match)
# print(body_text)
# subject = model.generate_content("generate a mail subject after analysing the %s that is a mail body. the mail subject is one line long. "%(body_response))

# print(subject+"\n\n"+body_text) 





