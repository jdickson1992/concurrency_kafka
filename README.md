## Intro 📖

This repo will explore ways to *increase the concurrency of a Kafka consumer* so that we can achieve more with a single consumer than simply increasing the number of partitions.

A **multi-threaded** consumer model will be investigated.

1. A single main thread will call `poll()` and fetch data from multiple / single partition(s).
2. Once a batch of messages has been received by the main thread, they will deliver the messages to a pool of threads where the processing will be done *concurrently*.
3. The main thread is the only thread that commits an offset. It will wait for all threads to finish processing.

> All applications are *containerised* 🐳


## Getting started 🚀

Run:

```bash
docker-compose up -d
```

This should bring up a kafka cluster with some producer[s] and a consumer. 

There are several environment variables set inside `docker-compose.yml` which can be modified:

- `KAFKA_TOPIC`  = *The topic we produce/consume from*
- `BATCH_SIZE`   = *The size of the message batch that our consumer `polls()`.*
- `MULTI_THREAD` = *To determine whether we run a multi-threaded kafka consumer model (`true`) or a single-threaded consumer.*


For e.g. setting `MULTI_THREAD=false` in the compose file means that the messages within a batch will be processed **sequentially**, as shown below:

> https://user-images.githubusercontent.com/47530786/216725437-79ff1147-4f2b-4ca8-b8c2-f94c274ebbc2.mov

Setting `MULTI_THREAD=true` in the compose file means messages in the batch will be processed **concurrently**, as shown below:

> https://user-images.githubusercontent.com/47530786/216724131-e394165e-7abf-40ed-87eb-a54b8b2a3c5d.mov

⚠️ The **maximum** number of threads that will be running inside the kafka consumer container will be equal to **`BATCH_SIZE`+1** (1=`Main thread`)

## Finished 🔚

Run:

```bash
docker-compose down
```
