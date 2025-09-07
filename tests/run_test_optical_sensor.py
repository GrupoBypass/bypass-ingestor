import pandas as pd
import numpy as np
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from process.optical_processor import OpticalProcessor
from process.iot_processor import IOTProcessor

if __name__ == "__main__":

# Configurações
#num_pads = 64
#num_days = 10
#interval_minutes = 30
#records_per_day = (24 * 60) // interval_minutes
#num_records = num_days * records_per_day
#start_time = datetime(2025, 3, 1, 6, 0, 0)
#time_interval = timedelta(minutes=interval_minutes)

    num_pads = 64
    num_records = 52  # 52 timestamps
    start_time = datetime(2025, 3, 1, 4, 0, 0)
    time_interval = timedelta(minutes=138)  # espaçamento para cobrir 5 dias


    # Definição do SLA baseado na média
    def define_sla(mm):
        if mm > 90:
            return 'normal'
        elif mm > 77:
            return 'attention'
        else:
            return 'critical'

    # Geração dos dados de um trem conforme o caso
    def generate_data(train_id, case_type):
        data = []
        current_time = start_time

        for i in range(num_records):
            for pad_id in range(1, num_pads + 1):
                pad_label = f'F{pad_id}'

                if case_type == 'normal':
                    mm = 120 - 0.05 * i + np.random.normal(0, 0.2)

                elif case_type == 'attention':
                    if pad_id % 5 == 0:
                        mm = 120 - 1.0 * i + np.random.normal(0, 0.5)  # rápido, deve cair para < 90
                    else:
                        mm = 120 - 0.3 * i + np.random.normal(0, 0.2)  # mais lento

                elif case_type == 'critical':
                    if pad_id == 32 and i > 20:
                        mm = 60 - np.random.normal(0, 2)
                    else:
                        mm = 120 - 0.3 * i + np.random.normal(0, 0.2)

                status = define_sla(mm)

                data.append([
                    current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    f'{train_id:02}',
                    pad_label,
                    round(mm, 2),
                    status
                ])

            current_time += time_interval

        return pd.DataFrame(data, columns=["timestamp", "train_id", "brake_pad_id", "brake_pad_mm", "sla_status"])

    # Gerar os dados
    df_normal = generate_data(1, 'normal')
    df_attention = generate_data(2, 'attention')
    df_critical = generate_data(3, 'critical')
    df_consolidated = pd.concat([df_normal, df_attention, df_critical], ignore_index=True)

    # Exportar os arquivos CSV com separador ';'
    df_normal.to_csv("train_01_normal_sla.csv", index=False, sep=';')
    df_attention.to_csv("train_02_attention_sla.csv", index=False, sep=';')
    df_critical.to_csv("train_03_critical_sla.csv", index=False, sep=';')
    df_consolidated.to_csv("train_consolidated_sla.csv", index=False, sep=';')