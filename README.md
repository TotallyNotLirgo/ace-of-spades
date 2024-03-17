# Ace Of Spades

## Description
This is an API for a site that allows users to see
movies' lack of sexual content score. The API will
allow users to see the score of a movie, to rate
the movies themselves, and also to post comments
about the movie. It includes basic CRUD operations
for users, and comments. The movies are fetched
from the TMDB API. The API is built using FastAPI.

## Installation

1. Clone the repository
```bash
git clone https://github.com/TotallyNotLirgo/ace-of-spades.git
```
2. Install the dependencies
```bash
pip install -r requirements.txt
```
3. Copy the .env.example file to .env
```bash
cp .env.example .env
```
4. Fill the .env file with the required information

## Usage

1. Run the server
```bash
python .
```
2. Go to the server's address in your browser as stated in the console

## Running with docker

You may also run the server using docker. To do so, you need to have docker
and docker-compose installed on your machine.

1. Build the docker image
```bash
docker-compose up --build
```
2. Go to the server's address in your browser as stated in the console
3. To use the API there is an admin account with the following credentials:
```json
{
  "username": "Admin",
  "password": "Admin123!"
}
```
To edit the admin account, you can change the values in the initialize.sql file
