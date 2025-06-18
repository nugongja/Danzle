# 1. Danzle Server Architecture

Danzle is an AI-based K-pop dance training system that performs real-time pose evaluation and feedback generation. The backend server system is composed of four main components: **Spring Boot**, **Flask**, **AWS S3**, and **AWS RDS (MySQL)** — all orchestrated using **Docker Compose** for local development and integrated with AWS for cloud services.

---

## System Overview

### Spring Boot (Main API Backend)
- Manages session flow, user API requests, and accuracy evaluation logic
- Communicates with Flask for pose scoring
- Generates GPT-based feedback for low-score frames
- Uploads/downloads videos, audio, and user content via AWS S3
- Stores metadata (sessions, scores, feedback) in **AWS RDS (MySQL)**

-> [See more](https://github.com/sohee6989/CapstoneProject_Capjjang/blob/Server/backend-spring.md)

---

### Flask Server (Pose Analysis Engine)
- Performs real-time pose evaluation using MediaPipe
- Loads reference pose `.json` files stored locally inside the container
- Returns detailed scoring for each frame using a BDP-based method

-> [See more](https://github.com/sohee6989/CapstoneProject_Capjjang/blob/Server/backend-flask.md)

---

###  AWS Services

#### S3 (Media Storage)
- Stores large media files:
  -  User performance videos
  -  Silhouette guide videos
  -  Background music
- Used only by Spring (Flask does not access S3 directly)

#### RDS (MySQL Database)
- Stores structured data:
  - Accuracy session metadata
  - Frame-by-frame scores
  - GPT-generated feedback
- Accessible by Spring Boot via JDBC over a secure connection

---

## Deployment (Docker Compose)

All local services run within a shared Docker network (`danzle_net`):

+------------------+ +-------------------+</br>
| Spring Boot | <--→--> | Flask Server |</br>
| (Port 8080) | | (Port 5000) |</br>
+--------|---------+ +---------|---------+</br>
| |</br>
↓ ↓</br>
AWS RDS (MySQL) AWS S3 (Media Storage)</br>

---

## Running the System

```bash
# 1. Configure environment files
#    - .env_spring → AWS keys, GPT key, RDS DB URL
#    - .env_flask  → Local Flask configs (optional)

# 2. Start all services
docker-compose up --build

# 3. Access APIs and services
- Spring Swagger UI: http://localhost:8080/swagger-ui/index.html
- Flask Pose API: POST http://localhost:5000/analyze
```

---

## ★ Project Structure (Simplified)

Danzle/</br>
├── flask_server/                    # Pose evaluation logic (Python)</br>
│   ├── flask_pose_eval.py</br>
│   ├── pose.py</br>
│   ├── Dockerfile</br>
│   ├── requirements.txt</br>
│   └── ref_keypoints/       # Reference poses</br>
├── spring_server/                   # API, logic, DB, GPT (Java)</br>
│   ├── Dockerfile</br>
│   └── .jar</br>
├── .env_spring               # AWS S3, RDS, GPT keys</br>
├── .env_flask</br>
├── docker-compose.yml</br>
└── README.md</br>

---

### Environment Variable Files
In this project, environment-specific configuration is split across two files:

- `.env_spring`: For the Spring Boot backend
- `.env_flask`: For the Flask pose analysis server

These files must be properly configured before running the system via Docker Compose.

#### 1. .env_spring  — Spring Boot Configuration
```
# ──────────────── Database (AWS RDS - MySQL) ────────────────
DB_HOST=<your-db-host>.rds.amazonaws.com
DB_PORT=3306
DB_NAME=<your-db-name>
DB_USERNAME=admin
DB_PASSWORD=<your-db-password>

# ──────────────── AWS S3 ────────────────
AWS_S3_BUCKET_NAME=<your-aws-s3-bucket-name>

# ──────────────── OAuth Credentials ────────────────
NAVER_CLIENT_ID=<your-naver-client-id>
NAVER_CLIENT_SECRET=<your-naver-client-secret>

GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>
GOOGLE_EMAIL=<your-google-email>
GOOGLE_APP_PASSWORD=<your-google-app-password>

# ──────────────── JWT Security Key ────────────────
JWT_SECRET=<your-jwt-secret>

# ──────────────── Redis (Docker container name or IP) ────────────────
REDIS_IP_ADDRESS=<your-redis-container-name>

# ──────────────── Flask API URL (Docker internal) ────────────────
FLASK_API_BASEURL=http://<flask-container>:5000

# ──────────────── GPT API (OpenAI) ────────────────
OPENAI_API_KEY=<your-openai-api-key>
```

#### Notes:
- LASK_API_BASEURL should match the Flask container name in Docker (e.g., http://flask:5000)

- JWT_SECRET is used for signing and verifying JWT tokens

- REDIS_IP_ADDRESS is typically the container name of the Redis instance

- Never expose secrets or commit .env_spring to version control


</br>

#### 2. .env_flask — Flask Server Configuration
```
# ──────────────── AWS S3 (for reference or video retrieval if needed) ────────────────
S3_BUCKET_NAME=<your-s3-bucket-name>
AWS_ACCESS_KEY_ID=<your-aws-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key
```
#### Notes:
- If the Flask server reads or writes to S3 (e.g., to access videos), these credentials must be valid

- If Flask does not interact with S3, this file may remain empty or minimal

</br></br>


</br></br>

# 2. Danzle Backend – Setup & Deployment Guide
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

pecific information -> [See more](https://github.com/sohee6989/CapstoneProject_Capjjang/blob/Server/README.md)

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
 After building the Spring Boot project, move the generated .jar file to the spring_server directory.
</br></br>
2. Flask (Python) : no build

---

## 6. AWS Deployment Notes (for Admins)
- This project is containerized and can be deployed to AWS EC2 via docker-compose

- Ensure EC2 Security Group allows:
TCP: 8080 (Spring), 5000 (Flask), 6379 (Redis), 3306 (MySQL) as needed

- Docker uses an internal bridge network; flask and spring can resolve each other via container names
