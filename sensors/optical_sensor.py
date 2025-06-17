import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class SLAGenerator:
    def __init__(self, num_pads: int = 64, num_records: int = 200,
                 start_time: datetime = datetime(2025, 3, 1, 4, 0, 0),
                 interval_min: int = 15, seed: int = 42):
        self.num_pads = num_pads
        self.num_records = num_records
        self.start_time = start_time
        self.time_interval = timedelta(minutes=interval_min)
        self.rng = np.random.default_rng(seed)

    def _define_sla(self, mm: float) -> str:
        if mm > 90:
            return "normal"
        elif mm > 77:
            return "attention"
        else:
            return "critical"

    def _generate_mm(self, i: int, pad_id: int, case_type: str) -> float:
        if case_type == "normal":
            return 120 - 0.05 * i + self.rng.normal(0, 0.2)

        elif case_type == "attention":
            if pad_id % 10 == 0:
                return 120 - 0.15 * i + self.rng.normal(0, 0.3)
            else:
                return 120 - 0.05 * i + self.rng.normal(0, 0.2)

        elif case_type == "critical":
            if pad_id == 32 and i > 100:
                return 60 - self.rng.normal(0, 2)
            else:
                return 120 - 0.05 * i + self.rng.normal(0, 0.2)

        else:
            raise ValueError(f"Tipo de caso desconhecido: {case_type}")

    def generate_data(self, train_id: int, case_type: str) -> pd.DataFrame:
        data = []
        current_time = self.start_time

        for i in range(self.num_records):
            for pad_id in range(1, self.num_pads + 1):
                mm = self._generate_mm(i, pad_id, case_type)
                status = self._define_sla(mm)

                data.append([
                    current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    f"{train_id:02}",
                    f"F{pad_id}",
                    round(mm, 2),
                    status
                ])

            current_time += self.time_interval

        return pd.DataFrame(data, columns=[
            "timestamp", "train_id", "brake_pad_id", "brake_pad_mm", "sla_status"
        ])

    def export_csv(self, df: pd.DataFrame, filename: str):
        df.to_csv(filename, index=False, sep=';')
