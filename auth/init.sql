CREATE DATABASE "microservice_auth";

create user auth_user with encrypted password 'Auth123'

grant all privileges on database "microservice_auth" to auth_user

CREATE TABLE user (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('lucas@email.com', 'Admin123');
