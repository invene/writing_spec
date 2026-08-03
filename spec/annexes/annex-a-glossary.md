# Annex A — Glossary (normative, living)

**Status:** v0.10.0-draft. This living annex contains 24 admitted entries.

Maintainers add, revise, and deprecate entries under §2.5. They version each change under §0.8.

Maintainers never delete entries. They mark withdrawn entries as deprecated and retain them.

ITWS has one shared core and twelve profiles. Profile metadata records where maintainers expect a term to be useful.

Profile metadata does not make the term assumed vocabulary. Each governed document still satisfies the entry's ladder prerequisites before using the term.

The `Domain tag` field is descriptive metadata, not a profile ID.

## A.1 Entry format

The entry format adapts the ASD-STE100 dictionary format. That format includes the word, part of speech, approved meaning, approved example, and unapproved alternatives.

ITWS adds ladder prerequisites, profile scope, a domain tag, and version history.

Each definition must pass §2.3 and §2.4. The definition must be operational, avoid forward references, and use only assumed vocabulary or earlier entries.

```
### <term> (<part of speech>) — <status: admitted | deprecated>
Definition:            <operational definition passing §2.3/§2.4>
Approved example:      <one sentence using the term correctly>
Do not use for / say:  <disallowed senses and rejected synonyms>
Ladder prerequisites:  <assumed baseline (Annex B) | earlier entries by name>
Profiles:               <one or more ITWS profile IDs>
Domain tag:             <research | reliability/platform | security/governance | other>
Version:               <added in vX.Y; revisions noted>
```

The `Ladder prerequisites` field makes the glossary a ladder, not a word list. A document may admit an entry only after all prerequisites are available.

The document can admit the prerequisites earlier or assume them under Annex B. Rule 2.3.1 still requires a definition before the entry's first use.

Annex A supplies the canonical meaning. The annex does not silently add terms to a document's vocabulary.

Prerequisite cycles are entry defects.

## A.2 Chain roots and profile scope

The research seed chain starts with one term that Annex B §B.1 treats as assumed vocabulary. The term appears here only to make the chain explicit.

Governed documents need not define `function`.

- **function** — assumed (Annex B §B.1: basic software concepts).

## A.3 Entries

### parameter (noun) — admitted
```
Definition:            A stored number that controls one part of an adjustable function's
                       input-to-output calculation.
Approved example:      The function stores 20 parameters that determine its output.
Do not use for / say:  Do not confuse this stored-setting sense with a function parameter that
                       names an input.
Ladder prerequisites:  assumed baseline (function — Annex B §B.1)
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.2.0-draft
```

### model (noun) — admitted
```
Definition:            A function plus many stored numeric settings, called parameters, that
                       determine how the function maps inputs to outputs. Here "parameter" means
                       a stored setting, not a function argument.
Approved example:      The model maps an input sentence to a score between 0 and 1.
Do not use for / say:  Do not use "model" for a mathematical abstraction of a system (the
                       statistics sense) without defining that sense. Do not say "network,"
                       "system," or "AI" as synonyms.
Ladder prerequisites:  assumed baseline (function); parameter
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

### training (noun) — admitted
```
Definition:            An automated search for a model's parameter values. The search repeatedly
                       adjusts arbitrary starting values until the model's outputs approach
                       the outputs marked as correct in the examples.
Approved example:      Training ran for two days on eight million examples.
Do not use for / say:  Do not say "learning," "teaching," or "the model learned" without the
                       §2.6 defusing definition. Do not use "training" for human instruction.
Ladder prerequisites:  model
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

### loss (noun) — admitted
```
Definition:            A number measuring how wrong a model's outputs are on a set of examples,
                       where smaller values indicate better outputs. The experimenter's fixed
                       function computes the number, and training searches for parameter values
                       that reduce the number.
Approved example:      The loss on held-out examples stopped falling after the third day.
Do not use for / say:  Do not say "error" and "loss" interchangeably in one document (§2.1).
                       Pick one. Do not use "cost" as a synonym.
Ladder prerequisites:  model, training
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

### gradient (noun) — admitted
```
Definition:            For each trainable model parameter, the direction and relative amount
                       that would raise the loss fastest after a small parameter change.
                       Training computes this from the loss and then moves each parameter the
                       opposite way, which is the direction that reduces the loss.
Approved example:      Each training step adjusts every trainable parameter a small amount in
                       the direction opposite the gradient.
Do not use for / say:  Do not use "gradient" loosely for "trend" or "slope of a plot." This entry
                       admits the operational sense, not the calculus definition as a vector of
                       partial derivatives.
Ladder prerequisites:  model, training, loss
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

### neural network (noun) — admitted
```
Definition:            A model made by composing small functions into ordered stages. Each
                       function combines inputs with model parameters, and each stage passes its
                       outputs to the next stage.
Approved example:      The neural network has about seven billion parameters.
Do not use for / say:  Do not say "net," "the AI," or "the brain." Do not use a biological
                       analogy without stating its breaking point (§6.1).
Ladder prerequisites:  model
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

### layer (noun) — admitted
```
Definition:            One stage of a neural network, containing small functions that run on the
                       same inputs at the same depth. Each stage consumes the previous stage's
                       outputs.
Approved example:      The twelfth layer's outputs feed every later layer's inputs.
Do not use for / say:  Do not use "layer" for software layering (as in "storage layer") in the
                       same document without renaming one of the two senses.
Ladder prerequisites:  neural network
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

### weight (noun) — admitted
```
Definition:            A single neural-network parameter that a small function multiplies by one
                       of its inputs. The plural form means all parameter values of a network
                       together.
Approved example:      Copying a model means copying its weights.
Do not use for / say:  Do not mix "weight" and "parameter" as free variants in one document
                       (§2.1). State once that weights are the network's parameters. Then pick
                       one term.
Ladder prerequisites:  neural network, model
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

### token (noun) — admitted
```
Definition:            One item from a fixed list of text units: a word, part of a word, or
                       punctuation mark. A model reads and produces text one item at a time.
Approved example:      The input document is 4,000 tokens long.
Do not use for / say:  Do not use "word" and "token" interchangeably. Word and token counts
                       differ. Do not use "token" in its security sense (access token) without
                       renaming that sense.
Ladder prerequisites:  model, training
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

### embedding (noun) — admitted
```
Definition:            A mapping that training creates from items such as tokens to fixed-length
                       lists of numbers. The mapping places items used in similar ways near each
                       other numerically.
Approved example:      The two words receive nearby embeddings because they appear in similar
                       contexts.
Do not use for / say:  Do not say "vector representation" as an unexplained synonym. If you use
                       the hashing analogy, state its breaking point (§6.1). Training creates an
                       embedding that preserves similarity, but a hash scatters items.
Ladder prerequisites:  token, training, model
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

### attention (noun) — admitted
```
Definition:            A neural-network component that scores input positions and mixes
                       information from the highest-scoring positions for each output position.
                       Training sets the parameters that calculate the scores.
Approved example:      Attention lets the model use a token from the start of the document when
                       processing the last token.
Do not use for / say:  Do not use "attention" in the psychological sense in the same document.
                       "The model attends to X" requires the §2.6 defusing definition.
Ladder prerequisites:  neural network, layer, token, training
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

### transformer (noun) — admitted
```
Definition:            A neural network built from repeated layers that combine attention with a
                       small function at each position. These networks read tokens as input, and
                       most current text-processing models have this form.
Approved example:      Both models are transformers with 24 layers.
Do not use for / say:  Do not expand as "the Transformer" with a citation in place of a
                       definition (§2.4: no definition by citation alone).
Ladder prerequisites:  neural network, layer, attention, token
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

### fine-tuning (noun) — admitted
```
Definition:            Additional training of an already-trained model on a smaller example set
                       chosen for one task. The additional training starts from the model's
                       existing parameter values, not arbitrary values.
Approved example:      Fine-tuning on 10,000 labeled support tickets took one hour.
Do not use for / say:  Do not use "fine-tuning" loosely for any small adjustment ("we fine-tuned
                       the config"). Do not say "post-training" as an unexplained synonym.
Ladder prerequisites:  training, model
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

### overfitting (noun) — admitted
```
Definition:            A training failure in which loss decreases on training examples while the
                       model's outputs worsen on new examples. The model stores example-specific
                       details instead of a rule that carries over.
Approved example:      Overfitting began after day two, when held-out loss rose while training
                       loss kept falling.
Do not use for / say:  Do not use "memorization" as a bare synonym. Tie the term to this
                       definition at first use.
Ladder prerequisites:  training, loss, model
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

### inference (noun) — admitted
```
Definition:            Running a trained model on new inputs to get outputs without changing its
                       parameters. This operation is the deployment phase, whereas training is
                       the search phase.
Approved example:      Inference on one document takes 200 milliseconds.
Do not use for / say:  Do not use the statistics sense (drawing conclusions from data) or the
                       everyday sense in the same document without renaming either sense. Do not
                       use inference as a synonym for "prediction."
Ladder prerequisites:  model, training
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

### held-out examples (noun) — admitted
```
Definition:            Examples set aside before training and never used to adjust parameters.
                       They measure how a model behaves on data that training did not use.
Approved example:      Section 4 reports results only from held-out examples.
Do not use for / say:  Prefer this term over bare "test set" / "validation set" until those are
                       admitted with their distinct roles. Do not use "unseen data" loosely.
Ladder prerequisites:  training, model
Profiles:               research-paper
Domain tag:             research
Version:               added in v0.1
```

## A.4 Non-research seed chains

These entries show that the ladder also applies to engineering and governance domains.

The entries describe generic concepts. They do not encode facts specific to an organization or product.

### service (noun) — admitted
```
Definition:            A running software unit that accepts requests through a defined
                       interface. The unit returns results or performs work for another unit or
                       user.
Approved example:      The service accepts an HTTP request and returns the stored record.
Do not use for / say:  Do not use "service" as a synonym for any process, library, or team.
                       State the unit's interface and responsibility.
Ladder prerequisites:  assumed baseline (process, interface, client/server — Annex B §B.1)
Profiles:               design-rfc, procedure, explanation, incident, technical-report,
                       investigation-log, epic, task, subtask
Domain tag:             reliability/platform
Version:               added in v0.2.0-draft
```

### service-level indicator (noun) — admitted
```
Definition:            A measured quantity that describes one aspect of a service's behavior for
                       its users. An example is the fraction of successful requests.
Approved example:      The service-level indicator is the fraction of requests completed within
                       300 milliseconds.
Do not use for / say:  Do not use the abbreviation "SLI" before admission. Do not call an
                       unmeasured intention an indicator.
Ladder prerequisites:  service; assumed baseline (measurement, fraction, request)
Profiles:               design-rfc, incident, technical-report, investigation-log, epic,
                       task, subtask
Domain tag:             reliability/platform
Version:               added in v0.2.0-draft
```

### service-level objective (noun) — admitted
```
Definition:            A target range for a service-level indicator during a stated period.
Approved example:      The service-level objective requires at least 99.9% of requests to succeed
                       in each 30-day period.
Do not use for / say:  Do not use the abbreviation "SLO" before admission. Do not present the
                       target as an observed result.
Ladder prerequisites:  service-level indicator; assumed baseline (range, period)
Profiles:               design-rfc, decision-record, incident, technical-report, epic, task,
                       subtask
Domain tag:             reliability/platform
Version:               added in v0.2.0-draft
```

### error budget (noun) — admitted
```
Definition:            The amount of unsuccessful or over-limit behavior that a service-level
                       objective permits during its stated period.
Approved example:      Failed requests consumed one quarter of the monthly error budget.
Do not use for / say:  Do not use "budget" without naming the indicator, objective, and period.
                       An error budget is not a financial budget.
Ladder prerequisites:  service-level indicator, service-level objective
Profiles:               design-rfc, decision-record, incident, technical-report, epic, task,
                       subtask
Domain tag:             reliability/platform
Version:               added in v0.2.0-draft
```

### asset (noun) — admitted
```
Definition:            Data, software, equipment, or a capability that an identified party needs
                       to protect from loss, damage, disclosure, or unauthorized change.
Approved example:      The stored access records are assets because disclosure would expose user
                       activity.
Do not use for / say:  Do not call something an asset without identifying who values it and what
                       kind of harm protection addresses.
Ladder prerequisites:  assumed baseline (data, software, access, change)
Profiles:               design-rfc, decision-record, procedure, explanation, incident,
                       technical-report, investigation-log, epic, task, subtask
Domain tag:             security/governance
Version:               added in v0.2.0-draft
```

### threat (noun) — admitted
```
Definition:            A possible event or action that could harm an asset in a stated way under
                       stated conditions.
Approved example:      Unauthorized copying is a threat because it would disclose the access
                       records.
Do not use for / say:  Do not use "threat" for a person or group without describing the possible
                       harmful action and conditions.
Ladder prerequisites:  asset; assumed baseline (event, condition)
Profiles:               design-rfc, decision-record, procedure, explanation, incident,
                       technical-report, investigation-log, epic, task, subtask
Domain tag:             security/governance
Version:               added in v0.2.0-draft
```

### control (noun) — admitted
```
Definition:            A technical or organizational measure intended to reduce the chance or
                       effect of a stated threat to an asset.
Approved example:      Requiring two approvals is a control intended to reduce unauthorized
                       configuration changes.
Do not use for / say:  Do not claim that a control eliminates risk unless the evidence supports
                       elimination.
Ladder prerequisites:  asset, threat; assumed baseline (measure, chance, effect)
Profiles:               design-rfc, decision-record, procedure, explanation, incident,
                       technical-report, investigation-log, epic, task, subtask
Domain tag:             security/governance
Version:               added in v0.2.0-draft
```

### residual risk (noun) — admitted
```
Definition:            The stated chance and effect of harm from a threat after the selected
                       controls are in place.
Approved example:      The residual risk is an estimated one mistaken disclosure per 10,000
                       approved exports, with one record disclosed per event.
Do not use for / say:  Do not call risk "accepted" unless an identified decision owner has
                       recorded that decision.
Ladder prerequisites:  threat, control
Profiles:               design-rfc, decision-record, incident, technical-report,
                       investigation-log, epic, task, subtask
Domain tag:             security/governance
Version:               added in v0.2.0-draft
```

## A.5 Seed status and next steps

The research chain remains the research-profile proof of the ladder. Its main sequence is:

- parameter → model → training → loss → gradient → neural network → layer → weight → token → embedding → attention → transformer → fine-tuning → overfitting

Inference and held-out examples are additional research entries.

The reliability/platform chain is service → service-level indicator → service-level objective → error budget.

The security/governance chain is asset → threat → control → residual risk.

Future seed work balances profiles. Research entry counts do not drive priorities.

Add terms only when a governed document needs them. Retain profile and domain metadata.

Rewrite each candidate until it passes §2.3 and §2.4.
