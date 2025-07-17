import matplotlib.pyplot as plt
import pandas as pd

from ..app.parametros import*
from ..app.utilidades import*

def analisar_dados():
    print("\n--- ANÁLISE DE DADOS DO AGACHAMENTO ---")
    dados = carregar_dados_csv(CSV_FILE_NAME)

    if dados:
        tempo_total_em_pe_seg = calcular_tempo_total_em_pe(dados, FPS)
        print(f"\nTempo total em pé: {tempo_total_em_pe_seg:.2f} segundos")
        
        lista_agachamentos = analisar_agachamentos_individuais(dados, FPS)
        print(f"\n--- Agachamentos Individuais ---")
        if lista_agachamentos:
            for i, squat in enumerate(lista_agachamentos):
                print(f"Agachamento {i+1}:")
                print(f"  Início no Frame: {squat['inicio_frame']}")
                print(f"  Fim no Frame: {squat['fim_frame']}")
                print(f"  Duração: {squat['duracao_segundos']:.2f} segundos")
        else:
            print("Nenhum agachamento completo detectado.")
    else:
        print("Não foi possível carregar ou analisar os dados do CSV.")