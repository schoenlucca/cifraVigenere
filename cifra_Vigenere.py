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

def cifra_vigenere(texto, chave):
    chave = chave.upper()
    chave_estendida = ''
    texto_cifrado = ''
    j = 0  # índice da chave

    for i in range(len(texto)):
        caractere = texto[i]
        if caractere.upper() in alfabeto:
            letra = caractere.upper()
            k = alfabeto.index(chave[j % len(chave)])
            p = alfabeto.index(letra)
            c = (p + k) % 26
            nova_letra = alfabeto[c]

            if caractere.islower():
                nova_letra = nova_letra.lower()
            texto_cifrado += nova_letra
            j += 1
        else:
            texto_cifrado += caractere
    return texto_cifrado


def decifra_vigenere(texto, chave):
    chave = chave.upper()
    texto_decifrado = ''
    j = 0  # índice da chave

    for i in range(len(texto)):
        caractere = texto[i]
        if caractere.upper() in alfabeto:
            letra = caractere.upper()
            k = alfabeto.index(chave[j % len(chave)])
            c = alfabeto.index(letra)
            p = (c - k + 26) % 26
            nova_letra = alfabeto[p]

            if caractere.islower():
                nova_letra = nova_letra.lower()
            texto_decifrado += nova_letra
            j += 1
        else:
            texto_decifrado += caractere
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



texto1 = """
A criptografia é a ciência que estuda técnicas para garantir a confidencialidade, integridade e autenticidade da informação. Desde a antiguidade, 
diversas civilizações desenvolveram métodos para ocultar mensagens, seja utilizando cifras simples como a cifra de César, seja métodos mais elaborados. 
Com o avanço da tecnologia, principalmente com o surgimento dos computadores, a criptografia evoluiu para sistemas complexos baseados em princípios 
matemáticos. Atualmente, é essencial para proteger comunicações digitais, transações financeiras e dados pessoais em uma era altamente conectada.

Além da proteção, a criptografia também permite a autenticação e a verificação da integridade dos dados, garantindo que a informação não foi alterada 
durante a transmissão. As chaves criptográficas, que podem ser simétricas ou assimétricas, são o coração dos sistemas modernos. Em sistemas simétricos, 
a mesma chave é usada para cifrar e decifrar a mensagem, enquanto em sistemas assimétricos, são usadas chaves públicas e privadas.

O uso da criptografia está presente em diversas aplicações do dia a dia, desde o acesso seguro a sites através do protocolo HTTPS até o uso de carteiras digitais 
e assinaturas eletrônicas. Contudo, a crescente capacidade computacional levanta desafios, pois algoritmos que antes eram seguros podem se tornar vulneráveis 
com o tempo, exigindo o desenvolvimento contínuo de novos métodos e padrões.
"""

texto2 = """
A segurança da informação é um campo que visa proteger os dados contra acessos não autorizados, uso indevido, divulgação, destruição ou alteração. 
Ela envolve políticas, procedimentos e controles técnicos que abrangem a confidencialidade, integridade e disponibilidade da informação, conhecidos como 
triângulo CIA. A proteção adequada desses elementos é fundamental para garantir a continuidade dos negócios e a confiança de usuários e clientes.

Organizações implementam diversas camadas de segurança, incluindo firewalls, criptografia, sistemas de detecção de intrusão e autenticação multifator. 
Além disso, a conscientização dos usuários é crucial, pois muitos ataques exploram falhas humanas, como phishing ou engenharia social. A gestão de riscos 
é parte integrante do processo de segurança, identificando vulnerabilidades e mitigando ameaças.

Com a digitalização crescente, novos desafios surgem, como a proteção de dados em nuvem, a segurança em dispositivos móveis e o combate a ameaças cibernéticas 
cada vez mais sofisticadas. Regulamentações, como a GDPR na Europa e a LGPD no Brasil, impõem requisitos legais para o tratamento e proteção de dados pessoais.
"""

texto3 = """
A internet é uma rede mundial de computadores que permite a comunicação e o compartilhamento de informações de forma rápida e eficiente. Sua origem remonta à ARPANET, 
um projeto dos Estados Unidos desenvolvido nos anos 1960 para interligar centros de pesquisa. Com o tempo, a rede cresceu exponencialmente, incorporando novas tecnologias 
e protocolos, como o TCP/IP, que se tornaram padrões para a comunicação entre dispositivos.

A popularização da internet na década de 1990 revolucionou o acesso à informação, permitindo o surgimento de serviços como e-mail, websites e, posteriormente, redes sociais 
e plataformas de streaming. Essa transformação impactou profundamente a economia, a cultura e as relações sociais em escala global. Atualmente, bilhões de pessoas utilizam a internet diariamente.

Apesar dos benefícios, a internet também trouxe desafios significativos, incluindo questões relacionadas à privacidade, segurança cibernética, disseminação de desinformação 
e desigualdade no acesso à rede. Organizações internacionais, governos e empresas buscam soluções para enfrentar esses problemas e garantir um ambiente digital mais seguro e inclusivo.
"""

texto4 = """
A inteligência artificial (IA) é um ramo da ciência da computação que busca criar sistemas capazes de realizar tarefas que, tradicionalmente, exigem inteligência humana. 
Essas tarefas incluem reconhecimento de fala, visão computacional, tomada de decisão, aprendizado e planejamento. O campo da IA combina conhecimentos de matemática, estatística, 
neurociência e engenharia para desenvolver algoritmos e modelos que permitem máquinas "pensarem".

Nos últimos anos, avanços significativos foram alcançados com técnicas de aprendizado profundo, que utilizam redes neurais artificiais para resolver problemas complexos 
em áreas como tradução automática, diagnóstico médico e veículos autônomos. Além dos benefícios práticos, a IA levanta importantes questões éticas, como a privacidade dos dados, 
o impacto no mercado de trabalho e a responsabilidade por decisões automatizadas.

Instituições acadêmicas, empresas e governos investem pesadamente em pesquisas para aprimorar a IA, visando ampliar sua aplicabilidade e mitigar riscos. A discussão sobre regulamentações, 
transparência e desenvolvimento responsável da IA tornou-se central para garantir que essas tecnologias sejam utilizadas de forma benéfica para a sociedade.
"""

texto5 = """
Os algoritmos de criptografia moderna são fundamentados em princípios matemáticos complexos para garantir a segurança da informação em sistemas digitais. Um exemplo clássico é o RSA, 
que utiliza a dificuldade da fatoração de números primos grandes para proteger dados. Outro algoritmo amplamente utilizado é o AES, que é simétrico e oferece alta eficiência e segurança 
em diversos dispositivos.

Além da criptografia, protocolos de segurança como o SSL/TLS são essenciais para estabelecer conexões seguras na internet, garantindo a confidencialidade e integridade das comunicações. 
O desenvolvimento de algoritmos quânticos, como o algoritmo de Shor, trouxe novos desafios para a criptografia, uma vez que poderiam quebrar sistemas tradicionais, impulsionando pesquisas 
em criptografia pós-quântica.

A segurança computacional não depende apenas dos algoritmos, mas também da implementação correta, gestão de chaves e conscientização dos usuários. O cenário dinâmico das ameaças exige 
atualizações constantes e colaboração entre pesquisadores, desenvolvedores e órgãos reguladores para manter a proteção dos dados.
"""


texto_teste = "Filho de Irinéia e Jessé, Zeca nasceu no Irajá, onde desde pequeno passou a frequentar rodas de samba por influência de sua família. Durante a juventude, foi office-boy e apontador de jogo do bicho.[3] Morou em diversos bairros do Rio, mas sempre demonstrou apreço especial por Xerém (distrito do município de Duque de Caxias), onde possui um sítio (no qual foram gravados os DVDs da série O Quintal do Pagodinho) e uma escola de música para crianças carentes da região. Sua primeira gravação foi em 1983, com o samba Camarão que dorme a onda leva, de sua autoria, Arlindo Cruz e Beto sem Braço, a partir do convite de sua madrinha no samba, Beth Carvalho. Dois anos depois, figurou entre os nomes escolhidos pelo produtor musical Milton Manhães, da gravadora RGE, para participar do álbum colaborativo Raça Brasileira, junto de Elaine Machado, Jovelina Pérola Negra, Mauro Diniz e Pedrinho da Flor. O disco, que revelou toda uma geração de sambistas, contava com uma cinco de composições de Zeca: Leilão (parceria com Beto Sem Braço), Mal de Amor (com Beto Sem Braço e Mauro Diniz), Santa Paciência, Garrafeiro (ambas com Diniz), A Vaca (com Ratinho) e o sucesso Bagaço da Laranja (com Arlindo Cruz e Jovelina Pérola Negra). A parceria com a RGE perduraria ainda por alguns anos, sendo a gravadora responsável pelos lançamentos subsequentes do artista até 1988. Em 1986 lançou seu primeiro álbum solo, com participações especiais dos cantores Deni e Ana Clara. O sucesso do disco foi tamanho que a música Judia de Mim foi incluída na trilha sonora da novela Hipertensão. Esta seria apenas a primeira gravação de Zeca a ser veiculada em uma telenovela; ele ainda seria o intérprete das canções de abertura de O Cravo e a Rosa (com Jura, de Sinhô) e Bom Sucesso (com O Sol Nascerá, de Cartola e Elton Medeiros, em dueto com Teresa Cristina). A partir do disco de estreia, engatou uma carreira fonográfica que hoje chega a quatro décadas, com álbuns como Patota de Cosme (1987), Samba Pras Moças (1995), Água da Minha Sede (2000) e Mais Feliz (2019), construindo uma imagem pública de malandro boêmio e romântico através de sucessos como Quintal do Céu, Maneiras, Fita Amarela e Uma Prova de Amor. Tendo se tornado uma figura pública conhecida e extremamente popular, foi garoto propaganda das cervejas Nova Schin (em 2003) e, posteriormente, Brahma (a partir de 2004), marca com a qual sua imagem é associada até os dias atuais. Em 2003, no auge de sua carreira, foi o segundo artista de samba a gravar um especial de TV, CD e DVD pela MTV Brasil (tradicional reduto do rock e do pop). Antes disso, apenas o grupo Art Popular havia recebido o convite para gravar um especial, em 2000. Contendo versões ao vivo de alguns de seus maiores sucessos, o Acústico MTV Zeca Pagodinho, gravado no Rio, tornou-se um de seus discos mais vendidos, rendendo inclusive uma segunda edição em 2006 (sendo o primeiro Acústico a ganhar uma continuação na história da MTV Brasil). O segundo disco, batizado de Acústico MTV Zeca Pagodinho 2 - Gafieira, homenageou o samba de gafieira através de um seleto repertório (que compreende composições de Geraldo Pereira, Noel Rosa, Cartola e Billy Blanco), embalado pelos arranjos do maestro Rildo Hora. Em 2007, o cantor criou o selo ZecaPagodiscos, em parceria com o produtor musical Max Pierre, ex-diretor artístico da Universal Music no Brasil. O primeiro trabalho da parceria (lançado em conjunto com o Música Fabril, novo selo de Max, com distribuição da gravadora EMI) foi o CD e DVD Cidade do Samba, gravado na Cidade do Samba Joãosinho Trinta, reunindo vários artistas brasileiros de diversos estilos musicais, como Martinho da Vila, Jair Rodrigues, Cláudia Leitte, Ivete Sangalo Nando Reis, Erasmo Carlos, Gilberto Gil, entre outros. Em 2013, comemorou 30 anos de carreira com um show especial para o canal televisivo Multishow, lançado em disco como Multishow Ao Vivo: 30 Anos - Vida Que Segue. O repertório homenageava uma série de importantes compositores da história do samba, como João da Baiana, Sinhô, Zé Kéti, Adoniran Barbosa, Martinho da Vila, João Nogueira e Paulinho da Viola. Em 2016, foi um dos convidados especiais na Cerimônia de Abertura dos Jogos Olímpicos Rio 2016. Foi o artista escolhido pela Prefeitura do Rio de Janeiro para o show principal da virada do ano na praia de Copacabana no reveillón de 2023. Em 27 de janeiro de 2024, Zeca se apresentou no reality show Big Brother Brasil 24, junto de Pretinho da Serrinha. O ano foi marcado pelas celebrações de seus 40 anos de carreira e 65 de vida, pontuadas por uma apresentação repleta de convidados realizada no Engenhão (estádio do Botafogo, seu time do coração) no dia 4 de fevereiro, data de seu aniversário. As comemorações foram coroadas com o lançamento do disco Zeca Pagodinho - 40 Anos (Ao Vivo). Atualmente, Zeca reside na Barra da Tijuca com a mulher, Mônica Silva, e seus quatro filhos: Eduardo, Louis, Elisa e Maria Eduarda. Em 2024, Zeca recebeu da Alerj o título de Cidadão Benemérito do Estado do Rio de Janeiro."

texto_teste = limpar_texto(texto_teste)
texto_cifrado = cifra_vigenere(texto_teste, 'LUCCA')
saida = contador_de_trincas(texto_cifrado)
saida_2 = verifica_distancias(saida)  
divisores = todos_divisores_em_uma_lista(saida_2)
saida_3 = mais_frequente(divisores)
colunas = colunas_i(texto_cifrado, saida_3)
saida_4 = encontrar_chave_por_frequencia(colunas, frequencia_pt)
saida_4 = reduzir_chave(saida_4)
print(saida_4)
saida_5 = decifra_vigenere(texto_cifrado, saida_4)
print(saida_5)