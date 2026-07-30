[app]

# (str) Título do aplicativo exibido no celular.
title = FIAP PosTech Quiz

# (str) Nome do pacote (somente letras/números, sem espaços).
package.name = fiapquiz

# (str) Domínio do pacote. Junto com package.name forma o applicationId:
# br.com.brunojose.fiapquiz  -> use algo único e que você controle.
package.domain = br.com.brunojose

# (str) Diretório onde está o main.py (raiz do projeto).
source.dir = .

# (list) Extensões de arquivos a incluir no pacote.
source.include_exts = py,png,jpg,jpeg,ttf

# (list) Diretórios que NÃO devem entrar no APK/AAB (materiais de estudo, docs, etc.).
source.exclude_dirs = Base-de-Conhecimento, Documentação, Prompt Kimi K3, .github, p4a-recipes, bin, .buildozer, .git, .venv, venv, __pycache__

# (list) Padrões de arquivos a excluir.
source.exclude_patterns = LICENSE,*.spec,*.txt,*.md,*.docx,*.csv,*.pdf

# (str) Versão do aplicativo (usada na Play Store).
version = 1.0.0

# (list) Requisitos Python do app. pygame-ce é compilado pela receita local abaixo.
requirements = python3,pygame-ce

# (str) Imagem de apresentação (splash) exibida ao abrir.
presplash.filename = %(source.dir)s/assets/robots_80s_background.png

# (str) Ícone do aplicativo (idealmente um PNG quadrado 512x512).
# Reaproveitamos a arte de fundo; troque por um ícone dedicado quando tiver um.
icon.filename = %(source.dir)s/assets/robots_80s_background.png

# (list) Orientações suportadas. O jogo usa layout 1200x800 (paisagem).
orientation = landscape

# (bool) Aplicativo em tela cheia.
fullscreen = 1

#
# Configurações específicas do Android
#

# (str) Cor de fundo da splash (COLOR_BG do jogo).
android.presplash_color = #12121e

# (int) API alvo do Android (deve ser alta; a Play Store exige API recente).
android.api = 34

# (int) API mínima suportada pelo APK/AAB.
android.minapi = 24

# (int) NDK API mínima (normalmente igual a android.minapi).
android.ndk_api = 24

# (bool) Aceita automaticamente as licenças do SDK (necessário para build automatizado/CI).
android.accept_sdk_license = True

# (list) Arquiteturas de CPU a compilar.
# arm64-v8a e armeabi-v7a cobrem praticamente todos os celulares reais.
# (Adicione x86_64 apenas se for testar em emulador.)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Backup automático do Android.
android.allow_backup = True

# (str) Formato do artefato em modo release enviado à Play Store.
android.release_artifact = aab

# (str) Formato do artefato em modo debug (para testes no celular).
android.debug_artifact = apk

#
# Configurações do python-for-android (p4a)
#

# (str) Pasta com receitas de build personalizadas (receita do pygame-ce).
p4a.local_recipes = ./p4a-recipes

# (str) Bootstrap usado no build Android.
p4a.bootstrap = sdl2

[buildozer]

# (int) Nível de log (2 = debug detalhado, útil para diagnosticar erros de build).
log_level = 2

# (int) Avisar caso o buildozer seja executado como root.
warn_on_root = 1
