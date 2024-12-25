from collections import Counter
from janome.tokenizer import Tokenizer
import os
import re


class TextoAnalyzer:
    """Classe para analisar textos e contar palavras."""

    def __init__(self, texto):
        self.texto = self._limpar_texto(texto).lower()

    def _limpar_texto(self, texto):
        """Remove pontuações do texto."""
        texto = re.sub(r"[^\w\s]", "", texto)
        texto = re.sub(r"[。、「」『』]", "", texto)
        return texto

    def _filtrar_numeros(self, palavras, incluir_numeros):
        """Filtra números da lista de palavras, dependendo da flag `incluir_numeros`."""
        if not incluir_numeros:
            return [p for p in palavras if not p.isdigit()]
        return palavras

    def contar_palavras_japones(self, incluir_numeros=False):
        """Conta palavras em japonês usando Janome, com opção de incluir ou não números."""
        tokenizer = Tokenizer()
        palavras = [token.surface for token in tokenizer.tokenize(self.texto)]
        palavras_filtradas = self._filtrar_numeros(palavras, incluir_numeros)
        return Counter(palavras_filtradas)

    def contar_palavras_ocidentais(self, incluir_numeros=False):
        """Conta palavras separadas por espaços, com opção de incluir ou não números."""
        palavras = self.texto.split()
        palavras_filtradas = self._filtrar_numeros(palavras, incluir_numeros)
        return Counter(palavras_filtradas)

    def contar_palavras(self, tipo, incluir_numeros=False):
        """Retorna a contagem de palavras de acordo com o tipo especificado e flag de incluir números."""
        if tipo == "japones":
            return self.contar_palavras_japones(incluir_numeros)
        elif tipo == "ocidental":
            return self.contar_palavras_ocidentais(incluir_numeros)
        else:
            raise ValueError("Tipo inválido. Use 'japones' ou 'ocidental'.")

    @staticmethod
    def filtrar_contagem(contagem, itens_removiveis):
        """Filtra palavras removendo itens especificados e ignora palavras vazias."""
        itens_removiveis = set(itens_removiveis)
        return [
            (palavra, freq)
            for palavra, freq in contagem.items()
            if palavra and palavra.strip() and palavra not in itens_removiveis
        ]


class ProcessadorTexto:
    """Classe para gerenciar arquivos e processar textos."""

    def __init__(self, pasta_textos):
        self.pasta_textos = pasta_textos

    def carregar_texto(self, caminho_arquivo):
        """Carrega o texto de um arquivo."""
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            return arquivo.read()

    def salvar_resultados(self, resultados, caminho_arquivo):
        """Salva os resultados em um arquivo, ordenados por frequência decrescente."""
        resultados_ordenados = sorted(resultados, key=lambda x: x[1], reverse=True)
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            for palavra, freq in resultados_ordenados:
                arquivo.write(f"{palavra}: {freq}\n")

    def carregar_itens_removiveis(self, caminho_arquivo):
        """Carrega uma lista de itens removíveis de um arquivo."""
        if not caminho_arquivo or not os.path.exists(caminho_arquivo):
            return []

        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            return [linha.strip() for linha in arquivo if linha.strip()]

    def processar_arquivo(self, caminho_arquivo, tipo, itens_removiveis=None):
        """Processa um único arquivo."""
        texto = self.carregar_texto(caminho_arquivo)
        analyzer = TextoAnalyzer(texto)

        contagem = analyzer.contar_palavras(tipo)

        itens_removiveis = itens_removiveis or []
        contagem_filtrada = TextoAnalyzer.filtrar_contagem(contagem, itens_removiveis)

        pasta_resultado = os.path.join(os.path.dirname(caminho_arquivo), "resultado")
        os.makedirs(pasta_resultado, exist_ok=True)

        nome_arquivo = os.path.basename(caminho_arquivo)
        caminho_resultado = os.path.join(pasta_resultado, f"resultado_{tipo}_{nome_arquivo}")
        self.salvar_resultados(contagem_filtrada, caminho_resultado)
        print(f"Análise concluída para '{nome_arquivo}'.")

    def processar_pasta(self, tipo, consolidar=True, itens_removiveis=None):
        """Processa todos os arquivos na pasta."""
        arquivos_txt = [
            os.path.join(self.pasta_textos, f) for f in os.listdir(self.pasta_textos) if f.endswith('.txt')
        ]

        if not arquivos_txt:
            print("Nenhum arquivo .txt encontrado na pasta.")
            return

        contador_total = Counter()

        for caminho_arquivo in arquivos_txt:
            print(f"Analisando arquivo: {os.path.basename(caminho_arquivo)}")
            texto = self.carregar_texto(caminho_arquivo)
            analyzer = TextoAnalyzer(texto)

            contagem = analyzer.contar_palavras(tipo)

            contagem_filtrada = TextoAnalyzer.filtrar_contagem(contagem, itens_removiveis or [])

            pasta_resultado = os.path.join(os.path.dirname(caminho_arquivo), "resultado")
            os.makedirs(pasta_resultado, exist_ok=True)

            nome_arquivo = os.path.basename(caminho_arquivo)
            caminho_resultado = os.path.join(pasta_resultado, f"resultado_{tipo}_{nome_arquivo}")
            self.salvar_resultados(contagem_filtrada, caminho_resultado)

            if consolidar:
                contador_total.update(contagem)

        if consolidar:
            contagem_filtrada = TextoAnalyzer.filtrar_contagem(contador_total, itens_removiveis or [])
            caminho_resultado_consolidado = os.path.join(
                os.path.dirname(arquivos_txt[0]), "resultado", f"resultado_{tipo}_consolidado.txt"
            )
            self.salvar_resultados(contagem_filtrada, caminho_resultado_consolidado)
            print(f"Resultado consolidado salvo em: {caminho_resultado_consolidado}")


def main():
    diretorio_atual = os.path.dirname(__file__)
    pasta_textos = os.path.join(diretorio_atual, r"textos")
    caminho_itens_removiveis = os.path.join(diretorio_atual, "palavras_excluidas.txt")

    processador = ProcessadorTexto(pasta_textos)

    print("Escolha uma opção:")
    print("1. Processar um arquivo específico.")
    print("2. Processar todos os arquivos e gerar resultados individuais e consolidados.")

    opcao = input("Digite 1 ou 2: ").strip()

    tipo = input("Digite o tipo de análise ('japones' ou 'ocidental'): ").strip()
    itens_removiveis = processador.carregar_itens_removiveis(caminho_itens_removiveis)

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
