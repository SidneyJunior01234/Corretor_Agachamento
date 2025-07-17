# O Corretor de Agachamentos

## Introdução

O agachamento é um dos exercícios mais eficazes e completos para o desenvolvimento da força e da massa muscular dos membros inferiores e do core. No entanto, sua execução incorreta pode levar a sérias lesões, comprometendo não só o desempenho, mas a saúde a longo prazo. Problemas como desalinhamento dos joelhos, falta de profundidade e instabilidade da base são comuns, especialmente entre iniciantes ou em treinos sem supervisão adequada.

É nesse cenário que surge a necessidade de uma ferramenta acessível que auxilie os praticantes a aprimorar sua técnica. O projeto apresenta um Corretor de Agachamentos que utiliza visão computacional e o modelo de detecção de pose MediaPipe Pose para monitorar e analisar a execução do agachamento. A aplicação foi desenvolvida para identificar os principais erros relacionados a postura, como a abertura dos pés em relação aos ombros e a profundidade do movimento, onde um avatar por meio de cores retorna um feedback visual sobre o exercício.

## Desenvolvimento

O desenvolvimento do Corretor de Agachamentos baseia-se na visão computacional para análise de movimento e em algoritmos de processamento de dados, cujos os principais métodos e técnicas utilizados foram:

### 1. Detecção de Pose com MediaPipe Pose

O MediaPipe Pose identifica 33 pontos cruciais no corpo humano (como ombros, quadris, joelhos, tornozelos e calcanhares) em cada frame do vídeo. Esses pontos são fornecidos com suas coordenadas X, Y (no espaço 2D da imagem) e Z (profundidade relativa), além de uma pontuação de visibilidade.

### 2. Cálculo de Ângulos Articulares

Com os landmarks identificados, é utilizado a geometria analítica para calcular os ângulos formados pelas principais articulações envolvidas no agachamento.

  * Ângulos do Joelho: avalia a profundidade do agachamento. Calculamos o ângulo formado entre o quadril, o joelho e o tornozelo (para ambos os lados, esquerdo e direito). Um ângulo menor indica maior flexão do joelho, característico de um agachamento mais profundo.
  * Ângulos do Tornozelo: verifica a estabilidade da base. O ângulo é calculado entre o joelho, o tornozelo e o calcanhar.






