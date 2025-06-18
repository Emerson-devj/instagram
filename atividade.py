import mysql.connector

# aqui eu to Conectando ao banco de dados
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='unifesspa',
    database='mydb'
)

cursor = conexao.cursor()

# aqui eu to adicionando os selects
consultas = [
    "SELECT T.nome, T.telefone FROM Tutor T LEFT JOIN Animal a ON T.idTutor = a.idTutor;",
    "SELECT T.nome, COUNT(a.idAnimal) AS total FROM Tutor T LEFT JOIN Animal a ON T.idTutor = a.idTutor GROUP BY nome;",
    "SELECT T.nome, telefone FROM Tutor T LEFT JOIN Animal a ON T.idTutor= a.idTutor WHERE a.idAnimal IS NULL ORDER BY nome;"
]

# Executa cada SELECT
for i, consulta in enumerate(consultas, start=1):
    print(f"\n--- Resultado da Consulta {i} ---")
    cursor.execute(consulta)
    resultados = cursor.fetchall()

    # Imprime os resultados de forma simples
    for linha in resultados:
        print(linha)

# Finalizar conexão
cursor.close()
conexao.close()
