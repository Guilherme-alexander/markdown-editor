# Authot: Guilherme-alexander
# Version 2.0.0
# Github: https://github.com/Guilherme-alexander/markdown-editor
import sys
import os
import re
import markdown
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QFileDialog, QMessageBox, QLabel, QSplitter, QMenuBar, QMenu, QToolBar, QAction, QStatusBar)
from PyQt5.QtCore import Qt, QFileSystemWatcher, QUrl
from PyQt5.QtGui import QFont, QTextCursor, QKeySequence, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings

class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.is_dark_mode = True  # Dark mode como default
        self.init_ui()
        self.init_shortcuts()
        
    def init_ui(self):
        # Configuração da janela principal
        self.setWindowTitle("Markdown Editor") # Visualizador e Editor
        self.setGeometry(100, 100, 1200, 700)
        
        # Configurar perfil WebEngine para permitir imagens
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
        
        # Criar editor e preview PRIMEIRO
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Courier New", 11))
        self.editor.setPlaceholderText("Digite seu conteúdo Markdown aqui...")
        self.editor.textChanged.connect(self.update_preview)
        
        self.preview = QWebEngineView()
        # Permitir carregar imagens
        self.preview.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.preview.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        self.preview.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, False)

        # Preview do Markdown (setHtml)
        self.preview.setHtml("""<h2 style="color: #666; text-align: center; margin-top: 50px;">
                              Preview do Markdown</h2>
                              <p style="text-align: center; color: #999;">O conteúdo aparecerá aqui</p>""")
        
        # DEPOIS criar menu e toolbar
        self.create_menu_bar()
        self.create_toolbar()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Splitter para dividir editor e visualização
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview)
        splitter.setSizes([400, 600]) # <-- SIZE (X Y)
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Pronto")
        
        # Aplicar estilo inicial (dark mode)
        self.apply_style()
        self.update_preview()
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # Menu Arquivo
        file_menu = menubar.addMenu("&Arquivo")
        
        new_action = QAction("&Novo", self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Abrir", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Salvar", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Salvar &Como...", self)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_html_action = QAction("Exportar como &HTML", self)
        export_html_action.triggered.connect(self.export_html)
        file_menu.addAction(export_html_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("&Sair", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Editar
        edit_menu = menubar.addMenu("&Editar")
        
        undo_action = QAction("&Desfazer", self)
        undo_action.setShortcut(QKeySequence("Ctrl+Z"))
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("&Refazer", self)
        redo_action.setShortcut(QKeySequence("Ctrl+Y"))
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("Recortar", self)
        cut_action.setShortcut(QKeySequence("Ctrl+X"))
        cut_action.triggered.connect(self.editor.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("Copiar", self)
        copy_action.setShortcut(QKeySequence("Ctrl+C"))
        copy_action.triggered.connect(self.editor.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Colar", self)
        paste_action.setShortcut(QKeySequence("Ctrl+V"))
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        select_all_action = QAction("Selecionar &Tudo", self)
        select_all_action.setShortcut(QKeySequence("Ctrl+A"))
        select_all_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_all_action)
        
        # Menu Visualização
        view_menu = menubar.addMenu("&Visualização")
        
        toggle_preview_action = QAction("Alternar &Preview", self)
        toggle_preview_action.setShortcut(QKeySequence("Ctrl+P"))
        toggle_preview_action.triggered.connect(self.toggle_preview)
        view_menu.addAction(toggle_preview_action)
        
        toggle_theme_action = QAction("Alternar &Tema Escuro", self)
        toggle_theme_action.setShortcut(QKeySequence("Ctrl+T"))
        toggle_theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(toggle_theme_action)
        
        # Menu Ajuda
        help_menu = menubar.addMenu("&Ajuda")
        
        about_action = QAction("&Sobre", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        toolbar = self.addToolBar("Ferramentas")
        toolbar.setMovable(False)
        
        # Botões
        new_btn = QPushButton("📄 Novo")
        new_btn.clicked.connect(self.new_file)
        toolbar.addWidget(new_btn)
        
        open_btn = QPushButton("📂 Abrir")
        open_btn.clicked.connect(self.open_file)
        toolbar.addWidget(open_btn)
        
        save_btn = QPushButton("💾 Salvar")
        save_btn.clicked.connect(self.save_file)
        toolbar.addWidget(save_btn)
        
        toolbar.addSeparator()
        
        # Botões de formatação rápida
        bold_btn = QPushButton("**B**")
        bold_btn.setToolTip("Negrito (Ctrl+B)")
        bold_btn.clicked.connect(lambda: self.insert_format("**", "**"))
        toolbar.addWidget(bold_btn)
        
        italic_btn = QPushButton("*I*")
        italic_btn.setToolTip("Itálico (Ctrl+I)")
        italic_btn.clicked.connect(lambda: self.insert_format("*", "*"))
        toolbar.addWidget(italic_btn)
        
        code_btn = QPushButton("`<>`")
        code_btn.setToolTip("Código inline")
        code_btn.clicked.connect(lambda: self.insert_format("`", "`"))
        toolbar.addWidget(code_btn)
        
        link_btn = QPushButton("🔗 Link")
        link_btn.setToolTip("Inserir link")
        link_btn.clicked.connect(self.insert_link)
        toolbar.addWidget(link_btn)
        
        image_btn = QPushButton("🖼️ Imagem")
        image_btn.setToolTip("Inserir imagem")
        image_btn.clicked.connect(self.insert_image)
        toolbar.addWidget(image_btn)
        
        toolbar.addSeparator()
        
        # Botão de tema
        theme_btn = QPushButton("🌙 Tema")
        theme_btn.clicked.connect(self.toggle_theme)
        toolbar.addWidget(theme_btn)
        
    def init_shortcuts(self):
        # Atalhos adicionais
        self.editor.setAcceptRichText(False)
        
    def insert_format(self, prefix, suffix):
        """Insere formatação no texto selecionado"""
        cursor = self.editor.textCursor()
        selected_text = cursor.selectedText()
        
        if selected_text:
            cursor.insertText(f"{prefix}{selected_text}{suffix}")
        else:
            cursor.insertText(f"{prefix}{suffix}")
            # Move cursor para dentro da formatação
            cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, len(suffix))
            self.editor.setTextCursor(cursor)
        
        self.editor.setFocus()
        
    def insert_link(self):
        """Insere um link markdown"""
        cursor = self.editor.textCursor()
        cursor.insertText("[Texto do link](url)")
        # Posiciona cursor no "Texto do link"
        cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 4)
        self.editor.setTextCursor(cursor)
        self.editor.setFocus()
        
    def insert_image(self):
        """Insere uma imagem markdown"""
        cursor = self.editor.textCursor()
        cursor.insertText("![Texto alternativo](url-da-imagem)")
        # Posiciona cursor no "Texto alternativo"
        cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 17)
        self.editor.setTextCursor(cursor)
        self.editor.setFocus()
        
    def new_file(self):
        if self.check_save():
            self.editor.clear()
            self.current_file = None
            self.setWindowTitle("Markdown Editor - Novo arquivo")
            self.statusBar.showMessage("Novo arquivo criado")
            self.update_preview()
            
    def open_file(self):
        if not self.check_save():
            return
            
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Abrir Arquivo", "", 
            "Arquivos Markdown (*.md *.markdown);;Todos os Arquivos (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.editor.setPlainText(content)
                    self.current_file = file_path
                    self.setWindowTitle(f"Markdown Editor - {os.path.basename(file_path)}")
                    self.statusBar.showMessage(f"Arquivo aberto: {file_path}")
                    self.update_preview()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível abrir o arquivo:\n{str(e)}")
                
    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(self.editor.toPlainText())
                    self.statusBar.showMessage(f"Arquivo salvo: {self.current_file}")
                    return True
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível salvar:\n{str(e)}")
                return False
        else:
            return self.save_file_as()
            
    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Salvar Arquivo Como", "", 
            "Arquivos Markdown (*.md *.markdown);;Todos os Arquivos (*.*)"
        )
        
        if file_path:
            if not file_path.endswith(('.md', '.markdown')):
                file_path += '.md'
            self.current_file = file_path
            self.setWindowTitle(f"Markdown Editor - {os.path.basename(file_path)}")
            return self.save_file()
        return False
        
    def check_save(self):
        """Verifica se precisa salvar antes de fechar/novo"""
        if self.editor.document().isModified():
            reply = QMessageBox.question(
                self, "Salvar Alterações",
                "O documento foi modificado. Deseja salvar as alterações?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            if reply == QMessageBox.Yes:
                return self.save_file()
            elif reply == QMessageBox.Cancel:
                return False
        return True
    
    def process_task_lists(self, html_content):
        """Processa listas de tarefas (checkboxes) no HTML"""
        # Padrão para encontrar listas de tarefas
        # - [x] item  ou  - [ ] item
        pattern = r'<li>\[([ x])\]\s*(.*?)</li>'
        
        def replace_checkbox(match):
            checked = match.group(1) == 'x'
            text = match.group(2)
            checkbox = f'<input type="checkbox" {"checked" if checked else ""} disabled> '
            return f'<li class="task-list-item">{checkbox}{text}</li>'
        
        # Substituir todas as ocorrências
        html_content = re.sub(pattern, replace_checkbox, html_content)
        
        # Adicionar classe para estilização
        html_content = html_content.replace('<ul>', '<ul class="task-list">')
        
        return html_content
    
    def fix_image_urls(self, html_content):
        """Converte URLs do GitHub para raw e corrige caminhos de imagem"""
        
        def convert_github_url(match):
            url = match.group(1)
            
            # Se for URL do GitHub (blob), converter para raw
            if 'github.com' in url and '/blob/' in url:
                # Converter https://github.com/user/repo/blob/branch/path/image.jpg
                # para https://raw.githubusercontent.com/user/repo/branch/path/image.jpg
                url = url.replace('github.com', 'raw.githubusercontent.com')
                url = url.replace('/blob/', '/')
                return f'<img src="{url}" alt="Imagem" style="max-width:100%;" />'
            
            # Se for URL do GitHub (raw), manter
            elif 'raw.githubusercontent.com' in url:
                return f'<img src="{url}" alt="Imagem" style="max-width:100%;" />'
            
            # Se for caminho local (relativo ou absoluto)
            elif not url.startswith(('http://', 'https://')):
                # Converter caminho relativo para absoluto baseado no diretório do arquivo
                if self.current_file:
                    base_dir = os.path.dirname(self.current_file)
                    local_path = os.path.join(base_dir, url)
                    if os.path.exists(local_path):
                        # Converter para URL file://
                        file_url = QUrl.fromLocalFile(local_path).toString()
                        return f'<img src="{file_url}" alt="Imagem" style="max-width:100%;" />'
                    else:
                        # Tentar caminho absoluto
                        if os.path.exists(url):
                            file_url = QUrl.fromLocalFile(url).toString()
                            return f'<img src="{file_url}" alt="Imagem" style="max-width:100%;" />'
            
            # Se não for possível, retornar a imagem com fallback
            return f'<img src="{url}" alt="Imagem" style="max-width:100%;" onerror="this.style.display=\'none\'" />'
        
        # Padrão para encontrar imagens markdown: ![alt](url)
        pattern = r'<img src="([^"]+)"'
        html_content = re.sub(pattern, convert_github_url, html_content)
        
        return html_content
        
    def update_preview(self):
        """Atualiza a visualização do Markdown com estilo GitHub"""
        try:
            markdown_text = self.editor.toPlainText()
            
            # GitHub CSS estilo
            if self.is_dark_mode:
                # Dark mode - estilo GitHub Dark
                css = """
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                        max-width: 900px;
                        margin: 40px auto;
                        padding: 32px;
                        line-height: 1.6;
                        background-color: #0d1117;
                        color: #c9d1d9;
                    }
                    h1, h2, h3, h4, h5, h6 {
                        margin-top: 24px;
                        margin-bottom: 16px;
                        font-weight: 600;
                        line-height: 1.25;
                        border-bottom: 1px solid #21262d;
                        padding-bottom: 0.3em;
                    }
                    h1 { font-size: 2em; }
                    h2 { font-size: 1.5em; }
                    h3 { font-size: 1.25em; }
                    h4 { font-size: 1em; }
                    h5 { font-size: 0.875em; }
                    h6 { font-size: 0.85em; color: #8b949e; }
                    p { margin-top: 0; margin-bottom: 16px; }
                    a { color: #58a6ff; text-decoration: none; }
                    a:hover { text-decoration: underline; }
                    code {
                        background-color: rgba(110,118,129,0.4);
                        padding: 0.2em 0.4em;
                        border-radius: 6px;
                        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
                        font-size: 85%;
                        color: #c9d1d9;
                    }
                    pre {
                        background-color: #161b22;
                        padding: 16px;
                        border-radius: 6px;
                        overflow-x: auto;
                        border: 1px solid #30363d;
                    }
                    pre code {
                        background-color: transparent;
                        padding: 0;
                        border-radius: 0;
                        font-size: 85%;
                        color: #c9d1d9;
                    }
                    blockquote {
                        border-left: 4px solid #30363d;
                        padding: 0 1em;
                        margin: 0 0 16px 0;
                        color: #8b949e;
                    }
                    table {
                        border-collapse: collapse;
                        width: 100%;
                        margin: 16px 0;
                    }
                    th, td {
                        border: 1px solid #30363d;
                        padding: 6px 13px;
                        text-align: left;
                    }
                    th {
                        background-color: #161b22;
                        font-weight: 600;
                    }
                    tr:nth-child(2n) {
                        background-color: #161b22;
                    }
                    img {
                        max-width: 100%;
                        background-color: #0d1117;
                        border-radius: 4px;
                        margin: 8px 0;
                    }
                    ul, ol {
                        padding-left: 2em;
                        margin-top: 0;
                        margin-bottom: 16px;
                    }
                    li {
                        margin-top: 0.25em;
                    }
                    li + li {
                        margin-top: 0.25em;
                    }
                    hr {
                        height: 0.25em;
                        padding: 0;
                        margin: 24px 0;
                        background-color: #21262d;
                        border: 0;
                    }
                    .task-list {
                        list-style-type: none;
                        padding-left: 0;
                    }
                    .task-list-item {
                        list-style-type: none;
                        margin: 0.25em 0;
                    }
                    .task-list-item input[type="checkbox"] {
                        margin: 0 0.5em 0.25em -1.6em;
                        vertical-align: middle;
                        accent-color: #58a6ff;
                        width: 16px;
                        height: 16px;
                        cursor: default;
                    }
                    .task-list-item input[type="checkbox"]:checked {
                        accent-color: #58a6ff;
                    }
                </style>
                """
            else:
                # Light mode - estilo GitHub
                css = """
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                        max-width: 900px;
                        margin: 40px auto;
                        padding: 32px;
                        line-height: 1.6;
                        background-color: #ffffff;
                        color: #24292f;
                    }
                    h1, h2, h3, h4, h5, h6 {
                        margin-top: 24px;
                        margin-bottom: 16px;
                        font-weight: 600;
                        line-height: 1.25;
                        border-bottom: 1px solid #d0d7de;
                        padding-bottom: 0.3em;
                    }
                    h1 { font-size: 2em; }
                    h2 { font-size: 1.5em; }
                    h3 { font-size: 1.25em; }
                    h4 { font-size: 1em; }
                    h5 { font-size: 0.875em; }
                    h6 { font-size: 0.85em; color: #57606a; }
                    p { margin-top: 0; margin-bottom: 16px; }
                    a { color: #0969da; text-decoration: none; }
                    a:hover { text-decoration: underline; }
                    code {
                        background-color: rgba(175,184,193,0.2);
                        padding: 0.2em 0.4em;
                        border-radius: 6px;
                        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
                        font-size: 85%;
                    }
                    pre {
                        background-color: #f6f8fa;
                        padding: 16px;
                        border-radius: 6px;
                        overflow-x: auto;
                        border: 1px solid #d0d7de;
                    }
                    pre code {
                        background-color: transparent;
                        padding: 0;
                        border-radius: 0;
                        font-size: 85%;
                    }
                    blockquote {
                        border-left: 4px solid #d0d7de;
                        padding: 0 1em;
                        margin: 0 0 16px 0;
                        color: #57606a;
                    }
                    table {
                        border-collapse: collapse;
                        width: 100%;
                        margin: 16px 0;
                    }
                    th, td {
                        border: 1px solid #d0d7de;
                        padding: 6px 13px;
                        text-align: left;
                    }
                    th {
                        background-color: #f6f8fa;
                        font-weight: 600;
                    }
                    tr:nth-child(2n) {
                        background-color: #f6f8fa;
                    }
                    img {
                        max-width: 100%;
                        background-color: #ffffff;
                        border-radius: 4px;
                        margin: 8px 0;
                    }
                    ul, ol {
                        padding-left: 2em;
                        margin-top: 0;
                        margin-bottom: 16px;
                    }
                    li {
                        margin-top: 0.25em;
                    }
                    li + li {
                        margin-top: 0.25em;
                    }
                    hr {
                        height: 0.25em;
                        padding: 0;
                        margin: 24px 0;
                        background-color: #d0d7de;
                        border: 0;
                    }
                    .task-list {
                        list-style-type: none;
                        padding-left: 0;
                    }
                    .task-list-item {
                        list-style-type: none;
                        margin: 0.25em 0;
                    }
                    .task-list-item input[type="checkbox"] {
                        margin: 0 0.5em 0.25em -1.6em;
                        vertical-align: middle;
                        accent-color: #0969da;
                        width: 16px;
                        height: 16px;
                        cursor: default;
                    }
                    .task-list-item input[type="checkbox"]:checked {
                        accent-color: #0969da;
                    }
                </style>
                """
            
            # Configurar extensões do Markdown (sem tasklist)
            extensions = [
                'extra', 
                'codehilite', 
                'tables', 
                'fenced_code'
            ]
            
            # Converter markdown para HTML
            html_content = markdown.markdown(
                markdown_text,
                extensions=extensions
            )
            
            # Processar listas de tarefas manualmente
            html_content = self.process_task_lists(html_content)
            
            # Corrigir URLs de imagens (GitHub e locais)
            html_content = self.fix_image_urls(html_content)
            
            # HTML completo
            # configs: lang="pt-br" or lang="us"
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                {css}
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            self.preview.setHtml(full_html)
            
        except Exception as e:
            self.preview.setHtml(f"<p style='color: red;'>Erro ao processar Markdown: {str(e)}</p>")
            
    def toggle_preview(self):
        """Alterna a visibilidade do preview"""
        if self.preview.isVisible():
            self.preview.hide()
            self.statusBar.showMessage("Preview oculto")
        else:
            self.preview.show()
            self.statusBar.showMessage("Preview visível")
            
    def toggle_theme(self):
        """Alterna entre tema claro e escuro"""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_style()
        self.update_preview()
        theme_name = "escuro" if self.is_dark_mode else "claro"
        self.statusBar.showMessage(f"Tema {theme_name} ativado")
        
    def apply_style(self):
        """Aplica o estilo atual (claro/escuro) - Dark mode como default"""
        if self.is_dark_mode:
            style = """
            QMainWindow {
                background-color: #0d1117;
            }
            QTextEdit {
                background-color: #0d1117;
                color: #c9d1d9;
                border: 1px solid #30363d;
                font-family: 'Courier New', monospace;
                selection-background-color: #264f78;
            }
            QMenuBar {
                background-color: #0d1117;
                color: #c9d1d9;
            }
            QMenuBar::item:selected {
                background-color: #161b22;
            }
            QMenu {
                background-color: #0d1117;
                color: #c9d1d9;
                border: 1px solid #30363d;
            }
            QMenu::item:selected {
                background-color: #161b22;
            }
            QPushButton {
                background-color: #21262d;
                color: #c9d1d9;
                border: 1px solid #30363d;
                padding: 5px 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #30363d;
            }
            QStatusBar {
                background-color: #0d1117;
                color: #c9d1d9;
            }
            QSplitter::handle {
                background-color: #30363d;
            }
            QScrollBar:vertical {
                background: #0d1117;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #30363d;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
            """
        else:
            style = """
            QMainWindow {
                background-color: #f6f8fa;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #24292f;
                border: 1px solid #d0d7de;
                font-family: 'Courier New', monospace;
                selection-background-color: #a8c8e4;
            }
            QMenuBar {
                background-color: #f6f8fa;
                color: #24292f;
            }
            QMenuBar::item:selected {
                background-color: #d0d7de;
            }
            QMenu {
                background-color: #ffffff;
                color: #24292f;
                border: 1px solid #d0d7de;
            }
            QMenu::item:selected {
                background-color: #d0d7de;
            }
            QPushButton {
                background-color: #f6f8fa;
                border: 1px solid #d0d7de;
                padding: 5px 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #d0d7de;
            }
            QStatusBar {
                background-color: #f6f8fa;
                color: #24292f;
            }
            QSplitter::handle {
                background-color: #d0d7de;
            }
            """
        
        self.setStyleSheet(style)
        
    def export_html(self):
        """Exporta o conteúdo como HTML"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exportar como HTML", "", "Arquivos HTML (*.html);;Todos os Arquivos (*.*)"
        )
        
        if file_path:
            if not file_path.endswith('.html'):
                file_path += '.html'
                
            try:
                markdown_text = self.editor.toPlainText()
                html_body = markdown.markdown(markdown_text, extensions=['extra', 'tables', 'fenced_code'])
                
                # Processar task lists na exportação
                html_body = self.process_task_lists(html_body)
                
                # CSS para exportação
                css = """
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                        max-width: 900px;
                        margin: 40px auto;
                        padding: 32px;
                        line-height: 1.6;
                        background-color: #ffffff;
                        color: #24292f;
                    }
                    h1, h2, h3, h4, h5, h6 {
                        margin-top: 24px;
                        margin-bottom: 16px;
                        font-weight: 600;
                        line-height: 1.25;
                        border-bottom: 1px solid #d0d7de;
                        padding-bottom: 0.3em;
                    }
                    code {
                        background-color: rgba(175,184,193,0.2);
                        padding: 0.2em 0.4em;
                        border-radius: 6px;
                        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
                        font-size: 85%;
                    }
                    pre {
                        background-color: #f6f8fa;
                        padding: 16px;
                        border-radius: 6px;
                        overflow-x: auto;
                        border: 1px solid #d0d7de;
                    }
                    pre code {
                        background-color: transparent;
                        padding: 0;
                        border-radius: 0;
                    }
                    blockquote {
                        border-left: 4px solid #d0d7de;
                        padding: 0 1em;
                        margin: 0 0 16px 0;
                        color: #57606a;
                    }
                    table {
                        border-collapse: collapse;
                        width: 100%;
                        margin: 16px 0;
                    }
                    th, td {
                        border: 1px solid #d0d7de;
                        padding: 6px 13px;
                        text-align: left;
                    }
                    th {
                        background-color: #f6f8fa;
                        font-weight: 600;
                    }
                    img {
                        max-width: 100%;
                        border-radius: 4px;
                        margin: 8px 0;
                    }
                    .task-list {
                        list-style-type: none;
                        padding-left: 0;
                    }
                    .task-list-item {
                        list-style-type: none;
                        margin: 0.25em 0;
                    }
                    .task-list-item input[type="checkbox"] {
                        margin: 0 0.5em 0.25em -1.6em;
                        vertical-align: middle;
                    }
                </style>
                """
                
                full_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>{os.path.basename(self.current_file) if self.current_file else "Documento Markdown"}</title>
                    {css}
                </head>
                <body>
                    {html_body}
                </body>
                </html>
                """
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(full_html)
                    
                QMessageBox.information(self, "Sucesso", f"Arquivo exportado para:\n{file_path}")
                self.statusBar.showMessage(f"Exportado para: {file_path}")
                
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível exportar:\n{str(e)}")
                
    def show_about(self):
        """Mostra informações sobre o aplicativo"""
        QMessageBox.about(
            self,
            "Sobre o Markdown Editor",
            """
            <h2>📝 Markdown Editor</h2>
            <p><b>Versão:</b> 2.0.0</p>
            <p>Um editor e visualizador de arquivos Markdown com preview em tempo real.</p>
            <p><b>Recursos:</b></p>
            <ul>
                <li>Editor com syntax highlighting</li>
                <li>Preview em tempo real estilo GitHub</li>
                <li>Tema claro/escuro (Dark mode default)</li>
                <li>Suporte a listas de tarefas (checkboxes)</li>
                <li>Suporte a imagens (GitHub e locais)</li>
                <li>Exportação para HTML</li>
                <li>Atalhos de teclado</li>
            </ul>
            <p><b>Tecnologias:</b> Python, PyQt5, Markdown</p>
            <p><b>Github:</b> https://github.com/Guilherme-alexander/markdown-editor<a href="https://github.com/Guilherme-alexander/markdown-editor"></p>
            """
        )
        
    def closeEvent(self, event):
        """Evento ao fechar o aplicativo"""
        if self.check_save():
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Markdown Editor")
    app.setApplicationDisplayName("Markdown Editor")
    
    window = MarkdownEditor()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
