CREATE DATABASE  IF NOT EXISTS `companion_app` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `companion_app`;
-- MySQL dump 10.13  Distrib 8.0.24, for Win64 (x86_64)
--
-- Host: localhost    Database: companion_app
-- ------------------------------------------------------
-- Server version	8.0.24

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `access_history`
--

DROP TABLE IF EXISTS `access_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `access_history` (
  `date_time_a` varchar(45) NOT NULL,
  `responder_id` varchar(45) DEFAULT NULL,
  `responder_name` varchar(45) DEFAULT NULL,
  `responder_course` varchar(45) DEFAULT NULL,
  `injury` varchar(45) DEFAULT NULL,
  `body_part` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`date_time_a`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `access_history`
--

LOCK TABLES `access_history` WRITE;
/*!40000 ALTER TABLE `access_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `access_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emergency_history`
--

DROP TABLE IF EXISTS `emergency_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emergency_history` (
  `date_time_e` varchar(45) NOT NULL,
  `responder_id` varchar(45) DEFAULT NULL,
  `responder_name` varchar(45) DEFAULT NULL,
  `responder_course` varchar(45) DEFAULT NULL,
  `patient_id` varchar(45) DEFAULT NULL,
  `patient_name` varchar(45) DEFAULT NULL,
  `patient_course` varchar(45) DEFAULT NULL,
  `injury` varchar(45) DEFAULT NULL,
  `body_part` varchar(45) DEFAULT NULL,
  `patient_gender` varchar(45) DEFAULT NULL,
  `patient_age` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`date_time_e`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emergency_history`
--

LOCK TABLES `emergency_history` WRITE;
/*!40000 ALTER TABLE `emergency_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `emergency_history` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-17  1:00:08
