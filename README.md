# TKU-homework: Text Analytics

## Environment
* System    : Windows 10
* Python    : 3.6.0
* Java jre  : 1.8.0_161
* Zookeeper : 3.4.11
* Kafka     : 2.11-1.1.0

## Flow

* **Refert to [如何在 Windows OS 安裝 Apache Kafka]**
* Install Java [jre] 
* Install [Kafka] 
* Install [Zookeeper]
1. Start **Zookeeper** and **Kafka**
2. Create your topics
```
\kafka\bin\windows\kafka-topics.bat --create --zookeeper YOUR_IP:YOUR_PORT --replication-factor 1 --partitions 1 --topic YOU_TOPIC
```
3. Write the Python web crawler with [pykafka]
4. Build [TF-IDF] Model for each article
5. pipe to the python text analytics

## START
* Get the news form [政治]/[娛樂] with web crawler
```
python newsCrawler.py p
python newsCrawler.py e
```
* Analytics 
```
python analytics.py p
python analytics.py e
```
[jre]: http://www.oracle.com/technetwork/java/javase/downloads/server-jre8-downloads-2133154.html "jre"
[kafka]: http://zookeeper.apache.org/releases.html "kafka"
[Zookeeper]: http://kafka.apache.org/downloads.html "Zookeeper"
[如何在 Windows OS 安裝 Apache Kafka]: https://blog.yowko.com/2017/03/windows-os-apache-kafka.html
[TF-IDF]: https://www.jianshu.com/p/edf666d3995f
[pykafka]: https://github.com/dpkp/kafka-python
[政治]: https://tw.news.yahoo.com/politics/archive
[娛樂]: https://tw.news.yahoo.com/politics/archive
