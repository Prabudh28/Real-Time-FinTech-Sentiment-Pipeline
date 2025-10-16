# Real-Time FinTech Market Sentiment Analysis Pipeline

## Project Overview
This project is an end-to-end, real-time data engineering pipeline designed to ingest synthetic FinTech news headlines, process them in the cloud to analyze market sentiment, and visualize the results on a live, interactive dashboard. It demonstrates a modern, scalable, cloud-native architecture using Microsoft Azure and Google Looker Studio.

The pipeline processes continuous data streams, performs real-time sentiment analysis, stores results in a robust cloud database, and delivers actionable insights through an interactive dashboard.

## Architecture
The data flows through the following stages:
1.  **Data Producer:** A local Python script generates synthetic news headlines and calculates sentiment using NLTK (VADER).
2.  **Ingestion:** The script sends data in real-time to **Azure Event Hubs**, a high-throughput data streaming service.
3.  **Real-Time Processing:** An **Azure Stream Analytics** job reads from the Event Hub, runs a SQL-like query to select and structure the key fields.
4.  **Data Storage:** The processed, real-time data is stored in a relational **Azure SQL Database**.
5.  **Visualization:** A **Google Looker Studio** dashboard connects directly to the Azure SQL Database to provide a live, interactive view of market sentiment.

Here is a visual representation of the pipeline's architecture:
![Project Architecture Diagram](https://github.com/Prabudh28/Real-Time-FinTech-Sentiment-Pipeline/blob/f04b6d2bf228803095bb29424d11209fe4751d9f/Images/Pipeline_Architecture.png)

The Azure Stream Analytics Job Diagram further illustrates the logical flow:
![Azure Stream Analytics Job Diagram](https://github.com/Prabudh28/Real-Time-FinTech-Sentiment-Pipeline/blob/f04b6d2bf228803095bb29424d11209fe4751d9f/Images/Job_Overview.png)

## Technologies Used
- **Data Producer:** Python, asyncio, Faker, NLTK (VADER)
- **Cloud Platform:** Microsoft Azure
- **Ingestion:** Azure Event Hubs
- **Stream Processing:** Azure Stream Analytics
- **Database:** Azure SQL Database
- **BI / Visualization:** Google Looker Studio
- **Version Control:** Git / GitHub

## Dashboard Showcase
Here is a screenshot of the final real-time dashboard, visualizing sentiment by company, overall market mood, and headline volume over time.

![Real-Time FinTech Sentiment Dashboard](https://github.com/Prabudh28/Real-Time-FinTech-Sentiment-Pipeline/blob/3a4bb893473475685628171ab7b6278583c9bb4b/Images/Live_Dashboard_1.png)

![Real-Time FinTech Sentiment Dashboard](https://github.com/Prabudh28/Real-Time-FinTech-Sentiment-Pipeline/blob/3a4bb893473475685628171ab7b6278583c9bb4b/Images/Live_Dashboard_2.png)

![Real-Time FinTech Sentiment Dashboard](https://github.com/Prabudh28/Real-Time-FinTech-Sentiment-Pipeline/blob/3a4bb893473475685628171ab7b6278583c9bb4b/Images/Live_Dashboard_3.png)

## Implementation Highlights & Visual Proof

### 1\. Data Producer in Action
The Python script generates continuous FinTech news headlines with calculated sentiment, forming the initial data stream.
![Python Producer Running](https://github.com/Prabudh28/Real-Time-FinTech-Sentiment-Pipeline/blob/3a4bb893473475685628171ab7b6278583c9bb4b/Images/Streaming_Data.png)

### 2\. Azure Pipeline Monitoring
Proof of live data flow through the Azure Stream Analytics job, showing a steady stream of input events and successfully processed output events.
![Azure Stream Analytics Pipeline Monitoring](https://github.com/Prabudh28/Real-Time-FinTech-Sentiment-Pipeline/blob/3a4bb893473475685628171ab7b6278583c9bb4b/Images/Overview.png)

### 3\. Data Persistence in Azure SQL Database
Demonstration of processed data successfully landing in the Azure SQL Database, ready for consumption by BI tools.

![Data in Azure SQL Database](https://github.com/Prabudh28/Real-Time-FinTech-Sentiment-Pipeline/blob/3a4bb893473475685628171ab7b6278583c9bb4b/Images/Database_log.png)

## Key Challenges & Resolutions

This project involved navigating several common data engineering challenges:

### 1\. Stream Analytics Output Failure (Table Not Found)
**Challenge:** The Stream Analytics job initially failed to write data to the Azure SQL Database, reporting a "Cannot find table" error in the Activity Log. This occurred despite ASA's capability to auto-create tables.
![ASA Activity Log - Table Not Found Error](https://github.com/Prabudh28/Real-Time-FinTech-Sentiment-Pipeline/blob/3a4bb893473475685628171ab7b6278583c9bb4b/Images/Logs.png)

**Resolution:** The issue was resolved by manually creating the `SentimentData` table in the Azure SQL Database using the Azure Portal's Query Editor. This provided a pre-existing target, allowing the ASA job to successfully insert data upon restart. The Activity Log later confirmed successful operations.
![ASA Activity Log - Successful Operations After Fix](https://github.com/Prabudh28/Real-Time-FinTech-Sentiment-Pipeline/blob/3a4bb893473475685628171ab7b6278583c9bb4b/Images/Activity_log.png)

### 2\. Azure Firewall Configuration
**Challenge:** Initially, Google Looker Studio was unable to connect to the Azure SQL Database, indicating a network access issue.
**Resolution:** A firewall rule was added to the Azure SQL Server to allow connections from all IP addresses (`0.0.0.0` to `255.255.255.255`). This temporary rule for demonstration purposes enabled Looker Studio to establish a connection.

### 3\. Cloud Service Integration (Power BI Licensing)
**Challenge:** Initial plans to use Power BI for visualization were blocked by licensing restrictions on the student account.
**Resolution:** The architecture was adapted to use Azure SQL Database for storage and Google Looker Studio for visualization, providing a robust and free alternative that enhanced the project's technical diversity.

## Actionable Insights

The dashboard is designed not just for monitoring, but for enabling data-driven actions for various stakeholders:

  * **For a Trader or Investor:**
      * **Identify Momentum Shifts:** A sudden spike in negative sentiment for a specific company could be an early warning signal to review a long position or investigate shorting opportunities.
      * **Spot Emerging Opportunities:** A consistent rise in positive sentiment for a lesser-known company could indicate a breakout potential, prompting further due diligence.
  * **For a Corporate Strategy or PR Team:**
      * **Competitor Monitoring:** Real-time benchmarking of public perception against key competitors. A dip in competitor sentiment is a potential competitive advantage.
      * **Crisis Management:** The live headline ticker (if implemented as a table) acts as an early warning system, allowing PR teams to respond immediately to negative news.
  * **For a Product Manager:**
      * **Gauge Product Launch Reception:** Immediate, unfiltered feedback on market reception for new product launches.
      * **Identify Market Needs:** Consistent negative news about a specific sector problem could highlight opportunities for new product development.

## Local Setup & Installation
1.  Clone the repository.
2.  Create and activate a Python virtual environment.
3.  Install dependencies: `pip install -r requirements.txt`
4.  Set up the necessary Azure resources (Event Hub, Stream Analytics, SQL Database).
5.  Create a `config.ini` file (using `config.example.ini` as a template) with the Azure Event Hub connection string.
6.  Run the producer script: `python producer.py`

## Future Improvements
- Integrate with a real-time news API (e.g., NewsAPI.org, Alpaca).
- Deploy the Python producer script to a serverless Azure Function for continuous, 24/7 data generation without a local machine.
- Implement more advanced NLP models (e.g., fine-tuned transformer models like FinBERT) for more nuanced and accurate sentiment and topic analysis.

## Appendix
  * **Source Code:** The complete source code for the Python producer and project setup files are available on GitHub: [Link to Your GitHub Repository]
  * **SQL Table Schema:**
    ```sql
    CREATE TABLE SentimentData (
        EventTimestamp DATETIME2,
        headline NVARCHAR(MAX),
        company NVARCHAR(MAX),
        sentiment NVARCHAR(50),
        compound_score FLOAT
    );
    ```

    
