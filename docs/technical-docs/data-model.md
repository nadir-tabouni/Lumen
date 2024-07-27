---
title: Data Model
parent: Technical Docs
nav_order: 2
---

{: .label }
Cennet Kurnaz

{: .no_toc }
# Data model

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

```mermaid
erDiagram
    USER {
        int id PK
        varchar username
        varchar email
        varchar password_hash
    }
    FLASHCARDDECK {
        int id PK
        varchar name
        varchar description
        int user_id FK
    }
    FLASHCARD {
        int id PK
        varchar question
        varchar answer
        int deck_id FK
    }
    USER ||--o{ FLASHCARDDECK : owns
    FLASHCARDDECK ||--o{ FLASHCARD : contains
```

### Description:
- **USER**: The table stores user data such as `id`, `username`, `email`, and `password_hash`.
- **FLASHCARDDECK**: This table stores information about flashcard decks such as `id`, `name`, `description`, and `user_id`, which is a foreign key referring to the `USER` table.
- **FLASHCARD**: This table stores flashcards with fields `id`, `question`, `answer`, and `deck_id`, which is a foreign key referring to the `FLASHCARDDECK` table.

### Relationships:
- A **USER** can own multiple **FLASHCARDDECKS**.
- A **FLASHCARDDECK** can contain multiple **FLASHCARDS**.
