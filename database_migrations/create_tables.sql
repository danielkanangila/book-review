DROP SEQUENCE IF EXISTS books_id_seq;
CREATE SEQUENCE books_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 10003 CACHE 1;

CREATE TABLE "public"."books" (
    "id" integer DEFAULT nextval('books_id_seq') NOT NULL,
    "isbn" character varying,
    "title" character varying,
    "author" character varying,
    "year" character varying,
    "average_rating" text,
    CONSTRAINT "books_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "reviews";
DROP SEQUENCE IF EXISTS reviews_id_seq;
CREATE SEQUENCE reviews_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 18 CACHE 1;

CREATE TABLE "public"."reviews" (
    "id" integer DEFAULT nextval('reviews_id_seq') NOT NULL,
    "user_id" integer,
    "book_id" integer,
    "comment" text,
    "rating" integer,
    "created_at" date,
    "updated_at" date,
    CONSTRAINT "reviews_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "reviews_book_id_fkey" FOREIGN KEY (book_id) REFERENCES books(id) NOT DEFERRABLE,
    CONSTRAINT "reviews_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) NOT DEFERRABLE
) WITH (oids = false);


DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS users_id_seq;
CREATE SEQUENCE users_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 73 CACHE 1;

CREATE TABLE "public"."users" (
    "id" integer DEFAULT nextval('users_id_seq') NOT NULL,
    "first_name" character varying NOT NULL,
    "last_name" character varying NOT NULL,
    "email" character varying NOT NULL,
    "password" text NOT NULL,
    "is_active" boolean,
    "access_token" text,
    CONSTRAINT "users_email" UNIQUE ("email"),
    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "verification_tokens";
DROP SEQUENCE IF EXISTS verification_tokens_id_seq;
CREATE SEQUENCE verification_tokens_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 7 CACHE 1;

CREATE TABLE "public"."verification_tokens" (
    "id" integer DEFAULT nextval('verification_tokens_id_seq') NOT NULL,
    "user_id" integer NOT NULL,
    "token" integer NOT NULL,
    "created_at" timestamp NOT NULL,
    "updated_at" timestamp,
    CONSTRAINT "verification_tokens_id" PRIMARY KEY ("id"),
    CONSTRAINT "verification_tokens_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) NOT DEFERRABLE
) WITH (oids = false);