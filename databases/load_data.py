import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load the dataset
df = pd.read_csv("../dataset/data.csv")

# Print column names to verify
print(df.columns)

# Database connection parameters
db_params = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT"))
}

try:
    conn = mysql.connector.connect(**db_params)
    cursor = conn.cursor()
    print("Connected to MySQL")

    # Call stored procedure for inserting patients
    insert_patient = "CALL InsertPatient(%s, %s);"

    # Define SQL INSERT statements
    insert_tumor_mean = """
    INSERT INTO tumor_mean (
        id, radius_mean, texture_mean, perimeter_mean, area_mean, 
        smoothness_mean, compactness_mean, concavity_mean, concave_points_mean, 
        symmetry_mean, fractal_dimension_mean
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    insert_tumor_se = """
    INSERT INTO tumor_se (
        id, radius_se, texture_se, perimeter_se, area_se, 
        smoothness_se, compactness_se, concavity_se, concave_points_se, 
        symmetry_se, fractal_dimension_se
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    insert_tumor_worst = """
    INSERT INTO tumor_worst (
        id, radius_worst, texture_worst, perimeter_worst, area_worst, 
        smoothness_worst, compactness_worst, concavity_worst, concave_points_worst, 
        symmetry_worst, fractal_dimension_worst
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    # Insert data into MySQL
    for _, row in df.iterrows():
        patient_id = str(row["id"])
        
        # Insert into Patients using Stored Procedure
        cursor.execute(insert_patient, (patient_id, row["diagnosis"]))
        
        # Insert into TumorMean
        cursor.execute(insert_tumor_mean, (
            patient_id, row["radius_mean"], row["texture_mean"], row["perimeter_mean"], row["area_mean"],
            row["smoothness_mean"], row["compactness_mean"], row["concavity_mean"], row["concave points_mean"],
            row["symmetry_mean"], row["fractal_dimension_mean"]
        ))
        
        # Insert into TumorSE
        cursor.execute(insert_tumor_se, (
            patient_id, row["radius_se"], row["texture_se"], row["perimeter_se"], row["area_se"],
            row["smoothness_se"], row["compactness_se"], row["concavity_se"], row["concave points_se"],
            row["symmetry_se"], row["fractal_dimension_se"]
        ))
        
        # Insert into TumorWorst
        cursor.execute(insert_tumor_worst, (
            patient_id, row["radius_worst"], row["texture_worst"], row["perimeter_worst"], row["area_worst"],
            row["smoothness_worst"], row["compactness_worst"], row["concavity_worst"], row["concave points_worst"],
            row["symmetry_worst"], row["fractal_dimension_worst"]
        ))

    # Commit changes
    conn.commit()
    print("Data successfully inserted into Database (MySQL).")

except Error as e:
    print(f"Error: {e}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("MySQL connection closed.")
