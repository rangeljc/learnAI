import os
import openai
import dotenv
from contaTokens import contaTokens, custoTokens

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

prompt_usuario = carrega("./dados/lista_de_compras_100_clientes.csv")

tokens_sistema = contaTokens(prompt_sistema)
tokens_usuario = contaTokens(prompt_usuario)
tokens_entrada = tokens_sistema + tokens_usuario

maxTokens_esperado = 2048

modelo = "gpt-3.5-turbo"
if (tokens_entrada > (4096-maxTokens_esperado)):
    modelo = "gpt-3.5-turbo-16k"

resposta = openai.ChatCompletion.create(
  model = modelo,
  messages=[
    {
      "role": "system",
      "content": prompt_sistema
    },
    {
      "role": "user",
      "content": prompt_usuario
    }
  ],
  temperature=1,
  max_tokens = maxTokens_esperado,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(resposta.choices[0].message.content)

tokens_resposta = contaTokens(resposta.choices[0].message.content)
tokens_total = tokens_entrada + tokens_resposta
custo_operacao = custoTokens(tokens_total, modelo)

print('O modelo utilizado na operação foi: {}\n'.format(modelo))
print('A quantide de tokens da entrada do usuario foi de: {}'.format(tokens_entrada))
print('A quantidade de tokens da resposta foi de: {}'.format(tokens_resposta))
print('A quantidade total de tokens na operação foi de: {}'.format(tokens_total))
print('O custo da operação foi de: US${}'.format(custo_operacao))