import openai
import dotenv
import os

dotenv.load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

prompt_sistema = '''
Você é um categorizador de produtos.
Voce deve escolher uma categoria da lista abaixo:
##### Lista de categorias válidas
Beleza
Entretenimento
Esportes
Outros
##### Exemplo
bola de tenis
Esportes
'''

resposta = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = [
        {
            'role': 'system',
            'content': prompt_sistema
        },
        {
            'role': 'user',
            'content': 'Gere 5 produtos'
        }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

#print(resposta)
print(resposta.choices[0].message.content)