Web Scraping e Data Science

Nesse projeto eu consegui desenvolver minhas habilidades em Web Scraping e DataScience, Web Scraping para a coleta dos dados e DataScience para o tratamento dos dados em questão.

Para desenvolver esse projeto eu criei 3 tópicos importantes para a entrega;

## 1 - Fazer uma busca em todas as páginas do site que continham o produto que eu queria.
## 2 - Tratar os dados coletados removendo e alterando o que fosse necessário.
## 3 - Criar um DataFrame com os dados coletados.

Tópico número 1: Fazer uma busca em todas as páginas do site que continham o produto que eu queria.
Primeiramente eu fiz a importação das bibliotecas:
```
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
```

Depois eu desenvolvi o web scraping para coletar os dados, o site que usei de exemplo foi o site da Magazine Luiza.
Nesse exemplo eu utilizei um contador para ir alterando o número da página, essa lógia foi implementada porque analisei que a cada página o url ia mudando colocando o número da página em questão.

Criei 3 listas para fazer a coleta dos dados que eu queria, nome do produto, preço do produto e link do produto. O link do produto foi coletado diretamente do href da página html.
```
driver = webdriver.Chrome()

cont = 1
lista_nome = []
lista_preco = []
lista_link = []
while True:
    driver.get(f'https://www.magazineluiza.com.br/busca/iphone/?page={cont}')
    nome_produto = driver.find_elements(By.XPATH, "//h2[@class='sc-cvalOF cQhIqz']")
    preco_produto = driver.find_elements(By.XPATH, "//p[@class='sc-dcJsrY eLxcFM sc-jdkBTo etFOes']")
    link_produto = driver.find_elements(By.XPATH, "//a[@class='sc-fHjqPf eXlKzg sc-fvwjDU gftEET sc-fvwjDU gftEET']")

    time.sleep(3)
    if len(nome_produto) == 0:
        break
    else:
        for nome in nome_produto:
            lista_nome.append(nome.text)
            
        for preco in preco_produto:
            lista_preco.append(preco.text)
            
        for link in link_produto:
            lista_link.append(link.get_attribute('href'))
    cont += 1
driver.quit()

```

Após isso eu fiz a criação do DataFrame, utilizando o ```zip()``` no python, ele permite que você crie uma lista de tuplas com os valores que foi passado, nesse exemplo eu passei valores das 3 listas que eu criei ```lista_nome```, ```lista_preco``` e ```lista_link```.
```
dados = zip(lista_nome, lista_preco, lista_link)
df = pd.DataFrame(dados, columns=['nome', 'preco', 'link'])
```

Após a criação eu comecei com o tratamento dos dados, criei uma função lambda para deixar os nomes dos produtos em letra maiúscula, pois assim facilitaria na hora da visualização.
A função ocorria da seguinte forma: se o nome em questão fosse um objeto do tipo ```str``` ele ficaria maiúsculo, se não retornaria o valor original, essa verificação é importante porque poderia conter dados nulos ou vazios no DataFrame.
```
df['nome'] = df['nome'].apply(lambda x: x.upper() if isinstance(x, str) else x)
```

Após isso eu fiz um tratamento na coluna de preço, removi o texto "ou R$ " que continha em cada texto, removi somente o "R$ ", alterei os pontos por vázios ".", e por fim alterei as viruglas por pontos para fazer a conversão para númerico.
```
df['preco'] = df['preco'].str.replace('ou R$ ', '', regex=False)
df['preco'] = df['preco'].str.replace('R$ ', '', regex=False)
df['preco'] = df['preco'].str.replace('.', '', regex=False)
df['preco'] = df['preco'].str.replace(',', '.', regex=False)
```

```
df['preco'] = pd.to_numeric(df['preco'], errors='coerce')
```

Após isso eu removi as linhas que continham valores nulos, para essa verificação decidi fazer isso ao invés de tratar os valores, porque nesse caso em específico não é viável ter valores nulos tendo em vista que se não tiver ou o preço do produto, ou o nome do produto, ou o link do produto não é interessante.
```
df = df.dropna()
```

Após tudo isso eu executei um comando para ordenar o preço dos produtos do menor para o maior.
```
df = df.sort_values(by='preco', ascending=True)
```
