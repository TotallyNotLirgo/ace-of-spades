BEGIN TRANSACTION;
DROP TABLE IF EXISTS "movies";
CREATE TABLE IF NOT EXISTS "movies" (
	"id"	INTEGER,
	"title"	TEXT,
	"date_of_release"	INTEGER,
	"genres"	TEXT,
	"description"	TEXT,
	"imdb_rating"	REAL,
	"tmdb_rating"	REAL,
	"ace_user_rating"	REAL,
	"ace_rating"	REAL,
	"background_image"	TEXT,
	"poster_image"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "comments";
CREATE TABLE IF NOT EXISTS "comments" (
	"id"	INTEGER,
	"user_id"	INTEGER,
	"movie_id"	INTEGER,
	"content"	TEXT,
	"date_created"	INTEGER,
	"date_edited"	INTEGER,
	FOREIGN KEY("movie_id") REFERENCES "movies"("id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "users";
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"email"	TEXT UNIQUE,
	"password"	TEXT,
	"username"	TEXT UNIQUE,
	"profile_picture"	TEXT,
	"role"	TEXT,
	"token"	TEXT UNIQUE,
	"expiration"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
