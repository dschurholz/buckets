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

Feel free to correct it, play with it improve it, etc.

Bière, bière!
