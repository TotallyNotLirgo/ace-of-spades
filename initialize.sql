USE `ace-of-spades`;
DROP TABLE IF EXISTS `movie`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `session`;
DROP TABLE IF EXISTS `comment`;

CREATE TABLE `movie` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `year` INT NOT NULL,
  `runtime` INT NOT NULL,
  `genres` VARCHAR(255) NOT NULL,
  `director` VARCHAR(255) NOT NULL,
  `poster` VARCHAR(255) NOT NULL,
  `background` VARCHAR(255) NOT NULL,
  `imdb_rating` REAL NOT NULL,
  `tmdb_rating` REAL NOT NULL,
  `ace_rating` REAL NOT NULL,
  `ace_user_rating` REAL NOT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `role` VARCHAR(255) NOT NULL,
  `profile_picture` VARCHAR(255),
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
);
CREATE TABLE `session` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `token` VARCHAR(255) NOT NULL,
  `expiration` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
);
CREATE TABLE `comment` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `movie_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `content` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`movie_id`) REFERENCES `movie`(`id`),
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`),
  UNIQUE KEY `movie_user` (`movie_id`, `user_id`)
);

INSERT INTO `user` (`username`, `password`, `email`, `role`, `created_at`, `updated_at`) VALUES ('Admin', '3eb3fe66b31e3b4d10fa70b5cad49c7112294af6ae4e476a1c405155d45aa121', 'admin@email.com', 'admin', NOW(), NOW());

