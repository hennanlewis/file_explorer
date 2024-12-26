import os
from typing import List, Optional
from collections import Counter
from .file_reader import LeitorArquivo
from .analyzer import TextoAnalyzer


class ProcessadorTexto:
    """Classe para gerenciar arquivos e processar textos."""

    def __init__(self, pasta_textos: str, leitor_arquivo: LeitorArquivo) -> None:
        self.pasta_textos: str = pasta_textos
        self.leitor_arquivo: LeitorArquivo = leitor_arquivo

    def carregar_itens_removiveis(self, caminho_arquivo: str) -> List[str]:
        """Carrega uma lista de itens removíveis de um arquivo."""
        if not caminho_arquivo or not os.path.exists(caminho_arquivo):
            return []

        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            return [linha.strip() for linha in arquivo if linha.strip()]

    def processar_arquivo(self, caminho_arquivo: str, tipo: str, itens_removiveis: Optional[List[str]] = None) -> None:
        """Processa um único arquivo."""
        texto = self.leitor_arquivo.carregar(caminho_arquivo)
        analyzer = TextoAnalyzer(texto)
        contagem = analyzer.contar_palavras(tipo)

        itens_removiveis = itens_removiveis or []
        contagem_filtrada = TextoAnalyzer.filtrar_contagem(contagem, itens_removiveis)

        pasta_resultado = os.path.join(os.path.dirname(caminho_arquivo), "resultado")
        os.makedirs(pasta_resultado, exist_ok=True)

        nome_arquivo = os.path.basename(caminho_arquivo)
        caminho_resultado = os.path.join(pasta_resultado, f"resultado_{tipo}_{nome_arquivo}")
        self.leitor_arquivo.salvar(contagem_filtrada, caminho_resultado)
        print(f"Análise concluída para '{nome_arquivo}'.")

    def processar_pasta(self, tipo: str, consolidar: bool = True, itens_removiveis: Optional[List[str]] = None) -> None:
        """Processa todos os arquivos na pasta."""
        arquivos_txt = [
            os.path.join(self.pasta_textos, f) for f in os.listdir(self.pasta_textos)
            if f.endswith(('.txt', '.ass', '.srt'))
        ]

        if not arquivos_txt:
            print("Nenhum arquivo suportado encontrado na pasta.")
            return

        contador_total = Counter()

        for caminho_arquivo in arquivos_txt:
            print(f"Analisando arquivo: {os.path.basename(caminho_arquivo)}")
            texto = self.leitor_arquivo.carregar(caminho_arquivo)
            analyzer = TextoAnalyzer(texto)

            contagem = analyzer.contar_palavras(tipo)

            contagem_filtrada = TextoAnalyzer.filtrar_contagem(contagem, itens_removiveis or [])

            pasta_resultado = os.path.join(os.path.dirname(caminho_arquivo), "resultado")
            os.makedirs(pasta_resultado, exist_ok=True)

            nome_arquivo = os.path.basename(caminho_arquivo)
            caminho_resultado = os.path.join(pasta_resultado, f"resultado_{tipo}_{nome_arquivo}")
            self.leitor_arquivo.salvar(contagem_filtrada, caminho_resultado)

            if consolidar:
                contador_total.update(contagem)

        if consolidar:
            contagem_filtrada = TextoAnalyzer.filtrar_contagem(contador_total, itens_removiveis or [])
            caminho_resultado_consolidado = os.path.join(
                os.path.dirname(arquivos_txt[0]), "resultado", f"resultado_{tipo}_consolidado.txt"
            )
            self.leitor_arquivo.salvar(contagem_filtrada, caminho_resultado_consolidado)
            print(f"Resultado consolidado salvo em: {caminho_resultado_consolidado}")
