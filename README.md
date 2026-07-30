# FIAP PosTech 2026 — IA para DEVs — Revisão Fase 1

Quiz gamificado em cards (feito em **Python + Pygame CE**) para testar os
conhecimentos da **Fase 1 da PosTech FIAP - IA para Devs (2026)**: Fundamentos
de IA, Machine Learning, Machine Learning Avançado, Visão Computacional e IA
Generativa.

- **Autor:** Bruno José e Silva — brunojose1977@yahoo.com.br
- **Licença:** Apache 2.0
- **LinkedIn:** https://www.linkedin.com/in/bruno-jos%C3%A9-e-silva-61140a2a/

---

## Índice

- [Executar no computador (desktop)](#-executar-no-computador-desktop)
- [Gerar o binário Android (APK/AAB)](#-gerar-o-binário-android-apkaab)
  - [Opção A — GitHub Actions (recomendada no Windows)](#opção-a--github-actions-recomendada-no-windows)
  - [Opção B — Docker (Linux/macOS/WSL2)](#opção-b--docker-linuxmacoswsl2)
  - [Opção C — Buildozer direto no Linux/WSL2](#opção-c--buildozer-direto-no-linuxwsl2)
- [Assinar o AAB de release](#-assinar-o-aab-de-release)
- [Enviar o APP para a Play Store](#-enviar-o-app-para-a-play-store)
- [Estrutura do projeto](#-estrutura-do-projeto)

---

## 🖥 Executar no computador (desktop)

Pré-requisitos: **Python 3.10+**.

```bash
# 1. Crie e ative um ambiente virtual (opcional, porém recomendado)
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Rode o jogo
python fiap_postech_quiz.py
```

---

## 📦 Gerar o binário Android (APK/AAB)

O jogo é empacotado para Android com **[Buildozer](https://buildozer.readthedocs.io/)**
+ **python-for-android (p4a)**, usando uma receita personalizada do `pygame-ce`
(em `p4a-recipes/pygame-ce/`), porque o p4a não traz suporte oficial ao pygame
moderno.

**Conceitos importantes:**

- **APK** (`.apk`) → usado para **instalar e testar** o app diretamente no
  celular.
- **AAB** (`.aab`, *Android App Bundle*) → é o **formato exigido pela Play Store**
  para publicação. É este o arquivo que você envia para a Google.
- O **Buildozer só roda em Linux**. No Windows, use a **Opção A (GitHub Actions)**
  ou a **Opção B (WSL2 + Docker)**.

Arquivos que controlam o build (já incluídos no repositório):

| Arquivo | Função |
|---------|--------|
| `main.py` | Ponto de entrada exigido pelo Android (chama o jogo). |
| `buildozer.spec` | Configuração do build (nome, versão, ícone, arquiteturas, AAB). |
| `p4a-recipes/pygame-ce/__init__.py` | Receita que compila o pygame-ce para Android. |
| `.github/workflows/android-build.yml` | Build automático na nuvem (APK + AAB). |

### Opção A — GitHub Actions (recomendada no Windows)

Como você está no Windows, a forma mais simples de gerar o binário é deixar o
GitHub compilar por você (em uma máquina Linux, de graça):

1. Envie o projeto para um repositório no GitHub:

   ```bash
   git add .
   git commit -m "Configura build Android (APK/AAB) com Buildozer"
   git push
   ```

2. No GitHub, abra a aba **Actions** → selecione o workflow
   **"Build Android (APK + AAB)"** → clique em **Run workflow**.
   (Você também pode disparar publicando uma tag de versão:
   `git tag v1.0.0 && git push origin v1.0.0`.)

3. Aguarde o build terminar (a primeira execução baixa o SDK/NDK e leva
   ~30–60 min; as próximas são mais rápidas por causa do cache).

4. Ao final, entre na execução concluída e baixe o artefato
   **`fiap-quiz-android`**. Dentro do `.zip` estarão o `.apk` (para testar) e o
   `.aab` (para a Play Store).

### Opção B — Docker (Linux/macOS/WSL2)

Requer **Docker** instalado. No Windows, instale o **WSL2** e o **Docker Desktop**.

```bash
# A partir da raiz do projeto:
mkdir -p .docker/buildozer

# Gera o APK de debug (para testar no celular)
docker run --rm \
  -v "$(pwd)":/home/user/hostcwd \
  -v "$(pwd)/.docker/buildozer":/home/user/.buildozer \
  kivy/buildozer -v android debug

# Gera o AAB de release (para a Play Store)
docker run --rm \
  -v "$(pwd)":/home/user/hostcwd \
  -v "$(pwd)/.docker/buildozer":/home/user/.buildozer \
  kivy/buildozer -v android release
```

Os binários aparecem na pasta `bin/`.

### Opção C — Buildozer direto no Linux/WSL2

Em uma distribuição Linux (nativa ou no WSL2 Ubuntu):

```bash
# 1. Dependências de sistema
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip \
  autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
  libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev build-essential ccache

# 2. Buildozer e Cython
pip install --upgrade buildozer "Cython<0.30"

# 3. Build (a partir da raiz do projeto)
buildozer -v android debug     # gera bin/*.apk (teste)
buildozer -v android release   # gera bin/*.aab (Play Store)
```

> Dica: para instalar o APK de debug num celular conectado por USB (com
> **Depuração USB** ativada), use `buildozer android deploy run` ou
> `adb install bin/*.apk`.

---

## 🔐 Assinar o AAB de release

A Play Store **só aceita AABs assinados**. O `buildozer android release` gera um
AAB **não assinado** (`bin/*-release-unsigned.aab` ou similar). Assine-o assim:

1. Crie **uma única vez** uma chave de assinatura (guarde-a em local seguro; se
   você a perder, não conseguirá mais atualizar o app):

   ```bash
   keytool -genkey -v -keystore fiapquiz.keystore \
     -alias fiapquiz -keyalg RSA -keysize 2048 -validity 10000
   ```

2. Assine o AAB com o `jarsigner` (vem com o JDK):

   ```bash
   jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
     -keystore fiapquiz.keystore \
     bin/fiapquiz-1.0.0-release-unsigned.aab fiapquiz
   ```

   (ajuste o nome do arquivo conforme o gerado em `bin/`).

> **Alternativa recomendada:** use o **Play App Signing** da Google. Nesse modo
> você pode enviar um AAB com uma chave de *upload* e a própria Google gerencia
> a chave final de assinatura — mais seguro contra perda de chave.
>
> ⚠️ **Nunca** faça commit do arquivo `.keystore`/`.jks` nem das senhas. O
> `.gitignore` já bloqueia esses arquivos.

---

## 🚀 Enviar o APP para a Play Store

Passo a passo para publicar o `.aab` na **Google Play Store**:

### 1. Criar a conta de desenvolvedor

1. Acesse o [Google Play Console](https://play.google.com/console/).
2. Faça login com uma conta Google e crie uma **conta de desenvolvedor**.
3. Pague a **taxa única de US$ 25** e conclua a verificação de identidade
   (pode levar alguns dias).

### 2. Criar o aplicativo no Play Console

1. No Play Console, clique em **Criar app**.
2. Informe **nome do app**, **idioma padrão**, se é **app ou jogo** (selecione
   *Jogo*) e se é **gratuito ou pago**.
3. Aceite as declarações e políticas.

### 3. Preencher a ficha da loja (Store Listing)

1. Em **Presença na Play Store → Ficha principal da loja**, preencha:
   - Descrição breve e descrição completa.
   - **Ícone** (512×512 px, PNG de 32 bits).
   - **Imagem de destaque** (1024×500 px).
   - **Capturas de tela** (mínimo de 2, no formato de telefone).
2. Em **Conteúdo do app**, preencha os questionários obrigatórios:
   - **Política de privacidade** (URL).
   - **Classificação de conteúdo** (questionário IARC).
   - **Público-alvo e conteúdo**.
   - **Segurança dos dados**.
   - **Anúncios** (declare se o app tem anúncios — este não tem).

### 4. Enviar o binário (AAB)

1. No menu lateral, vá em **Testes** (recomendado começar por *Teste interno*)
   ou diretamente em **Produção**.
2. Clique em **Criar nova versão**.
3. Se for a primeira versão, ative o **Play App Signing** quando solicitado.
4. Em **App bundles**, faça **upload do arquivo `.aab`** gerado e assinado.
5. Defina o **nome da versão** e as **notas da versão** (novidades).
6. Clique em **Avançar / Salvar** e revise os avisos.

### 5. Publicar

1. Depois de testar (recomenda-se usar as trilhas de **Teste interno/fechado**
   antes de ir para produção), vá em **Produção → Criar versão** e envie o AAB.
2. Clique em **Enviar para revisão**.
3. A Google analisa o app (normalmente de algumas horas a alguns dias).
4. Após aprovado, o app fica disponível na **Play Store**. 🎉

> **Dicas importantes:**
> - A cada nova atualização, **incremente a `version`** no `buildozer.spec`
>   (ex.: `1.0.0` → `1.0.1`) e gere um novo AAB. O `versionCode` interno é
>   calculado automaticamente pelo Buildozer.
> - A Play Store exige um `targetSdkVersion` recente — mantenha
>   `android.api` alto no `buildozer.spec` (já configurado como `34`).
> - Guarde a chave de assinatura (ou use o Play App Signing): a **mesma chave**
>   é obrigatória para publicar futuras atualizações.

---

## 📁 Estrutura do projeto

```
.
├── fiap_postech_quiz.py          # Código do jogo (desktop + Android)
├── main.py                       # Entry point exigido pelo Android
├── buildozer.spec                # Configuração do build Android (APK/AAB)
├── requirements.txt              # Dependências desktop (pygame-ce)
├── assets/
│   └── robots_80s_background.png # Arte de fundo / splash / ícone
├── p4a-recipes/
│   └── pygame-ce/__init__.py     # Receita para compilar o pygame-ce no Android
├── .github/workflows/
│   └── android-build.yml         # Build automático na nuvem (APK + AAB)
├── Base-de-Conhecimento/         # PDFs e prints de estudo (não vão no APP)
└── Documentação/                 # Documentos do projeto
```
