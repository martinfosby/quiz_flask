-- Insert test data into `user` table
INSERT INTO `quiz_web_app`.`user` (`username`, `email`, `password_hash`, `first_name`, `last_name`, `is_anonymous`, `is_regular`, `is_admin`, `uuid`, `create_time`)
VALUES
    ('john_doe', 'john@example.com', 'password123', 'John', 'Doe', 0, 1, 0, 'abc123', CURRENT_TIMESTAMP),
    ('jane_smith', 'jane@example.com', 'password456', 'Jane', 'Smith', 0, 1, 0, 'def456', CURRENT_TIMESTAMP);

-- Insert test data into `quiz` table
INSERT INTO `quiz_web_app`.`quiz` (`title`, `active`, `comment`, `passed`, `administrator_id`)
VALUES
    ('Quiz 1', 1, 'This is the first quiz', 0, 1),
    ('Quiz 2', 1, 'This is the second quiz', 0, 2);

-- Insert test data into `question` table
INSERT INTO `quiz_web_app`.`question` (`id`, `quiz_id`, `text`, `answer_type`, `passed`, `category`)
VALUES
    (1, 1, 'What is the capital of France?', 'multiple', 0, 'Geography'),
    (2, 1, 'Who painted the Mona Lisa?', 'single', 0, 'Art');

-- Insert test data into `answer` table
INSERT INTO `quiz_web_app`.`answer` (`id`, `question_id`, `question_quiz_id`, `answer`, `comment`, `correct`)
VALUES
    (1, 1, 1, 'Paris', 'Correct answer', 1),
    (2, 1, 1, 'London', 'Incorrect answer', 0),
    (3, 2, 1, 'Leonardo da Vinci', 'Correct answer', 1),
    (4, 2, 1, 'Pablo Picasso', 'Incorrect answer', 0);

-- Insert test data into `user_has_answer` table
INSERT INTO `quiz_web_app`.`user_has_answer` (`user_id`, `answer_id`, `answer_question_id`, `answer_question_quiz_id`)
VALUES
    (1, 1, 1, 1),
    (1, 3, 2, 1),
    (2, 2, 1, 1),
    (2, 3, 2, 1);


