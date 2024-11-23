
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

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

dados = zip(lista_nome, lista_preco, lista_link)
df = pd.DataFrame(dados, columns=['nome', 'preco', 'link'])

df['nome'] = df['nome'].apply(lambda x: x.upper() if isinstance(x, str) else x)

df['preco'] = df['preco'].str.replace('ou R$ ', '', regex=False)
df['preco'] = df['preco'].str.replace('R$ ', '', regex=False)
df['preco'] = df['preco'].str.replace('.', '', regex=False)
df['preco'] = df['preco'].str.replace(',', '.', regex=False)

df['preco'] = pd.to_numeric(df['preco'], errors='coerce')

df = df.dropna()

df = df.sort_values(by='preco', ascending=True)