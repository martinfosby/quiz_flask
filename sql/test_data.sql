



INSERT INTO user (username, password_hash, first_name, last_name)
VALUES
    ('amandasmith', 'password678'),
    ('michaeljones', 'password901'),
    ('sophiawilliams', 'password234'),
    ('samuelbrown', 'password567'),
    ('oliviawilson', 'password890');


INSERT INTO quiz (title, question, active, category, type, comment)
VALUES 
    ('Science Quiz', 'What is the chemical symbol for gold?', 1, 'Chemistry', 'multiple' ),
    ('History Quiz', 'Who was the first president of the United States?', 1, 'single'),
    ('Geography Quiz', 'What is the capital city of Australia?', 0, 'Geography', 2),
    ('Literature Quiz', 'Who wrote the novel "To Kill a Mockingbird"?', 1, 'Literature', 1),
    ('Math Quiz', 'What is the value of pi?', 1, 'Mathematics', 3),
    ('Music Quiz', 'Who composed the opera "The Barber of Seville"?', 0, 'Music', 4),
    ('Sports Quiz', 'Which country won the FIFA World Cup in 2018?', 1, 'Sports', 2),
    ('Technology Quiz', 'What is the name of Apple''s virtual assistant?', 1, 'Technology', 4),
    ('Animal Quiz', 'What is the largest mammal in the world?', 1, 'Science', 3),
    ('Food Quiz', 'What is the national dish of Italy?', 0, 'Cuisine', 1),
    ('Movie Quiz', 'Who directed the movie "Pulp Fiction"?', 1, 'Movies', 2);

INSERT INTO answer (answer, passed, quiz_id)
VALUES 
  ('Hydrogen',     1, 1), ('Helium',   0, 1), ('Oxygen',   0, 1), ('Carbon', 0, 1), 
  ('George Washington', 1, 2), ('Thomas Jefferson', 0, 2), ('John Adams', 0, 2), ('Benjamin Franklin', 0, 2),
  ('Canberra', 1, 3), ('Melbourne', 0, 3), ('Sydney', 0, 3), ('Brisbane', 0, 3),
  ('Harper Lee', 1, 4), ('John Steinbeck', 0, 4), ('Ernest Hemingway', 0, 4), ('F. Scott Fitzgerald', 0, 4),
  ('3.14', 1, 5), ('2.72', 0, 5), ('1.61', 0, 5), ('1.41', 0, 5),
  ('Gioachino Rossini', 1, 6), ('Wolfgang Amadeus Mozart', 0, 6), ('Johann Sebastian Bach', 0, 6), ('Ludwig van Beethoven', 0, 6),
  ('France', 0, 7), ('Germany', 0, 7), ('Brazil', 1, 7), ('Argentina', 0, 7),
  ('Siri', 1, 8), ('Alexa', 0, 8), ('Cortana', 0, 8), ('Google Assistant', 0, 8),
  ('Blue Whale', 1, 9), ('African Elephant', 0, 9), ('Giraffe', 0, 9), ('Hippopotamus', 0, 9),
  ('Pizza', 0, 10), ('Lasagna', 0, 10), ('Risotto', 0, 10), ('Spaghetti', 1, 10),
  ('Quentin Tarantino', 1, 11), ('Martin Scorsese', 0, 11), ('Steven Spielberg', 0, 11), ('Christopher Nolan', 0, 11);


INSERT INTO user_has_quiz (user_id, quiz_id) 
SELECT user.id, quiz.id 
FROM user 
JOIN quiz;


-- INSERT INTO user_has_answer (user_id, answer_id) 
-- SELECT user.id, answer.id 
-- FROM user 
-- JOIN answer;