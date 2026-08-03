# How a read cache reduces database load

ITWS version: 0.10.0-draft
Profile: explanation

## Summary

Keeping a recent result close to the caller can reduce read latency. The system returns that stored result instead of repeating a slower lookup.

## Concepts

A *cache* is a store that holds a result under the same key used to request it. Each stored result carries an expiration condition.

A stored result is *stale* when the source value changed after the cache stored the result.

## Mechanism

The caller asks the cache for a key. If the cache holds an unexpired result for that key, the cache returns it.

Otherwise the caller performs the original lookup. The caller stores the result under the key. The caller then returns the result.

## Examples

Suppose 100 requests ask for one record while the cache holds it. The system serves 100 cache reads and zero database reads.

Suppose the same 100 requests arrive while the cache holds nothing. Every request performs the original lookup, so the database serves 100 reads.

## Limits

A stored result can be stale until it expires. A caller that needs the current value must read the source.

Simultaneous misses on one key can each repeat the original lookup. The cache does not prevent that repetition on its own.

A cache trades memory and freshness for fewer slow source reads. The trade is worthwhile only when reads repeat.
