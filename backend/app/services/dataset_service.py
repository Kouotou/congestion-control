import uuid
from pathlib import Path
from typing import Dict
import pandas as pd

DATA_DIR = Path("./data")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_dataset(file_name: str, contents: bytes) -> Dict[str, str]:
    dataset_id = str(uuid.uuid4())
    target_path = DATA_DIR / f"{dataset_id}_{file_name}"
    target_path.write_bytes(contents)
    return {"dataset_id": dataset_id, "path": str(target_path)}


def inspect_dataset(file_path: str) -> Dict[str, object]:
    df = pd.read_csv(file_path)
    schema = {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)}
    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "schema": schema,
    }
