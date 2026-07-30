#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIAP PosTech 2026 - IA para DEVs - Revisão Fase 1
Jogo Quiz Gamificado em Cards

Licença: Apache 2.0
Autor: Bruno José e Silva - brunojose1977@yahoo.com.br
LinkedIn: https://www.linkedin.com/in/bruno-jos%C3%A9-e-silva-61140a2a/
Repositório: https://github.com/brunojose1977/brunojose1977-Fiap-PostTech-2026-Revisao_Fase1
"""

import pygame
import random
import sys
import math
import os
import webbrowser
from array import array

# =============================================================================
# CONFIGURAÇÕES GLOBAIS
# =============================================================================
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
BACKGROUND_ALPHA = int(0.40 * 255)
BACKGROUND_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "robots_80s_background.png",
)

# Cores
COLOR_BG = (18, 18, 30)
COLOR_CARD_BG = (30, 30, 50)
COLOR_CARD_BORDER = (100, 100, 200)
COLOR_TEXT = (230, 230, 240)
COLOR_TEXT_DIM = (150, 150, 170)
COLOR_ACCENT = (0, 200, 255)
COLOR_SUCCESS = (50, 220, 120)
COLOR_ERROR = (255, 80, 80)
COLOR_WARNING = (255, 180, 50)
COLOR_BUTTON = (60, 60, 100)
COLOR_BUTTON_HOVER = (80, 80, 140)
COLOR_FOOTER_BG = (10, 10, 20)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FIAP PosTech 2026 - IA para DEVs - Revisão Fase 1")
clock = pygame.time.Clock()

# Fontes
try:
    font_title = pygame.font.Font(None, 56)
    font_subtitle = pygame.font.Font(None, 40)
    font_text = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 26)
    font_tiny = pygame.font.Font(None, 22)
except:
    font_title = pygame.font.SysFont("arial", 56)
    font_subtitle = pygame.font.SysFont("arial", 40)
    font_text = pygame.font.SysFont("arial", 32)
    font_small = pygame.font.SysFont("arial", 26)
    font_tiny = pygame.font.SysFont("arial", 22)


def load_background():
    """Carrega a arte de fundo em versões opaca e translúcida (alpha 0.40)."""
    try:
        image = pygame.image.load(BACKGROUND_PATH).convert()
    except (pygame.error, FileNotFoundError):
        return None, None

    opaque = pygame.transform.smoothscale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    faded = opaque.copy()
    faded.set_alpha(BACKGROUND_ALPHA)
    return opaque, faded


BACKGROUND_OPAQUE, BACKGROUND_FADED = load_background()

# =============================================================================
# BANCO DE PERGUNTAS (Baseado nos PDFs enviados)
# =============================================================================

QUESTIONS_DB = [
    # FÁCEIS
    {"question": "O que é Visão Computacional?", "options": ["Uma área da IA que treina computadores para interpretar dados visuais", "Um tipo de banco de dados", "Um sistema operacional", "Uma linguagem de programação", "Um framework web"], "answer": 0, "difficulty": "easy", "category": "Visão Computacional", "explanation": "A Visão Computacional é uma área da Inteligência Artificial que treina computadores para 'ver', interpretar e compreender o mundo visual."},
    {"question": "Qual técnica de Deep Learning é mais comum em Visão Computacional?", "options": ["RNN", "CNN", "SVM", "KNN", "Decision Tree"], "answer": 1, "difficulty": "easy", "category": "Visão Computacional", "explanation": "As Redes Neurais Convolucionais (CNNs) são a técnica mais comum e eficaz para tarefas complexas de Visão Computacional."},
    {"question": "O que é OCR?", "options": ["Reconhecimento Óptico de Caracteres", "Objeto de Classificação de Redes", "Operador de Cálculo Rápido", "Otimização de Código Reduzido", "Organização de Classes de Rede"], "answer": 0, "difficulty": "easy", "category": "Visão Computacional", "explanation": "OCR (Optical Character Recognition) é o processo de converter texto de uma imagem digital em texto editável e pesquisável."},
    {"question": "Qual biblioteca é comumente usada para Visão Computacional em Python?", "options": ["OpenCV", "Pandas", "NumPy", "Matplotlib", "Flask"], "answer": 0, "difficulty": "easy", "category": "Visão Computacional", "explanation": "A OpenCV (cv2) é a biblioteca mais popular para processamento de imagens e visão computacional."},
    {"question": "O que é Machine Learning?", "options": ["Um campo da IA onde máquinas aprendem padrões a partir de dados", "Um tipo de hardware", "Um sistema de rede social", "Um protocolo de internet", "Um banco de dados NoSQL"], "answer": 0, "difficulty": "easy", "category": "Machine Learning", "explanation": "Machine Learning é um campo da Inteligência Artificial onde algoritmos aprendem padrões a partir de dados históricos."},
    {"question": "Qual é a métrica que mede a proporção de previsões corretas?", "options": ["Precisão", "Recall", "Acurácia", "F1-Score", "Especificidade"], "answer": 2, "difficulty": "easy", "category": "Machine Learning Avançado", "explanation": "A Acurácia representa a proporção de previsões corretas em relação ao total de previsões."},
    {"question": "O que é uma Rede Neural Convolucional (CNN)?", "options": ["Uma rede projetada para processar dados em grade como imagens", "Uma rede para processamento de texto", "Um tipo de banco de dados", "Um sistema de recomendação", "Um algoritmo de ordenação"], "answer": 0, "difficulty": "easy", "category": "Visão Computacional", "explanation": "CNNs são projetadas para processar dados estruturados em grade, como imagens, usando camadas convolucionais."},
    {"question": "Qual função de ativação é comum em CNNs?", "options": ["ReLU", "Sigmoid", "Tanh", "Softmax", "Todas as anteriores"], "answer": 4, "difficulty": "easy", "category": "Visão Computacional", "explanation": "ReLU, Sigmoid, Tanh e Softmax são todas funções de ativação usadas em diferentes partes de uma CNN."},
    {"question": "O que é Transfer Learning?", "options": ["Reutilizar um modelo treinado em uma tarefa para outra similar", "Transferir dados entre servidores", "Copiar código de um projeto para outro", "Mover arquivos entre pastas", "Trocar de linguagem de programação"], "answer": 0, "difficulty": "easy", "category": "Visão Computacional", "explanation": "Transfer Learning reutiliza um modelo treinado em uma tarefa como ponto de partida para uma segunda tarefa."},
    {"question": "Qual modelo é famoso por detecção de objetos em tempo real?", "options": ["YOLO", "ResNet", "VGG", "AlexNet", "LeNet"], "answer": 0, "difficulty": "easy", "category": "Visão Computacional", "explanation": "YOLO (You Only Look Once) é um modelo famoso por detecção de objetos em tempo real."},
    {"question": "O que é uma GAN?", "options": ["Rede Adversarial Generativa", "Grande Algoritmo Numérico", "Grupo de Análise de Rede", "Gerador de Aplicações Novas", "Gateway de Acesso à Nuvem"], "answer": 0, "difficulty": "easy", "category": "Visão Computacional", "explanation": "GAN (Generative Adversarial Network) é composta por um Gerador e um Discriminador que competem entre si."},
    {"question": "Qual é o propósito do K-Means?", "options": ["Clusterização não supervisionada", "Classificação supervisionada", "Regressão linear", "Processamento de imagens", "Tradução de texto"], "answer": 0, "difficulty": "easy", "category": "Machine Learning Avançado", "explanation": "K-Means é um algoritmo de clusterização não supervisionado que agrupa dados em K clusters."},
    {"question": "O que é Feature Scaling?", "options": ["Técnica para mudar a escala dos valores das features", "Redimensionar imagens", "Aumentar o dataset", "Reduzir dimensionalidade", "Codificar variáveis categóricas"], "answer": 0, "difficulty": "easy", "category": "Machine Learning", "explanation": "Feature Scaling é a categoria de técnicas usadas para mudar a escala dos valores das features."},
    {"question": "Qual técnica transforma dados para média 0 e desvio padrão 1?", "options": ["Normalização Min-Max", "Padronização (Z-Score)", "Label Encoding", "One-Hot Encoding", "Robust Scaling"], "answer": 1, "difficulty": "easy", "category": "Machine Learning", "explanation": "A Padronização (Z-Score Standardization) transforma dados para terem média 0 e desvio padrão 1."},
    {"question": "O que é PCA?", "options": ["Análise de Componentes Principais", "Processamento de Código Aberto", "Programação de Computadores Avançada", "Protocolo de Comunicação de Aplicações", "Processamento Central de Algoritmos"], "answer": 0, "difficulty": "easy", "category": "Machine Learning", "explanation": "PCA (Principal Component Analysis) é uma técnica estatística para reduzir a dimensionalidade dos dados."},

    # MÉDIAS
    {"question": "Na curva ROC, o que representa o eixo Y?", "options": ["Taxa de Falsos Positivos", "Taxa de Verdadeiros Positivos (Sensibilidade)", "Acurácia", "Precisão", "Especificidade"], "answer": 1, "difficulty": "medium", "category": "Machine Learning Avançado", "explanation": "No eixo Y da curva ROC temos a Taxa de Verdadeiros Positivos (TVP), também conhecida como Sensibilidade."},
    {"question": "O que significa AUC = 0.93 em uma curva ROC?", "options": ["Modelo aleatório", "Modelo excelente", "Modelo ruim", "Modelo com overfitting", "Modelo com underfitting"], "answer": 1, "difficulty": "medium", "category": "Machine Learning Avançado", "explanation": "Um AUC próximo de 1.0 (como 0.93) indica um modelo com excelente capacidade de discriminação."},
    {"question": "Qual é a fórmula do F1-Score?", "options": ["Média harmônica entre Precisão e Recall", "Soma de Precisão e Recall", "Produto de Precisão e Recall", "Diferença entre Precisão e Recall", "Divisão de Precisão por Recall"], "answer": 0, "difficulty": "medium", "category": "Machine Learning Avançado", "explanation": "F1-Score é a média harmônica entre Precisão e Recall, útil para buscar equilíbrio entre essas métricas."},
    {"question": "O que é Validação Cruzada (Cross-Validation)?", "options": ["Técnica para obter estimativa robusta do desempenho do modelo", "Método para aumentar dados", "Técnica de normalização", "Algoritmo de clusterização", "Tipo de rede neural"], "answer": 0, "difficulty": "medium", "category": "Machine Learning Avançado", "explanation": "Validação Cruzada obtém uma estimativa mais robusta e confiável do desempenho e da capacidade de generalização do modelo."},
    {"question": "Qual método automatiza a otimização de hiperparâmetros testando combinações?", "options": ["GridSearchCV", "Random Forest", "KNN", "SVM", "PCA"], "answer": 0, "difficulty": "medium", "category": "Machine Learning Avançado", "explanation": "GridSearchCV é um método de 'força bruta' que testa exaustivamente combinações de hiperparâmetros."},
    {"question": "O que é Ensemble Learning no contexto de Random Forest?", "options": ["Combinação de múltiplos modelos para produzir previsão mais precisa", "Uso de uma única árvore de decisão", "Técnica de redução de dimensionalidade", "Método de codificação categórica", "Algoritmo de otimização"], "answer": 0, "difficulty": "medium", "category": "Machine Learning Avançado", "explanation": "Random Forest é um ensemble que constrói múltiplas árvores de decisão e combina suas previsões."},
    {"question": "O que é a 'Técnica do Cotovelo' no K-Means?", "options": ["Método para encontrar o número ideal de clusters", "Técnica de redução de ruído", "Método de normalização", "Algoritmo de otimização", "Técnica de data augmentation"], "answer": 0, "difficulty": "medium", "category": "Machine Learning Avançado", "explanation": "A técnica do cotovelo analisa a inércia vs número de clusters para identificar o ponto onde a redução de erro diminui significativamente."},
    {"question": "Qual é a diferença entre Label Encoding e One-Hot Encoding?", "options": ["LE transforma em inteiros, OHE cria colunas binárias", "LE cria colunas binárias, OHE transforma em inteiros", "Ambos fazem a mesma coisa", "LE é para imagens, OHE para texto", "LE é supervisionado, OHE não supervisionado"], "answer": 0, "difficulty": "medium", "category": "Machine Learning", "explanation": "Label Encoding transforma categorias em inteiros. One-Hot Encoding cria colunas binárias para cada categoria."},
    {"question": "O que é o 'MSE' em regressão linear?", "options": ["Mean Squared Error - Erro Quadrático Médio", "Mean Standard Error", "Maximum Squared Error", "Minimum Standard Estimation", "Model Selection Error"], "answer": 0, "difficulty": "medium", "category": "Machine Learning", "explanation": "MSE (Mean Squared Error) calcula a média dos quadrados das diferenças entre valores previstos e reais."},
    {"question": "Qual modelo de IA Generativa usa Generator e Discriminator?", "options": ["GAN", "VAE", "Transformer", "RNN", "CNN"], "answer": 0, "difficulty": "medium", "category": "Fundamentos de IA", "explanation": "GANs (Generative Adversarial Networks) usam duas redes: um Generator que cria dados sintéticos e um Discriminator que tenta identificar o que é falso."},
    {"question": "O que é um Autoencoder Variacional (VAE)?", "options": ["Modelo generativo com encoder e decoder", "Modelo de classificação", "Algoritmo de clusterização", "Técnica de feature scaling", "Método de validação cruzada"], "answer": 0, "difficulty": "medium", "category": "Fundamentos de IA", "explanation": "VAE é um modelo generativo que usa um encoder para comprimir dados em um espaço latente e um decoder para reconstruí-los."},
    {"question": "Qual arquitetura revolucionou o NLP com mecanismo de atenção?", "options": ["RNN", "LSTM", "Transformer", "CNN", "GRU"], "answer": 2, "difficulty": "medium", "category": "Fundamentos de IA", "explanation": "A arquitetura Transformer revolucionou o NLP substituindo RNNs pelo mecanismo de atenção."},
    {"question": "O que é LangChain?", "options": ["Framework para desenvolver aplicações com LLMs", "Uma linguagem de programação", "Um banco de dados", "Um sistema operacional", "Um tipo de rede neural"], "answer": 0, "difficulty": "medium", "category": "Fundamentos de IA", "explanation": "LangChain é um framework de código aberto projetado para simplificar o desenvolvimento de aplicações que utilizam Grandes Modelos de Linguagem (LLMs)."},
    {"question": "O que é RAG (Retrieval-Augmented Generation)?", "options": ["Técnica que permite LLMs acessarem informações externas", "Um tipo de rede neural", "Um algoritmo de ordenação", "Um framework de jogos", "Um método de compressão de dados"], "answer": 0, "difficulty": "medium", "category": "Fundamentos de IA", "explanation": "RAG permite que LLMs acessem e usem informações externas àquelas com que foram originalmente treinados."},
    {"question": "Qual é a principal vantagem do YOLO sobre outros detectores?", "options": ["Velocidade de detecção em tempo real", "Maior precisão em todos os casos", "Menor uso de memória", "Não precisa de GPU", "Funciona apenas com imagens pequenas"], "answer": 0, "difficulty": "medium", "category": "Visão Computacional", "explanation": "YOLO é otimizado para detecção de objetos em tempo real, processando a imagem em uma única passagem."},
    {"question": "O que é o 'Max Pooling' em uma CNN?", "options": ["Redução de dimensionalidade selecionando valores máximos", "Aumento da dimensionalidade", "Normalização de batch", "Dropout de neurônios", "Função de ativação"], "answer": 0, "difficulty": "medium", "category": "Visão Computacional", "explanation": "Max Pooling reduz a dimensionalidade dos mapas de características selecionando o valor máximo em cada região."},
    {"question": "Qual dataset é usado para benchmark de classificação de imagens?", "options": ["ImageNet", "COCO", "MNIST", "Reuters", "Iris"], "answer": 0, "difficulty": "medium", "category": "Visão Computacional", "explanation": "ImageNet é o benchmark mais famoso para avaliar a precisão de modelos de classificação de imagens."},
    {"question": "O que é 'Overfitting'?", "options": ["Quando o modelo se ajusta demais aos dados de treino", "Quando o modelo é muito simples", "Quando faltam dados", "Quando há muitos outliers", "Quando as features não estão escaladas"], "answer": 0, "difficulty": "medium", "category": "Machine Learning", "explanation": "Overfitting ocorre quando o modelo aprende demais os dados de treinamento, incluindo ruídos, perdendo a capacidade de generalizar."},
    {"question": "Qual é o propósito do Dropout em redes neurais?", "options": ["Evitar overfitting desativando neurônios aleatoriamente", "Aumentar a velocidade de treinamento", "Normalizar os dados de entrada", "Reduzir a dimensionalidade", "Codificar variáveis categóricas"], "answer": 0, "difficulty": "medium", "category": "Fundamentos de IA", "explanation": "Dropout é uma técnica de regularização que desativa aleatoriamente neurônios durante o treinamento para evitar overfitting."},
    {"question": "O que é o 'Adam' em redes neurais?", "options": ["Um otimizador", "Uma função de ativação", "Uma camada da rede", "Um tipo de loss", "Um dataset"], "answer": 0, "difficulty": "medium", "category": "Fundamentos de IA", "explanation": "Adam (Adaptive Moment Estimation) é um algoritmo de otimização popular para ajustar pesos durante o treinamento de redes neurais."},

    # DIFÍCEIS
    {"question": "Na matriz de confusão, o que representa um Falso Negativo?", "options": ["Modelo previu negativo mas o real era positivo", "Modelo previu positivo mas o real era negativo", "Modelo acertou o positivo", "Modelo acertou o negativo", "Modelo não fez previsão"], "answer": 0, "difficulty": "hard", "category": "Machine Learning Avançado", "explanation": "Falso Negativo (FN) ocorre quando o modelo previu a classe negativa, mas o valor real era positivo. É um erro tipo II."},
    {"question": "Qual métrica é mais importante quando o custo de um falso positivo é elevado?", "options": ["Recall", "Precisão", "Acurácia", "F1-Score", "AUC"], "answer": 1, "difficulty": "hard", "category": "Machine Learning Avançado", "explanation": "A Precisão indica quantas das previsões positivas são realmente positivas. É crucial quando o custo do falso positivo é alto."},
    {"question": "O que é o 'Dying ReLU' e como o Leaky ReLU resolve?", "options": ["Neurônios que param de aprender; Leaky ReLU permite gradiente negativo pequeno", "Overfitting; Leaky ReLU aumenta dados", "Underfitting; Leaky ReLU reduz camadas", "Vanishing gradient; Leaky ReLU normaliza batch", "Exploding gradient; Leaky ReLU clipa valores"], "answer": 0, "difficulty": "hard", "category": "Visão Computacional", "explanation": "Dying ReLU ocorre quando neurônios sempre produzem zero. Leaky ReLU permite um pequeno gradiente negativo, evitando neurônios mortos."},
    {"question": "Qual é a diferença entre VAE e GAN?", "options": ["VAE reconstrói dados; GAN gera dados novos via competição", "VAE é supervisionado; GAN é não supervisionado", "VAE usa CNN; GAN usa RNN", "VAE é mais rápido; GAN é mais lento", "Não há diferença"], "answer": 0, "difficulty": "hard", "category": "Fundamentos de IA", "explanation": "VAE usa encoder-decoder para reconstruir dados. GAN usa Generator e Discriminator competindo para gerar dados novos realistas."},
    {"question": "O que é 'Early Stopping' no treinamento de redes neurais?", "options": ["Interromper treinamento quando erro de validação aumenta", "Aumentar épocas automaticamente", "Reduzir learning rate", "Aumentar batch size", "Trocar o otimizador"], "answer": 0, "difficulty": "hard", "category": "Fundamentos de IA", "explanation": "Early Stopping interrompe o treinamento quando o erro no conjunto de validação começa a aumentar, evitando overfitting."},
    {"question": "Qual técnica é usada em Random Forest para garantir baixa correlação entre árvores?", "options": ["Bagging + seleção aleatória de features", "Boosting sequencial", "Gradient Descent", "Backpropagation", "Cross-Validation"], "answer": 0, "difficulty": "hard", "category": "Machine Learning Avançado", "explanation": "Random Forest usa Bagging (amostragem com reposição) e em cada nó considera apenas um subconjunto aleatório de features."},
    {"question": "O que é 'sparse_categorical_crossentropy' diferente de 'categorical_crossentropy'?", "options": ["Usa rótulos inteiros ao invés de one-hot", "Usa one-hot ao invés de inteiros", "É para regressão", "É para clusterização", "Não há diferença"], "answer": 0, "difficulty": "hard", "category": "Fundamentos de IA", "explanation": "sparse_categorical_crossentropy é usada quando os rótulos são inteiros (0,1,2...), enquanto categorical_crossentropy exige one-hot encoding."},
    {"question": "Qual é a principal limitação do Random Forest para extrapolação temporal?", "options": ["Não pode prever valores fora do intervalo de treino", "É muito lento", "Não suporta dados numéricos", "Requer normalização obrigatória", "Só funciona com imagens"], "answer": 0, "difficulty": "hard", "category": "Fundamentos de IA", "explanation": "Random Forest só pode prever valores dentro do intervalo do target visto no treinamento. Para extrapolação, Regressão Linear é mais indicada."},
    {"question": "O que é 'Backpropagation' em Deep Learning?", "options": ["Algoritmo que ajusta pesos usando gradiente da função de perda", "Método para carregar dados", "Técnica de normalização", "Tipo de camada convolucional", "Método de validação"], "answer": 0, "difficulty": "hard", "category": "Fundamentos de IA", "explanation": "Backpropagation calcula os gradientes da função de perda em relação aos pesos e os ajusta via descida do gradiente."},
    {"question": "Qual é a função da camada Embedding em NLP?", "options": ["Mapear índices de palavras em vetores densos", "Achatar imagens", "Aplicar convolução", "Fazer pooling", "Normalizar batch"], "answer": 0, "difficulty": "hard", "category": "Fundamentos de IA", "explanation": "Embedding mapeia números inteiros (índices de palavras) em vetores densos de ponto flutuante, capturando relações semânticas."},
    {"question": "O que é o 'Indíce de Gini' em Árvores de Decisão?", "options": ["Medida de impureza usada para divisões", "Métrica de acurácia", "Função de ativação", "Técnica de regularização", "Método de otimização"], "answer": 0, "difficulty": "hard", "category": "Machine Learning Avançado", "explanation": "O índice de Gini mede a impureza de um nó. CART usa Gini para classificação e MSE para regressão."},
    {"question": "Qual é o propósito do 'GlobalMaxPooling1D' em uma CNN para texto?", "options": ["Reduzir dimensionalidade pegando o valor máximo por feature", "Aumentar a dimensionalidade", "Aplicar convolução 2D", "Criar embeddings", "Normalizar dados"], "answer": 0, "difficulty": "hard", "category": "Fundamentos de IA", "explanation": "GlobalMaxPooling1D reduz a saída da camada de embedding para um vetor único por amostra, pegando o valor máximo de cada feature."},
    {"question": "O que é 'SMOTE' no contexto de datasets desbalanceados?", "options": ["Técnica de oversampling sintético", "Método de undersampling", "Algoritmo de clusterização", "Técnica de feature selection", "Método de normalização"], "answer": 0, "difficulty": "hard", "category": "Machine Learning Avançado", "explanation": "SMOTE (Synthetic Minority Over-sampling Technique) cria amostras sintéticas da classe minoritária para balancear dados."},
    {"question": "Qual é a diferença entre Bagging e Boosting?", "options": ["Bagging treina árvores em paralelo; Boosting treina sequencialmente corrigindo erros", "Bagging é sequencial; Boosting é paralelo", "Bagging para classificação; Boosting para regressão", "Não há diferença", "Bagging usa CNN; Boosting usa RNN"], "answer": 0, "difficulty": "hard", "category": "Machine Learning Avançado", "explanation": "Bagging (usado em Random Forest) treina modelos independentes em paralelo. Boosting (GBM, XGBoost) treina sequencialmente, corrigindo erros das árvores anteriores."},
    {"question": "O que representa a 'Entropia' em um nó de Árvore de Decisão?", "options": ["Medida de desordem/impureza dos dados", "Taxa de acerto do modelo", "Número de amostras", "Probabilidade de acerto", "Nível de profundidade da árvore"], "answer": 0, "difficulty": "hard", "category": "Machine Learning Avançado", "explanation": "Entropia mede a impureza/desordem de um nó. Valor 0 significa nó puro (todos da mesma classe)."},
    {"question": "Qual é o papel do 'Discriminator' em uma GAN?", "options": ["Distinguir entre amostras reais e geradas", "Gerar novas amostras", "Otimizar pesos do gerador", "Normalizar dados de entrada", "Aplicar data augmentation"], "answer": 0, "difficulty": "hard", "category": "Visão Computacional", "explanation": "O Discriminator tenta identificar o que é real vs falso, enquanto o Generator tenta enganá-lo."},
    {"question": "O que é 'Fine-tuning' no contexto de Transfer Learning?", "options": ["Ajustar um modelo pré-treinado para uma tarefa específica", "Treinar do zero", "Remover camadas da rede", "Congelar todos os pesos", "Aumentar o dataset"], "answer": 0, "difficulty": "hard", "category": "Visão Computacional", "explanation": "Fine-tuning ajusta um modelo pré-treinado em uma nova tarefa, geralmente treinando apenas as camadas finais."},
    {"question": "Qual é a principal função do 'Flatten' em uma CNN?", "options": ["Transformar matriz 2D em vetor 1D", "Aplicar convolução", "Reduzir dimensionalidade por pooling", "Aplicar função de ativação", "Normalizar batch"], "answer": 0, "difficulty": "hard", "category": "Visão Computacional", "explanation": "Flatten achata a saída das camadas convolucionais (2D) em um vetor 1D para alimentar as camadas densas."},
    {"question": "O que é 'Gradient Vanishing' em redes neurais profundas?", "options": ["Gradientes que ficam muito pequenos nas camadas iniciais", "Gradientes que explodem", "Pesos que não atualizam", "Dados que somem", "Camadas que desaparecem"], "answer": 0, "difficulty": "hard", "category": "Fundamentos de IA", "explanation": "Gradient Vanishing ocorre quando gradientes ficam exponencialmente pequenos nas camadas iniciais, impedindo o aprendizado. ResNet resolve com conexões residuais."},
    {"question": "O que é 'Shapley Value' no contexto de interpretabilidade de ML?", "options": ["Método para explicar contribuição de cada feature", "Métrica de acurácia", "Técnica de clusterização", "Algoritmo de otimização", "Método de validação cruzada"], "answer": 0, "difficulty": "hard", "category": "Machine Learning Avançado", "explanation": "Shapley Values vêm da teoria dos jogos e explicam a contribuição de cada feature para uma previsão específica."},
]

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================
def create_sound(segments, volume=0.25):
    """Sintetiza áudio tecnológico com varreduras e modulação robótica."""
    if not pygame.mixer.get_init():
        return None

    sample_rate, _, channels = pygame.mixer.get_init()
    samples = array("h")
    amplitude = int(32767 * volume)

    for start_frequency, end_frequency, duration in segments:
        sample_count = int(sample_rate * duration)
        phase = 0.0
        for index in range(sample_count):
            progress = index / max(1, sample_count - 1)
            frequency = start_frequency + (
                end_frequency - start_frequency
            ) * progress
            if frequency == 0:
                value = 0
            else:
                phase += 2 * math.pi * frequency / sample_rate
                time = index / sample_rate
                modulation = (
                    0.08 * math.sin(2 * math.pi * 8 * time)
                    + 0.02 * math.sin(2 * math.pi * 19 * time)
                )
                carrier = math.sin(phase + modulation)
                harmonic = math.sin(phase * 2.01 + modulation * 0.5)
                metallic = math.sin(phase * 3.73 + modulation)
                energy_hum = math.sin(phase * 0.5)
                wave = (
                    0.86 * carrier
                    + 0.10 * harmonic
                    + 0.02 * metallic
                    + 0.02 * energy_hum
                )

                # Envelope curto mantém o som limpo e com ataque eletrônico.
                attack = min(1.0, index / max(1, int(sample_rate * 0.005)))
                release = min(
                    1.0,
                    (sample_count - index) / max(1, int(sample_rate * 0.035)),
                )
                value = int(amplitude * wave * attack * release)
            for _ in range(channels):
                samples.append(value)

    return pygame.mixer.Sound(buffer=samples.tobytes())


def create_crystal_sound(notes, volume=0.04):
    """Sintetiza notas suaves com timbre cristalino e sem varreduras."""
    if not pygame.mixer.get_init():
        return None

    sample_rate, _, channels = pygame.mixer.get_init()
    samples = array("h")
    amplitude = int(32767 * volume)

    for frequency, duration in notes:
        sample_count = int(sample_rate * duration)
        for index in range(sample_count):
            if frequency == 0:
                value = 0
            else:
                progress = index / max(1, sample_count - 1)
                phase = 2 * math.pi * frequency * index / sample_rate
                attack = min(1.0, index / max(1, int(sample_rate * 0.012)))
                decay = math.exp(-2.8 * progress)
                wave = (
                    0.74 * math.sin(phase)
                    + 0.20 * math.sin(phase * 2.01)
                    + 0.06 * math.sin(phase * 4.03)
                )
                value = int(amplitude * wave * attack * decay)
            for _ in range(channels):
                samples.append(value)

    return pygame.mixer.Sound(buffer=samples.tobytes())


def shuffle_question_options(question):
    """Copia uma pergunta e embaralha suas alternativas preservando a resposta."""
    shuffled_question = question.copy()
    indexed_options = list(enumerate(question["options"]))
    random.shuffle(indexed_options)
    shuffled_question["options"] = [option for _, option in indexed_options]
    shuffled_question["answer"] = next(
        index
        for index, (original_index, _) in enumerate(indexed_options)
        if original_index == question["answer"]
    )
    return shuffled_question


def draw_rounded_rect(surface, color, rect, radius):
    """Desenha um retângulo com cantos arredondados."""
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_background(surface, faded=False):
    """Preenche a tela com a arte de robôs anos 80 ou com a cor padrão."""
    surface.fill(COLOR_BG)
    image = BACKGROUND_FADED if faded else BACKGROUND_OPAQUE
    if image is not None:
        surface.blit(image, (0, 0))


def draw_scrim(surface, rect, alpha=180, radius=20):
    """Escurece uma região para manter o texto legível sobre a arte de fundo."""
    overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(
        overlay, (10, 10, 25, alpha), overlay.get_rect(), border_radius=radius
    )
    surface.blit(overlay, rect.topleft)


def draw_text(surface, text, font, color, center_pos, max_width=None):
    """Desenha texto centralizado, com quebra de linha se necessário."""
    if max_width is None:
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=center_pos)
        surface.blit(text_surf, text_rect)
        return text_rect.height

    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test = ' '.join(current_line + [word])
        if font.size(test)[0] <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))

    total_height = 0
    line_height = font.get_height() + 4
    start_y = center_pos[1] - (len(lines) * line_height) // 2
    for i, line in enumerate(lines):
        text_surf = font.render(line, True, color)
        text_rect = text_surf.get_rect(center=(center_pos[0], start_y + i * line_height + line_height//2))
        surface.blit(text_surf, text_rect)
        total_height += line_height
    return total_height

def draw_button(surface, text, font, rect, color, hover_color, text_color, hovered):
    """Desenha um botão."""
    c = hover_color if hovered else color
    draw_rounded_rect(surface, c, rect, 12)
    draw_text(surface, text, font, text_color, rect.center)
    return rect


def draw_sound_button(surface, enabled):
    """Desenha um alto-falante indicando se o áudio está ligado ou desligado."""
    rect = pygame.Rect(SCREEN_WIDTH - 70, SCREEN_HEIGHT - 125, 50, 45)
    hovered = rect.collidepoint(pygame.mouse.get_pos())
    background = COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON
    icon_color = COLOR_SUCCESS if enabled else COLOR_ERROR
    draw_rounded_rect(surface, background, rect, 10)
    pygame.draw.rect(surface, COLOR_CARD_BORDER, rect, 2, border_radius=10)

    # Corpo do alto-falante.
    pygame.draw.rect(surface, icon_color, (rect.x + 10, rect.y + 17, 8, 11))
    pygame.draw.polygon(
        surface,
        icon_color,
        [
            (rect.x + 18, rect.y + 17),
            (rect.x + 28, rect.y + 10),
            (rect.x + 28, rect.y + 35),
            (rect.x + 18, rect.y + 28),
        ],
    )

    if enabled:
        pygame.draw.arc(
            surface,
            icon_color,
            (rect.x + 23, rect.y + 12, 17, 21),
            -math.pi / 3,
            math.pi / 3,
            2,
        )
        pygame.draw.arc(
            surface,
            icon_color,
            (rect.x + 20, rect.y + 7, 27, 31),
            -math.pi / 3,
            math.pi / 3,
            2,
        )
    else:
        pygame.draw.line(
            surface,
            icon_color,
            (rect.x + 34, rect.y + 15),
            (rect.x + 44, rect.y + 30),
            3,
        )
        pygame.draw.line(
            surface,
            icon_color,
            (rect.x + 44, rect.y + 15),
            (rect.x + 34, rect.y + 30),
            3,
        )
    return rect


def draw_footer(surface):
    """Desenha o rodapé e devolve as áreas dos links clicáveis."""
    footer_height = 70
    footer_rect = pygame.Rect(0, SCREEN_HEIGHT - footer_height, SCREEN_WIDTH, footer_height)
    draw_rounded_rect(surface, COLOR_FOOTER_BG, footer_rect, 0)

    # Linha separadora
    pygame.draw.line(surface, COLOR_CARD_BORDER, (20, SCREEN_HEIGHT - footer_height), 
                     (SCREEN_WIDTH - 20, SCREEN_HEIGHT - footer_height), 2)

    y_base = SCREEN_HEIGHT - footer_height + 12
    line1 = "Desenvolvido por Bruno José e Silva - brunojose1977@yahoo.com.br"
    line2 = "Licença: Apache 2.0  |  Autor: Bruno José e Silva"
    github_label = "GitHub: repositório do projeto"
    linkedin_label = "LinkedIn: Bruno José e Silva"
    separator = "  |  "

    mouse_pos = pygame.mouse.get_pos()
    txt1 = font_tiny.render(line1, True, COLOR_TEXT_DIM)
    txt2 = font_tiny.render(line2, True, COLOR_TEXT_DIM)
    surface.blit(txt1, (SCREEN_WIDTH//2 - txt1.get_width()//2, y_base))
    surface.blit(txt2, (SCREEN_WIDTH//2 - txt2.get_width()//2, y_base + 18))

    github_size = font_tiny.size(github_label)
    linkedin_size = font_tiny.size(linkedin_label)
    separator_size = font_tiny.size(separator)
    total_width = github_size[0] + separator_size[0] + linkedin_size[0]
    start_x = SCREEN_WIDTH//2 - total_width//2
    link_y = y_base + 36

    github_rect = pygame.Rect(start_x, link_y, *github_size)
    linkedin_rect = pygame.Rect(
        github_rect.right + separator_size[0], link_y, *linkedin_size
    )
    github_color = COLOR_SUCCESS if github_rect.collidepoint(mouse_pos) else COLOR_ACCENT
    linkedin_color = COLOR_SUCCESS if linkedin_rect.collidepoint(mouse_pos) else COLOR_ACCENT

    github_text = font_tiny.render(github_label, True, github_color)
    separator_text = font_tiny.render(separator, True, COLOR_TEXT_DIM)
    linkedin_text = font_tiny.render(linkedin_label, True, linkedin_color)
    surface.blit(github_text, github_rect)
    surface.blit(separator_text, (github_rect.right, link_y))
    surface.blit(linkedin_text, linkedin_rect)
    pygame.draw.line(surface, github_color, github_rect.bottomleft, github_rect.bottomright)
    pygame.draw.line(surface, linkedin_color, linkedin_rect.bottomleft, linkedin_rect.bottomright)

    return [
        (
            github_rect,
            "https://github.com/brunojose1977/"
            "brunojose1977-Fiap-PostTech-2026-Revisao_Fase1",
        ),
        (
            linkedin_rect,
            "https://www.linkedin.com/in/bruno-jos%C3%A9-e-silva-61140a2a/",
        ),
    ]

# =============================================================================
# CLASSE PRINCIPAL DO JOGO
# =============================================================================
class QuizGame:
    def __init__(self):
        self.state = "MENU"  # MENU, DIFFICULTY, PLAYING, RESULTS, REVIEW
        self.difficulty = None
        self.questions = []
        self.current_q_index = 0
        self.score = 0
        self.wrong_answers = []
        self.category_stats = {}
        self.selected_option = -1
        self.timer = 120  # 2 minutos em segundos
        self.timer_started = False
        self.last_tick = 0
        self.anim_offset = 0
        self.feedback_state = None  # None, "correct", "wrong"
        self.feedback_timer = 0
        self.review_index = 0
        self.footer_links = []
        self.points_per_hit = {"easy": 1000, "medium": 1250, "hard": 1500}
        self.sound_enabled = True
        self.results_sound_played = False
        self.intro_sound = None
        self.correct_sound = None
        self.wrong_sound = None
        self.results_sound = None
        self.bonus_sound = None
        self.setup_sounds()

    def setup_sounds(self):
        """Prepara áudio eletrônico discreto para a interface do jogo."""
        try:
            self.intro_sound = create_crystal_sound(
                [
                    (261.63, 0.28), (329.63, 0.28), (392.00, 0.28),
                    (0, 0.12), (329.63, 0.24), (440.00, 0.24),
                    (523.25, 0.32), (392.00, 0.24),
                ],
                volume=0.035,
            )
            self.correct_sound = create_crystal_sound(
                [
                    (659.25, 0.11), (880.00, 0.21),
                ],
                volume=0.045,
            )
            self.wrong_sound = create_sound(
                [
                    (440, 300, 0.14), (300, 220, 0.16),
                    (220, 160, 0.18),
                ],
                volume=0.03,
            )
            self.results_sound = create_crystal_sound(
                [
                    (783.99, 0.28), (659.25, 0.28), (523.25, 0.34),
                    (0, 0.10), (698.46, 0.24), (659.25, 0.24),
                    (587.33, 0.24), (523.25, 0.28),
                ],
                volume=0.035,
            )
            self.bonus_sound = create_sound(
                [
                    (520, 780, 0.10), (660, 990, 0.10),
                    (780, 1170, 0.12), (880, 1320, 0.12),
                    (990, 1480, 0.16),
                ],
                volume=0.03,
            )
            if self.sound_enabled and self.intro_sound:
                self.intro_sound.play()
        except pygame.error:
            # O jogo continua normalmente em computadores sem dispositivo de áudio.
            self.intro_sound = self.correct_sound = self.wrong_sound = None
            self.results_sound = self.bonus_sound = None

    def play_sound(self, sound):
        """Reproduz um som somente quando o áudio estiver ativado."""
        if self.sound_enabled and sound:
            return sound.play()
        return None

    def toggle_sound(self):
        """Alterna o áudio e interrompe imediatamente os sons ao desligá-lo."""
        self.sound_enabled = not self.sound_enabled
        if not self.sound_enabled and pygame.mixer.get_init():
            pygame.mixer.stop()

    def start_game(self, difficulty):
        self.difficulty = difficulty
        # Filtrar perguntas por dificuldade
        filtered = [q for q in QUESTIONS_DB if q["difficulty"] == difficulty]
        random.shuffle(filtered)

        limits = {"easy": 10, "medium": 20, "hard": 30}
        self.questions = [
            shuffle_question_options(question)
            for question in filtered[:limits[difficulty]]
        ]

        self.current_q_index = 0
        self.score = 0
        self.wrong_answers = []
        self.category_stats = {}
        self.selected_option = -1
        self.timer = 120
        self.timer_started = False
        self.feedback_state = None
        self.results_sound_played = False
        self.state = "PLAYING"

    def next_question(self):
        if self.current_q_index < len(self.questions) - 1:
            self.current_q_index += 1
            self.selected_option = -1
            self.timer = 120
            self.timer_started = False
            self.feedback_state = None
        else:
            self.state = "RESULTS"

    def check_answer(self, option_idx):
        q = self.questions[self.current_q_index]
        cat = q["category"]

        if cat not in self.category_stats:
            self.category_stats[cat] = {"correct": 0, "total": 0}
        self.category_stats[cat]["total"] += 1

        if option_idx == q["answer"]:
            self.score += 1
            self.category_stats[cat]["correct"] += 1
            self.feedback_state = "correct"
            self.play_sound(self.correct_sound)
        else:
            self.wrong_answers.append({
                "question": q["question"],
                "your_answer": q["options"][option_idx],
                "correct_answer": q["options"][q["answer"]],
                "explanation": q["explanation"],
                "category": cat
            })
            self.feedback_state = "wrong"
            self.play_sound(self.wrong_sound)

        self.feedback_timer = pygame.time.get_ticks()

    def update_timer(self):
        if self.state == "PLAYING" and self.timer_started and self.feedback_state is None:
            now = pygame.time.get_ticks()
            if now - self.last_tick >= 1000:
                self.timer -= 1
                self.last_tick = now
                if self.timer <= 0:
                    # Tempo esgotado - conta como erro
                    q = self.questions[self.current_q_index]
                    cat = q["category"]
                    if cat not in self.category_stats:
                        self.category_stats[cat] = {"correct": 0, "total": 0}
                    self.category_stats[cat]["total"] += 1
                    self.wrong_answers.append({
                        "question": q["question"],
                        "your_answer": "TEMPO ESGOTADO",
                        "correct_answer": q["options"][q["answer"]],
                        "explanation": q["explanation"],
                        "category": cat
                    })
                    self.play_sound(self.wrong_sound)
                    self.next_question()

    def draw_menu(self):
        draw_background(screen)
        draw_scrim(screen, pygame.Rect(140, 70, SCREEN_WIDTH - 280, 550))

        # Título animado
        self.anim_offset = math.sin(pygame.time.get_ticks() / 500) * 5
        draw_text(screen, "FIAP PosTech 2026", font_title, COLOR_ACCENT, 
                  (SCREEN_WIDTH//2, 120 + self.anim_offset))
        draw_text(screen, "IA para DEVs - Revisão Fase 1", font_subtitle, COLOR_TEXT, 
                  (SCREEN_WIDTH//2, 190))

        # Subtítulo
        draw_text(screen, "Quiz Gamificado de Conhecimentos", font_text, COLOR_TEXT_DIM, 
                  (SCREEN_WIDTH//2, 260))

        # Botões principais
        btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 250, 350, 300, 60)
        btn_exit = pygame.Rect(SCREEN_WIDTH//2 + 70, 350, 180, 60)
        mouse_pos = pygame.mouse.get_pos()
        hovered = btn_rect.collidepoint(mouse_pos)
        draw_button(screen, "INICIAR JOGO", font_subtitle, btn_rect, 
                   COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_TEXT, hovered)
        exit_hovered = btn_exit.collidepoint(mouse_pos)
        draw_button(
            screen,
            "SAIR",
            font_subtitle,
            btn_exit,
            (120, 35, 55),
            (175, 45, 70),
            COLOR_TEXT,
            exit_hovered,
        )

        # Instruções
        instructions = [
            "• Responda perguntas sobre os conteúdos da Fase 1",
            "• Escolha entre os níveis: Fácil, Médio ou Difícil",
            "• Você tem até 2 minutos para cada pergunta",
            "• Receba feedback detalhado no final"
        ]
        y_start = 460
        for i, inst in enumerate(instructions):
            draw_text(screen, inst, font_small, COLOR_TEXT_DIM, 
                     (SCREEN_WIDTH//2, y_start + i * 35))

        self.footer_links = draw_footer(screen)
        return btn_rect, btn_exit

    def draw_difficulty(self):
        screen.fill(COLOR_BG)
        draw_text(screen, "ESCOLHA O NÍVEL", font_title, COLOR_ACCENT, 
                  (SCREEN_WIDTH//2, 120))

        mouse_pos = pygame.mouse.get_pos()
        buttons = []

        # Fácil
        btn_easy = pygame.Rect(SCREEN_WIDTH//2 - 200, 250, 400, 70)
        h = btn_easy.collidepoint(mouse_pos)
        draw_button(screen, "FÁCIL (10 perguntas)", font_subtitle, btn_easy,
                   (40, 120, 60), (60, 160, 80), COLOR_TEXT, h)
        buttons.append((btn_easy, "easy"))

        # Médio
        btn_med = pygame.Rect(SCREEN_WIDTH//2 - 200, 350, 400, 70)
        h = btn_med.collidepoint(mouse_pos)
        draw_button(screen, "MÉDIO (20 perguntas)", font_subtitle, btn_med,
                   (120, 100, 30), (160, 130, 40), COLOR_TEXT, h)
        buttons.append((btn_med, "medium"))

        # Difícil
        btn_hard = pygame.Rect(SCREEN_WIDTH//2 - 200, 450, 400, 70)
        h = btn_hard.collidepoint(mouse_pos)
        draw_button(screen, "DIFÍCIL (30 perguntas)", font_subtitle, btn_hard,
                   (140, 40, 40), (180, 50, 50), COLOR_TEXT, h)
        buttons.append((btn_hard, "hard"))

        btn_exit = pygame.Rect(SCREEN_WIDTH//2 - 100, 570, 200, 50)
        h = btn_exit.collidepoint(mouse_pos)
        draw_button(
            screen, "SAIR", font_text, btn_exit,
            (120, 35, 55), (175, 45, 70), COLOR_TEXT, h
        )

        self.footer_links = draw_footer(screen)
        return buttons, btn_exit

    def draw_playing(self):
        draw_background(screen, faded=True)

        if not self.timer_started:
            self.timer_started = True
            self.last_tick = pygame.time.get_ticks()

        q = self.questions[self.current_q_index]

        # Barra de progresso
        progress = (self.current_q_index) / len(self.questions)
        bar_width = SCREEN_WIDTH - 100
        pygame.draw.rect(screen, (40, 40, 60), (50, 20, bar_width, 20), border_radius=10)
        pygame.draw.rect(screen, COLOR_ACCENT, (50, 20, int(bar_width * progress), 20), border_radius=10)
        prog_text = font_small.render(f"Pergunta {self.current_q_index + 1} de {len(self.questions)}", True, COLOR_TEXT)
        screen.blit(prog_text, (SCREEN_WIDTH//2 - prog_text.get_width()//2, 45))

        # Timer
        timer_color = COLOR_SUCCESS if self.timer > 30 else COLOR_WARNING if self.timer > 10 else COLOR_ERROR
        timer_text = font_subtitle.render(f"⏱ {self.timer}s", True, timer_color)
        screen.blit(timer_text, (SCREEN_WIDTH - 150, 20))

        # Card da pergunta
        card_rect = pygame.Rect(50, 90, SCREEN_WIDTH - 100, 160)
        draw_rounded_rect(screen, COLOR_CARD_BG, card_rect, 16)
        pygame.draw.rect(screen, COLOR_CARD_BORDER, card_rect, 3, border_radius=16)

        # Categoria
        cat_text = font_tiny.render(f"📚 {q['category']} | Nível: {q['difficulty'].upper()}", True, COLOR_ACCENT)
        screen.blit(cat_text, (70, 105))

        # Pergunta
        draw_text(screen, q["question"], font_text, COLOR_TEXT, 
                 (SCREEN_WIDTH//2, 185), max_width=SCREEN_WIDTH - 140)

        # Opções
        mouse_pos = pygame.mouse.get_pos()
        option_buttons = []
        y_start = 280
        for i, opt in enumerate(q["options"]):
            opt_rect = pygame.Rect(80, y_start + i * 75, SCREEN_WIDTH - 160, 60)

            # Cor baseada no estado
            if self.feedback_state == "correct" and i == q["answer"]:
                color = COLOR_SUCCESS
                border = COLOR_SUCCESS
            elif self.feedback_state == "wrong" and i == self.selected_option:
                color = COLOR_ERROR
                border = COLOR_ERROR
            elif self.feedback_state == "wrong" and i == q["answer"]:
                color = COLOR_SUCCESS
                border = COLOR_SUCCESS
            else:
                color = COLOR_BUTTON
                border = COLOR_CARD_BORDER
                if self.feedback_state is None and opt_rect.collidepoint(mouse_pos):
                    color = COLOR_BUTTON_HOVER

            draw_rounded_rect(screen, color, opt_rect, 10)
            pygame.draw.rect(screen, border, opt_rect, 2, border_radius=10)

            label = chr(65 + i) + ") " + opt
            draw_text(screen, label, font_small, COLOR_TEXT, opt_rect.center, max_width=SCREEN_WIDTH - 200)
            option_buttons.append(opt_rect)

        # Feedback temporário
        if self.feedback_state is not None:
            if pygame.time.get_ticks() - self.feedback_timer > 1200:
                self.next_question()

        btn_menu = pygame.Rect(210, 655, 180, 40)
        h = btn_menu.collidepoint(mouse_pos)
        draw_button(
            screen, "MENU", font_small, btn_menu,
            COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_TEXT, h
        )

        btn_exit = pygame.Rect(410, 655, 140, 40)
        h = btn_exit.collidepoint(mouse_pos)
        draw_button(
            screen, "SAIR", font_small, btn_exit,
            (120, 35, 55), (175, 45, 70), COLOR_TEXT, h
        )

        self.footer_links = draw_footer(screen)
        return option_buttons, btn_menu, btn_exit

    def draw_results(self):
        draw_background(screen, faded=True)

        draw_text(screen, "RESULTADOS FINAIS", font_title, COLOR_ACCENT, 
                  (SCREEN_WIDTH//2, 60))

        total = len(self.questions)
        correct = self.score
        wrong = total - correct
        pct_correct = (correct / total * 100) if total > 0 else 0
        pct_wrong = (wrong / total * 100) if total > 0 else 0
        base_points = correct * self.points_per_hit[self.difficulty]
        perfect_bonus = 2000 if total > 0 and correct == total else 0
        final_score = base_points + perfect_bonus

        if not self.results_sound_played:
            channel = self.play_sound(self.results_sound)
            if channel and perfect_bonus and self.bonus_sound:
                channel.queue(self.bonus_sound)
            self.results_sound_played = True

        # Card principal
        card = pygame.Rect(100, 110, SCREEN_WIDTH - 200, 180)
        draw_rounded_rect(screen, COLOR_CARD_BG, card, 16)
        pygame.draw.rect(screen, COLOR_CARD_BORDER, card, 3, border_radius=16)

        draw_text(screen, f"✅ Acertos: {correct} de {total} ({pct_correct:.1f}%)", 
                 font_subtitle, COLOR_SUCCESS, (SCREEN_WIDTH//2, 150))
        draw_text(screen, f"❌ Erros: {wrong} ({pct_wrong:.1f}%)", 
                 font_subtitle, COLOR_ERROR, (SCREEN_WIDTH//2, 200))
        bonus_text = " + bônus perfeito de 2.000" if perfect_bonus else ""
        draw_text(
            screen,
            f"🏆 SCORE FINAL: {final_score:,} pontos{bonus_text}".replace(",", "."),
            font_text,
            COLOR_WARNING,
            (SCREEN_WIDTH//2, 255),
        )

        # Desempenho por categoria
        y_cat = 320
        draw_text(screen, "DESEMPENHO POR ASSUNTO", font_text, COLOR_ACCENT, 
                 (SCREEN_WIDTH//2, y_cat))

        y_cat += 40
        for cat, stats in sorted(self.category_stats.items()):
            pct = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            if pct >= 70:
                color = COLOR_SUCCESS
                emoji = "🟢"
            elif pct >= 50:
                color = COLOR_WARNING
                emoji = "🟡"
            else:
                color = COLOR_ERROR
                emoji = "🔴"

            txt = f"{emoji} {cat}: {stats['correct']}/{stats['total']} ({pct:.0f}%)"
            draw_text(screen, txt, font_small, color, (SCREEN_WIDTH//2, y_cat), max_width=SCREEN_WIDTH - 200)
            y_cat += 32

        # Botões
        mouse_pos = pygame.mouse.get_pos()

        btn_review = pygame.Rect(190, 560, 250, 50)
        h = btn_review.collidepoint(mouse_pos)
        draw_button(screen, "📋 Revisar Erros", font_small, btn_review,
                   COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_TEXT, h)

        btn_menu = pygame.Rect(475, 560, 250, 50)
        h = btn_menu.collidepoint(mouse_pos)
        draw_button(screen, "🔄 Jogar Novamente", font_small, btn_menu,
                   COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_TEXT, h)

        btn_exit = pygame.Rect(760, 560, 250, 50)
        h = btn_exit.collidepoint(mouse_pos)
        draw_button(
            screen, "SAIR", font_small, btn_exit,
            (120, 35, 55), (175, 45, 70), COLOR_TEXT, h
        )

        # Conselho
        if pct_correct >= 80:
            msg = "🎉 Excelente! Você domina os conteúdos da Fase 1!"
        elif pct_correct >= 60:
            msg = "👍 Bom! Alguns tópicos precisam de revisão."
        else:
            msg = "📚 Continue estudando! Revise os materiais da Fase 1."
        draw_text(screen, msg, font_text, COLOR_ACCENT, (SCREEN_WIDTH//2, 650))

        self.footer_links = draw_footer(screen)
        return btn_review, btn_menu, btn_exit

    def draw_review(self):
        screen.fill(COLOR_BG)

        if not self.wrong_answers:
            draw_text(screen, "PARABÉNS! Você não errou nenhuma questão!", 
                     font_subtitle, COLOR_SUCCESS, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            btn_back = pygame.Rect(SCREEN_WIDTH//2 - 100, 500, 200, 50)
            h = btn_back.collidepoint(pygame.mouse.get_pos())
            draw_button(screen, "Voltar", font_text, btn_back, COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_TEXT, h)
            self.footer_links = draw_footer(screen)
            return [(btn_back, "menu")], True

        wa = self.wrong_answers[self.review_index]

        draw_text(screen, f"REVISÃO DE ERROS ({self.review_index + 1}/{len(self.wrong_answers)})", 
                 font_title, COLOR_ACCENT, (SCREEN_WIDTH//2, 50))

        # Card pergunta
        card = pygame.Rect(50, 90, SCREEN_WIDTH - 100, 500)
        draw_rounded_rect(screen, COLOR_CARD_BG, card, 16)
        pygame.draw.rect(screen, COLOR_CARD_BORDER, card, 3, border_radius=16)

        y = 120
        # Pergunta
        q_surf = font_text.render("Pergunta:", True, COLOR_ACCENT)
        screen.blit(q_surf, (70, y))
        y += 35
        y += draw_text(screen, wa["question"], font_small, COLOR_TEXT, 
                      (SCREEN_WIDTH//2, y), max_width=SCREEN_WIDTH - 140)

        y += 25
        # Sua resposta
        r_surf = font_small.render(f"❌ Sua resposta: {wa['your_answer']}", True, COLOR_ERROR)
        screen.blit(r_surf, (70, y))
        y += 35

        # Resposta correta
        c_surf = font_small.render(f"✅ Resposta correta: {wa['correct_answer']}", True, COLOR_SUCCESS)
        screen.blit(c_surf, (70, y))
        y += 45

        # Explicação
        e_surf = font_small.render("Explicação:", True, COLOR_ACCENT)
        screen.blit(e_surf, (70, y))
        y += 30
        y += draw_text(screen, wa["explanation"], font_small, COLOR_TEXT_DIM, 
                      (SCREEN_WIDTH//2, y), max_width=SCREEN_WIDTH - 140)

        # Categoria
        cat_surf = font_tiny.render(f"Categoria: {wa['category']}", True, COLOR_TEXT_DIM)
        screen.blit(cat_surf, (70, 560))

        # Botões navegação
        mouse_pos = pygame.mouse.get_pos()

        buttons = []
        if self.review_index > 0:
            btn_prev = pygame.Rect(100, 620, 180, 45)
            h = btn_prev.collidepoint(mouse_pos)
            draw_button(screen, "◀ Anterior", font_small, btn_prev, COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_TEXT, h)
            buttons.append((btn_prev, "prev"))

        if self.review_index < len(self.wrong_answers) - 1:
            btn_next = pygame.Rect(SCREEN_WIDTH - 280, 620, 180, 45)
            h = btn_next.collidepoint(mouse_pos)
            draw_button(screen, "Próxima ▶", font_small, btn_next, COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_TEXT, h)
            buttons.append((btn_next, "next"))

        btn_back = pygame.Rect(SCREEN_WIDTH//2 - 90, 620, 180, 45)
        h = btn_back.collidepoint(mouse_pos)
        draw_button(screen, "🏠 Menu", font_small, btn_back, COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_TEXT, h)
        buttons.append((btn_back, "menu"))

        self.footer_links = draw_footer(screen)
        return buttons, False

    def run(self):
        running = True

        while running:
            mouse_pos = pygame.mouse.get_pos()
            clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state in ["PLAYING", "RESULTS", "REVIEW"]:
                            self.state = "MENU"

            # Atualizações
            if self.state == "PLAYING":
                self.update_timer()

            # Renderização
            if self.state == "MENU":
                btn, btn_exit = self.draw_menu()
                if clicked:
                    if btn.collidepoint(mouse_pos):
                        self.state = "DIFFICULTY"
                    elif btn_exit.collidepoint(mouse_pos):
                        running = False

            elif self.state == "DIFFICULTY":
                btns, btn_exit = self.draw_difficulty()
                if clicked:
                    if btn_exit.collidepoint(mouse_pos):
                        running = False
                    else:
                        for rect, diff in btns:
                            if rect.collidepoint(mouse_pos):
                                self.start_game(diff)

            elif self.state == "PLAYING":
                opts, btn_menu, btn_exit = self.draw_playing()
                if clicked:
                    if btn_exit.collidepoint(mouse_pos):
                        running = False
                    elif btn_menu.collidepoint(mouse_pos):
                        self.state = "MENU"
                    elif self.feedback_state is None:
                        for i, rect in enumerate(opts):
                            if rect.collidepoint(mouse_pos):
                                self.selected_option = i
                                self.check_answer(i)

            elif self.state == "RESULTS":
                btn_review, btn_menu, btn_exit = self.draw_results()
                if clicked:
                    if btn_review.collidepoint(mouse_pos):
                        self.review_index = 0
                        self.state = "REVIEW"
                    elif btn_menu.collidepoint(mouse_pos):
                        self.state = "MENU"
                    elif btn_exit.collidepoint(mouse_pos):
                        running = False

            elif self.state == "REVIEW":
                buttons, empty = self.draw_review()
                if clicked:
                    for item in buttons:
                        if len(item) == 2:
                            rect, action = item
                            if rect.collidepoint(mouse_pos):
                                if action == "prev" and self.review_index > 0:
                                    self.review_index -= 1
                                elif action == "next" and self.review_index < len(self.wrong_answers) - 1:
                                    self.review_index += 1
                                elif action == "menu":
                                    self.state = "MENU"

            sound_button = draw_sound_button(screen, self.sound_enabled)

            if clicked:
                if sound_button.collidepoint(mouse_pos):
                    self.toggle_sound()
                for link_rect, url in self.footer_links:
                    if link_rect.collidepoint(mouse_pos):
                        webbrowser.open(url, new=2)
                        break

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()

# =============================================================================
# EXECUÇÃO
# =============================================================================
if __name__ == "__main__":
    game = QuizGame()
    game.run()
