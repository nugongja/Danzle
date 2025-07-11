package capston.capston_spring.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.Duration;
import java.time.LocalDateTime;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@ToString
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class AccuracySession {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @EqualsAndHashCode.Include
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private AppUser user;

    @ManyToOne
    @JoinColumn(name = "song_id", nullable = false)
    private Song song;

    @Column(nullable = false)       // 정확도 평가 세션
    private LocalDateTime startTime;

    @Column(nullable = false)
    private LocalDateTime endTime;

    @Column(nullable = false)
    private Double avg_score; // score 기본값 0 설정

    /** 모드 (예: full, highlight) 추가 **/
    @Column(nullable = false)
    private String mode;

    /** GPT 피드백 완료 여부 **/
    @Column(nullable = false)
    private boolean feedbackCompleted = false;
    
    // 생성 시간 자동 저장
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    // 생성 시점 자동 설정
    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }

    @Column(nullable = false)
    private String resultLevel = "Unscored";

    /** 초 단위 값을 LocalDateTime으로 변환하는 메서드 **/
    public void setStartTimeFromSeconds(int seconds) {
        this.startTime = LocalDateTime.of(1970, 1, 1, 0, 0).plusSeconds(seconds);
    }

    public void setEndTimeFromSeconds(int seconds) {
        this.endTime = LocalDateTime.of(1970, 1, 1, 0, 0).plusSeconds(seconds);
    }

    /** LocalDateTime을 초 단위 값으로 변환 **/
    public int getStartTimeInSeconds() {
        return (int) (this.startTime.toEpochSecond(java.time.ZoneOffset.UTC) -
                LocalDateTime.of(1970, 1, 1, 0, 0).toEpochSecond(java.time.ZoneOffset.UTC));
    }

    public int getEndTimeInSeconds() {
        return (int) (this.endTime.toEpochSecond(java.time.ZoneOffset.UTC) -
                LocalDateTime.of(1970, 1, 1, 0, 0).toEpochSecond(java.time.ZoneOffset.UTC));
    }

    /** 수정된 부분: Duration을 계산하여 "00:00:SS" 형식으로 반환하는 메서드 추가 **/
    public String getDuration() {
        Duration duration = Duration.between(this.startTime, this.endTime);
        return String.format("00:00:%02d", duration.toSeconds());
    }


    /** 추가된 부분: mode 포함 생성자 (id, createdAt 제외) **/
    public AccuracySession(AppUser user, Song song, LocalDateTime startTime, LocalDateTime endTime,
                           Double score, String mode) {
        this.user = user;
        this.song = song;
        this.startTime = startTime;
        this.endTime = endTime;
        this.avg_score = score;
        this.mode = mode;
        this.createdAt = LocalDateTime.now(); // 자동으로 생성 시간 설정
    }
}
