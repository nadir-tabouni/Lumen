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



