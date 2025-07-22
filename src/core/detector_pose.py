# src/core/detector_pose.py

import mediapipe as mp
from config.configuracoes import MIN_CONFIDENCE_DETECCAO, MIN_CONFIDENCE_RASTREAMENTO

class DetectorPose:
    """
    Gerencia a detecção de pose usando MediaPipe.
    """
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=MIN_CONFIDENCE_DETECCAO,
            min_tracking_confidence=MIN_CONFIDENCE_RASTREAMENTO
        )

    def processar_frame(self, frame_rgb):
        """
        Processa um frame RGB para detectar landmarks de pose.
        
        Args:
            frame_rgb (numpy.ndarray): O frame da imagem no formato RGB.
            
        Returns:
            mediapipe.python.solution_base.SolutionOutputs: Os resultados da detecção de pose.
        """
        return self.pose.process(frame_rgb)

    def fechar(self):
        """
        Libera os recursos do detector de pose.
        """
        self.pose.close()