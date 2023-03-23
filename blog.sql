-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-03-2023 a las 22:53:06
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `blog`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comments`
--

CREATE TABLE `comments` (
  `id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `content` text NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `comments`
--

INSERT INTO `comments` (`id`, `post_id`, `content`, `user_id`, `created_at`) VALUES
(105, 2174, 'Hola soy anonimo\n', 75, '2023-03-13 20:21:03'),
(113, 2174, 'hola', 3, '2023-03-23 19:58:47'),
(114, 2174, 'gf', 3, '2023-03-23 20:01:25'),
(117, 2174, 'Hola\n', 3, '2023-03-23 20:47:04'),
(121, 2174, 'esta pub es mia', 2, '2023-03-23 20:54:08');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `posts`
--

CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `posts`
--

INSERT INTO `posts` (`id`, `title`, `content`, `user_id`, `created_at`) VALUES
(2174, 'The Thing (1982)', 'Un equipo científico de la Antártida descubre un ente extraño que podría ser letal para la humanidad, un extraterrestre que puede duplicar otras formas de vida.', 2, '2023-03-13 19:06:56');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `avatar` varchar(255) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `created_at`, `avatar`) VALUES
(1, 'JhonnysDS', 'j_honydavid@hotmail.com', 'pbkdf2:sha256:260000$LfXUvNQQJRRaS86T$94e992efbb910878ad5f04abfef48d6ec4c8d16e5e9bf247cc0482280ad4eff3', '2023-01-13 03:26:27', NULL),
(2, 'jds', 'jds@mail.com', 'pbkdf2:sha256:260000$pn7Rzpk51PpLxKXz$350d11bb0c4a24acf7f00004ed31ea1b4a9860f29b7b83abfd60c972cb9eb0c5', '2023-01-16 18:34:18', '{\'imagenFullName\': \'cat-gbfd27a440_1280.jpg\', \'imageName\': \'cat-gbfd27a440_1280\', \'imageExt\': \'.jpg\', \'imageSize\': 320729, \'imagePath\': \'cat-gbfd27a440_1280-20230323162002\', \'imageServer\': \'true\'}'),
(3, 'kalel Morningstar', 'kal@gmail.com', 'pbkdf2:sha256:260000$ZS1GyM3ox19SQYi4$3c56d1b05c1e80aa43562cc9d0f1afcf46eae2ea7471bb60a5847e59f6bfe08a', '2023-01-16 16:58:40', '{\'imagenFullName\': \'84248.png\', \'imageName\': \'84248\', \'imageExt\': \'.png\', \'imageSize\': 205680, \'imagePath\': \'84248-20230323161833\', \'imageServer\': \'true\'}'),
(30, '', '', 'pbkdf2:sha256:260000$8T6MCEr6mqjTX7sN$d8b6b44094b18e366ddf551f66d2070eeef3135f1858408cf198f199f7fec1fd', '2023-02-09 21:11:16', NULL),
(102, 'anonimo', 'anonimo@gmail.com', 'pbkdf2:sha256:260000$LVwmW11MZft8BhYc$e836f2080ddda5e076faeabb801b1456414bf09ef653d619e2239372f90e8ed8', '2023-03-16 16:20:17', '{\'imagenFullName\': \'anonimous.jpg\', \'imageName\': \'anonimous\', \'imageExt\': \'.jpg\', \'imageSize\': 921910, \'imagePath\': \'anonimous-20230323162043\', \'imageServer\': \'true\'}'),
(104, 'gato', 'gato@hotmail.com', 'pbkdf2:sha256:260000$LW1dZC4HcFDI7l26$934a6418eb66200636ec35f863bd0b3c5eb80440cc29527d9587225057f79632', '2023-03-16 19:33:39', '{\'imagenFullName\': \'cat-gbfd27a440_1280.jpg\', \'imageName\': \'cat-gbfd27a440_1280\', \'imageExt\': \'.jpg\', \'imageSize\': 320729, \'imagePath\': \'cat-gbfd27a440_1280-20230323162124\', \'imageServer\': \'true\'}');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `post_id` (`post_id`);

--
-- Indices de la tabla `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user_id` (`user_id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `comments`
--
ALTER TABLE `comments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=123;

--
-- AUTO_INCREMENT de la tabla `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2184;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=112;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`);

--
-- Filtros para la tabla `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `posts_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
