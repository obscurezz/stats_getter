# Oracle GoldenGate stats getter

***

# Problem

Known problem is GoldenGate has limited stats buffer size.
Due to this problem sometimes it isn't possible to collect all tables stats data using `stats replicat` command.

# Desicion

* Stats getter gets input list with replicats name, formatted like:
> REPLA
> 
> REPLB
> 
> REPLC

* Then it gets input with stats formatted `hourly|daily|total`
* Returns json file with table stats

# Usage
```
python3 -m stats_getter.py
```

* Next update well release shell script for process run