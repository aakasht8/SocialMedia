# Project Name: Social Media Application

**Description:** Django project created to manage multiple users, allowing them to interact with other users via friend requests.

# Table of Contents

1. [Installation](#installation)
2. [API Usage](#api-usage)


# Installation
To run this project locally using Docker, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aakasht8/SocialMedia.git

2. **Navigate to the project directory**
   ```bash
   cd home

3. **Build and run the Docker containers using Docker Compose:**
   ```bash
   docker-compose up --build

4. **Once the containers are running, you can access the Django application at http://localhost:8000 in your web browser or Postman**

5. **Import the file: Postman.json in the home directory to import the postman collection.**

6. **Import the file: Postman.json in the home directory to import the postman environment collection.**



# API Usage 
These are the following API's included in this project

1. **Signup a new User:**
   API url: http://127.0.0.1:8000/api/signup/ (POST Method)

   Request Body:
   ```json
   {
    "username": "Sarthak",
    "email": "sarthak@england.com",
    "password": "England"
   }

2. **Login to existing User:**
   API url: http://127.0.0.1:8000/api/signup/ (POST Method)

   Request Body:
      ```json
   {
       "username": "Elias",
       "password": "England"
   }

3. **Logout User:**
   API url: http://127.0.0.1:8000/api/logout/ (POST Method)

4. **Search Users:**
   API url: http://127.0.0.1:8000/api/search?search=a (GET Method)

5. **Send friend request to User:**
   API url: http://127.0.0.1:8000/api/send_request/ (POST Method)

   Request Body:
      ```json
   {"receiver_id": 4}

6. **Respond to friend requests:**
   API url: http://127.0.0.1:8000/api/respond_request/22/1 (POST Method)

7. **List friend requests:**
   API url: http://127.0.0.1:8000/api/list_requests/ (GET Method)

8. **List friends:**
   API url: http://127.0.0.1:8000/api/list_friends/ (GET Method)


    
