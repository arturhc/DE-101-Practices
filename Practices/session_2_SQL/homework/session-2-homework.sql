CREATE SCHEMA IF NOT EXISTS clinic_db;
USE clinic_db;

CREATE TABLE IF NOT EXISTS clinic_db.doctor (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  last_name VARCHAR(45) NOT NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS clinic_db.specialization (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX name_unique (name ASC) VISIBLE)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS clinic_db.doctor_specialization (
  id INT NOT NULL AUTO_INCREMENT,
  doctor_id INT NOT NULL,
  specialization_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX fk_doctor_specialization_doc_idx (doctor_id ASC) VISIBLE,
  INDEX fk_doctor_specialization_specialization_idx (specialization_id ASC) VISIBLE,
  CONSTRAINT fk_doctor_specialization_doc
    FOREIGN KEY (doctor_id)
    REFERENCES clinic_db.doctor (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_doctor_specialization_specialization
    FOREIGN KEY (specialization_id)
    REFERENCES clinic_db.specialization (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS clinic_db.patient (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  last_name VARCHAR(45) NOT NULL,
  address VARCHAR(100) NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS clinic_db.appointment (
  id INT NOT NULL AUTO_INCREMENT,
  date DATE NOT NULL,
  time TIME NOT NULL,
  patient_id INT NOT NULL,
  doctor_id INT NOT NULL,
  specialization_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX fk_appointment_doctor_idx (doctor_id ASC) VISIBLE,
  INDEX fk_appointment_patient_idx (patient_id ASC) VISIBLE,
  INDEX fk_appointment_specialization_idx (specialization_id ASC) VISIBLE,
  CONSTRAINT fk_appointment_doctor
    FOREIGN KEY (doctor_id)
    REFERENCES clinic_db.doctor (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_appointment_patient
    FOREIGN KEY (patient_id)
    REFERENCES clinic_db.patient (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_appointment_specialization
    FOREIGN KEY (specialization_id)
    REFERENCES clinic_db.specialization (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

