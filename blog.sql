-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-01-2023 a las 23:42:37
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
(1, 1, 'comentario editado', 0, '2023-01-16 19:14:41'),
(2, 2, 'comentario de prueba', 0, '2023-01-16 19:15:14'),
(4, 2, 'comentario de prueba con id del usuario', 2, '2023-01-16 20:09:07'),
(5, 4, 'comentario de prueba con id del usuario con id 3', 3, '2023-01-16 20:10:16'),
(6, 5, 'comentario de prueba con id del usuario con id 3', 3, '2023-01-16 20:11:28'),
(7, 5, 'comentario de prueba con id del usuario con id 1', 1, '2023-01-16 20:12:03'),
(8, 1, '', 3, '2023-01-16 22:34:01'),
(9, 1, 'dasdasdsad', 3, '2023-01-16 22:34:09'),
(10, 1, 'asdsadasda', 3, '2023-01-16 22:34:14'),
(11, 4, 'gffffffffffffffff', 3, '2023-01-16 22:34:25'),
(12, 4, 'ya se crea', 3, '2023-01-16 22:36:13'),
(13, 3, 'Ejemplo numero yo no sé qué', 3, '2023-01-16 22:37:23'),
(14, 3, 'otro ejemplo', 3, '2023-01-16 22:38:35'),
(15, 3, 'sas', 3, '2023-01-16 22:39:03');

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
(1, 'prueba', 'prueba', 2, '2023-01-16 13:59:26'),
(2, 'prueba 2', 'prueba 2', 2, '2023-01-16 16:54:41'),
(3, 'prueba 3', 'prueba 3', 1, '2023-01-16 16:56:38'),
(4, 'Prueba desde front', 'detalles de prueba desde front', 2, '2023-01-16 17:05:11'),
(5, 'prueba kal', 'kal prueba', 3, '2023-01-16 18:57:18');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `created_at`) VALUES
(1, 'JhonnysDS', 'j_honydavid@hotmail.com', 'pbkdf2:sha256:260000$LfXUvNQQJRRaS86T$94e992efbb910878ad5f04abfef48d6ec4c8d16e5e9bf247cc0482280ad4eff3', '2023-01-13 03:26:27'),
(2, 'jds', 'jds@mail.com', 'pbkdf2:sha256:260000$pn7Rzpk51PpLxKXz$350d11bb0c4a24acf7f00004ed31ea1b4a9860f29b7b83abfd60c972cb9eb0c5', '2023-01-16 18:34:18'),
(3, 'kal', 'kal@gmail.com', 'pbkdf2:sha256:260000$WwOMoRt1SnRBnDrf$222b0c9beaa267acb3bb16174bae9a80d2b87fcfc27bfbd062e60bc4f3343b0d', '2023-01-16 16:58:40');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_post_id` (`post_id`),
  ADD KEY `user_id` (`user_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

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
