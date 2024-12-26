import os
from typing import List, Tuple


class LeitorArquivo:
    """Classe para leitura de arquivos."""

    @staticmethod
    def carregar(caminho_arquivo: str) -> str:
        """Carrega o conteúdo de um arquivo de texto."""
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            return arquivo.read()

    @staticmethod
    def salvar(resultados: List[Tuple[str, int]], caminho_arquivo: str) -> None:
        """Salva os resultados em um arquivo, ordenados por frequência decrescente."""
        resultados_ordenados = sorted(resultados, key=lambda x: x[1], reverse=True)
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            for palavra, freq in resultados_ordenados:
                arquivo.write(f"{palavra}: {freq}\n")

    @staticmethod
    def carregar_itens_removiveis(caminho_arquivo: str) -> List[str]:
        """Carrega uma lista de itens removíveis de um arquivo."""
        if not caminho_arquivo or not os.path.exists(caminho_arquivo):
            return []

        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            return [linha.strip() for linha in arquivo if linha.strip()]
