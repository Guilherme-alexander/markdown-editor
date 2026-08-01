# 📝 Markdown Editor

Um editor de Markdown com **preview em tempo real** estilo GitHub, construído em Python com PyQt5. Interface com tema escuro por padrão, suporte a imagens locais e remotas, listas de tarefas e exportação para HTML.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## ✨ Funcionalidades

- **Editor com preview em tempo real** — visualize o resultado do Markdown enquanto digita, lado a lado com o editor.
- **Estilo GitHub** — CSS cuidadosamente ajustado para reproduzir a aparência do GitHub, tanto no modo claro quanto no escuro.
- **Tema claro/escuro** — alterne com um clique ou atalho de teclado (dark mode como padrão).
- **Listas de tarefas (checkboxes)** — suporte a `- [ ]` e `- [x]` renderizados como checkboxes interativos visualmente.
- **Suporte completo a imagens**:
  - Conversão automática de links do GitHub (`blob`) para `raw.githubusercontent.com`.
  - Resolução de caminhos de imagem locais (relativos e absolutos) com base no diretório do arquivo aberto.
  - Fallback gracioso quando a imagem não pode ser carregada.
- **Exportação para HTML** — gera um arquivo `.html` autocontido, pronto para compartilhar ou publicar.
- **Barra de ferramentas e menus completos** — atalhos rápidos para negrito, itálico, código, links e imagens.
- **Atalhos de teclado** — `Ctrl+N`, `Ctrl+O`, `Ctrl+S`, `Ctrl+Shift+S`, `Ctrl+P` (alternar preview), `Ctrl+T` (alternar tema), entre outros.
- **Proteção contra perda de dados** — aviso para salvar alterações antes de criar um novo arquivo, abrir outro ou fechar o aplicativo.

## 🖥️ Tecnologias

- [Python 3](https://www.python.org/)
- [PyQt5](https://pypi.org/project/PyQt5/) — interface gráfica
- [PyQtWebEngine](https://pypi.org/project/PyQtWebEngine/) — renderização do preview em HTML
- [Python-Markdown](https://python-markdown.github.io/) — conversão de Markdown para HTML

## 📦 Instalação

### Pré-requisitos

- Python 3.8^

### Passos

```bash
# Clone o repositório
git clone https://github.com/Guilherme-alexander/markdown-editor.git
cd markdown-editor

# Instale as dependências
pip install -r requirements.txt
```

### Criar ambiente virtual (Opcional)
```bash
# crie um ambiente virtual
python -m venv venv

source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### Requirements

```txt
PyQt5
PyQtWebEngine
markdown
```

## ▶️ Uso

```bash
python markdown_editor.py
```

1. Crie um novo arquivo (`Ctrl+N`) ou abra um existente (`Ctrl+O`).
2. Digite ou cole o conteúdo Markdown no painel esquerdo.
3. Acompanhe o preview renderizado em tempo real no painel direito.
4. Salve (`Ctrl+S`) ou exporte o resultado como HTML pelo menu **Arquivo → Exportar como HTML**.

## ⌨️ Atalhos de teclado

| Atalho             | Ação                          |
|---------------------|-------------------------------|
| `Ctrl+N`            | Novo arquivo                  |
| `Ctrl+O`            | Abrir arquivo                 |
| `Ctrl+S`            | Salvar                        |
| `Ctrl+Shift+S`      | Salvar como                   |
| `Ctrl+P`            | Alternar preview              |
| `Ctrl+T`            | Alternar tema claro/escuro    |
| `Ctrl+Z` / `Ctrl+Y` | Desfazer / Refazer            |
| `Ctrl+X/C/V`        | Recortar / Copiar / Colar     |
| `Ctrl+A`            | Selecionar tudo                |

## 📁 Estrutura do projeto

```
markdown-editor/
├── markdown_editor.py   # Aplicação principal
├── requirements.txt     # Dependências do projeto
├── markdown.ico         # Icone markdown
└── README.md            # Este arquivo
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request* com melhorias, correções de bugs ou novas funcionalidades.

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Faça commit das suas alterações
4. Faça push para a branch
5. Abra um Pull Request

## 📄 Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---
Desenvolvido com ❤ e ☕ usando Claude code, Python e PyQt5.
