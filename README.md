🔹 Users Table

Stores information about users who register for the quiz. Each user has a unique username and mobile number. The password is also stored for login authentication.

🔹 Technologies Table

Stores the list of quiz technologies (such as Python, Java, SQL). Each technology has a unique name and is linked to its respective questions.

🔹 Questions Table

Stores all quiz questions along with multiple-choice options and the correct answer. Each question is linked to a specific technology. If a technology is deleted, all its related questions are automatically removed, ensuring data consistency.

🔹 Scores Table

Tracks the results of quizzes attempted by users. It stores the username, mobile number, technology name, score obtained, and the time taken to complete the quiz.
