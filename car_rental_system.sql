-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: car_rental_system
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `cars`
--

DROP TABLE IF EXISTS `cars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cars` (
  `car_ID` int NOT NULL AUTO_INCREMENT,
  `license_plate` varchar(10) NOT NULL,
  `make` varchar(50) NOT NULL,
  `model` varchar(50) NOT NULL,
  `year` int NOT NULL,
  `seating_capacity` int NOT NULL,
  `price_per_day` decimal(10,2) NOT NULL,
  `transmission` varchar(10) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`car_ID`),
  CONSTRAINT `cars_chk_1` CHECK ((`transmission` in (_utf8mb4'manual',_utf8mb4'automatic')))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cars`
--

LOCK TABLES `cars` WRITE;
/*!40000 ALTER TABLE `cars` DISABLE KEYS */;
INSERT INTO `cars` VALUES (1,'Pdd123','TOTYO','CROWN',2021,5,111.00,'automatic',NULL),(2,'IDS123','Nissan','FUGA',2023,7,393.00,'automatic',NULL);
/*!40000 ALTER TABLE `cars` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_ID` int NOT NULL AUTO_INCREMENT,
  `user_ID` int NOT NULL,
  `customer_first_name` varchar(50) NOT NULL,
  `customer_last_name` varchar(50) NOT NULL,
  `customer_address` varchar(255) DEFAULT NULL,
  `customer_phone_number` varchar(20) NOT NULL,
  PRIMARY KEY (`customer_ID`),
  KEY `user_ID` (`user_ID`),
  CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `users` (`user_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,3,'Customer','Customer','37 terrace','0000000'),(2,4,'Customer','Customer',NULL,'0000000'),(3,5,'Customer','Customer',NULL,'0000000'),(4,6,'Customer','Customer',NULL,'0000000'),(5,7,'Customer','Customer',NULL,'0000000'),(6,8,'Customer','Customer',NULL,'0000000'),(7,9,'Customer','Customer',NULL,'0000000');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staffs`
--

DROP TABLE IF EXISTS `staffs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staffs` (
  `staff_ID` int NOT NULL AUTO_INCREMENT,
  `user_ID` int NOT NULL,
  `staff_first_name` varchar(50) NOT NULL,
  `staff_last_name` varchar(50) NOT NULL,
  `staff_address` varchar(255) DEFAULT NULL,
  `staff_phone_number` varchar(20) NOT NULL,
  PRIMARY KEY (`staff_ID`),
  KEY `user_ID` (`user_ID`),
  CONSTRAINT `staffs_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `users` (`user_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staffs`
--

LOCK TABLES `staffs` WRITE;
/*!40000 ALTER TABLE `staffs` DISABLE KEYS */;
INSERT INTO `staffs` VALUES (1,1,'admin','admin',NULL,'0000000'),(2,10,'Staff','Staff',NULL,'0000000');
/*!40000 ALTER TABLE `staffs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_ID` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `user_type` varchar(30) NOT NULL,
  PRIMARY KEY (`user_ID`),
  CONSTRAINT `users_chk_1` CHECK ((`user_type` in (_utf8mb4'staff',_utf8mb4'customer',_utf8mb4'admin')))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','$2b$12$rqDFQEDEDDtajQaAaOmUB.k3IhHYDjdT3Sr1z/ef6fvgIUxF658O6','admin@gmail.com','admin'),(2,'CUS1','$2b$12$kd5l6OqoYTIhoB4tye7hG.MeIDj2Q/jHZ60tpzE4ZP/pBxSd490bC','cus1@gmail.com','customer'),(3,'c2','$2b$12$OWpFQnYY3MfvGYlgYZKrge8bGNMfMoMSKOm8HCszzsqb8ZvlZ0r6G','c2@gmail.com','customer'),(4,'c3','$2b$12$ugiqqIiuzWk/i6vdh2gJUuNsZ2bOw4ZT8VoBui14zTX/EM2cmU2z.','c3@gmail.com','customer'),(5,'c4','$2b$12$sL5VWH/NJxZF8rOspqAKr.KsW50sXQ2RbufT0SChfjQ3HyKzI87hy','c4@gmail.com','customer'),(6,'c5','$2b$12$EFVBvY5WVoLD4Isp0/qDb.Arf/za1rULi1GPtjBwJb7P/lO9WtC7G','c5@gmail.com','customer'),(7,'c6','$2b$12$2UdiGycTglB5A9o2UBcDB.AQ18K2Me01ZqOClkhd5gsD4V.qtDiVu','c6@gmail.com','customer'),(8,'c8','$2b$12$sxg5N5k6fLERywXkMnXcTuPyblQnL5VKkMYlYigflvHU.ZZEwBSrG','halloatticus@gmail.com','customer'),(9,'c11','$2b$12$ubVXNkVnChxjmckBiwCVnO2wedCfmloeCgLqH5zvMwf7rY7Gf2dQK','admin@gmail.com','customer'),(10,'s1','$2b$12$82Wws5E9ZDs03bJLD1K/Tu0kQSkAmNAmkdtK/G1f5MBnSAgqIhhMa','s1@gmail.com','staff');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-07 18:37:09
