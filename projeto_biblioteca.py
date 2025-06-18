from datetime import datetime
from collections import deque

def atualizar_generos(livros, generos):
        generos.clear()
        for livro in livros:
            generos.add(livro["Gênero"])

filas_espera = {}
def adicionar_usuario_na_fila(id_livro, id_usuario):
    if id_livro not in filas_espera:
        filas_espera[id_livro] = deque()
    filas_espera[id_livro].append(id_usuario)
    print(f"Usuário {id_usuario} adicionado à fila de espera do livro {id_livro}.")

def remover_usuario_da_fila(id_livro):
    if id_livro in filas_espera and filas_espera[id_livro]:
        usuario_atual = filas_espera[id_livro].popleft()
        return usuario_atual
    return None

def visualizar_filas_de_espera():
    print("\n--- Filas de Espera ---")
    if not filas_espera:
        print("Nenhuma fila de espera registrada.")
    else:
        for id_livro, fila in filas_espera.items():
            print(f"Livro {id_livro}: Usuario id:{list(fila)}")

def cadastrar_livro(livros, generos, historico):
    print("\n--- Cadastro de Livro ---")
    id_livro = len(livros) + 1
    titulo = input("Digite o título do livro: ")
    autor = input("Digite o autor do livro: ")
    ano = input("Digite o ano de publicação: ")
    genero = input("Digite o gênero do livro: ")

    livro = {
        "ID": id_livro,
        "Título": titulo,
        "Autor": autor,
        "Ano de Publicação": ano,
        "Gênero": genero,
        "Disponível": True
    }
    livros.append(livro)
    atualizar_generos(livros, generos)
    historico.registrar("Cadastro de Livro:", f"Livro: {titulo}, Autor: {autor}")
    print(f"\nLivro '{titulo}' cadastrado com sucesso!\n")

def consultar_livros(livros,historico):
    pesquisa = input("Digite o título, autor ou gênero para buscar: ").lower()
    encontrados = [livro for livro in livros if
                   pesquisa in livro["Título"].lower() or
                   pesquisa in livro["Autor"].lower() or
                   pesquisa in livro["Gênero"].lower()]

    if encontrados:
        print("\nLivros encontrados:")
        for livro in encontrados:
            print(f"ID: {livro['ID']}, Título: {livro['Título']}, Autor: {livro['Autor']}, Ano: {livro['Ano de Publicação']}, Gênero: {livro['Gênero']}, Disponível: {'Sim' if livro['Disponível'] else 'Não'}")
    else:
        print("Nenhum livro encontrado para a pesquisa.")
    historico.registrar("consulta de livros:",f"pesquisa:{pesquisa}")

def cadastrar_usuario(usuarios,historico):
    print("\n--- Cadastro de Usuário ---")
    id_usuario = len(usuarios) + 1
    nome = input("Digite o nome do usuário: ")

    while True:
        tipo = input("Digite o tipo de usuário (leitor ou bibliotecário): ").strip().lower()
        if tipo in ("leitor", "bibliotecário"):
            break
        else:
            print("Tipo inválido, por favor escolha entre leitor e bibliotecário.")

    usuario = {
        "ID": id_usuario,
        "Nome": nome,
        "Tipo": tipo
    }
    usuarios.append(usuario)
    historico.registrar("cadastro usuario",f"{id_usuario}")
    print(f"\nUsuário '{nome}' cadastrado com sucesso!\n")


def emprestar_livro(emprestimos, id_emprestimo, id_livro, id_usuario, data_devolucao, livros, historico, generos):
    for livro in livros:
        if livro["ID"] == id_livro:
            if livro["Disponível"]:
                emprestimos.append({
                    "ID Empréstimo": id_emprestimo,
                    "ID Livro": id_livro,
                    "ID Usuário": id_usuario,
                    "Data Empréstimo": datetime.today().strftime('%Y-%m-%d'),
                    "Data Devolução Prevista": data_devolucao
                })
                livro["Disponível"] = False
                print("Empréstimo registrado com sucesso!\n")
                atualizar_generos(livros, generos)
                historico.registrar("Empréstimo de Livro", f"Livro: {id_livro}, Usuário: {id_usuario}")
                return
            else:
                print("\nLivro indisponível! Usuário adicionado à fila de espera.")
                adicionar_usuario_na_fila(id_livro, id_usuario)
                return  
    print("\nErro: Livro não encontrado! Verifique o ID informado.\n")


def registrar_devolucao(emprestimos, livros, generos, historico):
    print("\n--- Registro de Devolução ---")
    id_livro = int(input("Digite o ID do livro a ser devolvido: "))

    for emprestimo in emprestimos:
        if emprestimo["ID Livro"] == id_livro:
            for livro in livros:
                if livro["ID"] == id_livro:
                    livro["Disponível"] = True
            proximo_usuario = remover_usuario_da_fila(id_livro)
            
            if proximo_usuario:
                print(f"Usuario ({proximo_usuario}) agora pode pegar o livro {[id_livro]}.")
                nova_data_devolucao = input(f"Digite a nova data de devolução prevista  (dia-mes-ano): ")
                id_emprestimo = len(emprestimos) + 1
                emprestar_livro(emprestimos, id_emprestimo, id_livro, proximo_usuario, nova_data_devolucao, livros, historico, generos)
            else:
                print(f"O livro {id_livro} está agora disponível para outros usuários.")

            atualizar_generos(livros, generos)
            historico.registrar("Devolução de Livro", f"Livro: {id_livro}")
            print(f"\nLivro ID {id_livro} devolvido com sucesso!\n")
            return

    print("\nEmpréstimo não encontrado. Verifique o ID informado.\n")

def relatorio_estatistico(livros, usuarios, emprestimos):
    print("Gerando relatório estatístico...")
    num_livros = len(livros)
    num_usuarios = len(usuarios)
    num_emprestimos = len(emprestimos)
    num_livros_disponiveis = sum(1 for livro in livros if livro["Disponível"])
    num_livros_indisponiveis = num_livros - num_livros_disponiveis

    print("\n--- Relatório Estatístico ---")
    print(f"Número de livros cadastrados: {num_livros}")
    print(f"Número de usuários cadastrados: {num_usuarios}")
    print(f"Número de empréstimos realizados: {num_emprestimos}")
    print(f"Número de livros disponíveis: {num_livros_disponiveis}")
    print(f"Número de livros emprestados (indisponíveis): {num_livros_indisponiveis}")


class HistoricoOperacoes:
    def __init__(self):
        self.historico = []

    def registrar(self, tipo, detalhes):
        self.historico.append({
            "tipo": tipo,
            "detalhes": detalhes,
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def desfazer(self):
        if self.historico:
            ultima_operacao = self.historico.pop()
            print(f"Última operação desfeita: {ultima_operacao}")
        else:
            print("Nenhuma operação para desfazer.")

    def exibir(self):
        if self.historico:
            print("\n--- Histórico de Operações ---")
            for operacao in reversed(self.historico):
                print(operacao)
        else:
            print("Nenhuma operação registrada.")


def menu():
    livros = []
    usuarios = []
    emprestimos = []
    generos = set()
    historico = HistoricoOperacoes()


    while True:
        print("=== Biblioteca ===")
        print("1. Cadastrar livro")
        print("2. Consultar livros")
        print("3. Cadastrar usuário")
        print("4. Emprestar livro")
        print("5. Registrar devolução")
        print("6. Fila de espera")
        print("7. Histórico de operações")
        print("8. Gêneros Disponíveis")
        print("9. Relatório estatístico")
        print("10. Desfazer última operação")
        print("11. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_livro(livros, generos, historico)
        elif opcao == "2":
            consultar_livros(livros,historico)
        elif opcao == "3":
            cadastrar_usuario(usuarios,historico)
        elif opcao == "4":
            id_emprestimo = len(emprestimos) + 1

            id_livro = int(input("Digite o ID do livro: "))
            livro_encontrado = None

            for livro in livros:
              if livro["ID"] == id_livro:
                  livro_encontrado = livro
                  break

            if not livro_encontrado:
                print("\nErro: Livro não encontrado! Verifique o ID informado.\n")
                continue

            id_usuario = int(input("Digite o ID do usuário: "))
            usuario_encontrado = None

            for usuario in usuarios:
              if usuario["ID"] == id_usuario:
                usuario_encontrado = usuario
                break 
            if not usuario_encontrado:
              print("\nErro: Usuário não encontrado! Verifique o ID informado.\n")
              continue

            data_devolucao = input("Digite a data de devolução prevista (dia-mes-ano): ")
            emprestar_livro(emprestimos, id_emprestimo, id_livro, id_usuario, data_devolucao,livros,historico,generos)
            livro_encontrado["Disponível"] = False

        elif opcao == "5":
            registrar_devolucao(emprestimos, livros, generos, historico)

        elif opcao == "6":
           visualizar_filas_de_espera()

        elif opcao == "7":
            historico.exibir()
        elif opcao == "8":
            print("\n--- Gêneros Disponíveis ---")
            if generos:
              for genero in generos:
                print(f"- {genero}")
            else:
              print("Nenhum genero cadastrado") 
        elif opcao== "9":
            relatorio_estatistico(livros, usuarios, emprestimos)
            
         
        elif opcao == "10":
            historico.desfazer()
        elif opcao == "11":
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.\n")

menu()