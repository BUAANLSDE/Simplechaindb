# Running Unit Tests

Once you've installed BigchainDB Server, you may want to run all the unit tests. This section explains how.

First of all, if you installed BigchainDB Server using `pip` (i.e. by getting the package from PyPI), then you didn't install the tests. **Before you can run all the unit tests, you must [install BigchainDB from source](setup-run-node.html#how-to-install-bigchaindb-from-source).**

To run all the unit tests, first make sure you have RethinkDB running:

```text
$ rethinkdb
```

then in another terminal, do:

```text
$ python setup.py test
```

(Aside: How does the above command work? The documentation for [pytest-runner](https://pypi.python.org/pypi/pytest-runner) explains. We use [pytest](http://docs.pytest.org/en/latest/) to write all unit tests.)


### Using docker-compose to Run the Tests

You can also use `docker-compose` to run the unit tests.

Start `RethinkDB` in the background:

```text
$ docker-compose up -d rdb
```

then run the unit tests using:

```text
$ docker-compose run --rm bdb py.test -v
```
