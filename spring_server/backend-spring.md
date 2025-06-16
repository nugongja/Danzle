# Spring Boot Backend

This is the Spring Boot backend component of the Danzle system, a K-pop dance training and evaluation platform. It provides RESTful APIs for real-time dance pose scoring, GPT-based feedback, session management, and AWS integration (S3, RDS).

### Features
- Real-time dance pose analysis coordination with Flask server

- GPT API integration to generate feedback from low-score segments

- OAuth2 login with Naver and Google

- Media file management using AWS S3

- Dance session and score data persistence using AWS RDS (MySQL)

- JWT-based authentication and Redis session handling

- Swagger-based API documentation

---

## Project Structure (Spring)
src/main/java/capston/capston_spring/</br>
├── config/          # Spring configs (security, CORS, S3, Redis, etc.)</br>
├── controller/      # REST controllers for dance sessions and auth</br>
├── dto/             # DTOs used for request/response payloads</br>
├── entity/          # JPA entity definitions for DB tables</br>
├── exception/       # Custom exception handling and error responses</br>
├── jwt/             # JWT token creation and validation logic</br>
├── oauth2/          # OAuth login handlers and user services</br>
├── repository/      # Spring Data JPA repositories</br>
├── service/         # Business logic layer (analysis coordination, feedback, etc.)</br>
└── utils/           # Utility classes (time sync, helpers, etc.)</br>

src/main/resources/templates/  # Static pages or e-mail templates (if needed)</br>
