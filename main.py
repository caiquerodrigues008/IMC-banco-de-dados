import sqlite3
from datetime import datetime

# Configuração do Banco de Dados
def setup_database():
    conn = sqlite3.connect('imc_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imc_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            altura REAL NOT NULL,
            peso REAL NOT NULL,
            imc REAL NOT NULL,
            data_calculo TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para calcular o IMC
def calcular_imc(peso, altura):
    return round(peso / (altura ** 2), 2)

# Inserir novo registro no banco
def inserir_registro(nome, altura, peso):
    imc = calcular_imc(peso, altura)
    data_calculo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('imc_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO imc_records (nome, altura, peso, imc, data_calculo)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, altura, peso, imc, data_calculo))
    conn.commit()
    conn.close()
    print(f"Registro de {nome} inserido com sucesso! IMC: {imc}")

# Listar todos os registros
def listar_registros():
    conn = sqlite3.connect('imc_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM imc_records')
    registros = cursor.fetchall()
    conn.close()
    if registros:
        print("\nRegistros armazenados:")
        for reg in registros:
            print(f"ID: {reg[0]}, Nome: {reg[1]}, Altura: {reg[2]}, Peso: {reg[3]}, IMC: {reg[4]}, Data: {reg[5]}")
    else:
        print("\nNenhum registro encontrado.")

# Buscar registros por nome
def buscar_por_nome(nome):
    conn = sqlite3.connect('imc_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM imc_records WHERE nome LIKE ?', (f"%{nome}%",))
    registros = cursor.fetchall()
    conn.close()
    if registros:
        print(f"\nRegistros encontrados para '{nome}':")
        for reg in registros:
            print(f"ID: {reg[0]}, Nome: {reg[1]}, Altura: {reg[2]}, Peso: {reg[3]}, IMC: {reg[4]}, Data: {reg[5]}")
    else:
        print(f"\nNenhum registro encontrado para '{nome}'.")

# Menu interativo
def menu():
    setup_database()
    while True:
        print("\n--- Aplicação de Cálculo de IMC ---")
        print("1. Inserir novo cálculo de IMC")
        print("2. Listar todos os cálculos")
        print("3. Buscar cálculo por nome")
        print("4. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            nome = input("Digite o nome do paciente: ")
            altura = float(input("Digite a altura (em metros): "))
            peso = float(input("Digite o peso (em kg): "))
            inserir_registro(nome, altura, peso)
        elif escolha == "2":
            listar_registros()
        elif escolha == "3":
            nome = input("Digite o nome para buscar: ")
            buscar_por_nome(nome)
        elif escolha == "4":
            print("Saindo... Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executar a aplicação
if __name__ == "__main__":
    menu()
