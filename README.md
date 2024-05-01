[![Backend CI/CD](https://github.com/software-students-spring2024/5-final-project-spring-2024-team7-final/actions/workflows/backend.yml/badge.svg)](https://github.com/software-students-spring2024/5-final-project-spring-2024-team7-final/actions/workflows/backend.yml)

# Final Project

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

## Project Description

The **School Task Manager** is designed to assist students in effectively managing their academic tasks. By using this web application, students can organize, track, and meet deadlines for their school assignments and projects, ensuring they never miss a due date.

**MongoDB Database**: The backend of the School Task Manager utilizes MongoDB to store user data, tasks, courses, and deadlines efficiently. This setup allows for high performance and scalability, which is ideal for handling multiple user requests simultaneously.

**Web Application**: The integrated web app(included both front&back end) is built with modern web technologies, providing a clean and user-friendly interface for students to interact with their task lists. Features include adding new tasks, setting deadlines, categorizing tasks by course or date, and getting notifications for upcoming due dates.

## Configuration/Run Instructions

There are two ways to access the School Task Manager:

### Method 1: Direct Access via Hosted Service

You can access the School Task Manager directly through our hosted version on **Digital Ocean**. Simply visit the following URL to get started:

- [School Task Manager](http://167.71.184.20:3000/)

This method is the easiest and does not require any setup on your part.

### Method 2: Running Locally via Docker

If you prefer to run the application locally or contribute to its development, follow these steps to get it running on your machine using **Docker**:

#### Prerequisites
- Docker installed on your machine.
- Docker Compose for managing multi-container Docker applications.

#### Environment Setup
1. Clone the repository to your local machine.
2. Navigate into the project directory.
3. Create a `.env` file in the root of the project by taking env.example as an example(adjust values as necessary)
4. Ensure MongoDB is running on your machine or set up a MongoDB container in your Docker configuration.

#### Running the Application
- To start the application, run: ```docker-compose up --build -d```
- Access the web-app from ```http://127.0.0.1:3000```

#### Link to the container image hosted on DockerHub
- If you want to pull from Docker Hub: ```docker pull zijiezhao/project5```

## Teammates

- Zijie Zhao ([github](https://github.com/ZijieZha0))
- Joyce Xie([github](https://github.com/joyxe-xie))
- Neal Haulsey ([github](https://github.com/nhaulsey))
- Babamayokun Okudero ([github](https://github.com/Mokudero))