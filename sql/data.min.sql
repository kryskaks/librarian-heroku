insert into users(login, password) values('admin', 'adminp@ss');

insert into books(title) values('The Lord of the Rings');

INSERT INTO authors(name) 
SELECT 'John Ronald Reuel Tolkien' 
WHERE NOT EXISTS(SELECT 1 FROM authors WHERE name = 'John Ronald Reuel Tolkien');

insert into books_to_authors(book_id, author_id) values(
	(select id from books where title = 'The Lord of the Rings'),
	(select id from authors where name = 'John Ronald Reuel Tolkien'));
----------------------------------------------------------------------------------------------------
insert into books(title) values('Pride and Prejudice');

INSERT INTO authors(name) 
SELECT 'Jane Austen' 
WHERE NOT EXISTS(SELECT 1 FROM authors WHERE name = 'Jane Austen');

insert into books_to_authors(book_id, author_id) values(
	(select id from books where title = 'Pride and Prejudice'),
	(select id from authors where name = 'Jane Austen'));
----------------------------------------------------------------------------------------------------
insert into books(title) values('His Dark Materials');

INSERT INTO authors(name) 
SELECT 'Philip Pullman' 
WHERE NOT EXISTS(SELECT 1 FROM authors WHERE name = 'Philip Pullman');

insert into books_to_authors(book_id, author_id) values(
	(select id from books where title = 'His Dark Materials'),
	(select id from authors where name = 'Philip Pullman'));
----------------------------------------------------------------------------------------------------
insert into books(title) values("The Hitchhiker's Guide to the Galaxy");

INSERT INTO authors(name) 
SELECT 'Douglas Adams' 
WHERE NOT EXISTS(SELECT 1 FROM authors WHERE name = 'Douglas Adams');

insert into books_to_authors(book_id, author_id) values(
	(select id from books where title = "The Hitchhiker's Guide to the Galaxy"),
	(select id from authors where name = 'Douglas Adams'));
----------------------------------------------------------------------------------------------------
insert into books(title) values('Harry Potter and the Goblet of Fire');

INSERT INTO authors(name) 
SELECT 'J. K. Rowling' 
WHERE NOT EXISTS(SELECT 1 FROM authors WHERE name = 'J. K. Rowling');

insert into books_to_authors(book_id, author_id) values(
	(select id from books where title = 'Harry Potter and the Goblet of Fire'),
	(select id from authors where name = 'J. K. Rowling'));
----------------------------------------------------------------------------------------------------
insert into books(title) values('To Kill a Mockingbird');

INSERT INTO authors(name) 
SELECT 'Harper Lee' 
WHERE NOT EXISTS(SELECT 1 FROM authors WHERE name = 'Harper Lee');

insert into books_to_authors(book_id, author_id) values(
	(select id from books where title = 'To Kill a Mockingbird'),
	(select id from authors where name = 'Harper Lee'));
----------------------------------------------------------------------------------------------------
insert into books(title) values('Winnie-the-Pooh');

INSERT INTO authors(name) 
SELECT 'Alan Alexander Milne' 
WHERE NOT EXISTS(SELECT 1 FROM authors WHERE name = 'Alan Alexander Milne');

insert into books_to_authors(book_id, author_id) values(
	(select id from books where title = 'Winnie-the-Pooh'),
	(select id from authors where name = 'Alan Alexander Milne'));
----------------------------------------------------------------------------------------------------
insert into books(title) values('Nineteen Eighty-Four');

INSERT INTO authors(name) 
SELECT 'George Orwell' 
WHERE NOT EXISTS(SELECT 1 FROM authors WHERE name = 'George Orwell');

insert into books_to_authors(book_id, author_id) values(
	(select id from books where title = 'Nineteen Eighty-Four'),
	(select id from authors where name = 'George Orwell'));
----------------------------------------------------------------------------------------------------
insert into books(title) values('The Lion, the Witch and the Wardrobe');

INSERT INTO authors(name) 
SELECT 'Clive Staples Lewis' 
WHERE NOT EXISTS(SELECT 1 FROM authors WHERE name = 'Clive Staples Lewis');

insert into books_to_authors(book_id, author_id) values(
	(select id from books where title = 'The Lion, the Witch and the Wardrobe'),
	(select id from authors where name = 'Clive Staples Lewis'));
----------------------------------------------------------------------------------------------------
insert into books(title) values('Little Women');

INSERT INTO authors(name) 
SELECT 'Louisa May Alcott' 
WHERE NOT EXISTS(SELECT 1 FROM authors WHERE name = 'Louisa May Alcott');

insert into books_to_authors(book_id, author_id) values(
	(select id from books where title = 'Little Women'),
	(select id from authors where name = 'Louisa May Alcott'));
