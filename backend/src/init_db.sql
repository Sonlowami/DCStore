-- Delete `dicom_db_dev` database if exists
DROP DATABASE IF EXISTS `dicom_db_dev`;

-- Create `dicom_db_dev` database if not exists
CREATE DATABASE IF NOT EXISTS `dicom_db_dev`;

-- Delete dicom user if exists
DROP USER IF EXISTS 'dicom'@'localhost';

-- Create user with privileges to access `dicom_db_dev` database
CREATE USER IF NOT EXISTS 'dicom'@'localhost' IDENTIFIED BY 'dicompass';
GRANT ALL PRIVILEGES ON `dicom_db_dev`.* TO 'dicom'@'localhost';
