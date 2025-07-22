# 🏋️ Corretor de Agachamento com IA

Analise e melhore a sua forma de exectar agachamentos com feedback visual e um relatório pós-análise.

![gif agachamento](https://github.com/SidneyJunior01234/Corretor_Agachamento/blob/main/relatorios/imagens/agachamento%20gif.gif)

## 📑 Sumário
   * Estrutura do Projeto

   * Funcionalidades

   * Introdução

   * Metodologia

   * Resultados da Análise

   * Métricas Gerais

   * Gráficos e Visualizações

   * Conclusão

   * Interface Interativa

   * Tecnologias

   * Como Executar

   * Licença

   * Referências Bibliográficas

## 📁 Estrutura do Projeto
    Corretor_Agachamento/
    ├── app.py
    ├── data/
    │   ├── brutos/
    │   │   └── video_exemplo.mp4
    ├── config/
    │   └── configuracoes.py
    ├── .gitignore
    ├── relatorios/
    │   ├── imagens/
    │   │   └── agachamento gif.gif
    │   │   └── avatar_correto.png
    │   │   └── avatar_trasicao.png
    │   │   └── grafico1.png
    │   │   └── grafico2.png
    │   │   └── grafico3.png
    │   │   └── interface.gif        
    │   └── README.md
    ├── requirements.txt
    └── src/
        ├── __init__.py
        ├── core/
        │   ├── __init__.py
        │   ├── analisador_agachamento.py
        │   ├── calculador_angulo.py
        │   └── detector_pose.py
        ├── manipulador_dados/
        │   ├── __init__.py
        │   └── gerenciador_csv.py
        └── visualizacao/
            ├── __init__.py
            ├── desenhista_cv2.py
            └── gerador_graficos.py
    ├── temp_upload/
    
## 🔍 Funcionalidades
   1. Detecção de pose em vídeos de agachamento.

   2. Análise do ângulo dos joelhos e da queda do quadril.

   3. Diferenciação dos estados de movimento: "Em Pé", "Agachado" e "Transição/Indefinido".

   4. Feedback visual no vídeo (cores para indicação de estado).

   5. Ajuste de limiares de agachamento via sliders na interface Streamlit, permitindo customização para diferentes mobilidades (ex: idosos).

   6. Geração de relatório detalhado com métricas e gráficos interativos (Plotly).

   7. Cálculo de tempo total em pé e duração de agachamentos individuais e seus intervalos de recuperação.

## 📌 Introdução

A execução correta do agachamento é fundamental para maximizar os benefícios do exercício e prevenir lesões. Este projeto propõe um sistema inteligente de visão computacional para auxiliar usuários na prática do agachamento, oferecendo feedback em tempo real e uma análise pós-exercício detalhada.

Utilizando a biblioteca MediaPipe Pose para detecção de landmarks corporais, o sistema monitora continuamente a posição dos joelhos e do quadril, classificando o movimento em diferentes estados. A interface interativa desenvolvida com Streamlit permite o upload de vídeos e o ajuste de parâmetros cruciais, como os limiares de ângulo do joelho e a profundidade de queda do quadril, tornando-o adaptável a diversos perfis de usuários, desde iniciantes a indivíduos com mobilidade reduzida.

O Corretor de Agachamento visa facilitar o acesso a um feedback sobre a execução de exercícios, contribuindo para uma prática física mais segura.

## ⚙️ Metodologia
### O processo de análise do agachamento envolve as seguintes etapas:

   1. Detecção de Pose: O vídeo do usuário é processado frame a frame utilizando o MediaPipe Pose. Isso extrai os landmarks (pontos chave) do corpo, como ombros, quadris, joelhos, tornozelos e pés.

   2. Cálculo de Ângulos: Com os landmarks, são calculados os ângulos das articulações do joelho e tornozelo para ambos os lados do corpo. A posição vertical do quadril também é monitorada.

   3. Calibração Inicial: No primeiro frame, a posição Y do quadril é calibrada como a posição de referência "em pé".

   4. Classificação do Estado do Agachamento: Utilizando os ângulos calculados e a queda do quadril em relação à posição inicial, o sistema classifica o estado do corpo em:

   5. "Em Pé": Joelhos estendidos (ângulo acima de um limiar_joelho_em_pe) e quadril na posição inicial (ou levemente abaixo).

  ![agachamento transicao](https://github.com/SidneyJunior01234/Corretor_Agachamento/blob/main/relatorios/imagens/avatar_trasicao.png)
  
   6. "Agachado": Joelhos flexionados (ângulo abaixo de um limiar_joelho_agachado) e quadril com queda significativa (acima de um limiar_queda_y_percentual em relação à posição inicial).

  ![aachamento correto](https://github.com/SidneyJunior01234/Corretor_Agachamento/blob/main/relatorios/imagens/avatar_correto.png)

   7. "Transição/Indefinido": Entre os estados "Em Pé" e "Agachado", ou em posições que não se encaixam claramente.

   8. Feedback Visual: O vídeo processado é exibido, com os landmarks e as linhas do esqueleto desenhados. A cor do esqueleto muda para indicar o estado atual (ex: verde para agachado correto, vermelho para pés desalinhados, amarelo para outros estados).

   9. Gravação de Dados: A cada frame, os dados da pose (ângulos, posições e estado) são registrados em um arquivo CSV (dados_agachamento.csv) para análise posterior.

   10. Relatório Final: Após o processamento do vídeo, um relatório detalhado é gerado, incluindo métricas resumidas e gráficos interativos.

### Ajustes de Limiares
Para garantir a adaptabilidade a diferentes usuários, o sistema permite o ajuste dinâmico dos seguintes limiares via sliders na interface:

   1. Ângulo Mín. Joelho "Em Pé": Ângulo mínimo para o joelho ser considerado esticado.

   2. Ângulo Máx. Joelho "Agachado": Ângulo máximo para o joelho ser considerado flexionado o suficiente para um agachamento.

   3. Queda do Quadril para Agachamento (%): Percentual da altura do corpo que o quadril deve descer para o agachamento ser considerado profundo.

## 📊 Resultados da Análise
### Métricas Gerais
Após a análise do vídeo, obtivemos as seguintes métricas gerais:

   1. Tempo total em pé (geral): [VALOR_DO_TEMPO_TOTAL_EM_PE] segundos

   2. Número de agachamentos completos detectados: [NÚMERO_DE_AGACHAMENTOS_DETECTADOS]

   3. Duração média por agachamento: [DURACAO_MEDIA_AGACHAMENTOS] segundos

   4. Tempo médio de recuperação entre agachamentos: [TEMPO_MEDIO_EM_PE_ENTRE_AGACHAMENTOS] segundos

## Gráficos e Visualizações
Para uma análise mais detalhada da execução do agachamento, os seguintes gráficos interativos foram gerados:

![grafico 1](https://github.com/SidneyJunior01234/Corretor_Agachamento/blob/main/relatorios/imagens/grafico1.png)
*Gráfico 1: Variação dos Ângulos dos Joelhos e Tornozelos*

![grafico 2](https://github.com/SidneyJunior01234/Corretor_Agachamento/blob/main/relatorios/imagens/grafico2.png)
*Gráfico 2: Posição Y Média do Quadril ao Longo do Tempo*

![grafico 3](https://github.com/SidneyJunior01234/Corretor_Agachamento/blob/main/relatorios/imagens/grafico3.png)
*Gráfico 3: Duração de Cada Agachamento e Tempo em Pé*

## ✅ Conclusão
O Corretor de Agachamento se mostrou uma ferramenta que pode auxiliar na análise e correção da forma do agachamento. A capacidade de ajustar os limiares de detecção através da interface Streamlit é crucial para adaptar o sistema a diferentes usuários e níveis de mobilidade, como no caso de agachamentos mais rasos para idosos.

As métricas e os gráficos interativos fornecem um feedback quantitativo e visual, permitindo ao usuário entender melhor seu desempenho e identificar áreas para melhoria.

## 💻 Interface Interativa
A interface do aplicativo foi desenvolvida com Streamlit, oferecendo uma experiência amigável e intuitiva para o upload de vídeos, visualização da análise e ajuste de parâmetros.

![gif carregando video](https://github.com/SidneyJunior01234/Corretor_Agachamento/blob/main/relatorios/imagens/interface.gif)

## 🛠️ Tecnologias
  * Python 3.12

  * MediaPipe

  * OpenCV

  * Streamlit

  * Plotly

  * Pandas

  * NumPy

## 👥 Equipe do Projeto
O desenvolvimento do Corretor de Agachamento foi realizado por:

Sidney Alves dos Santos Junior / github.com/SidneyJunior01234

## 🚀 Como Executar
Baixe o repositório (substitua SEU_USUARIO e SEU_REPOSITORIO):

```
mkdir Corretor_Agachamento
cd Corretor_Agachamento
git clone https://github.com/SidneyJunior01234/Corretor_Agachamento.git
```

Crie e ative o ambiente virtual venv:

```
python3 -m venv .venv
source .venv/bin/activate  # No Linux/macOS
# .venv\Scripts\activate   # No Windows
```

Instale as bibliotecas:

```
pip install -r requirements.txt
```

Execute o projeto:

```
streamlit run app.py
```

## 📄 Licença
O Corretor de Agachamento é licenciado sob a [Licença MIT](https://github.com/SidneyJunior01234/Corretor_Agachamento/blob/main/LICENSE).

## 📚 Referências Bibliográficas
MediaPipe. Disponível em: https://google.github.io/mediapipe/

Streamlit. Disponível em: https://streamlit.io/

Plotly. Disponível em: https://plotly.com/python/

OpenCV. Open Source Computer Vision Library. Disponível em: https://opencv.org/

Seaborn. Statistical data visualization. Disponível em: https://seaborn.pydata.org/

Pexels. Plataforma de vídeos e fotos de alta qualidade, licenciadas para uso gratuito. Disponível em: [https://www.pexels.com/](https://www.pexels.com/)
