
![Duckdb vs Pandas](./Images/duck.jpg)

# NYC TAXI Analysis with `DUCKDB & PANDAS`

![Static Badge](https://img.shields.io/badge/pandas-blue?logo=PANDAS)
![Static Badge](https://img.shields.io/badge/Duckdb-yellow?logo=Duckdb&logoColor=black)


## 🚕Project Overview:
This project investigates two important tools — DuckDB and Pandas — focusing on their performance (speed) in data analysis. The dataset used is NYC Yellow Taxi trip data from January to May 2026.

***Dataset size***: ~325 MB (5 Parquet files, ~19M rows). This size is well within Pandas' capacity, which makes the benchmark meaningful — any performance gap observed is due to the tools themselves, not memory limitations.


## 📝Business quesstions:
- **Which hours of the day have the most trips?**
  Helps plan the optimal number of taxis available throughout the day.

- **Which months have the highest trip volume?**
  Supports planning and seasonal scheduling across the year.

- **Which NYC zones generate the most trips and the highest revenue (fare amount)?**
  Identifies high-demand areas for better resource allocation.

## ⏳🦆🐼Comparing DuckDB and Pandas
|step|Execution Time Duckdb|Execution Time DPandas|Comments|
|---|---|---|---|
| Load data | 0.01* | 5.55 | *DuckDB's `read_parquet` is lazy — 0.01s reflects a forced `COUNT(*)` to ensure a fair, apples-to-apples comparison with Pandas' eager load. |
| Missing Value|0.58|7.28| Identifies null counts in columns|
| Missing value cross-check | 0.04 | 0.37 | Investigates whether null `passenger_count` correlates with nulls in the other 4 columns.
 Missing value root-cause (VendorID) | 0.17 | 0.87 | 25% of `passenger_count` is null — a considerable share. Grouping by `VendorID` shows Vendor 6 is 100% null, meaning it simply doesn't record this field. This confirms the missingness is systematic, not random, so the rows were kept rather than dropped. |
| Missing value by month | 0.20 | 0.95 | Checks whether null rate varies across months. |
| Statistical summary | 17.35 | 8.70 | Pandas was faster here. `SUMMARIZE` computes more per-column stats (including `approx_unique` and `null_percentage`) across *all* columns (numeric and categorical), while `.describe()` defaults to numeric columns only — the comparison isn't fully apples-to-apples. |
| Quantile calculation (90/95/99/99.9) | 0.56 | 0.20 | Pandas was faster. Since the data was already loaded in RAM, in-memory quantile computation outperformed DuckDB's per-query disk read. |
| Zone-level analysis | 0.25 | 3.93 | Joins trip data with the Taxi Zone Lookup table to find zones with the highest trip counts and revenue. |

## 📊 Key Findings:
- Missing values in passenger_count were investigated with a focus on VendorID and month to find the root cause. Results show that missingness is systematic across vendors — Vendor 6 does not record passenger_count at all. Since the size of missing values is significant (25%), we avoided dropping them.
- Calculating quantiles (90/95/99/99.9) for trip_distance shows that 99.9% of trips are under 30 miles, while the maximum value is 328,522 miles — demonstrating a significant data error that needed to be corrected.
- High-demand hours peak at 6 PM (1.34M trips), while the lowest demand occurs at 4 AM (151,000 trips). This pattern supports better fleet planning throughout the day.
- Comparing DuckDB and Pandas: for queries involving aggregation, DuckDB is 9 times faster than Pandas. However, for heavy statistical computations like SUMMARIZE/quantile calculations, Pandas outperforms DuckDB.

## 📁 Project Structure:
```text
|NYTAXI-DuckDB-Pandas\
|ــــ Images
|ــــ DATA\
|          |Taxi_zone_lookup.csv
|          | yellow_tripdata_2026-01.parquet
|          | yellow_tripdata_2026-02.parquet
|          | yellow_tripdata_2026-03.parquet
|          | yellow_tripdata_2026-04.parquet
|          | yellow_tripdata_2026-05.parquet
|ـــــ NYtaxi.py
|ـــــ README.md



## 🟥 prerequisit:
```bash
- uv init
- uv pip install pandas duckdb pyarrow fastparquet
```

## 🚀How to run:
uv run NYtaxi.py
