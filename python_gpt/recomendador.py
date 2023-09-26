import os
import openai
import dotenv
import json

'''
DESAFIO: Gerar e-mails com recomendações de produtos

1. Identificar perfis a partir de uma lista de compras recentes por clientes
2. Recomendar 3 produtos para cada perfil, a partir de uma lista de produtos
3. Escrever um e-mail de recomendação dos produtos escolhidos com até 3 paragrafos
'''

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")


def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")


def identifica_perfis(lista_de_compras_por_cliente):
    print("Iniciando identificação de perfis!")

    prompt_sistema = """
        Identifique o perfil de compra para cada cliente a seguir.

        O formato de saída deve ser em JSON:

        {
        "clientes" : [
            {
                "nome": "nome do cliente"
                "perfil": "descreva o perfil do cliente em 3 palavras"
            }
        ]
        }
    """

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": lista_de_compras_por_cliente
        }
        ]
    )

    conteudo = resposta.choices[0].message.content
    json_resultado = json.loads(conteudo)
    print("Finalisando identificação de perfis!")
    return json_resultado
    
def recomenda_produtos(perfil, produtos):
    print("Iniciando a recomendação de produtos!")
    prompt_sistema = f"""
        Voce é um recomendador de produtos.
        Considere o seguinte perfil: {perfil}
        Recomende 3 produtos a partir da lista de produtos validos e que sejam adequados ao perfil informado

        #### Lista de produtos validos para recomendação
        {produtos}

        A saída deve ser apenas o nome dos produtos recomendados, em bullet points.
    """

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {
            "role": "system",
            "content": prompt_sistema
        }
        ]
    )

    conteudo = resposta.choices[0].message.content
    print("Finalizando a recomendação de produtos!")
    return conteudo

def escreve_email(recomendacao):
    print("Escrevendo email de recomendação!")

    prompt_sistema = f"""
        Escreva um e-mail, recomendando os seguintes produtos:

        {recomendacao}
        
        O e-mail deve ter no maximo 3 parágrafos.
        O tom deve ser amigável, informal e descontraído.
        trate o cliente como alguém próximo e conhecido
    """

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {
            "role": "system",
            "content": prompt_sistema
        }
        ]
    )

    conteudo = resposta.choices[0].message.content
    print("E-mail encerrado!")

    return conteudo


dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

lista_produtos = carrega("dados/lista_de_produtos.txt")

lista_de_compras_por_cliente = carrega("./dados/lista_de_compras_10_clientes.csv")
perfis = identifica_perfis(lista_de_compras_por_cliente)

for cliente in perfis["clientes"]:
    nome_do_cliente = cliente["nome"]
    print(f"Identificando recomendação para o cliente: {nome_do_cliente}")
    recomendacoes = recomenda_produtos(cliente["perfil"], lista_produtos)
    #print(recomendacoes)
    email = escreve_email(recomendacoes)
    salva(f"email-{nome_do_cliente}.txt", email)
