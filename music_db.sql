-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 27, 2025 at 03:17 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `music_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `liked_songs`
--

CREATE TABLE `liked_songs` (
  `id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `liked_songs`
--

INSERT INTO `liked_songs` (`id`, `song_id`) VALUES
(3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `songs`
--

CREATE TABLE `songs` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `artist` varchar(255) NOT NULL,
  `file_path` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `songs`
--

INSERT INTO `songs` (`id`, `title`, `artist`, `file_path`) VALUES
(1, 'Make Some Noise For Desi Boyz', 'Pritam', 'C:/Users/dhvan/OneDrive/Desktop/NIKHAR/FinalProject-Sem-3/Demo1-Python/Songs/Make Some Noise For Desi Boyz by Pritam.mp3'),
(2, 'Naacho Naacho', 'Vishal Mishra', 'C:/Users/dhvan/OneDrive/Desktop/NIKHAR/FinalProject-Sem-3/Demo1-Python/Songs/Naacho Naacho by Vishal Mishra.mp3'),
(3, 'Sooraj Ki Bahon Mein', 'Shankar-Ehsaan-Loy', 'C:/Users/dhvan/OneDrive/Desktop/NIKHAR/FinalProject-Sem-3/Demo1-Python/Songs/Sooraj Ki Bahon Mein by Shankar-Ehsaan-Loy.mp3'),
(4, 'Aarambh', 'Piyush Mishra', 'C:/Users/dhvan/OneDrive/Desktop/NIKHAR/FinalProject-Sem-3/Demo1-Python/Songs/Aarambh by Piyush Mishra.mp3'),
(6, 'Khalasi', 'Aditya Gadhvi', 'C:/Users/dhvan/OneDrive/Desktop/NIKHAR/FinalProject-Sem-3/Demo1-Python/Songs/Khalasi by Aditya Gadhvi.mp3');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `liked_songs`
--
ALTER TABLE `liked_songs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `song_id` (`song_id`);

--
-- Indexes for table `songs`
--
ALTER TABLE `songs`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `liked_songs`
--
ALTER TABLE `liked_songs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `songs`
--
ALTER TABLE `songs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `liked_songs`
--
ALTER TABLE `liked_songs`
  ADD CONSTRAINT `liked_songs_ibfk_1` FOREIGN KEY (`song_id`) REFERENCES `songs` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
