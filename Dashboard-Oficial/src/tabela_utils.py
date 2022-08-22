# ----------------------------------------- Importando bibliotecas -----------------------------------------
import pandas as pd
import math

# ------------------------------------------------ Funções ------------------------------------------------
def filtrar_colunas(tabela: pd.DataFrame, filtros: list) -> pd.DataFrame: 
    """Filtra colunas mantendo apenas as especificadas no argumento 'filtros'

    Args:
        tabela (pd.DataFrame): A tabela que será filtrada
        filtros (list): Lista de colunas que serão mantidas

    Returns:
        pd.DataFrame: Dataframe com as colunas filtradas
    """
    linhas = tabela.values.tolist()
    cabecalhos = tabela.columns.to_list()
    indexes=[]
    resultado=[]

    cabecalhos_filtrados=[]
    for cabecalho in cabecalhos:
        if cabecalho in filtros:
            indexes.append(cabecalhos.index(cabecalho))
            cabecalhos_filtrados.append(cabecalho)
    
    linha_filtrada=[]
    for linha in linhas:
        linha_filtrada=[]
        for index in indexes:
            linha_filtrada.append(linha[index])
        resultado.append(linha_filtrada)

    return pd.DataFrame(resultado, columns=cabecalhos_filtrados)



def filtrar_linhas(tabela: pd.DataFrame, coluna: str, filtro: list) -> pd.DataFrame:
    """Filtra linhas mantendo apenas as especificadas no argumento 'filtro'
    
    Args:
        tabela (pd.DataFrame): Tabela a ser operada
        coluna (str): Coluna que contem os valores do filtro
        filtro (list): Linhas que devem permanecer na tabela
    Returns:
        pd.DataFrame: Tabela apenas com linhas colocadas no filtro
    """
    tabela = tabela.to_dict()
    linhas = tabela[coluna]
    linhas_a_apagar = []

    for index in linhas:
        valor = linhas[index]
        if not str(valor) in filtro:
            linhas_a_apagar.append(index)
    
    for linha in linhas_a_apagar:
        for cabecalho in tabela:
            tabela[cabecalho].pop(linha)
    
    return pd.DataFrame(tabela)



def fatiar(tabela: pd.DataFrame, cabeçalho_selecionado: str, alvo: int) -> pd.DataFrame: # TODO Faz a mesma coisa que filtrar linha, analizar possivel mescla
    """Filtra linhas mantendo apenas as com valores especificados no argumento 'alvo'
    
    Args:
        tabela (pd.DataFrame): Tabela a ser operada
        cabeçalho_selecionado (str): Coluna que contem os valores alvo
        alvo (int): Linhas que contem os inteiros que devem permanecer na tabela
    Returns:
        pd.DataFrame: Tabela apenas com linhas que contem o valor alvo no cabeçalho_selecionado
    """
    tabela = tabela.to_dict()
    fatiador = []
    linha = tabela[cabeçalho_selecionado]
    
    for id in linha:
        if linha[id] != alvo:
            fatiador.append(id)
    
    for linha in fatiador:
        for corte in tabela:
            tabela[corte].pop(linha)
    
    return pd.DataFrame(tabela)



def retirar_nulos(tabela: pd.DataFrame) -> pd.DataFrame:
    """Retira todas as linhas da tabela que contenham um valor NaN 

    Args:
        tabela (pd.DataFrame): A tabela a ser operada
    Returns:
        pd.DataFrame: Uma tabela com os valores NaN retirados
    """
    linhas = tabela.values.tolist()
    cabecalhos = tabela.columns.to_list()
    linhas_resultado=[]
    invalido = False

    for linha in linhas:
        invalido = False
        for coluna in linha:
            if isinstance(coluna, float):
                if math.isnan(coluna):
                    invalido = True
                    break
        if not invalido:
            linhas_resultado.append(linha)
    
    return pd.DataFrame(linhas_resultado, columns = cabecalhos)



def soma_por_categoria(tabela: pd.DataFrame, cabecalho_categoria: str, cabecalho_a_somar: str) -> pd.DataFrame:
    """Soma os valores da coluna 'cabecalho_a_somar' mantendo uma linha para cada categoria diferente em 'cabecalho_categoria'

    Args:
        tabela (pd.DataFrame): Tabela a ser operada
        cabecalho_categoria (str): Cabeçalho onde estão as categorias
        cabecalho_a_somar (str): Cabeçalho a ser calculada a soma
    Returns:
        pd.DataFrame: Dataframe com os dados calculados
    """
    tabela = tabela.to_dict()
    tabela_resultado = {cabecalho_categoria:{},cabecalho_a_somar:{}}
    coluna_a_somar = tabela[cabecalho_a_somar]
    coluna_categoria = tabela[cabecalho_categoria]
    soma = {}
    
    for index in coluna_categoria:
        valor_linha = coluna_categoria[index]
        if valor_linha in soma:
            soma[valor_linha]+=coluna_a_somar[index]
        else:
            soma[valor_linha]=coluna_a_somar[index]

    linhas = len(soma) # TODO variavel nao sendo usada
    i=1
    
    for categoria in soma:
        tabela_resultado[cabecalho_categoria][i] = categoria
        tabela_resultado[cabecalho_a_somar][i] = soma[categoria]
        i+=1

    return pd.DataFrame(tabela_resultado)



def soma_generica_colunas(tabela: pd.DataFrame) -> pd.DataFrame:
    """Soma todos os valores de cada coluna separadamente, só aceita valores somaveis
    
    Args:
        tabela (pd.DataFrame): Tabela a ser operada
    Returns:
        pd.DataFrame: Tabela com 2 linhas, cabeçalho + colunas somadas
    """
    tabela_cabecalho = tabela.columns.tolist() # Transformando o cabeçalho do dataframe pra lista
    tabela_valores = tabela.values.tolist() # Transformando os valores do dataframe pra lista
    lista_somas = [] # Lista onde serão armazenadas as respostas da soma de cada coluna
    
    for coluna in range(len(tabela_cabecalho)): # Fazendo uma repetição pra cada coluna
        soma_coluna = 0
        for linha in range(len(tabela_valores)): # Fazendo uma repetição pra cada linha da coluna atual
            soma_coluna += tabela_valores[linha][coluna]    
        lista_somas.append(soma_coluna)

    resultado = [tabela_cabecalho, lista_somas]
    return pd.DataFrame(resultado)
    # TODO substituir por return pd.DataFrame(lista_somas, columns = tabela_cabecalho) 



def maximo(tabela: pd.DataFrame, cabecalho_max: str) -> float:
    """Calcula o valor máximo de uma coluna

    Args:
        tabela (pd.DataFrame): Tabela a ser operada
        cabecalho_max (str): coluna a ser operada
    Returns:
        float: Valor máximo dentro da coluna
    """
    linhas = tabela.values.tolist()
    cabecalhos = tabela.columns.to_list()
    maximo = 0
    
    for linha in linhas:
        atual = linha[cabecalhos.index(cabecalho_max)]
        if atual > maximo:
            maximo = atual
    
    return maximo



def remover_pequenos(tabela: pd.DataFrame, cabeçalho_selecionado: str, alvo: int) -> pd.DataFrame:
    """Mantem na tabela apenas valores acima do limite estabelecido pelo parametro 'alvo'

    Args:
        tabela (pd.DataFrame): Tabela a ser operada
        cabeçalho_selecionado (str): Coluna que contem os valores a serem analizados
        alvo (int): Valor minimo que sera mantido na tabela
    Returns:
        pd.DataFrame: Tabela com apenas linhas com valores superiores ao alvo
    """
    tabela = tabela.to_dict()
    fatiador = []
    linha = tabela[cabeçalho_selecionado]
   
    for id in linha:
        if linha[id] < alvo:
            fatiador.append(id)
    
    for linha in fatiador:
        for corte in tabela:
            tabela[corte].pop(linha)
   
    return pd.DataFrame(tabela)



# ------------------------------------------ Funções sob analize ------------------------------------------
def manter_pequenos(tabela: pd.DataFrame, cabeçalho_selecionado: str, alvo: int) -> pd.DataFrame: # TODO funcoes outros e outros2 podem ser mescladas com a adicao de um parametro opcional
    """Mantem na tabela apenas valores abaixo do limite estabelecido pelo parametro alvo

    Args:
        tabela (pd.DataFrame): Tabela a ser operada
        cabeçalho_selecionado (str): Coluna que contem os valores a serem analizados
        alvo (int): Valor maximo que sera mantido na tabela
    Returns:
        pd.DataFrame: Tabela com apenas linhas com valores inferiores ao alvo
    """
    tabela = tabela.to_dict()
    fatiador = []
    linha = tabela[cabeçalho_selecionado]
    
    for id in linha:
        if linha[id] > alvo:
            fatiador.append(id)
    
    for linha in fatiador:
        for corte in tabela:
            tabela[corte].pop(linha)
   
    return pd.DataFrame(tabela)



def tirazero(tabela: pd.DataFrame):  # TODO remover ja que é inutil
    tabela = tabela.to_dict()
    apagar=[]
    for cabecalho in tabela:
        linhas = tabela[cabecalho]
        for index in linhas:
            if linhas[index] == 0:
                apagar.append(index)
    for linha in apagar:
        for coluna in tabela:
            tabela[coluna].pop(linha)
    return pd.DataFrame(tabela)