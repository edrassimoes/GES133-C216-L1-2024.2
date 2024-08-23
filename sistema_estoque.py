def adicionar_ao_estoque(estoque, produto):
    estoque.append(produto)
    print("Produto adicionado ao estoque.")

def cadastrar_jogo(estoque):
    titulo = input("Qual o titulo do jogo? ")
    desenvolvedor = input("Qual o desenvolvedor do jogo? ")
    plataforma = input("Qual a plataforma do jogo? ")
    quantidade = int(input("Quantas unidades do jogo estão disponíveis? "))
    jogo = {
        "Titulo": titulo, 
        "Desenvolvedor": desenvolvedor, 
        "Plataforma": plataforma, 
        "Quantidade": quantidade
    }
    adicionar_ao_estoque(estoque, jogo)

def listar_estoque(estoque):
    if len(estoque) == 0:
        print('Não há nada no estoque.')
    else:
        for jogo in estoque:
            print(f"Titulo: {jogo['Titulo']}, Desenvolvedor: {jogo['Desenvolvedor']}, Plataforma: {jogo['Plataforma']}, Quantidade: {jogo['Quantidade']}")

def consultar_estoque(estoque):
    titulo = input("Qual o titulo do jogo? ")
    for jogo in estoque:
        if jogo["Titulo"].lower() == titulo.lower():
            print(f"Titulo: {jogo['Titulo']}, Desenvolvedor: {jogo['Desenvolvedor']}, Plataforma: {jogo['Plataforma']}, Quantidade: {jogo['Quantidade']}")
            return
    print(f"O jogo '{titulo}' não foi encontrado no estoque.")

def vender_jogo(estoque):
    titulo = input("Qual o titulo do jogo? ")
    for jogo in estoque:
        if jogo["Titulo"].lower() == titulo.lower():
            quantidade = int(input("Quantas unidades serão vendidas? "))
            if jogo['Quantidade'] < quantidade:
                print('Quantidade indisponível, cheque o estoque para mais detalhes.')
                return
            else:
                jogo['Quantidade'] -= quantidade
                print(f"Venda realizada com sucesso! Restam {jogo['Quantidade']} unidades no estoque.")
                return
    print(f"O jogo '{titulo}' não foi encontrado no estoque.")

def main():
    estoque = []
    while True:
        print("\nMenu de Opções:")
        print("1. Cadastrar um jogo")
        print("2. Exibir estoque")
        print("3. Procurar um jogo")
        print("4. Vender um jogo")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            cadastrar_jogo(estoque)
        elif opcao == '2':
            listar_estoque(estoque)
        elif opcao == '3':
            consultar_estoque(estoque)
        elif opcao == '4':
            vender_jogo(estoque)
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")
                

if __name__ == "__main__":
    main()
