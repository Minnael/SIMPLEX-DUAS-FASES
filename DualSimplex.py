import re
import numpy as np

base_string = """
  1|0|<6
  0|1|<5
  2|3|<12
  1|-1|>1
  1|2|=|0|
"""

base_string2 = """
  1|2|>6
  -1|3|>2
  7|1|>1
  4|5|=|0|
"""

# X=0 PARA MAXIMIZACAO  /  X=1 PARA MINIMIZACAO
def CriandoVetores(base_string):
  variaveis_padrao = int(input("DIGITE O NÚMERO DE VARIAVEIS: "))
  variaveis_folga = []
  base_canonica = []

  for base in base_string:
    if base == "<":
      variaveis_folga.append(1)
    elif base == ">": 
      variaveis_folga.append(-1)

  numero_variaveis = len(variaveis_folga) + variaveis_padrao

  for i in range(numero_variaveis-1):
    componente = np.zeros(numero_variaveis+1)
    base_canonica.append(componente)

  componente_b = re.findall(r'[<>](-?\d+)', base_string)
  componente_b = [float(num) for num in componente_b]

  numeros_componentes = []  
  padrao = re.compile(r'(-?\d+)')
  for linha in base_string.split('\n'):
    numeros = padrao.findall(linha)
    if numeros:
      numeros_componentes.extend([float(num) for num in numeros[:-1]])  # Adicione todos os números exceto o último

  aux = 0
  for array in base_canonica:
    for i in range(variaveis_padrao):
      array[i] = numeros_componentes[aux]
      aux = aux + 1

  aux = 0
  for i in range(len(base_canonica)-1):
    base_canonica[i][variaveis_padrao + aux] = variaveis_folga[aux]
    aux = aux + 1

  aux = 0
  for i in range(len(base_canonica)-1):
    base_canonica[i][len(array)-1] = componente_b[aux]
    aux = aux +1

  x = 0
  if x == 1:
    return [-1 * array if i != len(base_canonica) - 1 else array for i, array in enumerate(base_canonica)]
  
  else:
    base_canonica[-1] *= -1

    for index, valor in enumerate(variaveis_folga):
      if valor < 0:
        base_canonica[index] *= -1
    
    return base_canonica




def PivoZ(base, componente_b):
   linha_z = base[len(base)-1]
   coordenada_linha = 0
   valor_linha = 0

   for index, numero in enumerate(componente_b):
      if numero < valor_linha:
         valor_linha = numero
         coordenada_linha = index
   
   coordenada_coluna = 0
   valor_coluna = 500

   for i in range(len(base[coordenada_linha])-1):
     if base[coordenada_linha][i] < 0 and linha_z[i] != 0:
      if abs(linha_z[i]/base[coordenada_linha][i]) < valor_coluna:
        valor_coluna = abs(linha_z[i]/base[coordenada_linha][i])
        coordenada_coluna = i
   
   return [coordenada_linha, coordenada_coluna]



def Eliminacao_Z(base):
    componente_b = []

    for array in base:
      componente_b.append(array[len(array)-1])

    coordenadas_pivo = PivoZ(base, componente_b)
    pivo = base[coordenadas_pivo[0]][coordenadas_pivo[1]]

    print(pivo)

    linha_pivo = base[coordenadas_pivo[0]]
    ultima_linha = base[len(base)-1]

    if pivo != 1: 
        for i in range(len(linha_pivo)):
          linha_pivo[i] = linha_pivo[i]/pivo
      
    for linha in base:
        linha_pivo_base = linha[coordenadas_pivo[1]]
      
        if (linha_pivo_base < 0).any() and not np.array_equal(linha, linha_pivo):
          for i in range(len(linha)):
            linha[i] = abs(linha_pivo_base)*linha_pivo[i] + linha[i] 
  
        elif (linha_pivo_base > 0).any() and not np.array_equal(linha, linha_pivo):
            for i in range(len(linha)):
              linha[i] = -linha_pivo_base*linha_pivo[i] + linha[i]
    
    
    ultima_linha = base[len(base)-1]
    
    for valor in ultima_linha:
      if valor < 0:
        Eliminacao_Z(base)
      
    Apresentar_Tabela(base)
   






def Apresentar_Tabela(base):
  for i in range(len(base)):
    print(f"LINHA{i} -> {base[i]}")





base = CriandoVetores(base_string)
Eliminacao_Z(base)