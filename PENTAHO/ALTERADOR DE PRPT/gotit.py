import os
import zipfile
import shutil


def criar_arquivo_exemplo(arquivo_txt):
    exemplo = (
        "jdbc:postgresql://localhost:5432/db_antigo => jdbc:postgresql://localhost:5432/db_novo\n"
        "schema_antigo => schema_novo"
    )
    with open(arquivo_txt, 'w', encoding='utf-8') as f:
        f.write(exemplo)
    print(f"[INFO] Arquivo '{arquivo_txt}' não encontrado. Um exemplo foi criado.\n")

def ler_substituicoes(arquivo_txt):
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
    print(f"\n📄 Conteúdo de '{arquivo_txt}':\n")
    try:
        with open(arquivo_txt, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            print(conteudo)
    except FileNotFoundError:
        print("[ERRO] Arquivo de substituições não encontrado.")
    input("\nPressione ENTER para voltar ao menu...")

def substituir_em_arquivo(caminho_arquivo, substituicoes):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        for antiga, nova in substituicoes:
            conteudo = conteudo.replace(antiga, nova)
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
    except:
        pass  # Ignora arquivos que não podem ser lidos como texto

def processar_diretorio(caminho_diretorio, arquivo_substituicoes):
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

    print(f"\n[INFO] {len(arquivos_prpt)} arquivos .prpt encontrados.\n")

    for caminho in arquivos_prpt:
        print(f"🔧 Processando: {caminho}")
        processar_prpt(caminho, arquivo_substituicoes)

def processar_prpt(caminho_prpt, arquivo_substituicoes):
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
    print(f"[✔] Relatório processado com sucesso!")
    print(f"Arquivo salvo como: {novo_prpt}\n")
    
def menu_principal():
    arquivo_substituicoes = "substituicoes.txt"

    if not os.path.exists(arquivo_substituicoes):
        criar_arquivo_exemplo(arquivo_substituicoes)

    while True:
        print("\n====== MENU ======")
        print("1. Visualizar Lista de substituições")
        print("2. Processar arquivo .prpt")
        print("3. Processar todos os .prpt de um diretório")
        print("4. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
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
            print("Saindo...")
            break
        else:
            print("[ERRO] Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()
