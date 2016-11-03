# Timestamps in BigchainDB

Each transaction, block and vote has an associated timestamp. Interpreting those timestamps is tricky, hence the need for this section.


## Timestamp Sources & Accuracy

A transaction's timestamp is provided by the client which created and submitted the transaction to a BigchainDB node. A block's timestamp is provided by the BigchainDB node which created the block. A vote's timestamp is provided by the BigchainDB node which created the vote.

When a BigchainDB client or node needs a timestamp, it calls a BigchainDB utility function named `timestamp()`. There's a detailed explanation of how that function works below, but the short version is that it gets the [Unix time](https://en.wikipedia.org/wiki/Unix_time) from its system clock, rounded to the nearest second.

We can't say anything about the accuracy of the system clock on clients. Timestamps from clients are still potentially useful, however, in a statistical sense. We say more about that below.

We advise BigchainDB nodes to run special software (an "NTP daemon") to keep their system clock in sync with standard time servers. (NTP stands for [Network Time Protocol](https://en.wikipedia.org/wiki/Network_Time_Protocol).)


## Converting Timestamps to UTC

To convert a BigchainDB timestamp (a Unix time) to UTC, you need to know how the node providing the timestamp was set up. That's because different setups will report a different "Unix time" value around leap seconds! There's [a nice Red Hat Developer Blog post about the various setup options](http://developers.redhat.com/blog/2015/06/01/five-different-ways-handle-leap-seconds-ntp/). If you want more details, see [David Mills' pages about leap seconds, NTP, etc.](https://www.eecis.udel.edu/~mills/leap.html) (David Mills designed NTP.)

We advise BigchainDB nodes to run an NTP daemon with particular settings so that their timestamps are consistent.

If a timestamp comes from a node that's set up as we advise, it can be converted to UTC as follows:

1. Use a standard "Unix time to UTC" converter to get a UTC timestamp.
2. Is the UTC timestamp a leap second, or the second before/after a leap second? There's [a list of all the leap seconds on Wikipedia](https://en.wikipedia.org/wiki/Leap_second).
3. If no, then you are done.
4. If yes, then it might not be possible to convert it to a single UTC timestamp. Even if it can't be converted to a single UTC timestamp, it _can_ be converted to a list of two possible UTC timestamps.
Showing how to do that is beyond the scope of this documentation.
In all likelihood, you will never have to worry about leap seconds because they are very rare.
(There were only 26 between 1972 and the end of 2015.)


## Calculating Elapsed Time Between Two Timestamps

There's another gotcha with (Unix time) timestamps: you can't calculate the real-world elapsed time between two timestamps (correctly) by subtracting the smaller timestamp from the larger one. The result won't include any of the leap seconds that occured between the two timestamps. You could look up how many leap seconds happened between the two timestamps and add that to the result. There are many library functions for working with timestamps; those are beyond the scope of this documentation.


## Avoid Doing Transactions Around Leap Seconds

Because of the ambiguity and confusion that arises with Unix time around leap seconds, we advise users to avoid creating transactions around leap seconds.


## Interpreting Sets of Timestamps

You can look at many timestamps to get a statistical sense of when something happened. For example, a transaction in a decided-valid block has many associated timestamps:

* its own timestamp
* the timestamps of the other transactions in the block; there could be as many as 999 of those
* the timestamp of the block
* the timestamps of all the votes on the block

Those timestamps come from many sources, so you can look at all of them to get some statistical sense of when the transaction "actually happened." The timestamp of the block should always be after the timestamp of the transaction, and the timestamp of the votes should always be after the timestamp of the block.


## How BigchainDB Uses Timestamps

BigchainDB _doesn't_ use timestamps to determine the order of transactions or blocks. In particular, the order of blocks is determined by RethinkDB's changefeed on the bigchain table.

BigchainDB does use timestamps for some things. It uses them to determine if a transaction has been waiting in the backlog for too long (i.e. because the node assigned to it hasn't handled it yet). It also uses timestamps to determine the status of timeout conditions (used by escrow).


## Including Trusted Timestamps

If you want to create a transaction payload with a trusted timestamp, you can.

One way to do that would be to send a payload to a trusted timestamping service. They will send back a timestamp, a signature, and their public key. They should also explain how you can verify the signature. You can then include the original payload, the timestamp, the signature, and the service's public key in your transaction. That way, anyone with the verification instructions can verify that the original payload was signed by the trusted timestamping service.


## How the timestamp() Function Works

BigchainDB has a utility function named `timestamp()` which amounts to:
```python
timestamp() = str(round(time.time()))
```

In other words, it calls the `time()` function in Python's `time` module, [rounds](https://docs.python.org/3/library/functions.html#round) that to the nearest integer, and converts the result to a string.

It rounds the output of `time.time()` to the nearest second because, according to [the Python documentation for `time.time()`](https://docs.python.org/3.4/library/time.html#time.time), "...not all systems provide time with a better precision than 1 second."

How does `time.time()` work? If you look in the C source code, it calls `floattime()` and `floattime()` calls [clock_gettime()](https://www.cs.rutgers.edu/~pxk/416/notes/c-tutorials/gettime.html), if it's available.
```text
ret = clock_gettime(CLOCK_REALTIME, &tp);
```

With `CLOCK_REALTIME` as the first argument, it returns the "Unix time." ("Unix time" is in quotes because its value around leap seconds depends on how the system is set up; see above.)


## Why Not Use UTC, TAI or Some Other Time that Has Unambiguous Timestamps for Leap Seconds?

It would be nice to use UTC or TAI timestamps, but unfortunately there's no commonly-available, standard way to get always-accurate UTC or TAI timestamps from the operating system on typical computers today (i.e. accurate around leap seconds).

There _are_ commonly-available, standard ways to get the "Unix time," such as clock_gettime() function available in C. That's what we use (indirectly via Python). ("Unix time" is in quotes because its value around leap seconds depends on how the system is set up; see above.)

The Unix-time-based timestamps we use are only ambiguous circa leap seconds, and those are very rare. Even for those timestamps, the extra uncertainty is only one second, and that's not bad considering that we only report timestamps to a precision of one second in the first place. All other timestamps can be converted to UTC with no ambiguity.
