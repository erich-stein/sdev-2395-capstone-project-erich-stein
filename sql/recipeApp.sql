/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.14-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: recipeApp
-- ------------------------------------------------------
-- Server version	10.11.14-MariaDB-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES
('ce255796a9b5');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipes`
--

DROP TABLE IF EXISTS `recipes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(128) NOT NULL,
  `long_desc` text DEFAULT NULL,
  `short_desc` varchar(512) NOT NULL,
  `categories` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`categories`)),
  `tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`tags`)),
  `ingredients` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`ingredients`)),
  `instructions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`instructions`)),
  `updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_recipes_timestamp` (`timestamp`),
  KEY `ix_recipes_user_id` (`user_id`),
  KEY `ix_recipes_title` (`title`),
  CONSTRAINT `recipes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipes`
--

LOCK TABLES `recipes` WRITE;
/*!40000 ALTER TABLE `recipes` DISABLE KEYS */;
INSERT INTO `recipes` VALUES
(10,'2026-05-05 21:18:52',1,'Vanilla Bean Scones','','Simple vanilla scones with vanilla bean glaze, much like the Starbucks vanilla scones.','[\"Dessert\", \"Breakfast\"]','[\"copycat\", \"vanilla beans\", \"scones\", \"dessert\", \"breakfast\"]','[\"2 cups all-purpose flour\", \"1/3 cup granulated sugar\", \"1 1/2 tsp baking powder\", \"1/2 tsp salt\", \"8 tbsp cold butter, sliced into pieces\", \"1/2 cup heavy cream\", \"2 tsp vanilla extract\", \"1 egg\", \"1 1/2 cup powdered sugar\", \"Seeds from 1 vanilla bean\", \"1 1/2 tbsp milk\"]','[\"Preheat oven to 375\\u00b0F\", \"Combine dry ingredients\", \"Mix cold butter pieces with dry mix until crumbly\", \"Whisk egg, vanilla extract, and heavy cream\", \"Combine wet and dry mixes\", \"Form dough into a ball\", \"On a floured surface, divide dough into two or three pieces\", \"Working with one piece at a time, flatten to about 1 1/2 inches thick, then divide into 6 triangular scones\", \"Bake in oven for 16 to 20 minutes\", \"To make glaze, combine powdered sugar, milk, and seeds scraped from vanilla bean\"]','2026-05-05 21:18:52'),
(12,'2026-05-05 21:53:24',1,'Cabbage Rolls','I used 50/50 ground pork and ground beef, but other meats can be used as well. I read about using sour or pickled cabbage to improve the flavor and make the recipe easier, but I haven\'t tried it yet. I used nappa cabbage.','Simple cabbage rolls made in a slow cooker.','[\"Main\", \"Slow Cooker\"]','[\"cabbage\", \"meat\", \"pork\", \"beef\"]','[\"2 tbsp butter\", \"1 large onion, chopped\", \"1 cup rice, long-grain preferred\", \"2 lbs ground meat\", \"1 head cabbage\", \"6 oz tomato paste\", \"Water or broth (as needed)\", \"Dried oregano\", \"Dried dill\", \"Sumac\", \"Salt and pepper (to taste)\"]','[\"Wash and core the cabbage\", \"Blanch cabbage in boiling water for about 3 to 4 minutes until soft\", \"Melt the butter in a skillet, add onion, and saute a few minutes until softened\", \"Add rice and saute for another minute\", \"In a large bowl, mix the ground meat, salt, pepper, oregano, dill, sumac, and the onion and rice mixture\", \"Once the cabbage has cooled enough, fill each leaf with about 1/4 cup of the meat mixture and roll, tucking in the ends\", \"Repeat with the remaining cabbage and meat mixture\", \"Any remaining cabbage may be chopped and added to the bottom of the slow cooker\", \"Layer cabbage rolls in slow cooker, combine tomato paste with water or broth and pour over cabbage rolls\", \"Add extra water or broth until rolls are covered\", \"Cover with lid and cook on high for 3 or 4 hours or until rolls reach 165\\u00b0F internally\"]','2026-05-05 21:53:24');
/*!40000 ALTER TABLE `recipes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'admin','scrypt:32768:8:1$sTxpok9X2GQpPYII$f4996ac5a7173298ff28949334e50e1c31798165ddbe2aa00c887212109831445c8e5d2ba14981c745fc58ed7f145beccad2da288dd9b9ed5f3c141a1d3dd9ee');
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

-- Dump completed on 2026-05-05 23:06:35
