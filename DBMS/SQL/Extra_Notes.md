### SQL Page Life Expectancy (PLE)

- PLE is an age of a data page in seconds in the buffer cache or buffer memory after querying the tables with loading data page into memory.
- Page Life Expectancy value indicates the memory pressure in allocated memory to the SQL Server instance. (Mostly) Page will be dropped from memory periodically.

- PLE always needs to be able 300 (5 minutes) (why? coz we need it as long as in memory cashe coz it is easier to read from memory than from disk, but cache has a limit and when the limit is hit the page needs to be dropped to make space for new queries)

- If possible track over time and observe trend to correlate with system performance.

[Source - youtube](https://youtu.be/V0y_kKKK95Q?si=_mGuxz8MmKZ-hgZv)


```
SELECT *
FROM sys.dm_os_performance_counters
WHERE [counter_name] = 'Page life expectancy'
```

### Troubleshooting Low PLE

- Insufficient Memory

If workload is steadily increasing and PLE is decreasing, you might be short on memory. Adding memory might help increase PLE, but won't make querying more effiecient.

- Expensive Operation

If the workload hasn't changed, but there is an increased demand on the buffer pool, it could be that the outliers are using more memory. Check to see if there are maintaining jobs running or index rebuilds in progress.

- Stale Statistics

Stale statistics can cause changes to the query plan. This increases demand on the buffer pool by causing expensive operations to run because they aren't synced with the new stats.






[Linkedin Article](https://www.linkedin.com/pulse/cache-bloating-sneaky-memory-hog-thats-probably-your-amit-prakash-njlsc/)