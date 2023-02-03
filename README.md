


## Getting started

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


Setting `MULTI_THREAD=true` in the compose file means messages in the batch will be processed **concurrently**, as shown below:
https://user-images.githubusercontent.com/47530786/216724131-e394165e-7abf-40ed-87eb-a54b8b2a3c5d.mov

The **maximum** number of threads that will be running inside the kafka consumer container will be equal to **`BATCH_SIZE`+1** (1=Main thread)
