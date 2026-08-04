ITWS version: 1.0.0
Profile: explanation
AI disclosure: generated — written as a deliberate violation corpus for tools/itws_literal.py; not yet reviewed

# Phrase-list fixture

**This file is a fixture, not a governed document.** It carries no conformance
claim, and it is deliberately full of violations: every phrase list in
`spec/phrases.md` that `itws_literal.py` screens has at least one instance
below. `itws_literal.py --self-test` fails when a list stops producing a finding,
which is how a phrase list added to the specification without a matching fixture
line gets caught.

Quoting a prohibited string is permitted under §2.6.4 ("except in quotation or
discussion of the word"), so the lines below state each string in running prose
instead. That is the point: the tool must find them.

## One line per list

We utilize the gateway to route requests, and the operator can perform a manual
restart. (§2.1.3)

The retry budget is defined below, and the failure taxonomy is described below.
(§2.3.3)

The scheduler is a state-of-the-art design and the rewrite produced a dramatic
improvement. (§2.6.3)

We delve into the tapestry of the deployment landscape, which boasts a robust
and intricate pipeline. (§2.6.4)

The planner wants a shorter queue, and the retry loop believes the host is
healthy. (§2.6.5)

Instead of the old approach, the router now hashes on tenant. Previously we
sharded on region. (§2.6.6)

It is important to note that the cache is cold on first request. Notably, the
warm path is faster. (§2.6.7)

Studies show that shorter sentences read faster, and experts say the effect is
large. (§2.6.8)

While specific details are limited, the outage probably began in the load
balancer. (§2.6.9)

Moreover, the queue drains in order.

Furthermore, the queue never reorders.

I hope this helps, and let's dive in to the retry semantics. (§2.6.11,
conversational)

The owner is [Your Name] and the cutover date is TBD. (§2.6.11, placeholders)

See the trace at https://example.invalid/x?utm_source=chatgpt.com for the
timings. (§2.6.11, tool leakage)

This is a bare sentence opener with no naming noun following it. (§3.6.2)

The rollout is somewhat slower and the error rate is relatively flat. (§3.9.1)

The queue is not just a buffer, and the router is not merely a hash function.
(§3.10.2)

The migration cut latency by half, highlighting the need for earlier capacity
work. (§3.10.4)

The gateway serves as a rate limiter and the sidecar functions as a proxy.
(§3.10.6)

The build passed on every runner 🎉 and the dashboard turned green. (§4.10.5)

Clearly the cache is correct, and obviously the eviction order does not matter.
(§5.6.1)

## Sentence-length and punctuation screens

This sentence exists to run past the twenty-five word descriptive cap that
section three point one point one states, and it keeps going well beyond that
point so the counter has something unambiguous to report. (§3.1.1)

The queue drains in order; the router never reorders a batch. (§3.8.1)

## The exporter does not drop spans

> **[Detail — a bounded block does not consume the opening slot]** Core §4.12.1
> excludes a bounded block from the scan path. This block sits directly under
> the heading, so a screen that took the first prose paragraph it found would
> stop here and never reach the opening chunk below.

The exporter does not drop spans, although sampling may discard them under load.
(§4.12.3)

Three things carry this line's weight. The heading above is the scan path's
first element and produces its own candidate. The paragraph is the section's
opening chunk and produces a second. The block between them produces neither.
§4.12.3 is bounded to the scan path, so a copy of this sentence further down a
section produces nothing, which is why the line lives here.

## Bounded-block screens

> **[Speculation — first connection failure]** The record shows that a
> credential refresh began the growth. (§7.3.3 — a verified-tier phrase inside a
> speculation block)

> **[Sidebar — not a permitted label]** A bounded block carries one of three
> labels. (§4.6.2)
