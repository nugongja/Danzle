# Danzle Server Architecture

Danzle is an AI-based K-pop dance training system that performs real-time pose evaluation and feedback generation. The backend server system is composed of four main components: **Spring Boot**, **Flask**, **AWS S3**, and **AWS RDS (MySQL)** — all orchestrated using **Docker Compose** for local development and integrated with AWS for cloud services.

---

## System Overview

### Spring Boot (Main API Backend)
- Manages session flow, user API requests, and accuracy evaluation logic
- Communicates with Flask for pose scoring
- Generates GPT-based feedback for low-score frames
- Uploads/downloads videos, audio, and user content via AWS S3
- Stores metadata (sessions, scores, feedback) in **AWS RDS (MySQL)**

-> [See more](docs/backend-spring.md)

---

### Flask Server (Pose Analysis Engine)
- Performs real-time pose evaluation using MediaPipe
- Loads reference pose `.json` files stored locally inside the container
- Returns detailed scoring for each frame using a BDP-based method

-> [See more](docs/backend-flask.md)

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


