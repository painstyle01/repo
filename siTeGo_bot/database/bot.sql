-- phpMyAdmin SQL Dump
-- version 3.5.1
-- http://www.phpmyadmin.net
--
-- Хост: 127.0.0.1
-- Время создания: Фев 19 2019 г., 22:24
-- Версия сервера: 5.5.25
-- Версия PHP: 5.3.13

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- База данных: `bot`
--

-- --------------------------------------------------------

--
-- Структура таблицы `brief`
--

CREATE TABLE IF NOT EXISTS `brief` (
  `id` int(11) NOT NULL,
  `client_name` text NOT NULL,
  `date` date NOT NULL,
  `contact` text NOT NULL,
  `phone` text NOT NULL,
  `e_mail` text NOT NULL,
  `1_1` text NOT NULL,
  `1_2` text NOT NULL,
  `1_3` text NOT NULL,
  `1_4` text NOT NULL,
  `1_5` text NOT NULL,
  `1_6` text NOT NULL,
  `1_7` text NOT NULL,
  `2_1` text NOT NULL,
  `3_1` text NOT NULL,
  `3_2` text NOT NULL,
  `4_1` text NOT NULL,
  `4_2` text NOT NULL,
  `4_3` text NOT NULL,
  `4_4` text NOT NULL,
  `4_5` text NOT NULL,
  `4_6` text NOT NULL,
  `4_7` text NOT NULL,
  `4_8` text NOT NULL,
  `5_1` text NOT NULL,
  `5_2` text NOT NULL,
  `5_3` text NOT NULL,
  `6_1` text NOT NULL,
  `6_2` text NOT NULL,
  `7_1` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Main brief data.';

-- --------------------------------------------------------

--
-- Структура таблицы `main`
--

CREATE TABLE IF NOT EXISTS `main` (
  `id` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `username` text NOT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Main table. Steps in bot + username to messaging';

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
