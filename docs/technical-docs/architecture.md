---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
Nadir Tabouni

{: .no_toc }
# Architecture

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview
Our application is a web-based flashcard management and learning system. It is designed to allow users to create, manage, and learn from custom flashcard decks. The core functionality includes user authentication, deck creation, flashcard creation, and a learning mode that utilizes spaced repetition principles to optimize memorization.

The application is built using the Flask framework for the backend and leverages SQLAlchemy for database interactions. The frontend uses HTML, CSS, and Jinja2 templating engine to render dynamic content.

Key Features:

+ User Authentication: 
  + Users can register, log in, and log out. Passwords are securely hashed using the Werkzeug security library. 
+ Flashcard Deck Management: 
  + Users can create, edit, and delete flashcard decks. Each deck can contain multiple flashcards. 
+ Flashcard Management:
  + Users can add, edit, and delete individual flashcards within a deck. 
+ Learning Mode: 
  + Users can engage in a learning session where flashcards are presented in a shuffled order. Users can mark flashcards as "memorized" or "not memorized," and cards are repeated until all are marked as memorized. 
+ Search and Browse: 
  + Users can search and browse through all available flashcard decks.


![use_case_diagram](images/lumen_use_case_diagram.png)


## Codemap

The application architecture follows the Model-View-Controller (MVC) pattern. The Model represents the data logic, the View is the presentation layer, and the Controller handles user input and interacts with the Model to update the View. 

The following MVC diagram provides a visual representation of how the application is structured:

```mermaid
classDiagram
class Models {
User
FlashcardDeck
Flashcard
}

    class Views {
        add_flashcard.html
        browse_decks.html
        change_password.html
        learning_hub.html
        edit_deck.html
        edit_flashcard.html
        index.html 
        layout.html
        learn_deck.html
        learning_sets.html
        login.html 
        new_deck.html
        profile.html 
        register.html
        view_deck.html
    }

    class Controllers {
        app.py
    }

    Models --> Views : "updates"
    Controllers --> Views : "Renders"
    Controllers --> Models : "Sends update to"
    Views --> Controllers : "Sends requests to"
```
Understanding the directory structure is crucial for navigating and contributing to the project efficiently. The directory structure provides a clear organization of the different components of the application

- lumen 
  - templates
    - add_flashcard.html
    - browse_decks.html
    - change_password.html
    - learning_hub.html
    - edit_deck.html
    - edit_flashcard.html
    - index.html 
    - layout.html
    - learn_deck.html
    - learning_sets.html
    - login.html 
    - new_deck.html
    - profile.html 
    - register.html
    - view_deck.html
  - static 
    - styles.css
  - app.py
  - db.py
  
## Cross-cutting concerns

### Security Measures
Security is a critical aspect of our application to protect user data and maintain user trust.

The application implements several security measures:

+ Password Hashing: 
  + Passwords are hashed using the werkzeug.security library before being stored in the database. This ensures that passwords are not stored in plain text, providing a layer of security against potential breaches.
+ Session Management: 
  + User sessions are managed using Flask's session management. When a user logs in, a session is created and maintained, which expires after a certain period to prevent unauthorized access. This ensures that only authenticated users can access specific parts of the application.

The following sequence diagram illustrates the password hashing and verification process during user login. It shows how the entered password is verified against the stored hash using the Werkzeug security library. Depending on the verification result, the user is either logged in or shown an error message.
```mermaid
sequenceDiagram
participant User
participant Browser
participant Server
participant Database
participant WerkzeugSecurity

    User ->> Browser: Enter login details
    Browser ->> Server: POST /login
    Server ->> Database: Query user credentials
    Database -->> Server: Return user data
    Server ->> WerkzeugSecurity: Verify password hash
    WerkzeugSecurity -->> Server: Verification result
    alt Password correct
        Server ->> Browser: Set session cookie
        Browser -->> User: Redirect to learning hub
    else Password incorrect
        Server -->> Browser: Show error message
        Browser -->> User: Display login error
    end
```

### Error Handling

Error handling is crucial for providing a robust user experience and maintaining the stability of the application. 

Our approach to error handling includes:
+ User-friendly Error Pages: 
  + Custom error pages are created to handle common HTTP errors such as 404 (Not Found) and 500 (Internal Server Error). 
  + These pages provide helpful information to the user without exposing sensitive details about the application.

### User Login

The following sequence diagram illustrates the process of user login and the interactions between different components of the application.

```mermaid
sequenceDiagram
participant User
participant Browser
participant Server
participant Database
    User ->> Browser: Enter login details
    Browser ->> Server: POST /login
    Server ->> Database: Query user credentials
    Database -->> Server: Return user data
    Server ->> Browser: Set session cookie
    Browser -->> User: Redirect to learning hub
```

### Learning Mode
The following sequence diagram illustrates the learning session process, showing how flashcards are presented and reviewed by the user.
```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Server
    participant Database

    User ->> Browser: Start learning session
    Browser ->> Server: GET /deck/:deck_id/learn
    Server ->> Database: Query flashcards for deck
    Database -->> Server: Return flashcards
    Server ->> Browser: Render learn_deck.html with flashcards
    Browser -->> User: Display first flashcard

    loop Until all flashcards memorized
        User ->> Browser: Mark flashcard as (memorized/not memorized)
        Browser ->> Server: POST /flashcard/:flashcard_id/update_status
        Server ->> Database: Update flashcard status
        Database -->> Server: Confirm update
        Server ->> Browser: Show next flashcard
    end

    Browser -->> User: Display success message
    Browser ->> Server: Redirect to learning hub
    Server ->> Browser: Render learning hub
```
