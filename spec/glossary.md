# ITWS glossary

**ITWS version:** 1.0 · **Status:** normative, living · 24 admitted entries

Canonical meanings for terms that recur across governed documents.

**A glossary entry does not make a term assumed.** The document still admits the term under core §2.3 before first use. What the entry fixes is *which* meaning: a document may not contradict an entry (§2.5.1), and at definitional first use it should quote the entry's wording (§2.5.2).

**Ladder prerequisites** are the terms an entry's definition stands on. Admit them first, or have them assumed under [reader.md](reader.md). Prerequisite cycles are entry defects.

`Profiles` records where the term is expected to be useful. It neither grants nor restricts use elsewhere.

Entries are never deleted — a withdrawn entry is marked deprecated and retained.

---

## Research chain

Order: parameter → model → training → loss → gradient → neural network → layer → weight → token → embedding → attention → transformer → fine-tuning → overfitting. Plus inference and held-out examples.

Root: **function** is assumed ([reader.md](reader.md)). Governed documents need not define it.

All entries below: `Profiles: research-paper` · domain tag `research`.

**parameter** (n) — A stored number that controls one part of an adjustable function's input-to-output calculation.
*Example:* "The function stores 20 parameters that determine its output."
*! Do not:* confuse this stored-setting sense with a function parameter naming an input.
*Prereq:* function (assumed).

**model** (n) — A function plus many stored numeric settings, called parameters, that determine how the function maps inputs to outputs. Here "parameter" means a stored setting, not a function argument.
*Example:* "The model maps an input sentence to a score between 0 and 1."
*! Do not:* use for the statistics sense (a mathematical abstraction of a system) without defining that sense; say "network", "system", or "AI" as synonyms.
*Prereq:* function (assumed), parameter.

**training** (n) — An automated search for a model's parameter values. The search repeatedly adjusts arbitrary starting values until the model's outputs approach the outputs marked as correct in the examples.
*Example:* "Training ran for two days on eight million examples."
*! Do not:* say "learning", "teaching", or "the model learned" without the §2.6.5 defusing definition; use for human instruction.
*Prereq:* model.

**loss** (n) — A number measuring how wrong a model's outputs are on a set of examples, where smaller values indicate better outputs. The experimenter's fixed function computes the number, and training searches for parameter values that reduce it.
*Example:* "The loss on held-out examples stopped falling after the third day."
*! Do not:* use "error" and "loss" interchangeably in one document (§2.1.2) — pick one; use "cost" as a synonym.
*Prereq:* model, training.

**gradient** (n) — For each trainable model parameter, the direction and relative amount that would raise the loss fastest after a small parameter change. Training computes this from the loss, then moves each parameter the opposite way, which reduces the loss.
*Example:* "Each training step adjusts every trainable parameter a small amount in the direction opposite the gradient."
*! Do not:* use loosely for "trend" or "slope of a plot". This entry admits the operational sense, not the calculus definition.
*Prereq:* model, training, loss.

**neural network** (n) — A model made by composing small functions into ordered stages. Each function combines inputs with model parameters, and each stage passes its outputs to the next.
*Example:* "The neural network has about seven billion parameters."
*! Do not:* say "net", "the AI", or "the brain"; use a biological analogy without stating its breaking point (§6.1.2).
*Prereq:* model.

**layer** (n) — One stage of a neural network, containing small functions that run on the same inputs at the same depth. Each stage consumes the previous stage's outputs.
*Example:* "The twelfth layer's outputs feed every later layer's inputs."
*! Do not:* use for software layering ("storage layer") in the same document without renaming one sense.
*Prereq:* neural network.

**weight** (n) — A single neural-network parameter that a small function multiplies by one of its inputs. Plural: all parameter values of a network together.
*Example:* "Copying a model means copying its weights."
*! Do not:* mix "weight" and "parameter" as free variants (§2.1.2). State once that weights are the network's parameters, then pick one term.
*Prereq:* neural network, model.

**token** (n) — One item from a fixed list of text units: a word, part of a word, or punctuation mark. A model reads and produces text one item at a time.
*Example:* "The input document is 4,000 tokens long."
*! Do not:* use "word" and "token" interchangeably — the counts differ; use the security sense (access token) without renaming it.
*Prereq:* model, training.

**embedding** (n) — A mapping that training creates from items such as tokens to fixed-length lists of numbers. The mapping places items used in similar ways near each other numerically.
*Example:* "The two words receive nearby embeddings because they appear in similar contexts."
*! Do not:* say "vector representation" as an unexplained synonym. If you use the hashing analogy, state its breaking point (§6.1.2): training preserves similarity, a hash scatters.
*Prereq:* token, training, model.

**attention** (n) — A neural-network component that scores input positions and mixes information from the highest-scoring positions for each output position. Training sets the parameters that calculate the scores.
*Example:* "Attention lets the model use a token from the start of the document when processing the last token."
*! Do not:* use the psychological sense in the same document. "The model attends to X" needs the §2.6.5 defusing definition.
*Prereq:* neural network, layer, token, training.

**transformer** (n) — A neural network built from repeated layers that combine attention with a small function at each position. These networks read tokens as input, and most current text-processing models have this form.
*Example:* "Both models are transformers with 24 layers."
*! Do not:* expand as "the Transformer" with a citation in place of a definition (§2.4.5).
*Prereq:* neural network, layer, attention, token.

**fine-tuning** (n) — Additional training of an already-trained model on a smaller example set chosen for one task. It starts from the model's existing parameter values, not arbitrary values.
*Example:* "Fine-tuning on 10,000 labeled support tickets took one hour."
*! Do not:* use loosely for any small adjustment ("we fine-tuned the config"); say "post-training" as an unexplained synonym.
*Prereq:* training, model.

**overfitting** (n) — A training failure in which loss decreases on training examples while the model's outputs worsen on new examples. The model stores example-specific details instead of a rule that carries over.
*Example:* "Overfitting began after day two, when held-out loss rose while training loss kept falling."
*! Do not:* use "memorization" as a bare synonym.
*Prereq:* training, loss, model.

**inference** (n) — Running a trained model on new inputs to get outputs without changing its parameters. This is the deployment phase; training is the search phase.
*Example:* "Inference on one document takes 200 milliseconds."
*! Do not:* use the statistics sense (drawing conclusions from data) or the everyday sense in the same document without renaming either; use as a synonym for "prediction".
*Prereq:* model, training.

**held-out examples** (n) — Examples set aside before training and never used to adjust parameters. They measure how a model behaves on data training did not use.
*Example:* "Section 4 reports results only from held-out examples."
*! Do not:* use bare "test set" / "validation set" until those are admitted with their distinct roles; use "unseen data" loosely.
*Prereq:* training, model.

---

## Reliability and platform chain

Order: service → service-level indicator → service-level objective → error budget. Domain tag `reliability/platform`.

**service** (n) — A running software unit that accepts requests through a defined interface and returns results or performs work for another unit or user.
*Example:* "The service accepts an HTTP request and returns the stored record."
*! Do not:* use as a synonym for any process, library, or team — state the unit's interface and responsibility.
*Prereq:* process, interface, client/server (assumed).
*Profiles:* `design-rfc`, `procedure`, `explanation`, `incident`, `technical-report`, `investigation-log`, `epic`, `task`, `subtask`.

**service-level indicator** (n) — A measured quantity describing one aspect of a service's behavior for its users, such as the fraction of successful requests.
*Example:* "The service-level indicator is the fraction of requests completed within 300 milliseconds."
*! Do not:* use "SLI" before admission; call an unmeasured intention an indicator.
*Prereq:* service; measurement, fraction, request (assumed).
*Profiles:* `design-rfc`, `incident`, `technical-report`, `investigation-log`, `epic`, `task`, `subtask`.

**service-level objective** (n) — A target range for a service-level indicator during a stated period.
*Example:* "The service-level objective requires at least 99.9% of requests to succeed in each 30-day period."
*! Do not:* use "SLO" before admission; present the target as an observed result.
*Prereq:* service-level indicator; range, period (assumed).
*Profiles:* `design-rfc`, `decision-record`, `incident`, `technical-report`, `epic`, `task`, `subtask`.

**error budget** (n) — The amount of unsuccessful or over-limit behavior a service-level objective permits during its stated period.
*Example:* "Failed requests consumed one quarter of the monthly error budget."
*! Do not:* use "budget" without naming the indicator, objective, and period. This is not a financial budget.
*Prereq:* service-level indicator, service-level objective.
*Profiles:* `design-rfc`, `decision-record`, `incident`, `technical-report`, `epic`, `task`, `subtask`.

---

## Security and governance chain

Order: asset → threat → control → residual risk. Domain tag `security/governance`.

**asset** (n) — Data, software, equipment, or a capability that an identified party needs to protect from loss, damage, disclosure, or unauthorized change.
*Example:* "The stored access records are assets because disclosure would expose user activity."
*! Do not:* call something an asset without identifying who values it and what harm protection addresses.
*Prereq:* data, software, access, change (assumed).
*Profiles:* all except `research-paper`, `maintenance-comment`.

**threat** (n) — A possible event or action that could harm an asset in a stated way under stated conditions.
*Example:* "Unauthorized copying is a threat because it would disclose the access records."
*! Do not:* use for a person or group without describing the possible harmful action and its conditions.
*Prereq:* asset; event, condition (assumed).
*Profiles:* all except `research-paper`, `maintenance-comment`.

**control** (n) — A technical or organizational measure intended to reduce the chance or effect of a stated threat to an asset.
*Example:* "Requiring two approvals is a control intended to reduce unauthorized configuration changes."
*! Do not:* claim a control eliminates risk unless the evidence supports elimination.
*Prereq:* asset, threat; measure, chance, effect (assumed).
*Profiles:* all except `research-paper`, `maintenance-comment`.

**residual risk** (n) — The stated chance and effect of harm from a threat after the selected controls are in place.
*Example:* "The residual risk is an estimated one mistaken disclosure per 10,000 approved exports, with one record disclosed per event."
*! Do not:* call risk "accepted" unless an identified decision owner has recorded that decision.
*Prereq:* threat, control.
*Profiles:* `design-rfc`, `decision-record`, `incident`, `technical-report`, `investigation-log`, `epic`, `task`, `subtask`.

---

## Adding an entry

Add a term only when a governed document needs it. Each candidate passes core §2.3 and §2.4: operational, no forward reference, built only from assumed vocabulary or earlier entries. Record ladder prerequisites, profiles, and domain tag. Adding an entry is a **minor** version change; changing a meaning may be **major** (core §9).
