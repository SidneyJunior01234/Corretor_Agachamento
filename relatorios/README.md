# O Corretor de Agachamentos

## Introdução

O agachamento é um dos exercícios mais eficazes e completos para o desenvolvimento da força e da massa muscular dos membros inferiores e do core. No entanto, sua execução incorreta pode levar a sérias lesões, comprometendo não só o desempenho, mas a saúde a longo prazo. Problemas como desalinhamento dos joelhos, falta de profundidade e instabilidade da base são comuns, especialmente entre iniciantes ou em treinos sem supervisão adequada.

É nesse cenário que surge a necessidade de uma ferramenta acessível que auxilie os praticantes a aprimorar sua técnica. O projeto apresenta um Corretor de Agachamentos que utiliza visão computacional e o modelo de detecção de pose MediaPipe Pose para monitorar e analisar a execução do agachamento. A aplicação foi desenvolvida para identificar os principais erros relacionados a postura, como a abertura dos pés em relação aos ombros e a profundidade do movimento, onde um avatar por meio de cores retorna um feedback visual sobre o exercício.

## Desenvolvimento

O desenvolvimento do Corretor de Agachamentos baseia-se na visão computacional para análise de movimento e em algoritmos de processamento de dados, cujos os principais métodos e técnicas utilizados foram:

### 1. Detecção de Pose com MediaPipe Pose

O MediaPipe Pose identifica 33 pontos cruciais no corpo humano (como ombros, quadris, joelhos, tornozelos e calcanhares) em cada frame do vídeo. Esses pontos são fornecidos com suas coordenadas X, Y (no espaço 2D da imagem) e Z (profundidade relativa), além de uma pontuação de visibilidade.

### 2. Cálculo de Ângulos Articulares e Análise da Posição Vertical do Quadril

Com os landmarks identificados, é utilizado a geometria analítica para calcular os ângulos formados pelas principais articulações envolvidas no agachamento.

  * Ângulos do Joelho: avalia a profundidade do agachamento. Calculamos o ângulo formado entre o quadril, o joelho e o tornozelo (para ambos os lados, esquerdo e direito). Um ângulo menor indica maior flexão do joelho, característico de um agachamento mais profundo.
  * Ângulos do Tornozelo: verifica a estabilidade da base. O ângulo é calculado entre o joelho, o tornozelo e o calcanhar.

Para complementar a avaliação da profundidade e determinar os estados de "Em Pé" e "Agachado", monitoramos a posição vertical (coordenada Y) do quadril.

 * Calibração Inicial: A posição Y média do quadril no primeiro frame.
 * Detecção de Queda: Comparamos a posição Y atual do quadril com a posição inicial. Se a queda exceder um limiar (definido como uma porcentagem da altura do frame para adaptabilidade), isso indica que o usuário desceu o suficiente para ser considerado em um agachamento ou transição.

### 3. Avaliação da Distância dos Pés em Relação aos Ombros

Um agachamento eficaz e seguro requer que os pés estejam posicionados aproximadamente na largura dos ombros.

 * Cálculo de Distâncias: A distância horizontal (X) entre os ombros e a distância horizontal entre os tornozelos (ou calcanhares) são calculadas em pixels.

 * Tolerância Percentual: Definido uma TOLERANCIA_PES_OMBRO_PERCENTUAL para permitir uma pequena variação na largura dos pés em relação aos ombros.

### 4. Estados do Agachamento

O sistema classifica o estado do usuário em "Em Pé", "Agachado" ou "Transição/Indefinido" com base nos ângulos dos joelhos e na posição do quadril.

 * "Em Pé": Ângulo do joelho maior que THRESHOLD_ANGULO_JOELHO_EM_PE e quadril próximo à posição inicial.
 * "Agachado": Ângulo do joelho menor que THRESHOLD_ANGULO_JOELHO_AGACHADO e quadril com queda significativa em relação à posição inicial.
 * "Transição/Indefinido": Qualquer estado intermediário.

### 5. Feedback Visual e Textual

Visual na Tela: A cor dos landmarks no avatar muda dinamicamente:

 * Verde: Indica que o usuário está em uma posição de agachamento correta.
 * Amarelo: Representa um estado de transição ou indefinido.
 * Vermelho: Sinaliza um erro postural, especificamente pés mal posicionados quando a pessoa está em pé, alertando para a correção da base antes do agachamento.

Textual: Detalhes sobre o estado atual da pose, valores dos ângulos, posições do quadril e o status dos pés são impressos no console.

### 6. Geração de Dados para Análise (CSV)

Todos os dados calculados para cada frame (número do frame, estado, ângulos dos joelhos e tornozelos, distâncias dos pés e ombros, posições Y de ombros e quadris) são registrados em um arquivo CSV (parametros.csv). Este arquivo serve como um log completo da sessão de treino, permitindo análises posteriores detalhadas, identificação de padrões e até mesmo a geração de gráficos para visualização do progresso.

## Resultados

A ferramenta consegue realizar o carregamento de vídeo, onde para cada frame realiza a análise necessária retornando feedbacks visuais (Avatar indicando o quão correto está sendo o exercício) no próprio vídeo. Assim como no console de forma textual e uma análise, logo a seguir será exibido imagens extraídas da aplicação em execução.

![Exercício em transição](https://github.com/SidneyJunior01234/Corretor_Agachamento/blob/main/relatorios/imagens/avatar_trasicao.png?raw=true)
 *Avatar indicando transição*

![Exercício correto](https://github.com/SidneyJunior01234/Corretor_Agachamento/blob/main/relatorios/imagens/avatar_correto.png?raw=true)
 *Avatar indicando agachamento correto*

Com a realização dos movimento e o auxílio do avatar, temos como informações para cada frame.

![Feedback](https://github.com/SidneyJunior01234/Corretor_Agachamento/blob/main/relatorios/imagens/feedback.png?raw=true)
 *Informações no console sobre os parâmetros de análise*

As informações são armazenadas em um arquivo *.csv* que posteriormente retornam informações sobre o tempo de execução para cada agachamento e o tempo total em que foi detectado o esstado "em pé".

![Dados armazenados](https://github.com/SidneyJunior01234/Corretor_Agachamento/blob/main/relatorios/imagens/dados%20salvos.png?raw=true)
 *Dados armazenados em csv*

![Análise dos dados](https://github.com/SidneyJunior01234/Corretor_Agachamento/blob/main/relatorios/imagens/analise.png?raw=true)
 *Análise exibida no console*


