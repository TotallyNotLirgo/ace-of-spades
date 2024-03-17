USE `ace-of-spades`;
DROP TABLE IF EXISTS `comment`;
DROP TABLE IF EXISTS `session`;
DROP TABLE IF EXISTS `movie`;
DROP TABLE IF EXISTS `user`;

CREATE TABLE `movie` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `year` INT NOT NULL,
  `runtime` INT NOT NULL,
  `genres` VARCHAR(255) NOT NULL,
  `director` VARCHAR(255) NOT NULL, `poster` VARCHAR(255) NOT NULL,
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

INSERT INTO `user` (`username`, `password`, `email`, `role`, `created_at`, `updated_at`) VALUES ('Admin', SHA2('Admin123!', 256), 'admin@email.com', 'admin', NOW(), NOW());
INSERT INTO `user` (`username`, `password`, `email`, `role`, `created_at`, `updated_at`) VALUES ('NewUser', SHA2('NewUser123!', 256), 'new_user@email.com', 'new_user', NOW(), NOW());
INSERT INTO `session` (`user_id`, `token`, `expiration`) VALUES (2, 'new_user_token', DATE_ADD(NOW(), INTERVAL 1 HOUR));
INSERT INTO `user` (`username`, `password`, `email`, `role`, `created_at`, `updated_at`) VALUES ('User', SHA2('User123!', 256), 'user@email.com', 'user', NOW(), NOW());
INSERT INTO `session` (`user_id`, `token`, `expiration`) VALUES (3, 'user_token', DATE_ADD(NOW(), INTERVAL 1 HOUR));
