# Checking generated sentences against their input before accepting them

ITWS version: 0.6.0-draft
Profile: research-paper
Conformance tier: publication

## Abstract

Systems that generate text sometimes state facts their input does not support. We call such a fact an *unsupported statement*.

We built a checker that compares each generated sentence with the input before the system accepts the sentence. On three question-answering test sets, the checker reduced unsupported statements from 8.1% of sentences to 4.6%. Generation cost rose by a factor of 1.9.

## Introduction

A text-generating system reads an input document and produces sentences. A reader who cannot see the input cannot tell which produced sentences the input supports.

Two responses to that problem exist. The first response asks a reader to check every produced sentence against the input by hand. That response is accurate and does not scale past a few hundred sentences per day.

The second response asks the system to check its own output before the system returns it. That response scales, and its accuracy is the open question this paper measures.

We chose the second response because our deployment produces about 40,000 sentences each day. A hand check at that volume needs about nine full-time readers, and the pod has none.

This paper reports one measurement: how far a sentence-level check reduces unsupported statements, and what that check costs.

We report the reduction, the cost, and the effect on answer accuracy. We do not report a comparison against other published checkers, because those checkers need inputs our deployment does not record.

## Background from first principles

This section admits the five terms the rest of the paper needs. Each term arrives after the terms its definition depends on.

Every measurement below comes from one running system. The system reads an input document, produces sentences, and returns those sentences to a caller. The caller is a question-answering front end that shows the produced sentences to a person.

The person who reads the answer cannot see the input document. That absence is what makes an unsupported statement harmful instead of visible. A person who can compare the answer with the input detects the error in a second. A person who cannot compare them has no signal at all.

The system at the centre of this paper is an adjustable function. An adjustable function maps an input to an output, and a set of stored numbers changes how it performs that mapping. Changing one stored number changes the output for some inputs and leaves the output unchanged for others.

The stored numbers are not written by a person. An automated procedure searches for values that make the outputs match a set of examples marked correct. The procedure starts from arbitrary values and adjusts them repeatedly.

That search is the expensive part of building such a system. Running the finished system on a new input is much cheaper, and the two operations are worth separating by name.

Measuring the finished system needs care. A result measured on the same examples the search used describes memory, not behavior on new inputs. Researchers therefore set examples aside before the search begins and measure on those examples only.

### Admitted terms

A *parameter* is a stored number that controls one part of an adjustable function's calculation from input to output. This sense is a stored setting, not a function argument.

A *model* is a function plus many stored parameters that determine how the function maps inputs to outputs.

*Training* is an automated search for a model's parameter values. The search adjusts arbitrary starting values until the outputs approach the outputs marked correct.

## Method or what we built

The checker takes one generated sentence and the input document. It returns accept or reject.

The checker accepts a sentence when every named entity and every number in the sentence appears in the input document. The checker rejects the sentence otherwise. A rejected sentence is generated again, at most three times.

The entity comparison is exact after three normalizations. The checker lowercases both strings, removes leading articles, and collapses runs of whitespace to one space. It applies no synonym list and no spelling correction.

The number comparison is exact after two normalizations. The checker removes thousands separators and treats a trailing zero after a decimal point as absent. A number written as a word is compared as a word, because the checker performs no conversion.

These choices make the checker conservative. A sentence that restates an input fact in different words is rejected, and the system pays the cost of generating that sentence again. We accepted the conservative behavior because a wrongly accepted sentence reaches a person and a wrongly rejected sentence does not.

The retry limit of three is the one setting we tuned. At a limit of one, 3.1% of answers ended with no acceptable sentence. At three, that figure fell to 0.4%. At five, it fell to 0.3% and generation cost rose by a further factor of 1.3.

The checker runs after generation and before the answer reaches the caller. It adds no state, so two answers can be checked at the same time without any shared lock.

We did not change the generating system. Every difference this paper reports comes from adding the checker in front of an unchanged system, so the comparison isolates the check.

## Experimental setup

We ran three public question-answering test sets. Each set supplies an input document and a question. The three sets differ in document length: the shortest averages 180 words per document and the longest averages 2,400.

We chose public sets so another person can repeat the measurement without access to our deployment. Each set was published with a fixed split between the examples used to build a system and the examples reserved for measurement.

Set A supplies 4,200 question and document pairs drawn from encyclopedia articles. Set B supplies 2,800 pairs drawn from product manuals. Set C supplies 1,100 pairs drawn from public financial filings.

We report each set separately in the appendix and pooled in the results below. Pooling is a weighted mean over the three sets, weighted by pair count.

The generating system was identical across all three sets and across both configurations. Its decoding settings were fixed before the first run and never changed.

One host ran every measurement. The host has 8 processor cores and 64 gigabytes of memory, and it ran no other work during a measurement.

Running a finished model on a new input has its own name. Its cost and its risk both differ from those of the search that produced the model.

*Inference* is running a trained model on new inputs to get outputs without changing its parameters.

Measuring on the examples the search already used reports memory, not behavior. The published splits exist to prevent that error. This paper uses the reserved side of each split.

*Held-out examples* are examples set aside before training and never used to adjust parameters. A result measured on held-out examples describes behavior on data the search did not use.

We ran the same model with and without the checker, on held-out examples only. Each configuration ran five times, and we report the median of the five runs.

Two annotators marked each output sentence as supported or unsupported. The annotators agreed on 94% of sentences. A third reader resolved the remaining 6%.

## Results

Without the checker, 8.1% of output sentences were unsupported. With the checker, 4.6% were unsupported.

Generation cost rose from 1.0 to 1.9 times the baseline, measured as inference calls per answer.

Answer accuracy was 61.2% without the checker and 60.4% with it.

## Discussion

The evidence indicates that a sentence-level check reduces unsupported statements on these three test sets. The reduction costs additional inference calls and does not improve answer accuracy.

The evidence does not establish a benefit on summarization, because every test set covered question answering.

## Limitations

We tested question answering only. We did not test summarization, translation, or dialogue.

Our checker compares named entities and numbers. The checker does not detect an unsupported relation between two supported entities.

We did not measure variance across training runs, so we cannot state which part of the reduction is stable.

Two annotators marked the outputs. We did not measure agreement with a third annotator.

## Reproducibility statement

Another person repeats this work with the three public test sets and the checker source at [checker/](https://example.invalid/itws-fixture/checker). The fixed decoding settings are recorded in `configs/`, and the five-run median script is beside them.

The model weights are not public. A reader who substitutes a different model reproduces the procedure but not the reported percentages.
