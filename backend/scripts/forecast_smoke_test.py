import pandas as pd
from app.ml.pipeline import ForecastPipeline

if __name__ == '__main__':
    df = pd.DataFrame({
        'timestamp': pd.date_range(start='2026-01-01', periods=20, freq='5min'),
        'concurrent_users': list(range(100, 120)),
        'requests_per_second': [10 + i * 0.1 for i in range(20)],
        'traffic_volume_mb': [50 + i * 1.5 for i in range(20)],
        'network_utilization': [40 + i * 0.5 for i in range(20)],
    })

    pipeline = ForecastPipeline(model_dir='backend/app/ml/models')
    prepared = pipeline.prepare_features(df, 'concurrent_users')
    print('prepared shape', prepared.shape)
    try:
        result = pipeline.train_models(prepared, 'concurrent_users')
        print('models', list(result.results.keys()))
        print(result.to_dict())
    except Exception as e:
        import traceback
        traceback.print_exc()
