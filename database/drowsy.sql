/*
SQLyog Community v8.71 
MySQL - 5.5.30 : Database - drowsy
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`drowsy` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `drowsy`;

/*Table structure for table `people` */

DROP TABLE IF EXISTS `people`;

CREATE TABLE `people` (
  `Id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(145) NOT NULL DEFAULT '',
  `password` varchar(145) NOT NULL DEFAULT '',
  `email` varchar(145) NOT NULL DEFAULT '',
  `mobile` varchar(145) NOT NULL DEFAULT '',
  `loginid` varchar(145) NOT NULL DEFAULT '',
  `address` varchar(145) NOT NULL DEFAULT '',
  `city` varchar(145) NOT NULL DEFAULT '',
  `state` varchar(145) NOT NULL DEFAULT '',
  `status` varchar(45) NOT NULL DEFAULT 'waiting',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `people` */

insert  into `people`(`Id`,`username`,`password`,`email`,`mobile`,`loginid`,`address`,`city`,`state`,`status`) values (2,'example','Example@12','example@gmail.com','9876543210','1','hyderabad','hyderabad','telangana','Approved');

/*Table structure for table `review` */

DROP TABLE IF EXISTS `review`;

CREATE TABLE `review` (
  `Id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sentence` varchar(200) NOT NULL DEFAULT '',
  `filename` varchar(205) NOT NULL DEFAULT '',
  `userid` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

/*Data for the table `review` */

insert  into `review`(`Id`,`sentence`,`filename`,`userid`) values (23,'Drowsiness','195.jpg',2),(24,'Normal','1004.jpg',2),(25,'Normal','195.jpg',2),(26,'Drowsiness','140.jpg',2);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
