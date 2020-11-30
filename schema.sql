DROP DATABASE IF EXISTS `quiz_manager`;
CREATE DATABASE `quiz_manager`;

USE `quiz_manager`;

CREATE TABLE `Permission` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Label` varchar(20) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE (`Label`)
);

CREATE TABLE `Authentication` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `PermissionID` int NOT NULL,
  `Username` varchar(20) NOT NULL,
  `Password` varchar(256) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE (`Username`),
  CONSTRAINT `FK_PermissionID` FOREIGN KEY (`PermissionID`) REFERENCES `Permission` (`ID`) ON DELETE RESTRICT ON UPDATE RESTRICT
);

CREATE TABLE `Quiz` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Title` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
);

CREATE TABLE `Question` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `QuizID` int NOT NULL,
  `QuestionText` varchar(200) NOT NULL,
  `QuestionOrder` int NOT NULL,
  `AnswerA` varchar(200) NOT NULL,
  `AnswerB` varchar(200) NOT NULL,
  `AnswerC` varchar(200) NOT NULL,
  `AnswerD` varchar(200) DEFAULT NULL,
  `AnswerE` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `FK_QuizID` FOREIGN KEY (`QuizID`) REFERENCES `Quiz` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE FUNCTION `encryptPassword` (inText varchar(256))
RETURNS varchar(200) DETERMINISTIC
RETURN SHA2(inText, 256);

DELIMITER //

CREATE TRIGGER `Authentication_BEFORE_INSERT` BEFORE INSERT
ON `Authentication` FOR EACH ROW
BEGIN
  SET NEW.Password = encryptPassword(NEW.Password);
END//

CREATE TRIGGER `Authentication_BEFORE_UPDATE` BEFORE UPDATE
ON `Authentication` FOR EACH ROW
BEGIN
  IF OLD.Password <> NEW.Password THEN
    SET NEW.Password = encryptPassword(NEW.Password);
  END IF;
END//

DELIMITER ;

DROP USER IF EXISTS 'quizmanager.backend'@'localhost';
CREATE USER 'quizmanager.backend'@'localhost' IDENTIFIED BY 'wNk_3X4=8Pf_PPyi';
GRANT ALL PRIVILEGES ON *.* TO 'quizmanager.backend'@'localhost';

DROP USER IF EXISTS 'quizmanager.pwdwriter'@'localhost';
CREATE USER 'quizmanager.pwdwriter'@'localhost' IDENTIFIED BY 'e+kXzEo%+fGdWq8V';
GRANT ALL PRIVILEGES ON *.* TO 'quizmanager.pwdwriter'@'localhost';
