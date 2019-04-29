/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : bai

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2019-04-29 12:35:13
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for spider_user_info
-- ----------------------------
DROP TABLE IF EXISTS `spider_user_info`;
CREATE TABLE `spider_user_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author` varchar(255) DEFAULT NULL COMMENT '用户昵称',
  `home_url` varchar(255) DEFAULT NULL COMMENT '用户主页地址',
  `fans_num` int(11) DEFAULT NULL COMMENT '粉丝数量',
  `avatar_url` varchar(255) DEFAULT NULL COMMENT '用户头像地址',
  `source_name` varchar(255) DEFAULT NULL COMMENT '来源名称 今日头条/百家号',
  `brief` varchar(1024) DEFAULT NULL COMMENT '作者简介',
  `biz` varchar(255) DEFAULT NULL COMMENT '平台对应的账户id',
  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `status` int(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1256 DEFAULT CHARSET=utf8;
