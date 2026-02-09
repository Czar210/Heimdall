# Tennis Vision & Physics Engine 🎾

> "Este projeto implementa um pipeline end-to-end de análise de tênis. Ele ingere vídeos brutos, utiliza uma CNN especializada (TrackNet) para segmentação de objetos pequenos em alta velocidade e aplica modelagem física para extrair métricas de jogo (velocidade, spin, mapa de calor de quiques). O foco é provar que hardware de consumo + algoritmos inteligentes podem rivalizar com sistemas proprietários de alto custo."

## 1. O Problema (Business Case)

No circuito profissional (ATP/WTA), usa-se o sistema **Hawk-Eye** com 10+ câmeras de alta velocidade e hardware dedicado de milhares de dólares para gerar estatísticas.
**Nosso objetivo:** Democratizar essa análise usando Visão Computacional moderna (Deep Learning) para extrair dados similares usando apenas um vídeo de YouTube ou celular (vídeo monocular).

## 2. A Stack Tecnológica (O "Techporn")

### Computer Vision Backbone: TrackNetV2
Utilizamos uma Rede Neural Convolucional Profunda baseada em U-Net.
*   **Por que V2 e não YOLO?** YOLO é ótimo para "coisas" (pessoas, carros), mas péssimo para objetos minúsculos em movimento rápido com motion blur. O TrackNet trata 3 frames consecutivos como um "bloco de tempo", aprendendo a trajetória e não apenas a aparência estática.

### Pipeline de Dados
*   **Python + OpenCV + Pandas**
*   Transformação de dados não estruturados (pixels de vídeo) em dados estruturados (séries temporais de coordenadas $x, y$).

### Physics Engine (Diferencial de Data Science)
*   **Conversão de Espaço:** Homografia (Matriz de Projeção) para transformar coordenadas de tela 2D em coordenadas de quadra 3D (Metros).
*   **Detecção de Eventos:** Cálculo de derivadas (velocidade/aceleração) para identificar hits (raquetadas) e bounces (quiques) sem precisar de um modelo de ML supervisionado para isso.

## 3. Por que começar com o TrackNetV2?

Essa é uma decisão estratégica de Engenharia:
*   **Complexidade vs. Valor:** O V3 introduz "Inpainting" (SOTA), mas adiciona complexidade.
*   **Princípio MVP:** O V2 já oferece 95% de precisão em vídeos claros. Melhor ter dados "sujos" hoje (limpáveis com filtros) do que nenhum dado.
*   **Modularidade:** O modelo é uma peça de LEGO. Trocar V2 por V3 futuramente é trivial.

## 4. Onde a "Ciência" entra (Fase 2)

Depois de gerar o CSV com as coordenadas brutas, aplicamos modelagem física:
*   **Ruído:** Filtros de Savitzky-Golay ou Kalman para suavizar a trajetória.
*   **Spin:** Ajuste de parábola na trajetória.
    *   Se a aceleração $g > 9.8 m/s^2$: **Topspin** (Efeito Magnus empurra para baixo).
    *   Se $g < 9.8 m/s^2$: **Slice** (Efeito Magnus sustenta a bola).

---

## Como Rodar

1.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

2.  Execute o pipeline principal:
    ```bash
    python main.py
    ```
