# How BigchainDB is Immutable / Tamper-Resistant

The word _immutable_ means "unchanging over time or unable to be changed." For example, the decimal digits of π are immutable (3.14159…).

The blockchain community often describes blockchains as “immutable.” If we interpret that word literally, it means that blockchain data is unchangeable or permanent, which is absurd. The data _can_ be changed. For example, a plague might drive humanity extinct; the data would then get corrupted over time due to water damage, thermal noise, and the general increase of entropy. In the case of Bitcoin, nothing so drastic is required: a 51% attack will suffice.

It’s true that blockchain data is more difficult to change than usual: it’s more tamper-resistant than a typical file system or database. Therefore, in the context of blockchains, we interpret the word “immutable” to mean tamper-resistant. (Linguists would say that the word “immutable” is a _term of art_ in the blockchain community.)

BigchainDB achieves strong tamper-resistance in the following ways:

1. **Replication.** All data is sharded and shards are replicated in several (different) places. The replication factor can be set by the federation. The higher the replication factor, the more difficult it becomes to change or delete all replicas.
2. **Internal watchdogs.** All nodes monitor all changes and if some unallowed change happens, then appropriate action is taken. For example, if a valid block is deleted, then it is put back.
3. **External watchdogs.** Federations may opt to have trusted third-parties to  monitor and audit their data, looking for irregularities. For federations with publicly-readable data, the public can act as an auditor.
4. **Cryptographic signatures** are used throughout BigchainDB as a way to check if messages (transactions, blocks and votes) have been tampered with enroute, and as a way to verify who signed the messages. Each block is signed by the node that created it. Each vote is signed by the node that cast it. A creation transaction is signed by the node that created it, although there are plans to improve that by adding signatures from the sending client and multiple nodes; see [Issue #347](https://github.com/bigchaindb/bigchaindb/issues/347). Transfer transactions can contain multiple fulfillments (one per asset transferred). Each fulfillment will typically contain one or more signatures from the owners (i.e. the owners before the transfer). Hashlock fulfillments are an exception; there’s an open issue ([#339](https://github.com/bigchaindb/bigchaindb/issues/339)) to address that.
5. **Full or partial backups** of the database may be recorded from time to time, possibly on magnetic tape storage, other blockchains, printouts, etc.
6. **Strong security.** Node owners can adopt and enforce strong security policies.
7. **Node diversity.** Diversity makes it so that no one thing (e.g. natural disaster or operating system bug) can compromise enough of the nodes. See [the section on the kinds of node diversity](diversity.html).

Some of these things come "for free" as part of the BigchainDB software, and others require some extra effort from the federation and node owners.
