import os
import zipfile
import shutil

# =======================================================
# Funções auxiliares para substituições
# =======================================================

def criar_arquivo_exemplo(arquivo_txt):
    """Cria um arquivo de exemplo com substituições caso não exista."""
    exemplo = (
        "jdbc:postgresql://localhost:5432/db_antigo => jdbc:postgresql://localhost:5432/db_novo\n"
        "schema_antigo => schema_novo"
    )
    with open(arquivo_txt, 'w', encoding='utf-8') as f:
        f.write(exemplo)
    print(f"[INFO] Arquivo '{arquivo_txt}' não encontrado. Um exemplo foi criado.\n")

def ler_substituicoes(arquivo_txt):
    """Lê substituições do arquivo e retorna como lista de tuplas (antiga, nova)."""
    substituicoes = []

    if not os.path.exists(arquivo_txt):
        criar_arquivo_exemplo(arquivo_txt)

    with open(arquivo_txt, 'r', encoding='utf-8') as f:
        for linha in f:
            if '=>' in linha:
                antiga, nova = linha.strip().split('=>')
                substituicoes.append((antiga.strip(), nova.strip()))

    return substituicoes

def mostrar_substituicoes(arquivo_txt):
    """Mostra na tela o conteúdo do arquivo de substituições."""
    print(f"\n📄 Conteúdo de '{arquivo_txt}':\n")
    try:
        with open(arquivo_txt, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            print(conteudo)
    except FileNotFoundError:
        print("[ERRO] Arquivo de substituições não encontrado.")
    input("\nPressione ENTER para voltar ao menu...")

def substituir_em_arquivo(caminho_arquivo, substituicoes):
    """Aplica substituições em um único arquivo de texto."""
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        for antiga, nova in substituicoes:
            conteudo = conteudo.replace(antiga, nova)
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
    except:
        pass  # Ignora arquivos que não podem ser lidos como texto

# =======================================================
# Funções específicas para arquivos .prpt
# =======================================================

def processar_diretorio(caminho_diretorio, arquivo_substituicoes):
    """Processa todos os arquivos .prpt de um diretório e subdiretórios."""
    if not os.path.isdir(caminho_diretorio):
        print("[ERRO] Diretório inválido.")
        return

    arquivos_prpt = []
    for root, _, files in os.walk(caminho_diretorio):
        for f in files:
            if f.endswith('.prpt'):
                arquivos_prpt.append(os.path.join(root, f))

    if not arquivos_prpt:
        print("[INFO] Nenhum arquivo .prpt encontrado no diretório ou subdiretórios.")
        return

    for caminho in arquivos_prpt:
    #    print(f"Processando: {caminho}")
        processar_prpt(caminho, arquivo_substituicoes)

    print(f"\n[INFO] {len(arquivos_prpt)} arquivos .prpt encontrados e modificados.\n")

def processar_prpt(caminho_prpt, arquivo_substituicoes):
    """Processa um único arquivo .prpt (descompacta, substitui, recompõe)."""
    if not os.path.exists(caminho_prpt):
        print("[ERRO] Caminho para o .prpt não encontrado.")
        return

    prpt_nome = os.path.basename(caminho_prpt)
    nome_base = os.path.splitext(prpt_nome)[0]
    zip_path = os.path.join(os.path.dirname(caminho_prpt), nome_base + '.zip')
    os.rename(caminho_prpt, zip_path)

    pasta_temporaria = os.path.join(os.path.dirname(zip_path), nome_base + '_temp')
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(pasta_temporaria)

    substituicoes = ler_substituicoes(arquivo_substituicoes)

    for root, _, files in os.walk(pasta_temporaria):
        for file in files:
            caminho_completo = os.path.join(root, file)
            substituir_em_arquivo(caminho_completo, substituicoes)

    novo_zip = os.path.join(os.path.dirname(zip_path), nome_base + '_modificado.zip')
    with zipfile.ZipFile(novo_zip, 'w', zipfile.ZIP_DEFLATED) as zip_out:
        for root, _, files in os.walk(pasta_temporaria):
            for file in files:
                caminho_completo = os.path.join(root, file)
                arcname = os.path.relpath(caminho_completo, pasta_temporaria)
                zip_out.write(caminho_completo, arcname)

    novo_prpt = os.path.join(os.path.dirname(zip_path), nome_base + '.prpt')
    os.rename(novo_zip, novo_prpt)

    os.remove(zip_path)
    shutil.rmtree(pasta_temporaria)
    #print(f"[✔] Relatório processado com sucesso!")
    print(f"✅ Modificado: {novo_prpt}")

# =======================================================
# Funções específicas para arquivos .kjb e .ktr
# =======================================================

def processar_kjb_ktr(diretorio, arquivo_substituicoes):
    """Processa arquivos .kjb e .ktr substituindo conforme regras."""
    substituicoes = ler_substituicoes(arquivo_substituicoes)

    if not os.path.isdir(diretorio):
        print("[ERRO] Diretório inválido.")
        return

    encontrados = []
    for root, _, files in os.walk(diretorio):
        for f in files:
            if f.endswith(('.kjb', '.ktr')):
                encontrados.append(os.path.join(root, f))

    if not encontrados:
        print("[INFO] Nenhum arquivo .kjb ou .ktr encontrado no diretório.")
        return

    for caminho in encontrados:
        substituir_em_arquivo(caminho, substituicoes)
        print(f"✅ Modificado: {caminho}")
    
    print(f"\n[INFO] {len(encontrados)} arquivos .kjb/.ktr encontrados e modificados.\n")
# =======================================================
# Menu principal
# =======================================================

def menu_principal():
    arquivo_substituicoes = "substituicoes.txt"

    if not os.path.exists(arquivo_substituicoes):
        criar_arquivo_exemplo(arquivo_substituicoes)

    while True:
        print("\n============== MENU ===============")
        print("  Use com cautela! tenha um backup!")
        print("===================================")
        print("0. Sobre o programa <-")
        print("1. Visualizar Lista de substituições")
        print("2. Processar UM arquivo .prpt")
        print("3. Processar TODOS os .prpt de um diretório")
        print("4. Processar TODOS os .kjb e .ktr de um diretório")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")
        if   opcao == '0':
            print("\n=========================================================")
            print("\nEste programa serve para fazer edição recursiva de arquivos")
            print("do tipo .prpt, .kjb e .ktr.")
            print("\nEX: Caso tenha alguma mudança de parametros de conexão")
            print("nomes schemas, tabelas, colunas ou qualquer estrutura.")
            print("O Script abre os arquivos e edita seguindo a lógica:")
            print("nome_antigo => nome_novo")
            print("\nBasta adicionar esta estrutura no arquivo substituicoes.txt")
            print("salvar e executar o programa, evitando assim edição manual")
            print("para cada .prpt, .kjb e .ktr do projeto")

        elif opcao == '1':
            mostrar_substituicoes(arquivo_substituicoes)
        elif opcao == '2':
            caminho = input("Digite o caminho completo do arquivo .prpt: ").strip()
            if caminho.endswith(".prpt") and os.path.exists(caminho):
                processar_prpt(caminho, arquivo_substituicoes)
            else:
                print("[ERRO] Caminho inválido ou arquivo não encontrado.")
        elif opcao == '3':
            caminho_diretorio = input("Digite o caminho do diretório com arquivos .prpt: ").strip()
            processar_diretorio(caminho_diretorio, arquivo_substituicoes)
        elif opcao == '4':
            caminho_diretorio = input("Digite o caminho do diretório com arquivos .kjb/.ktr: ").strip()
            processar_kjb_ktr(caminho_diretorio, arquivo_substituicoes)
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("[ERRO] Opção inválida. Tente novamente.")

# =======================================================
# Execução principal
# =======================================================
if __name__ == "__main__":
    menu_principal()
