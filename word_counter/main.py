import os
from word_counter.processor import ProcessadorTexto
from word_counter.file_reader import LeitorArquivo


def main():
    diretorio_atual = os.path.dirname(__file__)
    pasta_textos = os.path.join(diretorio_atual, "textos")
    caminho_itens_removiveis = os.path.join(diretorio_atual, "palavras_excluidas.txt")

    leitor_arquivo = LeitorArquivo()
    processador = ProcessadorTexto(pasta_textos, leitor_arquivo)

    print("Escolha uma opção:")
    print("1. Processar um arquivo específico.")
    print("2. Processar todos os arquivos e gerar resultados individuais e consolidados.")

    opcao = input("Digite 1 ou 2: ").strip()

    tipo = input("Digite o tipo de análise ('japones' ou 'ocidental'): ").strip()
    itens_removiveis = leitor_arquivo.carregar_itens_removiveis(caminho_itens_removiveis)

    if opcao == "1":
        arquivos_txt = [
            f for f in os.listdir(pasta_textos) if f.endswith(".txt")
        ]

        if not arquivos_txt:
            print("Nenhum arquivo .txt encontrado na pasta.")
            return

        print("Arquivos disponíveis:")
        for i, arquivo in enumerate(arquivos_txt, start=1):
            print(f"{i}. {arquivo}")

        escolha = int(input("Digite o número do arquivo que deseja processar: ").strip())
        if 1 <= escolha <= len(arquivos_txt):
            caminho_arquivo = os.path.join(pasta_textos, arquivos_txt[escolha - 1])
            processador.processar_arquivo(caminho_arquivo, tipo, itens_removiveis)
        else:
            print("Escolha inválida.")
    elif opcao == "2":
        processador.processar_pasta(tipo, consolidar=True, itens_removiveis=itens_removiveis)
    else:
        print("Opção inválida.")


if __name__ == "__main__":
    main()
