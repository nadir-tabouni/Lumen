---
title: Design Decisions
nav_order: 3
---

{: .label }
Lumen

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>


---

## 01: What Database to use

### Meta

Status
: **Decided**

Updated
: 16-Apr-2024

### Problem statement

Should we use SQLite or Firebase for our project's database needs?

Our web application requires a database solution, and we considered both SQLite and Firebase. 
We aimed to choose a database that aligns with our team's current expertise and the project's immediate requirements.

Therefore, we will likely:

+ Evaluate our database needs periodically to ensure that our chosen solution continues to meet our performance and scalability requirements.
+ Consider transitioning to a more scalable database solution.

### Decision

We chose SQLite.

Our team is already familiar with SQLite, and it fits well with our current project's scope. 
This decision allows us to leverage our existing knowledge and quickly implement the necessary database functionalities without a steep learning curve.

*Decision was taken by:* github.com/nadir-tabouni, github.com/Cennet99

### Regarded options

We regarded two alternative options:

+ SQLite
+ Firebase

| Criterion                   | SQLite                                   | Firebase                              |
|-----------------------------|------------------------------------------|---------------------------------------|
| **Know-how**                | ✔️ Familiar with SQLite                  | ❌ Limited experience with Firebase    |
| **Setup and Configuration** | ✔️ Simple and quick                      | ❔ Moderate complexity, requires setup |
| **Scalability**             | ❔ Limited for small to medium projects   | ✔️ Highly scalable                    |

---
## 02: How to perform Database operations

### Meta

Status
: **Decided**

Updated
: 18-Apr-2024

### Problem statement

Should we use SQLAlchemy for performing database CRUD (create, read, update, delete) operations in our application?

We need to decide whether to continue with plain SQL or adopt SQLAlchemy as an object-relational mapper (ORM) to improve code robustness and maintainability.

Therefore, we will likely:

+ Utilize SQLAlchemy’s ORM capabilities to abstract database operations, making future database engine changes smoother.

### Decision

We chose to use SQLAlchemy.

SQLAlchemy enhances the robustness of our code by eliminating the need for raw SQL statements, reducing the potential for errors and making the code more readable. 
Additionally, it provides an abstraction layer that simplifies switching to different database engines in the future, ensuring our code remains functional with minimal changes.

*Decision was taken by:* github.com/nadir-tabouni, github.com/Cennet99

### Regarded options

We regarded two alternative options:

+ Plain SQL
+ SQLAlchemy

| Criterion                       | Plain SQL                                     | SQLAlchemy                                     |
|---------------------------------|-----------------------------------------------|------------------------------------------------|
| **Know-how**                    | ✔️ Familiar with SQL                          | ❌ Need to get familiar with SQLAlchemy         |
| **Code Robustness**             | ❌ Prone to SQL injection and syntax errors    | ✔️ Less prone to errors due to ORM abstraction |
| **Database Engine Flexibility** | ❌ Requires code changes for different engines | ✔️ Abstracts database engine, easier to switch |

---

## 03: Password Hashing Strategy


### Meta


Status
: **Decided**


Updated
: 20-Apr-2024


### Problem statement


How should we securely store user passwords to protect against data breaches?


Secure storage of user passwords is critical to ensure that, in the event of a data leak, the passwords remain protected and unusable by malicious actors.


Therefore, we will likely:


+ Regularly review and update our security practices to maintain a high level of protection against emerging threats.


### Decision


We chose to use werkzeug.security for password hashing.


werkzeug.security provides a high level of security and is straightforward to implement, making it an ideal choice for our application.
When using werkzeug.security for password hashing, a password is converted into a unique hash value that cannot be reversed.


*Decision was taken by:* github.com/nadir-tabouni


### Regarded options


We regarded two alternative options:


+ werkzeug.security
+ Hashmaps


| Criterion                       | werkzeug.security                                | Hashmaps                                       |
|---------------------------------|--------------------------------------------------|------------------------------------------------|
| **Security**                    | ✔️ High security with strong hashing algorithms  | ❌ Lower security                               |
| **Implementation Ease**         | ✔️  Simple to implement with built-in functions  | ❌ More complex, requires custom implementation |


---

## 04: Choice of Learning Method


### Meta


Status
: **Decided**


Updated
: 22-Jun-2024


### Problem statement


How should we implement the flashcard learning method to maximize effectiveness and retention for users?


We need to decide whether to keep displaying flashcards without any specific system for users to go through at their own pace, implement the Leitner system with three categories of knowledge, or create a variation of the Leitner system where only incorrectly answered questions are repeated until all cards are correctly answered.


### Decision


We chose to implement a variation of the Leitner system.


In this variation, users will mark each flashcard as either "correctly answered" or "incorrectly answered." Only the flashcards marked as "incorrectly answered" will be repeated until all cards are marked as "correctly answered."
This method ensures focused repetition on areas where the user needs the most improvement while keeping the system simple and effective.


*Decision was taken by:* github.com/nadir-tabouni, github.com/Cennet99


### Regarded options


We regarded two alternative options:


+ Simple flashcard display without a specific system
+ Traditional Leitner system with three categories
+ Variation of the Leitner system focusing on incorrect answers


| Criterion                  | Simple Flashcards                           | Traditional Leitner System                | Variation of Leitner System                       |
|----------------------------|---------------------------------------------|-------------------------------------------|---------------------------------------------------|
| **Effectiveness**          | ❌ Limited, user may not focus on weak areas | ✔️ Effective, systematic repetition       | ✔️ Effective, targeted repetition                 |
| **Implementation Ease**    | ✔️ Simple to implement (already set up)     | ❌ complex, detailed algorithm             | ❔ Moderate complexity, simpler algorithm          |
| **User Engagement**        | ❌ May lead to user boredom                  | ✔️ Engages users with structured learning | ✔️  Keeps users engaged by focusing on challenges |


---





