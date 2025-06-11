FROM openjdk:21-slim
USER root
# javacv native dependency fix
RUN apt update && apt install -y \
    redis \
    sudo \
    curl \
    libopencv-dev \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libswscale-dev \
    libx264-dev \
    libopenblas-dev \
    libgtk2.0-dev \
    libv4l-dev \
    && apt clean && rm -rf /var/lib/apt/lists/*


COPY capston-spring-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]
