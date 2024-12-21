# Real-Time Analysis of Live Twitch Comments

## Project Overview

This project implements a real-time data processing pipeline designed to capture, analyze, and store live chat messages from Twitch streams. Using Python and the Twitchio API, live messages are ingested and sent to Apache Kafka, which acts as a distributed message broker. The architecture includes two Kafka consumers: one powered by Spark Streaming (PySpark) for real-time data analysis, and another dedicated to storing processed data in a Database. This dual-consumer setup ensures both immediate insights and long-term data availability, enabling seamless exploration and visualization of Twitch chat activity.

**(This project is not finished)**

### Objective:

- Use Python to retrieve live comments from one or more Twitch streams.
- Send the data to Kafka for processing and distribution to consumers.
- **1st Consumer:** Store the data in a ElasticSearch database.
- **2nd Consumer:** Perform real-time comment analysis using Spark Streaming connected to Kafka.

---

## Development Progress

- [x] Twitch Comments Retrieval: Developed a Python class to fetch live chat messages using the Twitchio API.
- [x] Kafka Connection: Implemented a Python class to establish a connection to Apache Kafka.
- [x] Data Ingestion: Successfully integrated the system to send Twitch chat data to Kafka as events.
- [ ] Multi-Channel Support: Enhance the Twitch listener to handle multiple Twitch channels simultaneously.
- [ ] Data Storage Consumer: Develop a Kafka consumer to store processed data in an ElasticSearch database.
- [ ] Real-Time Analysis: Implement real-time data analysis using PySpark for insights and transformations.

---

## Architecture

### a) Message Ingestion

- **Python + Twitchio API**: Used to capture live messages from Twitch streams.
- Messages are sent to Kafka as events.

### b) Processing Pipeline

- **Apache Kafka**: Buffers the messages and distributes them to consumers.

### c) Storage

- **Database (ElasticSearch)**: Used to store the results.

### d) Visualization and Exploration

- **Spark Streaming (PySpark)**: Consumes messages from Kafka and applies real-time analysis.

---

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/0xdaani/Real-Time-Twitch-Analysis
   cd https://github.com/0xdaani/Real-Time-Twitch-Analysis
   docker-compose up -d
   cd app/
   pip install -r requirements.txt
   ```

---

## Usage

```bash
python3 main.py [-h] -s SERVER -c CHANNEL -t TOPIC -tt TWITCH_TOKEN [-v]
```

Options:
-   -s SERVER          Kafka server address (e.g., localhost:9092)
-   -c CHANNEL         Twitch channel name
-   -t TOPIC           Kafka topic to send messages
-   -tt TWITCH_TOKEN   Twitch authentication token
-   -v                 Enable verbose mode (optional)


## Example usage
```bash
python3 main.py -s localhost:9092 --topic name_topic -tt token -c channel_name -v True
```


## Stop the Program

Use CTRL+C to terminate the script and stop the docker:
```bash
docker-compose down
```


