# %%
import duckdb
import pandas as pd
import time


# %%
!dir -lh  ".\Data\yellow_tripdata_2026-*.parquet"


# %%
start_time=time.time()
con=duckdb.connect("nyproject.duckdb")
df=con.read_parquet('./Data/yellow_tripdata_2026-*.parquet')
end_time=time.time()
print(f"execuation time: {end_time - start_time:.2f}")


# %%
start_time=time.time()
con=duckdb.connect("nyproject.duckdb")
df=con.read_parquet('./Data/yellow_tripdata_2026-*.parquet')
t=con.sql("select count(*) from df")
print(t.fetchone())
end_time=time.time()
print(f"execuation time: {end_time - start_time:.2f}")


# %%
start_time=time.time()
months=['2026-01','2026-02','2026-03','2026-04','2026-05']
df_pandas = [pd.read_parquet(f"./Data/yellow_tripdata_{i}.parquet", engine='fastparquet') for i in months]
df_pandas = pd.concat(df_pandas, ignore_index=True)

end_time = time.time()

print(f"execution_time: {end_time - start_time:.2f}")


# %%
print(df.columns)
print(df.shape)


# %%
df.query("ny","describe ny").show()


# %%
##Analysis :


# %%
start_time=time.time()
df_pandas=df.df()
res=df_pandas.isnull().sum()
print(res)
end_time=time.time()
print(f"execuation time: {end_time - start_time:.2f}")


# %%
start_time=time.time()
t=con.sql("""
SELECT
    SUM(CASE WHEN VendorID IS NULL THEN 1 ELSE 0 END) AS VendorID,
    SUM(CASE WHEN tpep_pickup_datetime IS NULL THEN 1 ELSE 0 END) AS tpep_pickup_datetime,
    SUM(CASE WHEN tpep_dropoff_datetime IS NULL THEN 1 ELSE 0 END) AS tpep_dropoff_datetime,
    SUM(CASE WHEN passenger_count IS NULL THEN 1 ELSE 0 END) AS passenger_count,
    SUM(CASE WHEN trip_distance IS NULL THEN 1 ELSE 0 END) AS trip_distance,
    SUM(CASE WHEN RatecodeID IS NULL THEN 1 ELSE 0 END) AS RatecodeID,
    SUM(CASE WHEN store_and_fwd_flag IS NULL THEN 1 ELSE 0 END) AS store_and_fwd_flag,
    SUM(CASE WHEN PULocationID IS NULL THEN 1 ELSE 0 END) AS PULocationID,
    SUM(CASE WHEN DOLocationID IS NULL THEN 1 ELSE 0 END) AS DOLocationID,
    SUM(CASE WHEN payment_type IS NULL THEN 1 ELSE 0 END) AS payment_type,
    SUM(CASE WHEN fare_amount IS NULL THEN 1 ELSE 0 END) AS fare_amount,
    SUM(CASE WHEN extra IS NULL THEN 1 ELSE 0 END) AS extra,
    SUM(CASE WHEN mta_tax IS NULL THEN 1 ELSE 0 END) AS mta_tax,
    SUM(CASE WHEN tip_amount IS NULL THEN 1 ELSE 0 END) AS tip_amount,
    SUM(CASE WHEN tolls_amount IS NULL THEN 1 ELSE 0 END) AS tolls_amount,
    SUM(CASE WHEN improvement_surcharge IS NULL THEN 1 ELSE 0 END) AS improvement_surcharge,
    SUM(CASE WHEN total_amount IS NULL THEN 1 ELSE 0 END) AS total_amount,
    SUM(CASE WHEN congestion_surcharge IS NULL THEN 1 ELSE 0 END) AS congestion_surcharge,
    SUM(CASE WHEN Airport_fee IS NULL THEN 1 ELSE 0 END) AS Airport_fee,
    SUM(CASE WHEN cbd_congestion_fee IS NULL THEN 1 ELSE 0 END) AS cbd_congestion_fee
FROM './Data/yellow_tripdata_2026-*.parquet'
""")
print(t)
end_time=time.time()
print(f"Executaion time: {end_time-start_time:.2f}")


# %%
## ANALYSIS ANd descision:


# %%
start_time=time.time()
df_3=df_pandas.loc[df_pandas['passenger_count'].isnull(),['store_and_fwd_flag','RatecodeID','congestion_surcharge','Airport_fee']]
print(df_3.count())
end_time = time.time()
print(f"execution_time: {end_time - start_time:.2f}")


# %%
start_time=time.time()
t4=con.sql("""
    select count(store_and_fwd_flag),count(RatecodeID),count(congestion_surcharge),count(Airport_fee)
    from df
    where passenger_count IS Null

""")
print(t4)
end_time = time.time()
print(f"execution_time: {end_time - start_time:.2f}")


# %%
## ANALYSIS::


# %%
print((4812280/df.shape[0])*100)


# %%
## ANALYSIS::


# %%
start_time=time.time()
x=df_pandas.groupby('VendorID')['passenger_count'].apply(lambda s: s.isnull().mean())
print(x)
end_time = time.time()
print(f"execution_time: {end_time - start_time:.2f}")


# %%
start_time=time.time()
t3=con.sql("""
        select VendorID,avg(case when passenger_count is Null then 1 else 0 end) as avg_p_n
        from df
        group by VendorID
        """)
t3.show()
end_time = time.time()
print(f"execution_time: {end_time - start_time:.2f}")


# %%
## Analysis:


# %%

# df_pandas['month']=df_pandas['tpep_pickup_datetime'].dt.month
# df_pandas['month'].value_counts()


# %%
##َ Analysis


# %%
start_time=time.time()
df_pandas['month']=df_pandas['tpep_pickup_datetime'].dt.month
df_g=df_pandas.groupby('month')['passenger_count'].apply(lambda x: x.isnull().mean()).sort_values()
print(df_g)
end_time = time.time()
print(f"execution_time: {end_time - start_time:.2f}")


# %%
start_time=time.time()
t6=con.sql("""
       with t as (
       select passenger_count,tpep_pickup_datetime , month(tpep_pickup_datetime) as month
       from  df )

       select  month, avg(case when passenger_count IS NULL then 1 else 0 end) as avg_
       from t
       group by month
       """)
t6.show()
end_time = time.time()
print(f"execution_time: {end_time - start_time:.2f}")


# %%
##Analysis:


# %%
start_time=time.time()
t1=con.sql("SUMMARIZE df")
t1.show()
end_time = time.time()
print(f"execution_time: {end_time - start_time:.2f}")


# %%
start_time=time.time()
df_7=df_pandas.describe()
print(df_7)
end_time = time.time()
print(f"execution_time: {end_time - start_time:.2f}")


# %%
start_time=time.time()
t0=con.sql("SELECT QUANTILE_CONT(trip_distance, [0.90, 0.95, 0.99, 0.999]) AS quantiles FROM df")
t0.show()
end_time = time.time()
print(f"execution_time: {end_time - start_time:.2f}")


# %%
# Calculate multiple quantiles
start_time=time.time()
quantiles = df_pandas['trip_distance'].quantile([0.90, 0.95, 0.99, 0.999])
print(quantiles)
end_time = time.time()
print(f"execution_time: {end_time - start_time:.2f}")


# %%
start_time=time.time()
t=con.sql(" with t as (select tpep_pickup_datetime, hour(tpep_pickup_datetime) as hour from df) select hour , count(*) as cnt from t group by hour order by hour ")
t.fetchall()
end_time = time.time()
print(f"execution_time: {end_time - start_time:.2f}")


# %%
start_time=time.time()
df_pandas['hour']=df_pandas['tpep_pickup_datetime'].dt.hour
df_h=df_pandas.groupby('hour')['hour'].count()
print(df_h)
end_time = time.time()
print(f"execution_time: {end_time - start_time:.2f}")


# %%
##َANALYSIS


# %%
start_time=time.time()
df_zone=pd.read_csv('./data/taxi_zone_lookup.csv')
df_zone = pd.read_csv("./data/taxi_zone_lookup.csv")
df_m = df_pandas.merge(
    df_zone,
    left_on="PULocationID",
    right_on="LocationID",
    how="left"
)
result = (
    df_m.groupby(["Borough", "LocationID"])
    .agg(
        avg_fare=("fare_amount", "mean"),
        cnt=("VendorID", "count")
    )
    .reset_index()
)
print(result)
end_time = time.time()
print(f"execution_time: {end_time - start_time:.2f}")


# %%
start_time=time.time()
t01=con.sql("""
        with t as (
        select *
        from df left join './data/taxi_zone_lookup.csv'  as zones  ON df.PULocationID=zones.LocationID)
        select   Borough,LocationID,count(*) as cnt,sum( fare_amount)
        from t
        group by Borough , LocationID
        order by cnt desc
        """)
t01.show()
end_time = time.time()
print(f"execution_time: {end_time - start_time:.2f}")


# %%
print(df_pandas.loc[df_pandas['fare_amount']<0,['fare_amount']].count())


# %%
(115467 / df_pandas.shape[0]) * 100


# %%


# %%
df_p1=df_pandas.loc[df_pandas['fare_amount'] < 0, ['fare_amount', 'total_amount', 'trip_distance', 'payment_type']]
print(df_p1.head(10))


# %%



