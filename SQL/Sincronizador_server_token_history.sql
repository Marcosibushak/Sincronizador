CREATE DATABASE  IF NOT EXISTS `Sincronizador` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `Sincronizador`;
-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: Sincronizador
-- ------------------------------------------------------
-- Server version	5.7.23-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `server_token_history`
--

DROP TABLE IF EXISTS `server_token_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_token_history` (
  `idserver_token_history` int(11) NOT NULL AUTO_INCREMENT,
  `access_token` varchar(255) NOT NULL,
  `created` varchar(255) NOT NULL,
  `refresh_token` varchar(255) NOT NULL,
  `public_key` varchar(255) NOT NULL,
  `milisegundo` varchar(45) NOT NULL,
  `valido` varchar(45) NOT NULL DEFAULT 'Si',
  PRIMARY KEY (`idserver_token_history`,`access_token`,`public_key`),
  UNIQUE KEY `idserver_token_history_UNIQUE` (`idserver_token_history`),
  UNIQUE KEY `access_token_UNIQUE` (`access_token`),
  UNIQUE KEY `milisegundo_UNIQUE` (`milisegundo`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_token_history`
--

LOCK TABLES `server_token_history` WRITE;
/*!40000 ALTER TABLE `server_token_history` DISABLE KEYS */;
INSERT INTO `server_token_history` VALUES (1,'API_ACCT-936896587e66b066fd37c48767880b5a9f5dbb102a9fefdca54551d453d5e0b8','2018-7-30T16:22:53','API_RT-798f3b5c004833dc3378c9199de8caa672aa1bcb455c49462739ec1c15d6aaf4','A1234567.','1532985773492','Si'),(2,'API_ACCT-ff76aa272df23cc91d3108b9dfa3f775ded35c1fdf2a069af83f74640e914e9d','2018-7-30T16:46:57','API_RT-b6f9f71e4360b0f3da2948ee582a19801388d70ad3b0836b401170f6124b73aa','A1234567.','1532987217809','Si');
/*!40000 ALTER TABLE `server_token_history` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-07-31 15:24:03
