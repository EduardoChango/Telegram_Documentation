from openai import OpenAI
import os



class GPT():

    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    



    def interaction(self,discusion_text: str) -> str:

        print('discuss_intiated')
        instruction = '''Tu trabajo es responder a la siguiente pregunta o comentario: {}'''.format(discusion_text.replace("\t"," "))
        

        prompt = instruction
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content.strip()
    