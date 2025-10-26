# 🌐 Explorador de Arquivos em Rede

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Um explorador de arquivos web que permite acessar e visualizar arquivos do seu computador remotamente via navegador. Perfeito para assistir filmes, ouvir música ou transferir arquivos entre dispositivos na mesma rede.

## 🚀 Funcionalidades

- **📁 Navegação Remota**: Acesse arquivos do seu PC via celular ou outros dispositivos
- **🎥 Visualização Direta**: Veja vídeos, imagens, textos e áudios diretamente no navegador
- **🔒 Autenticação Segura**: Sistema de autenticação com hash SHA-256 e timeout de sessão volátil
- **🛡️ Proteção contra Ataques**: Rate limiting e controle de tentativas de login
- **🌐 Detecção Inteligente**: Reconhecimento automático de acesso local vs remoto
- **📱 Interface Responsiva**: Funciona perfeitamente em desktop e mobile
- **🎨 Ícones Personalizados**: Diferentes ícones para cada tipo de arquivo

## 🏗️ Estrutura do Projeto

```bash
📁file_explorer/
├── 📁 api/             # Rotas da API
├── 📁 config/          # Configurações e mapeamentos
├── 📁 core/            # Núcleo da aplicação
│   ├── 📁 logging/     # Sistema de logs
│   ├── 📁 server/      # Estado do servidor
│   ├── 📁 services/    # Serviços principais
│   └── 📁 utils/       # Utilitários (rede, sessão, etc.)
├── 📁 modules/         # Módulos da aplicação
│   ├── 📁 auth/        # Autenticação
│   └── 📁 files/       # Gerenciamento de arquivos
├── 📁 static/          # Arquivos estáticos
│   ├── 📁 css/         # Estilos
│   └── 📁 icons/       # Ícones personalizados
├── 📁 templates/       # Templates HTML
├── 📄 app.py           # Aplicação principal
└── 📄 main.py          # Ponto de entrada
```

## ⚙️ Configuração de Segurança

O sistema agora inclui configurações de segurança avançadas:

- **SESSION_TIMEOUT**: Tempo máximo de sessão (padrão: 3600s)
- **MAX_LOGIN_ATTEMPTS**: Tentativas de login permitidas (padrão: 5)
- **SECRET_KEY**: Gerada automaticamente para segurança das sessões
- **Hash SHA-256**: Senhas são armazenadas com hash seguro

Para detalhes completos sobre as funcionalidades de segurança, consulte [SECURITY.md](doc/SECURITY.md)

## 🛠️ Instalação e Uso

### Pré-requisitos
- Python 3.13 ou superior
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (gerenciador de pacotes)

### Executando o Projeto

1. **Clone o repositório**:
```bash
git clone https://github.com/hennanlewis/file_explorer
cd file_explorer
```

2. **Instale as dependências:**
```bash
uv sync
```

3. **Execute o servidor:**
```bash
uv run python main.py
```

4. **Acesse no navegador:**
```bash
# Host: 
http://localhost:8080 # para configurar
# Cliente:
http://[IP-DO-HOST]:8080 # para logar
```

## 📸 Como Usar

1. **Configuração do Host**:
    - Acesse `http://localhost:8080` (reconhecimento automático como host)
    - Defina o caminho da pasta a ser compartilhada
    - Configure uma senha de acesso
2. **Acesso do Cliente**:
    - Acesse `http://[IP-DO-SERVIDOR]:8080` de qualquer dispositivo
    - Insira a senha configurada
    - Navegue pelos arquivos

3. **Visualização**:
    - **Vídeos/Audios**: Reproduza diretamente no navegador
    - **Imagens**: Visualize em tela cheia
    - **Textos**: Leia arquivos .txt, .pdf, etc.
    - **Outros**: Download direto


## 🎯 Tipos de Arquivo Suportados
| Tipo                    | Visualização   | Ícone                                                                       |
| ----------------------- | -------------- | --------------------------------------------------------------------------- |
| 📁 Pastas               | Próprio navegador | <img src="file_explorer/static/icons/folder.png" width="32" height="32" alt="Pastas">   |
| 📄 Texto                | Próprio navegador | <img src="file_explorer/static/icons/text-file.png" width="32" height="32" alt="Texto">   |
| 🖼️ Imagem               | Próprio navegador | <img src="file_explorer/static/icons/image-file.png" width="32" height="32" alt="Imagem"> |
| 🎵 Áudio                | Próprio navegador | <img src="file_explorer/static/icons/audio-file.png" width="32" height="32" alt="Áudio">  |
| 📹 Vídeo                | Próprio navegador | <img src="file_explorer/static/icons/video-file.png" width="32" height="32" alt="Vídeo">  |
| 📊 PDF                  | Próprio navegador | <img src="file_explorer/static/icons/svg/pdf-file.svg" width="32" height="32" alt="PDF">  |
| 📦 Outros | Arquivos apenas para baixar     | <img src="file_explorer/static/icons/file.png" width="32" height="32" alt="Arquivos mais gerais">      |

Existem vários outros ícones para vários outros arquivos, veja a [pasta com todos](file_explorer/static/icons/).


## 🔧 Desenvolvimento

### Estrutura de Módulos
- **`core/`**: Lógica central e serviços
- **`modules/`**: Funcionalidades específicas
- **`api/`**: Endpoints da aplicação
- **`static/`**: Recursos frontend

### Adicionando Novos Ícones

Adicione novos ícones em `file_explorer/static/icons/` e atualize `config/mime_map.json`

## 🤝 Contribuindo
Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests
