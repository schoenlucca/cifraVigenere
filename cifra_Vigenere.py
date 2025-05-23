import string
import unicodedata
from math import gcd
from functools import reduce

alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

frequencia_pt = [14.63, 1.04, 3.88, 4.99, 12.57, 1.02, 1.30, 1.28, 6.18, 0.40, 0.02, 2.78, 4.74,
                     5.05, 10.73, 2.52, 1.20, 6.53, 7.81, 4.34, 4.63, 1.67, 0.01, 0.21, 0.01, 0.47]
frequencia_en = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025,
                 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]

def estende_chave(chave, tamanho):
    chave = chave.upper()
    chave_estendida = ''
    count = 0
    while len(chave_estendida) < tamanho:
        chave_estendida += chave[count % len(chave)]
        count += 1
    return chave_estendida


def cifra_vigenere(plaintext, chave):
    plaintext = plaintext.upper()
    chave_estendida = estende_chave(chave, len(plaintext))
    texto_cifrado = ''
    i = 0  # índice para acompanhar a posição no texto

    for caractere in plaintext:
        if caractere.isalpha():
            p = alfabeto.index(caractere)   #posição do caractere plano no alfabeto
            k = alfabeto.index(chave_estendida[i])  #posição do elemento chave[i] no alfabeto
            c = (p + k) % 26    #cálculo da posição adequada de criptografia para a linha chave[i] na matriz de vigenere
            texto_cifrado += alfabeto[c]
        else:
            texto_cifrado += caractere  # Mantém espaços e pontuação
        i += 1  # incrementa o índice manualmente

    return texto_cifrado

def decifra_vigenere(criptograma, chave):
    criptograma = criptograma.upper()
    chave_estendida = estende_chave(chave, len(criptograma))
    texto_decifrado = ''
    i = 0  # índice manual

    for caractere in criptograma:
        if caractere.isalpha():
            c = alfabeto.index(caractere)   #posição do caractere criptografado no alfabeto
            k = alfabeto.index(chave_estendida[i])  #posição do elemento chave[i] no alfabeto 
            p = (c - k + 26) % 26    #cálculo da posição adequada de criptografia para a linha chave[i] na matriz de vigenere
            texto_decifrado += alfabeto[p]
        else:
            texto_decifrado += caractere
        i += 1  # incrementa o índice

    return texto_decifrado

def remover_acentos(texto):
    texto = unicodedata.normalize('NFD', texto)
    return ''.join(c for c in texto if unicodedata.category(c) != 'Mn')

def limpar_texto(texto):
    texto = texto.upper()
    texto = remover_acentos(texto)
    return ''.join(c for c in texto if c in alfabeto)



#função que conta as frequencias de todas as trincas presentes no texto
def contador_de_trincas(texto):
    texto = limpar_texto(texto)
    frequencia_trincas = {}
    for i in range(len(texto)-2):
        trinca = texto[i:i+3]
        if frequencia_trincas.get(trinca):
            frequencia_trincas[trinca].append(i)
        else:
            frequencia_trincas[trinca] = [i]
    return frequencia_trincas

def verifica_distancias(frequencia_trincas):
    distancias_trincas = {}
    for trinca in frequencia_trincas:
        if len(frequencia_trincas[trinca]) > 1:  # verificar se a trinca se repete (mais de uma posição)
            distancias_trincas[trinca] = []
            for i in range(len(frequencia_trincas[trinca]) - 1):
                distancia = frequencia_trincas[trinca][i+1] - frequencia_trincas[trinca][i]
                distancias_trincas[trinca].append(distancia)
    return distancias_trincas


#função usada em divisores_comuns_lista, calcula o MDC de todos os elementos da lista, retornando um número
def mdc_lista(nums):
    return reduce(gcd, nums)

#função usada em divisores_comuns_lista, retorna todos os divisores comuns do MDC encontrado em mdc_lista
def divisores(n):
    divs = set()
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divs.add(i)
            divs.add(n // i)
    return sorted(divs)

#recebe uma lista e retorna todos os divisores comuns de todos os elementos da lista 
def divisores_comuns_lista(nums):
    m = mdc_lista(nums)
    return divisores(m)

def todos_divisores_em_uma_lista(distancias_trincas):
    resultado = []
    for trinca, distancias in distancias_trincas.items():
        for d in distancias:
            resultado.extend(divisores(d))
    return resultado

def mais_frequente(divisores):
    aparicoes = {}
    for divisor in divisores:
        if divisor >= 2:  # Ignora 1
            aparicoes[divisor] = aparicoes.get(divisor, 0) + 1
    
    if not aparicoes:
        return 1  # Caso não encontre divisores
    
    # Pega os 3 divisores mais frequentes e escolhe o maior
    mais_comuns = sorted(aparicoes.items(), key=lambda x: (-x[1], x[0]))
    top3 = [d for d, _ in mais_comuns[:3]]
    return max(top3)  # Retorna o maior entre os mais frequentes     

def colunas_i(texto, tamanho_chave):
    colunas = []
    for i in range(tamanho_chave):
        coluna = []
        n = i
        while n < len(texto):
            coluna.append(texto[n])
            n = n + tamanho_chave
        colunas.append(coluna)
    return colunas

def encontrar_chave_por_frequencia(colunas, frequencia_lingua):
    chave = ''
    for coluna in colunas:
        melhor_correlacao = -1
        melhor_deslocamento = 0

        # Conta as frequências reais da coluna
        frequencias_coluna = [0] * 26
        for letra in coluna:
            if letra in alfabeto:
                frequencias_coluna[alfabeto.index(letra)] += 1

        total = sum(frequencias_coluna)
        if total == 0:
            chave += 'A'  # se a coluna estiver vazia por algum motivo
            continue

        # Normaliza para porcentagem
        frequencias_coluna = [f * 100 / total for f in frequencias_coluna]

        # Tenta todos os deslocamentos (0 a 25)
        for deslocamento in range(26):
            correlacao = 0
            for i in range(26):
                correlacao += frequencias_coluna[i] * frequencia_lingua[(i - deslocamento) % 26]  # Subtrai o deslocamento
            if correlacao > melhor_correlacao:
                melhor_correlacao = correlacao
                melhor_deslocamento = deslocamento

        chave += alfabeto[melhor_deslocamento]
    return chave

def reduzir_chave(chave_estimada):
    # Verifica se a chave pode ser dividida em partes menores repetidas
    for tamanho in range(1, len(chave_estimada) // 2 + 1):
        parte = chave_estimada[:tamanho]
        # Se a chave for composta por repetições da parte, retorna a parte
        if parte * (len(chave_estimada) // tamanho) == chave_estimada:
            return parte
    return chave_estimada  # Se não for repetida, retorna a original

"""

texto_teste = "Filho de Irinéia e Jessé, Zeca nasceu no Irajá, onde desde pequeno passou a frequentar rodas de samba por influência de sua família. Durante a juventude, foi office-boy e apontador de jogo do bicho.[3] Morou em diversos bairros do Rio, mas sempre demonstrou apreço especial por Xerém (distrito do município de Duque de Caxias), onde possui um sítio (no qual foram gravados os DVDs da série O Quintal do Pagodinho) e uma escola de música para crianças carentes da região. Sua primeira gravação foi em 1983, com o samba Camarão que dorme a onda leva, de sua autoria, Arlindo Cruz e Beto sem Braço, a partir do convite de sua madrinha no samba, Beth Carvalho. Dois anos depois, figurou entre os nomes escolhidos pelo produtor musical Milton Manhães, da gravadora RGE, para participar do álbum colaborativo Raça Brasileira, junto de Elaine Machado, Jovelina Pérola Negra, Mauro Diniz e Pedrinho da Flor. O disco, que revelou toda uma geração de sambistas, contava com uma cinco de composições de Zeca: Leilão (parceria com Beto Sem Braço), Mal de Amor (com Beto Sem Braço e Mauro Diniz), Santa Paciência, Garrafeiro (ambas com Diniz), A Vaca (com Ratinho) e o sucesso Bagaço da Laranja (com Arlindo Cruz e Jovelina Pérola Negra). A parceria com a RGE perduraria ainda por alguns anos, sendo a gravadora responsável pelos lançamentos subsequentes do artista até 1988. Em 1986 lançou seu primeiro álbum solo, com participações especiais dos cantores Deni e Ana Clara. O sucesso do disco foi tamanho que a música Judia de Mim foi incluída na trilha sonora da novela Hipertensão. Esta seria apenas a primeira gravação de Zeca a ser veiculada em uma telenovela; ele ainda seria o intérprete das canções de abertura de O Cravo e a Rosa (com Jura, de Sinhô) e Bom Sucesso (com O Sol Nascerá, de Cartola e Elton Medeiros, em dueto com Teresa Cristina). A partir do disco de estreia, engatou uma carreira fonográfica que hoje chega a quatro décadas, com álbuns como Patota de Cosme (1987), Samba Pras Moças (1995), Água da Minha Sede (2000) e Mais Feliz (2019), construindo uma imagem pública de malandro boêmio e romântico através de sucessos como Quintal do Céu, Maneiras, Fita Amarela e Uma Prova de Amor. Tendo se tornado uma figura pública conhecida e extremamente popular, foi garoto propaganda das cervejas Nova Schin (em 2003) e, posteriormente, Brahma (a partir de 2004), marca com a qual sua imagem é associada até os dias atuais. Em 2003, no auge de sua carreira, foi o segundo artista de samba a gravar um especial de TV, CD e DVD pela MTV Brasil (tradicional reduto do rock e do pop). Antes disso, apenas o grupo Art Popular havia recebido o convite para gravar um especial, em 2000. Contendo versões ao vivo de alguns de seus maiores sucessos, o Acústico MTV Zeca Pagodinho, gravado no Rio, tornou-se um de seus discos mais vendidos, rendendo inclusive uma segunda edição em 2006 (sendo o primeiro Acústico a ganhar uma continuação na história da MTV Brasil). O segundo disco, batizado de Acústico MTV Zeca Pagodinho 2 - Gafieira, homenageou o samba de gafieira através de um seleto repertório (que compreende composições de Geraldo Pereira, Noel Rosa, Cartola e Billy Blanco), embalado pelos arranjos do maestro Rildo Hora. Em 2007, o cantor criou o selo ZecaPagodiscos, em parceria com o produtor musical Max Pierre, ex-diretor artístico da Universal Music no Brasil. O primeiro trabalho da parceria (lançado em conjunto com o Música Fabril, novo selo de Max, com distribuição da gravadora EMI) foi o CD e DVD Cidade do Samba, gravado na Cidade do Samba Joãosinho Trinta, reunindo vários artistas brasileiros de diversos estilos musicais, como Martinho da Vila, Jair Rodrigues, Cláudia Leitte, Ivete Sangalo Nando Reis, Erasmo Carlos, Gilberto Gil, entre outros. Em 2013, comemorou 30 anos de carreira com um show especial para o canal televisivo Multishow, lançado em disco como Multishow Ao Vivo: 30 Anos - Vida Que Segue. O repertório homenageava uma série de importantes compositores da história do samba, como João da Baiana, Sinhô, Zé Kéti, Adoniran Barbosa, Martinho da Vila, João Nogueira e Paulinho da Viola. Em 2016, foi um dos convidados especiais na Cerimônia de Abertura dos Jogos Olímpicos Rio 2016. Foi o artista escolhido pela Prefeitura do Rio de Janeiro para o show principal da virada do ano na praia de Copacabana no reveillón de 2023. Em 27 de janeiro de 2024, Zeca se apresentou no reality show Big Brother Brasil 24, junto de Pretinho da Serrinha. O ano foi marcado pelas celebrações de seus 40 anos de carreira e 65 de vida, pontuadas por uma apresentação repleta de convidados realizada no Engenhão (estádio do Botafogo, seu time do coração) no dia 4 de fevereiro, data de seu aniversário. As comemorações foram coroadas com o lançamento do disco Zeca Pagodinho - 40 Anos (Ao Vivo). Atualmente, Zeca reside na Barra da Tijuca com a mulher, Mônica Silva, e seus quatro filhos: Eduardo, Louis, Elisa e Maria Eduarda. Em 2024, Zeca recebeu da Alerj o título de Cidadão Benemérito do Estado do Rio de Janeiro."

texto_teste = limpar_texto(texto_teste)
texto_cifrado = cifra_vigenere(texto_teste, 'LUCCA')
saida = contador_de_trincas(texto_cifrado)
saida_2 = verifica_distancias(saida)
print(texto_cifrado)    
print(saida)
print(saida_2)
divisores = todos_divisores_em_uma_lista(saida_2)
print(divisores)
saida_3 = mais_frequente(divisores)
print(saida_3)
colunas = colunas_i(texto_cifrado, saida_3)
print(colunas)
saida_4 = encontrar_chave_por_frequencia(colunas, frequencia_pt)
saida_4 = reduzir_chave(saida_4)
print(saida_4)
"""