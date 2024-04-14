import re
import numpy as np

base_canonica1 = [
        #  X1   X2   X3   X4   X5   X6   XA   B  #
        [ 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 6.0 ],
        [ 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 5.0 ],
        [ 2.0, 3.0, 0.0, 0.0, 1.0, 0.0, 0.0, 12.0],
        [ 1.0,-1.0, 0.0, 0.0, 0.0,-1.0, 1.0, 1.0 ],
        [-1.0,-2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
        [-1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0,-1.0 ],
]


base_canonica2 = [
        [ 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0 ],
        [ 1.0, 2.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 16.0],
        [ 2.0, 3.0, 0.0, 0.0,-1.0, 0.0, 0.0, 1.0, 15.0],
        [ 1.0,-1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 2.0 ],
        [-1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 2.0 ],
        [ 1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
        [-2.0,-3.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0,-15.0],
]


def PivoZ(base):
  linha_z = base[len(base)-1]
  indice_coluna = 0
  indice_linha = 0

  for indice in range(len(linha_z)-1):
    valor_linha = 0
    if linha_z[indice] < valor_linha:
      valor_linha = linha_z[indice]
      indice_coluna = indice
  
  coluna_pivo = []
  for linha in base:
    coluna_pivo.append(linha[indice_coluna])

  coluna_b = []
  for linha in base:
    coluna_b.append(linha[len(base)+1])

  valor_da_divisao = 500

  for i in range(len(coluna_pivo)):
    if coluna_b[i] >= 0 and coluna_pivo[i] > 0:
      if coluna_b[i]/coluna_pivo[i] < valor_da_divisao:
        valor_da_divisao = coluna_b[i]/coluna_pivo[i]
        indice_linha = i

  cordenadas_pivo = [indice_linha, indice_coluna]
  return cordenadas_pivo
  


def Eliminacao_Z(base):
    coordenadas_pivo = PivoZ(base)
    pivo = base[coordenadas_pivo[0]][coordenadas_pivo[1]]
    linha_pivo = base[coordenadas_pivo[0]]
    ultima_linha = base[len(base)-1]

    if pivo != 1: 
      for i in range(len(linha_pivo)):
        linha_pivo[i] = linha_pivo[i]/pivo
    
    for linha in base:
      linha_pivo_base = linha[coordenadas_pivo[1]]
     
      if linha_pivo_base < 0 and linha != linha_pivo:
        for i in range(len(linha)):
          linha[i] = abs(linha_pivo_base)*linha_pivo[i] + linha[i] 
 
      elif linha_pivo_base > 0 and linha != linha_pivo:
          for i in range(len(linha)):
            linha[i] = -linha_pivo_base*linha_pivo[i] + linha[i]
    

    for i in range(len(ultima_linha)-1):
      if ultima_linha[i] < 0:
        Eliminacao_Z(base)
      else:
        print("ELIMINACAO 'W' CONCLUIDA!")
        Apresentar_Tabela(base)


    
def PivoW(base):
  linha_w = base[len(base)-1]
  indice_coluna = 0
  indice_linha = 0

  for indice in range(len(linha_w)-1):
    valor_linha = 0
    if linha_w[indice] < valor_linha:
      valor_linha = linha_w[indice]
      indice_coluna = indice

  coluna_pivo = []
  for linha in base:
    coluna_pivo.append(linha[indice_coluna])
  coluna_pivo.pop(-2) # REMOVENDO ITEM Z COLUNA DO PIVO

  coluna_b = []
  for linha in base:
    coluna_b.append(linha[len(base)+1])
  coluna_b.pop(-2)    # REMOVENDO ITEM Z COLUNA B

  for i in range(len(coluna_pivo)):
    pivo = 500
    if coluna_b[i] > 0 and coluna_pivo[i] > 0:
      if coluna_b[i]/coluna_pivo[i] < pivo:
        pivo = coluna_pivo[i]
        indice_linha = i
  
  cordenadas_pivo = [indice_linha, indice_coluna]
  return cordenadas_pivo



def Eliminacao_W(base):
    pivo = base[PivoW(base)[0]][PivoW(base)[1]]
    linha_pivo = base[PivoW(base)[0]]

    print(linha_pivo)

    if pivo != 1: 
      for i in range(len(linha_pivo)):
        linha_pivo[i] = linha_pivo[i]/pivo
    
    for linha in base:
      linha_pivo_base = linha[PivoW(base)[1]]
     
      if linha_pivo_base < 0 and linha != linha_pivo:
        for i in range(len(linha)):
          linha[i] = abs(linha_pivo_base)*linha_pivo[i] + linha[i] 
 
      elif linha_pivo_base > 0 and linha != linha_pivo:
          for i in range(len(linha)):
            linha[i] = -linha_pivo_base*linha_pivo[i] + linha[i] 

    if base[len(base)-1][len(linha_pivo)-1] == 0:
      base.pop(-1)            #DELETANDO A ÚLTIMA LINHA DO 'W' QUE JÁ FOI ZERADA
      for linha in base:
        linha.pop(-2)         #DELETANDO COLUNA COM VALOR DA VARIAVEL ARTIFICIAL

      Apresentar_Tabela(base)
      print("ELIMINACAO 'W' CONCLUIDA!")
    else:
      Eliminacao_W(base)



def Apresentar_Tabela(base):
  for i in range(len(base)):
    print(f"LINHA{i} -> {base[i]}")






#Eliminacao_W(base_canonica2)
#Eliminacao_Z(base_canonica2)