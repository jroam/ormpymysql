/*
Navicat MySQL Data Transfer

Source Server         : 本地
Source Server Version : 50532
Source Host           : localhost:3306
Source Database       : xsite

Target Server Type    : MYSQL
Target Server Version : 50532
File Encoding         : 65001

Date: 2017-08-29 17:10:40
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for x_news
-- ----------------------------
DROP TABLE IF EXISTS `x_news`;
CREATE TABLE `x_news` (
  `news0` int(11) NOT NULL AUTO_INCREMENT,
  `news1` varchar(200) DEFAULT NULL,
  `news2` int(11) DEFAULT NULL,
  PRIMARY KEY (`news0`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of x_news
-- ----------------------------
INSERT INTO `x_news` VALUES ('1', '九寨沟三日游2356', '1111111');
INSERT INTO `x_news` VALUES ('2', '黄龙四日游', '11112222');

-- ----------------------------
-- Table structure for x_price
-- ----------------------------
DROP TABLE IF EXISTS `x_price`;
CREATE TABLE `x_price` (
  `price0` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `prices` int(11) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  PRIMARY KEY (`price0`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of x_price
-- ----------------------------
INSERT INTO `x_price` VALUES ('1', '平常价', '1000', '2');
INSERT INTO `x_price` VALUES ('2', '淡务价', '2000', '2');
