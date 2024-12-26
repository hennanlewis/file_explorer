from collections import Counter
from janome.tokenizer import Tokenizer
from typing import List, Tuple
import re

class TextoAnalyzer:
    """Classe para analisar textos e contar palavras."""

    def __init__(self, texto: str) -> None:
        self.texto: str = self._limpar_texto(texto.lower())

    def _limpar_texto(self, texto: str) -> str:
        """Remove pontuações do texto."""
        texto = re.sub(r"[^\w\s]", "", texto) # Para remover pontuações ocidentais comuns
        texto = re.sub(r"[。、「」『』]", "", texto) # Para remover pontuações específicas japonesas
        texto = re.sub(r"dialogue \d+\w+\d+", "", texto) # Para remover inconsistência em arquivos .srt
        texto = re.sub(r"\b\w*\d+\w*\b", "", texto) # Palavras com números que sobraram nos arquivos de legenda
        return texto

    def _filtrar_numeros(self, palavras: List[str], incluir_numeros: bool) -> List[str]:
        """Filtra números da lista de palavras, dependendo da flag `incluir_numeros`."""
        if not incluir_numeros:
            return [p for p in palavras if not p.isdigit()]
        return palavras

    def contar_palavras(self, tipo: str, incluir_numeros: bool = False) -> Counter:
        """Retorna a contagem de palavras de acordo com o tipo especificado e flag de incluir números."""
        if tipo == "japones":
            return self.contar_palavras_japones(incluir_numeros)
        elif tipo == "ocidental":
            return self.contar_palavras_ocidentais(incluir_numeros)
        else:
            raise ValueError("Tipo inválido. Use 'japones' ou 'ocidental'.")

    def contar_palavras_japones(self, incluir_numeros: bool) -> Counter:
        """Conta palavras em japonês usando Janome."""
        tokenizer = Tokenizer()
        palavras = [token.surface for token in tokenizer.tokenize(self.texto)]
        return Counter(self._filtrar_numeros(palavras, incluir_numeros))

    def contar_palavras_ocidentais(self, incluir_numeros: bool) -> Counter:
        """Conta palavras ocidentais separadas por espaços."""
        palavras = self.texto.split()
        return Counter(self._filtrar_numeros(palavras, incluir_numeros))

    @staticmethod
    def filtrar_contagem(contagem: Counter, itens_removiveis: List[str]) -> List[Tuple[str, int]]:
        """Filtra palavras removendo itens especificados e ignora palavras vazias."""
        itens_removiveis = set(itens_removiveis)
        return [(palavra, freq) for palavra, freq in contagem.items() if palavra and palavra.strip() and palavra not in itens_removiveis]

