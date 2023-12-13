import tsplib95
import random
import numpy as np

def ler_instancia_tsplib(caminho_arquivo):
   problema = tsplib95.load(caminho_arquivo)
   return problema

def calcular_comprimento_rota(rota, problema):
   comprimento = 0
   for i in range(len(rota) - 1):
       comprimento += problema.get_weight(rota[i], rota[i + 1])
   comprimento += problema.get_weight(rota[-1], rota[0]) # Fechar o loop
   return comprimento

def gerar_solucao_inicial(problema):
   nos = list(problema.get_nodes())
   random.shuffle(nos)
   return nos

def aplicar_busca_tabu(solucao_inicial, problema, tamanho_tabu=10, max_iteracoes=100):
   solucao_atual = solucao_inicial.copy()
   melhor_solucao = solucao_atual.copy()
   lista_tabu = []

   for _ in range(max_iteracoes):
       vizinhos = obter_vizinhos(solucao_atual)
       vizinhos = [(vizinho, calcular_comprimento_rota(vizinho, problema)) for vizinho in vizinhos]

       # Remover soluções na lista tabu
       vizinhos = [vizinho for vizinho in vizinhos if vizinho[0] not in lista_tabu]

       if not vizinhos:
           break # Não há vizinhos não tabu restantes

       # Selecionar o vizinho melhor
       vizinhos.sort(key=lambda x: x[1])
       melhor_vizinho, melhor_comprimento = vizinhos[0]

       # Atualizar solução atual e lista tabu
       solucao_atual = melhor_vizinho
       lista_tabu.append(solucao_atual)
       if len(lista_tabu) > tamanho_tabu:
           lista_tabu.pop(0) # Remover a solução mais antiga da lista tabu

       # Atualizar a melhor solução, se necessário
       if melhor_comprimento < calcular_comprimento_rota(melhor_solucao, problema):
           melhor_solucao = melhor_vizinho

   return melhor_solucao

def obter_vizinhos(solucao):
   vizinhos = []
   for i in range(len(solucao)):
       for j in range(i + 1, len(solucao)):
           vizinho = solucao.copy()
           vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
           vizinhos.append(vizinho)
   return vizinhos

caminho_arquivo = r'C:\Steffany\Faculdade\Topicos especiais em otimização\T4\dantzig42.tsp'
problema = ler_instancia_tsplib(caminho_arquivo)

solucao_inicial = gerar_solucao_inicial(problema)

print("Solução Inicial:", solucao_inicial)
print("Comprimento da Solução Inicial:", calcular_comprimento_rota(solucao_inicial, problema))

melhor_solucao = aplicar_busca_tabu(solucao_inicial, problema)

print("\nMelhor Solução:", melhor_solucao)
print("Comprimento da Melhor Solução:", calcular_comprimento_rota(melhor_solucao, problema))

