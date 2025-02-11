import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta
import csv

fake = Faker('pt_BR')

# Conectar ao banco de dados (ou criar um novo)
conn = sqlite3.connect('empresa.db')
cursor = conn.cursor()

# Criar tabela de compras se não existir
cursor.execute('''CREATE TABLE IF NOT EXISTS compras (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    idade INTEGER NOT NULL,
    telefone TEXT NOT NULL,
    estado TEXT NOT NULL,
    DataCompra DATE NOT NULL,
    produto TEXT NOT NULL,
    preco REAL NOT NULL,
    unidades INTEGER NOT NULL,
    ValorCompra REAL NOT NULL)''')
print("Tabela criada com sucesso!")

# Criação do dicionário com produtos e preços
produtos = {
    "Vestuário": {
        "Camisa Temática": 44.90,
        "Moletom": 98.90,
        "Boné": 39.90,
        "pijama": 85.90
    },
    "Action Figures e Colecionáveis": {
        "Action Figure": 180.50,
        "Funko Pop": 80.50,
        "Estatueta": 350.10,
        "Coleção de Figurinhas": 91.90
    },
    "Canecas e Utensílios": {
        "Caneca Personalizada": 29.90,
        "Copo Térmico": 39.90,
        "Jogo de Pratos e Talheres Temático": 19.90,
        "chaveiro": 10.75
    },
    "Leituras": {
        "Mangá": 36.90,
        "Quadrinho": 34.90,
        "Graphic Novel": 49.90,
        "Livro": 59.90
    },
    "Jogos de Tabuleiro": {
        "Jogo de Estratégia": 98.70,
        "Jogo de Cartas": 29.50,
        "Jogo de Festa": 62.40,
        "conjunto de dados RPG": 30.50
    },
    "Acessórios para Cosplay": {
        "Máscara": 49.90,
        "Fantasia": 112.50,
        "Peruca": 39.90,
        "Acessórios e adereços": 27.80
    },
    "Posters e Decoração": {
        "Poster": 45.50,
        "Quadro Decorativo": 39.60,
        "Adesivo de Parede": 24.90,
        "Luminária personalizada":250.10
    },
    "Jogos de Video Game": {
        "Jogo para Console": 109.90,
        "Acessório para Jogo": 89.90,
        "Console clássico": 999.90,
        "Console Portátil": 350.90
    },
     "Acessórios de Informática": {
        "Jogos para PC": 99.90,
        "Pendrive":34.90,
        "Teclado": 49.90,
        "Mouse": 39.90
    }
}

# Criação do dicionário com DDDs e estados
ddd_estados = {
    '11': 'São Paulo', '12': 'São Paulo', '13': 'São Paulo', '14': 'São Paulo',
    '15': 'São Paulo', '16': 'São Paulo', '17': 'São Paulo', '18': 'São Paulo',
    '19': 'São Paulo', '21': 'Rio de Janeiro', '22': 'Rio de Janeiro', '24': 'Rio de Janeiro',
    '27': 'Espírito Santo', '28': 'Espírito Santo', '31': 'Minas Gerais', '32': 'Minas Gerais',
    '33': 'Minas Gerais', '34': 'Minas Gerais', '35': 'Minas Gerais', '37': 'Minas Gerais',
    '38': 'Minas Gerais', '41': 'Paraná', '42': 'Santa Catarina', '43': 'Paraná',
    '44': 'Paraná', '45': 'Paraná', '46': 'Paraná', '47': 'Santa Catarina',
    '48': 'Santa Catarina', '49': 'Santa Catarina', '51': 'Mato Grosso', '52': 'Goiás',
    '53': 'Distrito Federal', '61': 'Distrito Federal', '62': 'Goiás', '63': 'Tocantins',
    '64': 'Goiás', '65': 'Mato Grosso', '66': 'Mato Grosso', '67': 'Mato Grosso do Sul',
    '68': 'Acre', '69': 'Acre', '71': 'Bahia', '73': 'Bahia', '74': 'Bahia', '75': 'Bahia',
    '77': 'Bahia', '79': 'Sergipe', '81': 'Pernambuco', '82': 'Alagoas', '83': 'Paraíba',
    '84': 'Rio Grande do Norte', '85': 'Ceará', '86': 'Piauí', '87': 'Pernambuco',
    '88': 'Ceará', '89': 'Piauí', '91': 'Pará', '92': 'Amazonas', '93': 'Pará',
    '94': 'Pará', '95': 'Roraima', '96': 'Amapá', '97': 'Amazonas', '98': 'Maranhão',
    '99': 'Maranhão'
}
# Gerar números de telefone de clientes
def gerar_telefone():
    ddd = fake.random_element(elements=list(ddd_estados.keys()))
    numero = fake.random_int(min=10000000, max=99999999)
    estado = ddd_estados[ddd]
    return f"({ddd}) {numero}", estado
#Gerar data que foi efetuada a compra pelo cliente
def gerar_data_compra():
    # Gera uma data aleatória entre 1 e 30 de outubro de 2024
    start_date = datetime(2024,12,1)
    end_date = datetime(2024,12,31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.date()  # Retorna a data no formato YYYY-MM-DD

# Gera e insere 2.500 registros
for _ in range(2500):
    nome_completo = f"{fake.first_name()} {fake.last_name()}" # Primeiro e último nome do cliente
    idade = fake.random_int(min=18, max=50) # Idade mínima de 18 anos e máxima de 50 anos
    telefone, estado = gerar_telefone()
    data_compra = gerar_data_compra()
    
    # Seleciona um produto aleatório do dicionário
    categoria = random.choice(list(produtos.keys()))
    produto = random.choice(list(produtos[categoria].keys()))
    
    # Verifica se o produto tem um intervalo de preços
    valor_produto = produtos[categoria][produto]
    if isinstance(valor_produto, tuple) and len(valor_produto) >= 2:  # Verifica se é uma tupla com pelo menos 2 elementos
        preco = round(random.uniform(valor_produto[0], valor_produto[1]), 2)  # Seleciona um valor aleatório dentro do intervalo
    else:
        preco = round(valor_produto, 2)  # Preço fixo
    
    unidades = random.randint(1, 10)  # Número de unidades compradas (1 a 10)
    # Calcula o valor da compra
    valor_compra = round(preco * unidades, 2)

    try:
        cursor.execute('''INSERT INTO compras (cliente, idade, telefone, estado, DataCompra, produto, preco, unidades, ValorCompra)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (nome_completo, idade, telefone, estado, data_compra, produto, preco, unidades, valor_compra))
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados: {e}")

# Salvar (commit) as alterações
conn.commit()
print("Dados inseridos com sucesso!")
# Consultar os dados
cursor.execute("SELECT * FROM compras")
compras = cursor.fetchall()

# Gerar arquivo CSV
with open('registros.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Escrever o cabeçalho
    writer.writerow(['ID Cliente', 'Cliente', 'Idade', 'Telefone', 'Estado', 'DataCompra', 'Produto', 'Preço', 'Unidades', 'ValorCompra'])
    # Escrever os dados
    writer.writerows(compras)

print("Arquivo CSV gerado com sucesso!")
# Fechar a conexão
conn.close()