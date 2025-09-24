# import numpy as np
# import pandas as pd

# columns_short = np.array([
#     "lp", "v", "GTT", "GTn", "GGn", "Ts", "Tp",
#     "T48", "T1", "T2", "P48", "P1", "P2", "Pexh",
#     "TIC", "mf", "GT_comp_decay", "GT_turb_decay"
# ])
# def ingest_sensor_data(input_file: str, output_file: str = None) -> pd.DataFrame:
#     Sensor_data_csv = pd.read_csv('data.txt', delimiter ='   ',header = None, names = columns_short)
#     Sensor_data_csv['time'] = range(len(Sensor_data_csv), 0, -1)
#     Sensor_data_csv.to_csv("Sensor_data.csv")

# def test_columns_and_length(tmp_path):
#     # Create a small test file
#     test_file = tmp_path / "data.txt"
#     test_file.write_text(
#         "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18\n"
#         "18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1"
#     )
#     output_csv = tmp_path / "Sensor_data.csv"
#     df = ingest_sensor_data(str(test_file), str(output_csv))
#     # Check columns
#     expected_cols = [
#         "lp", "v", "GTT", "GTn", "GGn", "Ts", "Tp",
#         "T48", "T1", "T2", "P48", "P1", "P2", "Pexh",
#         "TIC", "mf", "GT_comp_decay", "GT_turb_decay", "time"
#     ]
#     assert list(df.columns) == expected_cols, "Column names mismatch"
#     # Check number of rows
#     assert len(df) == 2, "Row count mismatch"
#     # Check descending time column
#     assert list(df['time']) == [2, 1], "Time column not descending correctly"
#     # Check CSV file is created
#     assert os.path.exists(output_csv), "CSV file not created"
# def test_data_values(tmp_path):
#     # Test data values
#     test_file = tmp_path / "data.txt"
#     test_file.write_text(
#         "10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180"
#     )
#     output_csv = tmp_path / "Sensor_data.csv"
#     df = ingest_sensor_data(str(test_file), str(output_csv))
#     # Check first row values
#     assert df.iloc[0]['lp'] == 10
#     assert df.iloc[0]['GGn'] == 50
#     assert df.iloc[0]['GT_turb_decay'] == 180
#     assert df.iloc[0]['time'] == 1