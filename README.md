Descritivo da Cifra de Vigenère e do Ataque por Análise de Frequência

Lucca Schoen de Almeida - 231018900

1. Introdução à Cifra de Vigenère

    A cifra de Vigenère é um método de criptografia polialfabética que utiliza uma chave composta por letras para cifrar um texto. Cada letra da chave define um deslocamento diferente aplicado aos caracteres do texto plano. Isso dificulta ataques por análise de frequência, comuns em cifras monoalfabéticas como a de César.

2. Implementação da Cifra

    A implementação consiste em:

    - estende_chave(chave, tamanho): estende a chave para que ela tenha o mesmo comprimento do texto.

    - cifra_vigenere(plaintext, chave): realiza a cifragem, deslocando cada letra do texto plano pela quantidade determinada pela letra correspondente na chave.

    - decifra_vigenere(criptograma, chave): reverte a cifra, aplicando o deslocamento inverso.

    O alfabeto usado é "A-Z" (26 letras). Caracteres não alfabéticos são mantidos.

3. Limpeza e Normalização do Texto

    Para garantir a correta aplicação dos algoritmos, o texto é limpo com:

    remover_acentos(texto): remove acentos.

    limpar_texto(texto): converte para maiúsculas e remove caracteres fora do alfabeto.

4. Ataque à Cifra: Estimativa de Tamanho da Chave

    O ataque inicia com a tentativa de descobrir o tamanho da chave:

    contador_de_trincas(texto): identifica sequências de três letras repetidas (trincas).

    verifica_distancias(freq_trincas): calcula distâncias entre ocorrências dessas trincas.

    todos_divisores_em_uma_lista(distancias): extrai todos os divisores das distâncias encontradas.

    mais_frequente(divisores): seleciona os divisores mais comuns como candidatos ao tamanho da chave.

    Essa técnica é inspirada no Método de Kasiski.

5. Estimativa da Chave: Análise de Frequência

    Com o tamanho estimado da chave, o texto é separado em colunas:

    colunas_i(texto, tamanho_chave): separa os caracteres do texto em colunas, cada uma cifrada com uma letra da chave.

    Cada coluna é analisada:

    encontrar_chave_por_frequencia(colunas, freq_lingua): para cada coluna, aplica-se um ataque por correlação com a distribuição de frequências da língua (português ou inglês). Tenta-se cada um dos 26 deslocamentos e calcula-se a correlação.

    reduzir_chave(chave_estimada): se a chave estimada for repetições de um padrão, essa função reduz para a menor unidade.

6. Considerações Finais

    A cifra de Vigenère é segura contra ataques simples, mas vulnerável à análise de frequência quando o texto é suficientemente longo. O sucesso do ataque depende da qualidade do texto (em termos de distribuição de letras) e do método de análise usado (correlação ou teste do qui-quadrado).

    Essa implementação cobre desde a cifragem até a recuperação da chave, com base em princípios clássicos da criptoanálise.

