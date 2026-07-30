# brunojose1977-Fiap-PostTech-2026-Revisao_Fase1

Programa, aplicativo ou jogo para testar conhecimentos da Fase 1 da PosTech FIAP - IA para Devs - ano 2026.

Trata-se de um quiz gamificado feito em **PyGame**, com perguntas de Fácil, Médio e Difícil, sistema de pontuação, arte de fundo temática e efeitos sonoros.

## Requisitos

- [Python 3.10+](https://www.python.org/downloads/) (testado com 3.13)
- [PyGame](https://www.pygame.org/) 2.6+

Instale as dependências com:

```bash
pip install pygame
```

## Como executar (a partir do código)

Na raiz do projeto, rode:

```bash
python fiap_postech_quiz.py
```

## Estrutura relevante

- `fiap_postech_quiz.py` — código do jogo.
- `assets/robots_80s_background.png` — arte de fundo usada nas telas.

## Como gerar o executável Windows (.exe)

O executável é criado com o [PyInstaller](https://pyinstaller.org/), empacotando o jogo e a pasta `assets` em um único arquivo.

### 1. Instale o PyInstaller

```bash
pip install pyinstaller
```

### 2. Gere o executável

Na raiz do projeto, execute (PowerShell ou CMD do Windows):

```bash
python -m PyInstaller --noconfirm --onefile --windowed --name "FIAP_PosTech_Quiz" --add-data "assets;assets" fiap_postech_quiz.py
```

Explicação das flags:

- `--onefile` — gera um único arquivo `.exe` autossuficiente.
- `--windowed` — não abre janela de console junto com o jogo.
- `--name "FIAP_PosTech_Quiz"` — nome do executável gerado.
- `--add-data "assets;assets"` — inclui a pasta `assets` dentro do executável. No Windows o separador é `;` (em Linux/macOS seria `:`).

> O código já resolve os caminhos dos recursos via `sys._MEIPASS`, então a arte de fundo é carregada corretamente tanto ao rodar o `.py` quanto pelo `.exe`.

### 3. Localize o resultado

O executável ficará em:

```
dist/FIAP_PosTech_Quiz.exe
```

Basta dar duplo clique para jogar. O arquivo é autossuficiente e pode ser copiado para outro PC Windows 64-bit **sem precisar de Python instalado**.

### Observações

- O PyInstaller também cria a pasta `build/` e o arquivo `FIAP_PosTech_Quiz.spec` (artefatos de build), que podem ser apagados sem afetar o executável.
- Alguns antivírus podem sinalizar executáveis gerados pelo PyInstaller como suspeitos (falso positivo comum). Para distribuição ampla, considere assinar digitalmente o binário.

## Licença

Apache 2.0.

## Autor

Bruno José e Silva — brunojose1977@yahoo.com.br
- [LinkedIn](https://www.linkedin.com/in/bruno-jos%C3%A9-e-silva-61140a2a/)
- [Repositório no GitHub](https://github.com/brunojose1977/brunojose1977-Fiap-PostTech-2026-Revisao_Fase1)
