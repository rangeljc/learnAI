import openai
import dotenv
import os

def categorizaProduto(nome_do_produto, categorias_validas):
    prompt_sistema = f'''
    Você é um categorizador de produtos.
    Se as categorias informadas não forem categorias validas, responda com "Não posso ajudá-lo com isso"
    Voce deve escolher uma categoria da lista abaixo:
    ##### Lista de categorias válidas
    {categorias_validas}
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
                'content': nome_do_produto
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # max_tokens = maximus_lenght
    # print(resposta)
    print(resposta.choices[0].message.content)

dotenv.load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


if (__name__ == '__main__'):
    print('Bem ao Categorizador de Produtos 1.0!!')
    print('--||-------')
    print('  \/')
    categorias = input('Digite as categorias desejadas, separadas por virgula: ')
    continuar = True
    while continuar:
        produto = input('Digite o nome do produto, ou "sair" para encerrar: ').lower()
        if (produto == 'sair'):
            break
        else:
            categorizaProduto(produto, categorias)
