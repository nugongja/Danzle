# 1. AuthController API Documentation

This controller handles user registration, social login redirection, and JWT token refreshing.

---

## 1. POST `/join`

**Purpose**  
Registers a new user.

**Method**  
POST

**Request Body**
```json
{
  "name": "username",
  "email": "user@example.com",
  "password1": "password123",
  "password2": "password123"
}
```

**Behavior**

- Validates input using `@Valid` and `BindingResult`.
- Checks if `password1` and `password2` match.
- If valid and not duplicated, creates a new user.
- Handles:
  - Field validation errors (returns field: error message pairs).
  - Password mismatch (`400 Bad Request`).
  - Duplicate email (`400 Bad Request` with message `"User already exists"`).
  - Unexpected errors (`400 Bad Request` with specific message).

**Responses**
- `200 OK`: `"User successfully registered."`
- `400 Bad Request`: with error message(s)

---

## 2. GET `/loginNaver`

**Purpose**  
Redirects to the Naver social login view.

**Method**  
GET

**Response**
- Returns `ModelAndView` pointing to `"socialLogin"` view.

---

## 3. GET `/loginGoogle`

**Purpose**  
Redirects to the Google social login view.

**Method**  
GET

**Response**
- Returns `ModelAndView` pointing to `"socialLogin"` view.

---

## 4. POST `/refresh`

**Purpose**  
Generates a new access token from a valid refresh token.

**Method**  
POST

**Headers**
```
Refresh-Token: <your-refresh-token>
```

**Behavior**

- Verifies whether the refresh token is expired.
- If valid, extracts email from token and creates a new access token (valid for 1 hour).

**Responses**

- `200 OK`  
```json
{
  "accessToken": "<new-access-token>"
}
```

- `401 Unauthorized`  
```json
{
  "error": "Refresh token expired"
}
```

---

## Summary Table

| Method | Endpoint       | Description                        |
|--------|----------------|------------------------------------|
| POST   | `/join`        | Registers a new user               |
| GET    | `/loginNaver`  | Redirects to Naver login view      |
| GET    | `/loginGoogle` | Redirects to Google login view     |
| POST   | `/refresh`     | Issues new access token by refresh |

---

# 2. AccuracySessionController API Documentation

This controller handles accuracy session management, real-time dance pose analysis, and evaluation result processing.

---

## 1. GET `/accuracy-session/user/me`

**Purpose**  
Retrieves all accuracy sessions for the currently authenticated user.

**Method**  
GET

**Response**
- 200 OK: List of session objects
- 400 Bad Request: Invalid input
- 500 Internal Server Error: Unexpected server error

---

## 2. GET `/accuracy-session/song/{songId}/user/me`

**Purpose**  
Retrieves accuracy sessions for a specific song and the current user.

**Method**  
GET

**Path Variables**
- songId: ID of the song

**Response**
- 200 OK: List of sessions
- 400 Bad Request: Invalid song or user
- 500 Internal Server Error: Unexpected failure

---

## 3. POST `/accuracy-session/analyze`

**Purpose**  
Analyzes a user frame (image) by sending it to the Flask server, and stores the per-frame result.

**Method**  
POST

**Content-Type**  
multipart/form-data

**Request Parameters**
- sec: Integer (time in seconds)
- songId: Long
- sessionId: Long
- frame: MultipartFile (image)

**Response**
- 200 OK: Analysis result including score, direction, etc.
- 400 Bad Request: Invalid parameters or session
- 500 Internal Server Error: Communication or processing error

---

## 4. POST `/accuracy-session/save`

**Purpose**  
Finalizes the session, computes overall results, and triggers GPT feedback generation.

**Method**  
POST

**Request Parameters**
- sessionId: Long

**Response**
- 200 OK: Session summary and feedback
- 400 Bad Request: Session invalid or already finalized
- 500 Internal Server Error: GPT or save failure

---

## 5. GET `/accuracy-session/result`

**Purpose**  
Retrieves detailed result for a specific accuracy session.

**Method**  
GET

**Query Parameters**
- sessionId: Long

**Response**
- 200 OK: Full session result
- 404 Not Found: Session not found
- 500 Internal Server Error: Unexpected error

---

## 6. GET `/accuracy-session/video-paths`

**Purpose**  
Returns silhouette video paths for a song by its name.

**Method**  
GET

**Query Parameters**
- songName: String

**Response**
- 200 OK: List of video path strings
- 400 Bad Request: Song not found or invalid input
- 500 Internal Server Error: Unexpected failure

---

## 7. POST `/accuracy-session/full`

**Purpose**  
Initializes a new full-mode accuracy session for a user and song.

**Method**  
POST

**Query Parameters**
- songId: Long

**Response**
- 200 OK: CorrectionResponse (session ID, song title)
- 400 Bad Request: Invalid song ID or user
- 500 Internal Server Error: Session creation failure

---

## 8. GET `/accuracy-session/summary`

**Purpose**  
Retrieves the summary result of an accuracy session after all frames have been evaluated.

**Method**  
GET

**Query Parameters**
- sessionId: Long

**Response**
- 200 OK: Summary statistics and final results
- 400 Bad Request: Missing or invalid session ID
- 404 Not Found: Session not found
- 500 Internal Server Error: Summary generation failure

---

## Summary Table

| Method | Endpoint                                  | Description                                        |
|--------|-------------------------------------------|----------------------------------------------------|
| GET    | /accuracy-session/user/me                 | Get all sessions for current user                 |
| GET    | /accuracy-session/song/{songId}/user/me   | Get sessions for song + user                      |
| POST   | /accuracy-session/analyze                 | Analyze user frame via Flask and store result     |
| POST   | /accuracy-session/save                    | Save full session result and trigger GPT feedback |
| GET    | /accuracy-session/result                  | Retrieve detailed session results                 |
| GET    | /accuracy-session/video-paths             | Get silhouette video paths by song name           |
| POST   | /accuracy-session/full                    | Start a full-mode accuracy session                |
| GET    | /accuracy-session/summary                 | Get summary statistics for an accuracy session    |

---

# 3. PracticeSessionController API Documentation

This controller manages practice sessions for users, including session creation and retrieval.

---

## 1. GET `/practice-session/user/me`

**Purpose**  
Retrieves all practice sessions for the currently authenticated user.

**Method**  
GET

**Response**
- 200 OK: List of `PracticeSessionResponse` DTOs
- 401 Unauthorized: If user is not authenticated

---

## 2. GET `/practice-session/song/{songId}/user/me`

**Purpose**  
Retrieves practice sessions for a specific song and the current user.

**Method**  
GET

**Path Variables**
- `songId`: ID of the song

**Response**
- 200 OK: List of `PracticeSessionResponse` DTOs
- 401 Unauthorized: If user is not authenticated

---

## 3. POST `/practice-session/full`

**Purpose**  
Starts a full-section (1절) practice session for the authenticated user and the specified song.

**Method**  
POST

**Query Parameters**
- `songId`: ID of the song

**Response**
- 200 OK: A list with one `PracticeSessionResponse` object
- 400 Bad Request: Invalid input (e.g. song not found or already in session)
- 500 Internal Server Error: On failure to create session

---

## 4. POST `/practice-session/highlight`

**Purpose**  
Starts a highlight-section practice session for the authenticated user and specified song.

**Method**  
POST

**Query Parameters**
- `songId`: ID of the song

**Response**
- 200 OK: A list with one `PracticeSessionResponse` object
- 400 Bad Request: Invalid input
- 500 Internal Server Error: On failure to create session

---

## 5. GET `/practice-session/video-paths`

**Purpose**  
Returns practice silhouette video paths for a given song name.  
(Note: This reuses logic from the AccuracySessionService.)

**Method**  
GET

**Query Parameters**
- `songName`: Title of the song (String)

**Response**
- 200 OK: List of video paths (e.g., URLs or file paths)
- 400 Bad Request: If song not found or name invalid
- 500 Internal Server Error: Server error while retrieving data

---

## Summary Table

| Method | Endpoint                                      | Description                                               |
|--------|-----------------------------------------------|-----------------------------------------------------------|
| GET    | /practice-session/user/me                     | Get all practice sessions of current user                |
| GET    | /practice-session/song/{songId}/user/me       | Get practice sessions for a specific song and user       |
| POST   | /practice-session/full                        | Start a full-section practice session                    |
| POST   | /practice-session/highlight                   | Start a highlight-section practice session               |
| GET    | /practice-session/video-paths                 | Get silhouette video paths for a specific song           |


---

# 4. ChallengeSessionController API Documentation

This controller handles operations related to challenge sessions, such as starting sessions, retrieving user-specific records, and accessing highlight/background data for a song.

---

## 1. GET `/challenge-session/user/me`

**Purpose**  
Retrieves all challenge sessions for the authenticated user.

**Method**  
GET

**Response**
- 200 OK: List of `ChallengeSessionResponse` DTOs
- 401 Unauthorized: If user is not authenticated

---

## 2. GET `/challenge-session/song/{songId}/user/me`

**Purpose**  
Retrieves challenge sessions for a specific song and the authenticated user.

**Method**  
GET

**Path Variables**
- `songId`: ID of the song

**Response**
- 200 OK: List of `ChallengeSessionResponse` DTOs
- 401 Unauthorized: If user is not authenticated

---

## 3. GET `/challenge-session/result`

**Purpose**  
Retrieves detailed information for a specific challenge session.

**Method**  
GET

**Query Parameters**
- `sessionId`: ID of the session (as query param)

**Response**
- 200 OK: `ChallengeSessionResponse` DTO
- 404 Not Found: If session does not exist
- 500 Internal Server Error: On unexpected failure

---

## 4. GET `/challenge-session/background/{songId}`

**Purpose**  
Returns the background resource (e.g., image or video path) used in the challenge mode for the given song.

**Method**  
GET

**Path Variables**
- `songId`: ID of the song

**Response**
- 200 OK: Background path as a plain string

---

## 5. GET `/challenge-session/highlight/{songId}`

**Purpose**  
Returns the highlight section info (e.g., time range or video path) of a song for challenge mode.  
Also creates and saves the challenge session automatically.

**Method**  
GET

**Path Variables**
- `songId`: ID of the song

**Authentication**
- Required (CustomUserDetails)

**Response**
- 200 OK: Highlight section string (e.g., timestamp or ID)
- 401 Unauthorized: If user is not authenticated

---

## Summary Table

| Method | Endpoint                                      | Description                                                   |
|--------|-----------------------------------------------|---------------------------------------------------------------|
| GET    | /challenge-session/user/me                    | Get all challenge sessions for current user                   |
| GET    | /challenge-session/song/{songId}/user/me      | Get challenge sessions for specific song and current user     |
| GET    | /challenge-session/result                     | Get challenge session detail by sessionId (query param)       |
| GET    | /challenge-session/background/{songId}        | Get background image or video path for challenge mode         |
| GET    | /challenge-session/highlight/{songId}         | Get highlight section for challenge mode and create session   |

---

# 5. SongController API Documentation

This controller provides endpoints for managing and retrieving song data, including search functionality, practice information, and song registration (admin only).

---

## 1. GET `/song/all`

**Purpose**  
Retrieves all songs or filters songs by keyword in title or artist.

**Method**  
GET

**Query Parameters**
- `keyword` (optional): If provided, filters songs by keyword in title or artist.

**Response**
- 200 OK:
```json
[
  {
    "id": 1,
    "title": "Song Title",
    "artist": "Artist Name",
    "coverImagePath": "path/to/image.jpg"
  }
]
```

- 500 Internal Server Error:
```json
{
  "error": "Internal Server Error"
}
```

---

## 2. GET `/song/search`

**Purpose**  
Search songs by title and/or artist.

**Method**  
GET

**Query Parameters**
- `title` (optional): Song title to search
- `artist` (optional): Artist name to search

**Response**
- 200 OK:
```json
[
  {
    "id": 2,
    "title": "Another Song",
    "artist": "Another Artist",
    "coverImagePath": "another/path.jpg"
  }
]
```

- 404 Not Found:
```json
{
  "error": "No search results found"
}
```

- 500 Internal Server Error:
```json
{
  "error": "Internal Server Error"
}
```

---

## 3. GET `/song/{songId}/song-info`

**Purpose**  
Returns dance guide video and section timing info for a given song.

**Method**  
GET

**Path Variables**
- `songId` (required): ID of the song

**Query Parameters**
- `mode` (optional): `'full'` or `'highlight'` – only for practice mode
- `for` (optional): `'accuracy'` or `'practice'` – determines info format

**Response**
- 200 OK (accuracy):
```json
{
  "silhouetteVideoUrl": "url/to/silhouette.mp4"
}
```

- 200 OK (practice):
```json
{
  "silhouetteVideoUrl": "url/to/silhouette.mp4",
  "startTime": 15.0,
  "endTime": 45.0
}
```

- 200 OK (invalid mode):
```json
{
  "silhouetteVideoUrl": "url/to/silhouette.mp4",
  "message": "Invalid mode. Use 'full' or 'highlight'."
}
```

---

## 4. POST `/song`

**Purpose**  
Registers a new song (Admin only)

**Method**  
POST

**Authentication**
- Requires user with `ROLE_ADMIN`

**Request Body**
```json
{
  "title": "New Song",
  "artist": "New Artist",
  "coverImagePath": "cover/path.jpg"
}
```

**Response**
- 200 OK:
```json
{
  "id": 3,
  "title": "New Song",
  "artist": "New Artist",
  "coverImagePath": "cover/path.jpg"
}
```

- 500 Internal Server Error:
```json
{
  "error": "Internal Server Error"
}
```
---

# 6. VideoController API Documentation

This controller manages recorded video operations such as retrieval, storage, session-based queries, and video replacement.

---

## 1. GET `/recorded-video/user/me`

**Purpose**  
Retrieve all recorded videos of the authenticated user, optionally filtered by mode.

**Method**  
GET

**Query Parameters**  
- `mode` (optional): Enum value of `VideoMode` (`PRACTICE`, `CHALLENGE`, `ACCURACY`)

**Authentication**  
Required (`@AuthenticationPrincipal`)

**Response**  
- 200 OK  
```json
[
  {
    "videoId": 1,
    "videoMode": "PRACTICE",
    "duration": 30,
    "recordedAt": "2025-06-17T12:00:00",
    "videoPath": "/videos/1.mp4"
  }
]
```
- 401 Unauthorized

---

## 2. GET `/recorded-video/{videoId}`

**Purpose**  
Retrieve metadata of a specific video by its ID.

**Method**  
GET

**Path Variables**  
- `videoId`: Long, ID of the recorded video

**Response**  
- 200 OK  
```json
{
  "videoId": 2,
  "videoMode": "CHALLENGE",
  "duration": 45,
  "recordedAt": "2025-06-16T15:00:00",
  "videoPath": "/videos/2.mp4"
}
```
- 404 Not Found  
```json
{
  "error": "Video not found with ID: {videoId}"
}
```

---

## 3. GET `/recorded-video/session`

**Purpose**  
Retrieve all recorded videos for a given session ID and mode.

**Method**  
GET

**Query Parameters**  
- `sessionId`: Long, ID of the session  
- `mode`: Enum value of `VideoMode`

**Response**  
- 200 OK  
```json
[
  {
    "videoId": 3,
    "videoMode": "ACCURACY",
    "duration": 40,
    "recordedAt": "2025-06-15T10:30:00",
    "videoPath": "/videos/3.mp4"
  }
]
```

---

## 4. POST `/recorded-video/saveVideo`

**Purpose**  
Save a newly recorded video along with its metadata.

**Method**  
POST (multipart/form-data)

**Authentication**  
Required

**Request Parameters**  
- `file`: MultipartFile, video file  
- `sessionId`: Long  
- `videoMode`: Enum (`PRACTICE`, `CHALLENGE`, `ACCURACY`)  
- `recordedAt`: ISO-8601 datetime string (e.g., `2025-06-17T12:00:00`)  
- `duration`: int (seconds)

**Response**  
- 200 OK  
```json
{
  "videoId": 4,
  "videoMode": "PRACTICE",
  "duration": 60,
  "recordedAt": "2025-06-17T12:00:00",
  "videoPath": "/videos/4.mp4"
}
```
- 400 Bad Request  
- 401 Unauthorized

---

## 5. POST `/recorded-video/{videoId}/edit`

**Purpose**  
Replace an existing recorded video with a new file.

**Method**  
POST (multipart/form-data)

**Path Variables**  
- `videoId`: Long, ID of the video to replace

**Request Parameters**  
- `file`: MultipartFile, new video file

**Response**  
- 200 OK  
```json
{
  "message": "Video updated successfully."
}
```
- 400 Bad Request  
```json
{
  "error": "Uploaded file is empty."
}
```

---

# 7. UserController API Documentation

This controller manages user-related operations, including profile viewing, editing personal information, and account deletion.

---

## 1. GET `/user/profile`

**Purpose**  
Retrieve the authenticated user's full profile information, including personal data, video list, and score history.

**Method**  
GET

**Authentication**  
Required

**Response**  
- 200 OK: Returns a `UserResponseDto` containing user profile, videos, and accuracy records.

---

## 2. PATCH `/user/profile/edit/name`

**Purpose**  
Update the authenticated user's name.

**Method**  
PATCH

**Authentication**  
Required

**Request Body**
```json
{
  "name": "newName"
}
```

**Validation**  
- Name must meet validation criteria defined in `EditNameRequest`

**Response**  
- 200 OK: 이름이 성공적으로 수정되었습니다.
- 400 Bad Request: If validation fails

---

## 3. PATCH `/user/profile/edit/password`

**Purpose**  
Change the authenticated user's password.

**Method**  
PATCH

**Authentication**  
Required

**Request Body**
```json
{
  "currentPassword": "currentPassword123",
  "newPassword1": "newPassword456",
  "newPassword2": "newPassword456"
}
```

**Behavior**  
- Validates that current password is correct
- Ensures new passwords match and meet criteria

**Response**  
- 200 OK: 비밀번호가 성공적으로 수정되었습니다.
- 400 Bad Request: 현재 비밀번호가 일치하지 않습니다 or validation errors

---

## 4. PATCH `/user/profile/edit/img`

**Purpose**  
Update the authenticated user's profile image.

**Method**  
PATCH

**Authentication**  
Required

**Consumes**  
`multipart/form-data`

**Request Parameters**  
- `file`: Multipart image file

**Response**  
- 200 OK: 프로필 이미지가 성공적으로 수정되었습니다.
- 400 Bad Request: If file is empty

---

## 5. DELETE `/user/profile/deleteAccount`

**Purpose**  
Delete the authenticated user's account.

**Method**  
DELETE

**Authentication**  
Required

**Response**  
- 200 OK: 계정이 성공적으로 삭제되었습니다.

---

# 8. PasswordResetController API Documentation

This controller manages the password reset process, including email verification and setting a new password.

---

## 1. POST `/password-reset/request`

**Purpose**  
Send a verification code to the user's email for password reset.

**Method**  
POST

**Request Body**
- email (string): The user's email address

**Validation**
- Email format must be valid

**Response**
- 200 OK: Verification code sent.
- 400 Bad Request: If email is invalid or format check fails

---

## 2. POST `/password-reset/verify`

**Purpose**  
Verify the code sent to the user's email.

**Method**  
POST

**Request Body**
- email (string): The user's email address  
- verificationCode (string): The code sent to the user's email

**Validation**
- Email and verification code must meet format constraints

**Response**
- 200 OK: Verification successful.
- 400 Bad Request: Invalid code or validation failure

---

## 3. POST `/password-reset/new-password`

**Purpose**  
Set a new password after successful code verification.

**Method**  
POST

**Request Body**
- email (string): The user's email address  
- newPassword1 (string): New password  
- newPassword2 (string): Confirmation of new password

**Validation**
- Passwords must match  
- Password format must meet validation rules

**Response**
- 200 OK: Password successfully reset.
- 400 Bad Request:
  - If passwords do not match  
  - If format validation fails

---

# 9. S3Controller API Documentation

This controller provides an endpoint to generate a presigned URL for direct uploads to AWS S3.

---

## 1. GET `/api/s3/presigned-url`

**Purpose**  
Generates a presigned URL that allows clients to upload a video file directly to S3 without needing AWS credentials.

**Method**  
GET

**Query Parameters**
- `filename` (string, required): The name of the file to be uploaded (e.g., `video123.mp4`). The file will be saved under the `videos/` directory in the S3 bucket.

**Response**
- 200 OK: Returns a presigned URL as a plain string
- 500 Internal Server Error: If URL generation fails

**Notes**
- The presigned URL is valid for 10 minutes
- The content type is fixed to `video/mp4`
- The file will be stored in the following S3 path format: `videos/{filename}`

