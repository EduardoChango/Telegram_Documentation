from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv('../.env')



class GPT():

    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    



    def interaction(self,discusion_text: str) -> str:

        print('discuss_intiated')
        instruction = '''Tu trabajo es responder a la siguiente pregunta o comentario: {}'''.format(discusion_text.replace("\t"," "))
        

        prompt = instruction
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content.strip()
    