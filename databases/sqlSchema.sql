-- Create a new database (if it doesn't exist)
CREATE DATABASE IF NOT EXISTS cancer_diagnosis_db;

-- Select the database
USE cancer_diagnosis_db;

-- Create Patients Table
CREATE TABLE patients (
    id VARCHAR(50) PRIMARY KEY,
    diagnosis VARCHAR(10) NOT NULL
);

-- Create Tumor Mean Table
CREATE TABLE tumor_mean (
    id VARCHAR(50),
    radius_mean FLOAT, texture_mean FLOAT, perimeter_mean FLOAT, area_mean FLOAT,
    smoothness_mean FLOAT, compactness_mean FLOAT, concavity_mean FLOAT, concave_points_mean FLOAT,
    symmetry_mean FLOAT, fractal_dimension_mean FLOAT,
    FOREIGN KEY (id) REFERENCES patients(id) ON DELETE CASCADE
);

-- Create Tumor SE Table
CREATE TABLE tumor_se (
    id VARCHAR(50),
    radius_se FLOAT, texture_se FLOAT, perimeter_se FLOAT, area_se FLOAT,
    smoothness_se FLOAT, compactness_se FLOAT, concavity_se FLOAT, concave_points_se FLOAT,
    symmetry_se FLOAT, fractal_dimension_se FLOAT,
    FOREIGN KEY (id) REFERENCES patients(id) ON DELETE CASCADE
);

-- Create Tumor Worst Table
CREATE TABLE tumor_worst (
    id VARCHAR(50),
    radius_worst FLOAT, texture_worst FLOAT, perimeter_worst FLOAT, area_worst FLOAT,
    smoothness_worst FLOAT, compactness_worst FLOAT, concavity_worst FLOAT, concave_points_worst FLOAT,
    symmetry_worst FLOAT, fractal_dimension_worst FLOAT,
    FOREIGN KEY (id) REFERENCES patients(id) ON DELETE CASCADE
);

-- Create a log table to track diagnosis changes
CREATE TABLE diagnosis_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(50),
    old_diagnosis VARCHAR(10),
    new_diagnosis VARCHAR(10),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Stored Procedure for inserting/updating Patients
DELIMITER //
CREATE PROCEDURE InsertPatient(IN p_id VARCHAR(50), IN p_diagnosis VARCHAR(10))
BEGIN
    INSERT INTO patients (id, diagnosis)
    VALUES (p_id, p_diagnosis)
    ON DUPLICATE KEY UPDATE diagnosis = p_diagnosis;
END;
//
DELIMITER ;

-- Create a Trigger to log diagnosis changes
DELIMITER //
CREATE TRIGGER before_diagnosis_update
BEFORE UPDATE ON patients
FOR EACH ROW
BEGIN
    INSERT INTO diagnosis_log (patient_id, old_diagnosis, new_diagnosis)
    VALUES (OLD.id, OLD.diagnosis, NEW.diagnosis);
END;
//
DELIMITER ;
