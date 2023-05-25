-- Insert test data into `user` table
INSERT INTO `quiz_web_app`.`user` (`username`, `email`, `password_hash`, `first_name`, `last_name`, `is_anonymous`, `is_regular`, `is_admin`, `uuid`, `create_time`)
VALUES
    ('john_doe', 'john@example.com', 'password123', 'John', 'Doe', 0, 1, 0, 'abc123', CURRENT_TIMESTAMP),
    ('jane_smith', 'jane@example.com', 'password456', 'Jane', 'Smith', 0, 1, 0, 'def456', CURRENT_TIMESTAMP),
    ('james_brown', 'james@example.com', 'password789', 'James', 'Brown', 0, 1, 0, 'ghi789', CURRENT_TIMESTAMP);

-- Insert test data into `quiz` table
INSERT INTO `quiz_web_app`.`quiz` (`title`, `active`, `comment`, `passed`, `administrator_id`)
VALUES
    ('Quiz 1', 1, 'This is the first quiz', 0, 1),
    ('Quiz 2', 1, 'This is the second quiz', 0, 2),
    ('Quiz 3', 1, 'This is the third quiz', 0, 3);

-- Insert test data into `question` table
INSERT INTO `quiz_web_app`.`question` (`quiz_id`, `title`, `content`, `answer_type`, `category`, `passed`)
VALUES
    (1, 'Question 1', 'Content of Question 1', 'multiple', 'Category 1', 0),
    (1, 'Question 2', 'Content of Question 2', 'single', 'Category 1', 0),
    (2, 'Question 3', 'Content of Question 3', 'essay', 'Category 2', 0),
    (2, 'Question 4', 'Content of Question 4', 'multiple', 'Category 2', 0),
    (3, 'Question 5', 'Content of Question 5', 'single', 'Category 3', 0);

-- Insert test data into `answer` table
INSERT INTO `quiz_web_app`.`answer` (`question_id`, `question_quiz_id`, `answer`, `comment`, `correct`)
VALUES
    (1, 1, 'Answer 1 for Question 1', 'Comment for Answer 1', 1),
    (1, 1, 'Answer 2 for Question 1', 'Comment for Answer 2', 0),
    (2, 1, 'Answer 1 for Question 2', 'Comment for Answer 1', 1),
    (2, 1, 'Answer 2 for Question 2', 'Comment for Answer 2', 0),
    (3, 2, '', 'Comment for Essay Answer', NULL),
    (4, 2, 'Answer 1 for Question 4', 'Comment for Answer 1', 1),
    (4, 2, 'Answer 2 for Question 4', 'Comment for Answer 2', 0),
    (5, 3, 'Answer 1 for Question 5', 'Comment for Answer 1', 1),
    (5, 3, 'Answer 2 for Question 5', 'Comment for Answer 2', 0);