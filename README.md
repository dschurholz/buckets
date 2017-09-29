# Network Flow Shpaing Buckets
Token bucket and leaky bucket simulation


## HOWTO

This script can only be used to simulate the behavior of a token bucket and leaky bucket. The paremeters have to be defined in the correct meassurments. They are available under the `--help command`.

Example executions:

### Token bucket

```{r}
python buckets.py --bucket-size=5000 --input-rate=10000000 --rate=100000 --packet-size=1000 --time-lapse=142 --exec-speed=0.2 --packet-dates 1 2 3 4 5 6 30 34 36 38 50 60 80 82 84 86 88 100

```

### Leaky Bucket

```{r}
python buckets.py --leaky --bucket-size=5000 --input-rate=10000000 --rate=100000 --packet-size=1000 --time-lapse=142 --exec-speed=0.2 --packet-dates 1 2 3 4 5 6 30 34 36 38 50 60 80 82 84 86 88 100

```

Help command extract:

```{r}
usage: buckets.py [-h] [--leaky] [--bucket-size BUCKET_SIZE]
                  [--input-rate INPUT_RATE] [--rate RATE]
                  [--packet-size PACKET_SIZE] [--time-lapse TIME_LAPSE]
                  [--exec-speed EXEC_SPEED]
                  [--packet-dates PACKET_DATES [PACKET_DATES ...]]

A python script that simulates the token bucket and leaky bucket algorithms
for flow control in computer networks.

optional arguments:
  -h, --help            show this help message and exit
  --leaky               set the bucket to leaky
  --bucket-size BUCKET_SIZE
                        set the bucket size (in bytes) (default 5KB)
  --input-rate INPUT_RATE
                        the rate at which packages arrive (in bytes per
                        second) (default 10MB/s)
  --rate RATE           the rate at which tokens arrive to the bucket (in
                        bytes per second) (default 100KB/s)
  --packet-size PACKET_SIZE
                        the size of each incoming packet (in bytes) (default
                        1KB)
  --time-lapse TIME_LAPSE
                        the time_lapse in which the bucket functions (in
                        millisecond) (default 100ms)
  --exec-speed EXEC_SPEED
                        the execution speed of the simulation (in seconds)
                        (default 0.5seconds/millisecond)
  --packet-dates PACKET_DATES [PACKET_DATES ...]
                        Set of packet dates in milliseconds (default [1, 2, 3,
                        4, 5, 6, 30, 34, 36, 38, 50, 60, 80, 82, 84, 86, 88,
                        100])

```

Feel free to correct it, play with it improve it, etc.

Bière, bière!
