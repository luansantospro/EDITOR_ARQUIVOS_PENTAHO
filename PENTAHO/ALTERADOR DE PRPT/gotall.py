import os

def carregar_substituicoes(caminho_arquivo):
    substituicoes = {}
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                if '=>' in linha:
                    antigo, novo = linha.strip().split('=>', 1)
                    substituicoes[antigo.strip()] = novo.strip()
    except FileNotFoundError:
        print("❌ Arquivo 'substituicoes.txt' não encontrado.")
    return substituicoes

def substituir_em_arquivo(caminho_arquivo, substituicoes):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        conteudo_modificado = conteudo
        for antigo, novo in substituicoes.items():
            conteudo_modificado = conteudo_modificado.replace(antigo, novo)

        if conteudo_modificado != conteudo:
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo_modificado)
            print(f"✅ Modificado: {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao processar {caminho_arquivo}: {e}")

def buscar_e_substituir_em_pasta(diretorio_raiz, substituicoes):
    print(f"\n🔍 Iniciando busca e substituição em: {diretorio_raiz}")
    for raiz, _, arquivos in os.walk(diretorio_raiz):
        for nome_arquivo in arquivos:
            if nome_arquivo.endswith(('.kjb', '.ktr')):
                caminho_completo = os.path.join(raiz, nome_arquivo)
                substituir_em_arquivo(caminho_completo, substituicoes)
    print("\n✅ Substituição concluída.")

def mostrar_menu():
    print("\n====== MENU ======")
    print("1. Listar substituições")
    print("2. Executar substituição nos arquivos .kjb e .ktr")
    print("3. Sair")
    print("==================")

def main():
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_substituicoes = os.path.join(caminho_atual, 'substituicoes.txt')

    substituicoes = carregar_substituicoes(caminho_substituicoes)
    if not substituicoes:
        print("⚠️ Nenhuma substituição encontrada. Verifique o arquivo.")
        return

    while True:
        mostrar_menu()
        escolha = input("Escolha uma opção (1-3): ").strip()

        if escolha == '1':
            print("\n🔁 Substituições carregadas:")
            for antigo, novo in substituicoes.items():
                print(f"  {antigo} => {novo}")

        elif escolha == '2':
            caminho_usuario = input("\n📁 Informe o caminho do diretório onde deseja fazer as substituições:\n> ").strip()

            if not os.path.isdir(caminho_usuario):
                print("❌ Diretório inválido. Tente novamente.")
            else:
                buscar_e_substituir_em_pasta(caminho_usuario, substituicoes)

        elif escolha == '3':
            print("👋 Encerrando o programa.")
            break

        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
