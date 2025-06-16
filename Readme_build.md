# Danzle Backend – Setup & Deployment Guide
This document explains how to build, run, and test the Danzle backend system, consisting of **Spring Boot**, **Flask**, **Docker**, and AWS services such as **RDS (MySQL)** and **S3**.

---

## Prerequisites

| Tool              | Version (or higher) |
|-------------------|---------------------|
| Java              | 17                  |
| Gradle            | 8                   |
| Python            | 3.9+                |
| Docker & Compose  | Latest              |
| Git               | Any                 |

Optional: IntelliJ IDEA, AWS CLI

---

## Project Structure Overview
Danzle/</br>
├── flask/ # Flask server (MediaPipe-based)</br>
├── src/ # Spring Boot source code</br>
├── .env_spring # Spring Boot environment variables (excluded from git)</br>
├── .env_flask # Flask environment variables (excluded from git)</br>
├── docker-compose.yml # Docker orchestration file</br>
└── README.md</br>

---

## 1. Clone the Repository
You can clone the repository with the default name:

```bash
git clone https://github.com/<your-org-or-username>/Danzle.git
cd Danzle
```

Or optionally rename it to match the project name:
```
git clone https://github.com/yourname/Danzle.git capston-spring
cd capston-spring
```
---

## 2. Environment Configuration
Create the following environment variable files in the project root:

1. .env_spring
2. .env_flask

Do not commit .env_* files to git. Keep them in .gitignore.

pecific information -> README.md

---

## 3. Run with Docker Compose
docker-compose up --build

---

## 4. AWS Integration
- MySQL: Deployed on AWS RDS and configured via .env_spring

- S3: Used to store user videos, guide videos, and audio files

- GPT API: Used by Spring Boot for generating dance feedback

---

## 5. Manual Build 
1. Spring Boot (Gradle)
```
./gradlew build
```

2. Flask (Python) : no build

---

## 6. AWS Deployment Notes (for Admins)
- This project is containerized and can be deployed to AWS EC2 via docker-compose

- Ensure EC2 Security Group allows:
TCP: 8080 (Spring), 5000 (Flask), 6379 (Redis), 3306 (MySQL) as needed

- Docker uses an internal bridge network; flask and spring can resolve each other via container names
