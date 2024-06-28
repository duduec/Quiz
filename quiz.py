import time
import re
import json
import random

# Função para carregar perguntas de um arquivo JSON
def carregar_perguntas(caminho):
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

# Lista de perguntas carregada do arquivo JSON
perguntas = carregar_perguntas('perguntas.json')

# Função para exibir a contagem regressiva
def contagem_regressiva(segundos):
    for i in range(segundos, 0, -1):
        print(f"Próxima pergunta em {i} segundos...")
        time.sleep(1)
    print("Próxima pergunta!\n")

# Função para exibir uma pergunta
def exibir_pergunta(pergunta):
    print("-" * 128)
    print()
    print(pergunta["Pergunta"])
    print()
    print("-" * 128)
    print("Opções")
    print()
    for i, opcao in enumerate(pergunta["Opções"]):
        print(f"{i + 1}. {opcao}")
    print()

# Função para obter a resposta do jogador
def obter_resposta():
    while True:
        try:
            resposta = int(input("Escolha uma das opções acima: "))
            if resposta < 1 or resposta > 4:
                print("Por favor, escolha uma opção válida!")
            else:
                return resposta - 1
        except ValueError:
            print("Por favor, insira um número válido.")

# Função para verificar se a resposta está correta e atualizar a pontuação
def verificar_resposta(pergunta, resposta, pontuacao):
    print("E a resposta está...")
    time.sleep(2)
    if resposta == pergunta["Resposta"]:
        print("Resposta Correta! :) \n")
        return True, pontuacao + 1
    else:
        resposta_correta = pergunta["Opções"][pergunta["Resposta"]]
        print("Resposta Incorreta! :( \n")
        print(f"A resposta correta é: {resposta_correta}\n")
        return False, pontuacao

# Função para verificar se o nome inserido é válido e único
def verificar_nome(nome):
    if not re.match("^[a-zA-Z]{2,2}$", nome):
        return "invalid_length"
    
    try:
        with open("pontuacoes.txt", "r") as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                nome_existente, _ = linha.strip().split(": ")
                if nome_existente == nome:
                    return "name_in_use"
    except FileNotFoundError:
        pass
    
    return "valid"

# Função da tela inicial
def tela_inicial():
    print()
    print("Olá, Seja muito bem-vindo ao Quiz!")
    time.sleep(1)
    
    while True:
        nome = None  
        while not nome: 
            nome = input("Digite seu apelido (dois dígitos): ").strip().upper()
            verifica_nome = verificar_nome(nome)
            if verifica_nome == "invalid_length":
                print("Digite um apelido que tenha apenas 2 dígitos.")
                nome = None 
            elif verifica_nome == "name_in_use":
                print("Este nome já está em uso. Escolha outro.")
                nome = None 
            else:
                break

        time.sleep(1)
        print(f"\nOlá, {nome}! O que gostaria de fazer?")
        time.sleep(1)

        while True:
            print("\n1. Jogar\n2. Regras\n3. Ranking\n4. Sair\n")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                time.sleep(1)
                return nome, True
            elif escolha == '2':
                print("\nO Quiz é formado por 10 perguntas.")
                print("As perguntas são carregadas de um arquivo, ou seja, sempre serão perguntas aleatórias.")
                print("Cada resposta correta equivale a 1 ponto.")
                print("No final, você verá sua pontuação.")
                print("Boa sorte!\n")
                time.sleep(1)
                input("Pressione Enter para voltar ao menu inicial...")
            elif escolha == '3':
                try:
                    with open("pontuacoes.txt", "r") as arquivo:
                        linhas = arquivo.readlines()
                        if not linhas:
                            print("\nNenhum jogador no ranking ainda.\n")
                        else:
                            print("\nRanking:\n")
                            for linha in linhas:
                                nome, pontuacao = linha.strip().split(": ")
                                print(f"{nome}: {pontuacao}\n")
                except FileNotFoundError:
                    print("\nNenhum jogador no ranking ainda.\n")
                input("Pressione Enter para voltar ao menu inicial...")
            elif escolha == '4':
                return nome, False
            else:
                print("Opção inválida! Por favor, escolha uma opção válida.")

# Função para salvar a pontuação do jogador
def salvar_pontuacao(nome, pontuacao):
    with open("pontuacoes.txt", "a") as arquivo:
        arquivo.write(f"{nome}: {pontuacao}\n")

# Função para jogar o quiz
def jogar_quiz(perguntas):
    while True:
        nome, jogar = tela_inicial()
        if not jogar:
            print("\nFicou com medo? Tudo bem, até logo!")
            break

        pontuacao = 0
        perguntas_sorteadas = random.sample(perguntas, 10)
        total_perguntas = len(perguntas_sorteadas)
        
        for idx, pergunta in enumerate(perguntas_sorteadas):
            exibir_pergunta(pergunta)
            print(f"Perguntas restantes: {total_perguntas - idx - 1}")
            resposta = obter_resposta()
            if resposta is not False:
                correta, pontuacao = verificar_resposta(pergunta, resposta, pontuacao)
                if correta and idx < len(perguntas_sorteadas) - 1:
                    contagem_regressiva(3)
                    print()
                elif not correta:
                    contagem_regressiva(3)
                    print()
                if idx == len(perguntas_sorteadas) - 1:
                    time.sleep(3) 

        print("=" * 28)
        print(f"Fim do Jogo, {nome}!")
        print(f"Você acertou: {pontuacao}/{total_perguntas}")

        if pontuacao == 10:
            print("Parabéns, você sabe muito!")
        elif 7 <= pontuacao <= 9:
            print("Foi quase!")
        elif 5 <= pontuacao <= 6:
            print("Bom trabalho!")
        elif 3 <= pontuacao <= 4:
            print("Você pode melhorar!")
        elif 1 <= pontuacao <= 2:
            print("Que isso, amigão, só isso?")
        elif pontuacao == 0:
            print("Que burro! Dá zero pra ele!")

        salvar_pontuacao(nome, pontuacao)
        print("=" * 28)

        break

jogar_quiz(perguntas)