import tiktoken

def contaTokens(exp):
    codificador = tiktoken.encoding_for_model('gpt-3.5-turbo-16k')

    lista_tokens = codificador.encode(exp)
    qtde_tokens = len(lista_tokens)
    #print(lista_tokens)
    #print('A expressão possui {} tokens!'.format(qtde_tokens))

    return qtde_tokens
    

def custoTokens(nTokens, modelo):
    # o custo dos tokens pode ser verificado na documentação do modelo, no site da openAI
    
    if (modelo == "gpt-3.5-turbo"):
        custo_entrada = nTokens*(0.0015/1000)
    else:
        custo_entrada = nTokens*(0.003/1000)

    #print('O custo da entrada é: US${}'.format(round(custo_entrada, 5)))

    return custo_entrada

if (__name__ == '__main__'):
    expressao = input('Digite a expressao que será analisada:\n')
    qtde_tokens = contaTokens(expressao)
    custo = custoTokens(qtde_tokens)

    print('A expressão possui {} tokens!'.format(qtde_tokens))
    print('O custo da entrada é: US${}'.format(round(custo, 5)))