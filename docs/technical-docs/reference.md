---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
Nadir Tabouni

{: .no_toc }
# Reference documentation

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>


## Authentication


### `index()`


**Route:** `/`


**Methods:** `GET`


**Purpose:** Display the homepage with options to log in or register.


**Sample output:**

+ Browser shows the homepage with options to log in or register


---


### `register()`


**Route:** `/register`


**Methods:** `POST` `GET`


**Purpose:** Handle user registration by collecting username, email, and password, hashing the password, and saving the user to the database.


**Sample output:**

+ GET: Browser shows the registration form (register.html)
+ POST (successful registration): Redirects to the /login page.
+ POST (username or email already exists): Shows the error message: 'Username or email already in use!'

---


### `login()`


**Route:** `/login`


**Methods:** `POST` `GET`


**Purpose:** Handle user login by verifying username and password, and establishing a session for the user.


**Sample output:**

+ GET: Browser shows the login form (login.html)
+ POST (successful login): Redirects to the /dashboard page
+ POST (invalid login): Shows the error message: 'Invalid login credentials!'

---
### `login_guest()`


**Route:** `/login-guest`


**Methods:** `POST`


**Purpose:** Log in as a guest user with limited functionality.


**Sample output:**

+ Redirects to the /dashboard page.

---
### `logout()`


**Route:** `/logout`


**Methods:** `POST` `GET`


**Purpose:** Log out the user, clear the session, and delete any guest-created decks and flashcards.


**Sample output:**

+ Redirects to the homepage (/)

---
## User Management


### `dashboard()`


**Route:** `/dashboard`


**Methods:** `GET`


**Purpose:** Display the user's dashboard with options to manage flashcard decks and access the learning mode.


**Sample output:**

+ Browser shows the dashboard page (dashboard.html)

---
### `profile()`


**Route:** `/profile`


**Methods:** `GET`


**Purpose:** Display the user's profile page with options to change the password.


**Sample output:**

+ Browser shows the profile page (profile.html)


---
### `change_password()`


**Route:** `/change-password`


**Methods:** `POST` `GET`


**Purpose:** Allow users to change their password by verifying the old password and setting a new one.


**Sample output:**

+ GET: Browser shows the change password form (change_password.html)
+ POST (successful change): Redirects to the /login page with a success message
+ POST (old password incorrect): Shows the error message: 'Old password is incorrect!'
+ POST (passwords do not match): Shows the error message: 'New passwords do not match!'

---
## Flashcard Deck Management


### `learning_sets()`


**Route:** `/learning-sets`


**Methods:** `GET`


**Purpose:** Show all flashcard decks available to the user.


**Sample output:**

+ Browser shows the learning sets page (learning_sets.html)

---


### `new_deck()`


**Route:** `/new-deck`


**Methods:** `POST` `GET`


**Purpose:** Allow users to create a new flashcard deck, with a restriction for guests to only create one deck.


**Sample output:**

+ GET: Browser shows the new deck form (new_deck.html)
+ POST (successful creation): Redirects to the /learning-sets page
+ POST (guest tries to create multiple decks): Shows the error message: 'Guests can only create one deck. Please register for an account to create more decks.'

---
### `view_deck(deck_id)`


**Route:** `/deck/<int:deck_id>`


**Methods:** `GET`


**Purpose:** Display the contents of a specific flashcard deck, allowing users to view and manage flashcards.


**Sample output:**

+ Browser shows the deck details page (view_deck.html)

---
### `delete_deck(deck_id)`


**Route:** `/deck/<int:deck_id>/delete`


**Methods:** `POST`


**Purpose:** Allow users to delete a specific flashcard deck along with its flashcards.


**Sample output:**

+ Redirects to the /learning-sets page with a success message

---

### `browse_decks()`


**Route:** `/browse-decks`


**Methods:** `POST` `GET`


**Purpose:** Allow users to browse and search for flashcard decks.


**Sample output:**

+ GET: Browser shows the browse decks page with a list of all decks (browse_decks.html)
+ POST (with search query): Browser shows the browse decks page with a list of decks matching the search query (browse_decks.html)

---

## Flashcard Management


### `add_flashcard(deck_id)`


**Route:** `/deck/<int:deck_id>/add-flashcard`


**Methods:** `POST` `GET`


**Purpose:** Allow users to add new flashcards to a specific deck.


**Sample output:**

+ GET: Browser shows the add flashcard form (add_flashcard.html)
+ POST: Redirects to the deck view page (/deck/<int:deck_id>)

---
### `edit_flashcard(flashcard_id)`


**Route:** `/flashcard/<int:flashcard_id>/edit`


**Methods:** `POST` `GET`


**Purpose:** Allow users to edit existing flashcards.


**Sample output:**

+ GET: Browser shows the edit flashcard form (edit_flashcard.html)
+ POST: Redirects to the deck view page (/deck/<int:deck_id>)


---


### `delete_flashcard(flashcard_id)`


**Route:** `/flashcard/<int:flashcard_id>/delete`


**Methods:** `POST`


**Purpose:** Allow users to delete a specific flashcard.


**Sample output:**

+ Redirects to the previous page or /learning-sets with a success message

---


## Learning Mode


### `learn_deck(deck_id)`


**Route:** `/deck/<int:deck_id>/learn`


**Methods:** `GET`


**Purpose:** Initiate the learning mode for a specific deck.


**Sample output:**

+ Browser shows the learn deck page (learn_deck.html)

---
