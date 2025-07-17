import cv2
import csv
import math
import mediapipe as mp
import sys

from ..analise.analise import analisar_dados
from .parametros import*
from .utilidades import calculate_angle

def main():
    if len(sys.argv) < 2:
        print("Execução: python seu_script.py <caminho_do_video>")
        sys.exit(1)

    caminho_do_video = sys.argv[1]
    captura = cv2.VideoCapture(caminho_do_video)

    if not captura.isOpened():
        print("Erro: Não foi possível abrir o vídeo. Verifique o caminho do arquivo.")
        sys.exit(1)

    FPS = captura.get(cv2.CAP_PROP_FPS)
    if FPS == 0:
        FPS = 30.0

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    csv_file = open(CSV_FILE_NAME, 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(CSV_HEADERS)

    # --- Variáveis de Estado e Calibração ---
    frame_count = 0
    initial_y_hip = None

    # Inicia o detector de pose
    with mp_pose.Pose(min_detection_confidence=MDC, min_tracking_confidence=MTC) as pose:

        while True:
            ret, frame = captura.read()

            if not ret:
                print("Fim do vídeo ou erro ao ler o frame.")
                break

            frame_count += 1

            frame.flags.writeable = False
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resultados = pose.process(frame)

            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            current_pose_state = "Transicao/Indefinido" # Estado padrão
            
            # Inicializa os dados da linha CSV
            row_data = [
                frame_count, ESTADOS_DICT[current_pose_state],
                'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A',
                'N/A', 'N/A', 'N/A', 'N/A'
            ]

            # --- Definição da cor inicial do avatar ---
            drawing_color = COR_AMARELO

            if resultados.pose_landmarks:
                landmarks = resultados.pose_landmarks.landmark
                h, w, c = frame.shape

                # --- Extração de Landmarks ---
                om_esq = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                om_dir = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                quadril_esq = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                quadril_dir = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                joelho_esq = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
                joelho_dir = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
                tornozelo_esq = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
                tornozelo_dir = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
                pe_esq = landmarks[mp_pose.PoseLandmark.LEFT_HEEL]
                pe_dir = landmarks[mp_pose.PoseLandmark.RIGHT_HEEL]

                # --- Cálculos de Posições e Ângulos ---
                om_esq_y_px = int(om_esq.y * h)
                om_dir_y_px = int(om_dir.y * h)
                quadril_esq_y_px = int(quadril_esq.y * h)
                quadril_dir_y_px = int(quadril_dir.y * h)
                
                avg_quadril_y_px = (quadril_esq_y_px + quadril_dir_y_px) / 2

                if initial_y_hip is None:
                    initial_y_hip = avg_quadril_y_px
                    print(f"\n--- CALIBRAÇÃO INICIAL ---")
                    print(f"Posição Y inicial do quadril calibrada: {initial_y_hip:.2f} pixels.")
                    print("Por favor, garanta que a pessoa está em pé no início do vídeo.")
                    print("---------------------------\n")

                angle_joelho_esq = calculate_angle(quadril_esq, joelho_esq, tornozelo_esq)
                angle_joelho_dir = calculate_angle(quadril_dir, joelho_dir, tornozelo_dir)
                avg_joelho_angle = (angle_joelho_esq + angle_joelho_dir) / 2

                angle_tornozelo_esq = calculate_angle(joelho_esq, tornozelo_esq, pe_esq)
                angle_tornozelo_dir = calculate_angle(joelho_dir, tornozelo_dir, pe_dir)

                dist_ombros_px = abs(int(om_dir.x * w) - int(om_esq.x * w))
                dist_pes_px = abs(int(tornozelo_dir.x * w) - int(tornozelo_esq.x * w))
                
                # --- Detecção do Estado (Em Pé / Agachado) e Definição da Cor ---
                if (avg_joelho_angle < THRESHOLD_ANGULO_JOELHO_AGACHADO and
                    initial_y_hip is not None and
                    avg_quadril_y_px > (initial_y_hip + h * Y_DROP_THRESHOLD_PX)):
                    current_pose_state = "Agachado"
                    drawing_color = COR_VERDE # Avatar verde quando agachado
                
                elif (avg_joelho_angle > THRESHOLD_ANGULO_JOELHO_EM_PE and
                    initial_y_hip is not None and 
                    avg_quadril_y_px < (initial_y_hip + h * (Y_DROP_THRESHOLD_PX / 2))):
                    current_pose_state = "Em Pe"
                    
                    # --- Verificação de Pés (SOMENTE quando "Em Pe") ---
                    limite_inferior_pes = dist_ombros_px * (1 - TOLERANCIA_PES_OMBRO_PERCENTUAL)
                    limite_superior_pes = dist_ombros_px * (1 + TOLERANCIA_PES_OMBRO_PERCENTUAL)

                    if not (limite_inferior_pes <= dist_pes_px <= limite_superior_pes):
                        drawing_color = COR_VERMELHO # Avatar vermelho se os pés estiverem incorretos
                        # O texto de feedback não será mais exibido no frame, apenas no console.
                else:
                    current_pose_state = "Transicao/Indefinido"
                    drawing_color = COR_AMARELO # Avatar amarelo em transição


                print(f"\n--- Frame {frame_count} ---")
                print(f"Estado da Pose: {current_pose_state}")
                print(f"Ângulo Médio Joelho: {avg_joelho_angle:.2f} graus")
                print(f"Posição Y Média Quadril (px): {avg_quadril_y_px:.2f} (Inicial: {initial_y_hip:.2f})")
                
                limite_inferior_pes = dist_ombros_px * (1 - TOLERANCIA_PES_OMBRO_PERCENTUAL)
                limite_superior_pes = dist_ombros_px * (1 + TOLERANCIA_PES_OMBRO_PERCENTUAL)

                print(f"Distância entre ombros (px): {dist_ombros_px:.2f}")
                print(f"Distância entre pés (px): {dist_pes_px:.2f}")

                if limite_inferior_pes <= dist_pes_px <= limite_superior_pes:
                    print("Status Pés: Pés na largura dos ombros (ou ligeiramente mais abertos/fechados). OK!")
                elif dist_pes_px < limite_inferior_pes:
                    print("Status Pés: Pés muito juntos. Abra mais!")
                else: 
                    print("Status Pés: Pés muito afastados. Aproxime!")

                print(f"Ângulo Joelho Esquerdo: {angle_joelho_esq:.2f} graus")
                print(f"Ângulo Joelho Direito: {angle_joelho_dir:.2f} graus")
                print(f"Ângulo Tornozelo Esquerdo: {angle_tornozelo_esq:.2f} graus")
                print(f"Ângulo Tornozelo Direito: {angle_tornozelo_dir:.2f} graus")

                print("-----------------------------\n")

                row_data = [
                    frame_count,
                    ESTADOS_DICT[current_pose_state],
                    f"{angle_joelho_esq:.2f}",
                    f"{angle_joelho_dir:.2f}",
                    f"{angle_tornozelo_esq:.2f}",
                    f"{angle_tornozelo_dir:.2f}",
                    f"{dist_pes_px:.2f}",
                    f"{dist_ombros_px:.2f}",
                    f"{om_esq_y_px}",
                    f"{om_dir_y_px}",
                    f"{quadril_esq_y_px}",
                    f"{quadril_dir_y_px}"
                ]
                
                # --- DESENHA OS LANDMARKS COM A COR DINÂMICA ---
                mp_drawing.draw_landmarks(
                    frame,
                    resultados.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=drawing_color, thickness=2, circle_radius=2),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=drawing_color, thickness=2, circle_radius=2)
                )

            csv_writer.writerow(row_data) # Escreve no CSV mesmo se não houver pose detectada

            cv2.imshow('Corretor de Agachamento', frame)

            if cv2.waitKey(30) & 0xFF == 27: # Pressione ESC para sair
                break

    csv_file.close() # Fecha o arquivo CSV no final
    captura.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    analisar_dados()