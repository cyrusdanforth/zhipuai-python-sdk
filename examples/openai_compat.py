import os
from openai import OpenAI
client=OpenAI(api_key=os.environ['OPENAI_API_KEY'],base_url=os.getenv('OPENAI_BASE_URL','https://argolink.io/v1'))
print(client.chat.completions.create(model=os.getenv('MODEL_ID','glm-5.3'),messages=[{'role':'user','content':'Say one sentence.'}]).choices[0].message.content)
