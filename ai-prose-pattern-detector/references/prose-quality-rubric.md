# AI Prose-Pattern Detector Prose Quality Rubric

Use this rubric to identify visible prose patterns that make writing sound
machine-shaped, over-processed, or generic. Patterns are signals, not proof of
authorship.

## Quick Scan

Use these questions to identify meaningful flags. Apply the risk threshold and
severity scale from `detector-settings.md`.

1. Does it open with filler before naming the real point?
2. Does it rely on vague verbs such as utilize, leverage, enable, optimize, or
   facilitate?
3. Does it use decorative adjectives such as robust, seamless, innovative,
   comprehensive, or transformative without proof?
4. Does it repeat the same point in adjacent sentences?
5. Do most sentences have the same length and structure?
6. Is there no sign of a person making a judgment, choosing a tradeoff, or
   speaking from experience?
7. Does it hedge every claim even when the evidence supports a clear position?
8. Does formatting carry more weight than the content?
9. Does it use familiar AI collocations such as actionable insights, meaningful
   outcomes, deep dive, unlock, or game-changer?
10. Does it end with a generic closer that could fit almost any topic?

## Category 1 - Filler Openings And Autopilot Transitions

Common tokens:
Furthermore, Moreover, Additionally, In conclusion, In summary, Overall,
Ultimately, That being said, It is worth noting, With that in mind, Needless to
say, As mentioned earlier, Moving on, On the other hand.

Pattern:
- the sentence exists to announce structure instead of adding meaning
- every paragraph opens with a transition
- the last sentence restates the paragraph

Fix:
- remove the throat-clearing
- start with the claim, decision, or evidence
- use transitions only when the logical relationship would otherwise be unclear

## Category 2 - Lifeless Verbs And Decorative Adjectives

Vague verbs:
utilize, leverage, facilitate, streamline, optimize, empower, enable, enhance,
implement when build, add, run, test, or change would be clearer.

Decorative adjectives:
robust, seamless, cutting-edge, innovative, comprehensive, scalable,
state-of-the-art, best-in-class, dynamic, impactful, holistic, transformative,
next-generation, industry-leading.

Pattern:
- the sentence sounds positive but does not name what happened
- a general verb hides the concrete action
- adjectives imply proof the sentence does not provide

Fix:
- choose the real verb
- delete adjectives unless a metric, example, or constraint earns them
- name the actor and action

## Category 3 - Empty Generalization

Common openings:
In today's landscape, With the rise of, In the modern era, When it comes to,
Across industries, It is important to note that.

Common padding:
plays a crucial role, has become increasingly important, offers numerous
benefits, cannot be overstated, serves as a foundation for, helps teams make
informed decisions.

Pattern:
- grammatically correct but informationally thin
- could appear in almost any article on the topic
- avoids the specific problem, audience, or tradeoff

Fix:
- replace the general claim with the specific situation
- use a concrete example
- delete the sentence if it only warms up the reader

## Category 4 - Formulaic Contrast

Common forms:
- "It is not X, it is Y."
- "This is not about X; it is about Y."
- "Not just X, but Y."
- "More than X, it is Y."

Why it matters:
Contrast is a useful project-management and scope-setting move. It becomes a
tell when it appears repeatedly or when the second half merely sounds bigger
than the first half.

Pattern:
- false opposition between two ideas that can both be true
- abstract escalation: tool -> operating model, process -> culture, task ->
  transformation
- repeated use in the same piece

Fix:
- state the positive point directly
- name the actual scope boundary
- use "the practical distinction is..." when a contrast is truly needed
- replace the slogan with an example

## Category 5 - Condensed Expert Prose

Signals:
- five or more comma-separated capabilities, methods, outcomes, or risks
- long noun stacks: portfolio governance decision cadence operating model
  alignment
- slash-heavy labels: strategy/ops/governance/reporting/cadence
- one sentence carries too many ideas

Pattern:
- the prose sounds knowledgeable but cramped
- readers must unpack the sentence before they can use it
- action disappears behind categories

Fix:
- split the sentence
- choose the primary claim
- name who does what
- turn secondary ideas into a second sentence or remove them

## Category 6 - Synthetic Rhythm

Signals:
- sentences cluster around the same length
- every paragraph has the same number of sentences
- lists have perfect parallel structure even when the ideas do not need it
- the tone never shifts

Pattern:
- the draft sounds polished but airless
- nothing feels discovered, chosen, or emphasized

Fix:
- vary sentence length
- let one sentence be blunt
- combine or split paragraphs based on meaning
- remove unnecessary parallelism

## Category 7 - Redundancy And Over-Explanation

Common bridges:
In other words, Put simply, Simply put, What this means is, This means that,
This helps ensure, This is important because, which in turn.

Pattern:
- one idea appears three ways
- the final sentence summarizes what was already clear
- obvious implications are spelled out

Fix:
- keep the strongest version
- delete the echo
- add new information or stop

## Category 8 - Mechanical Objectivity

Signals:
- every claim is hedged
- tradeoffs are balanced when the evidence supports a choice
- passive voice hides the decision-maker
- no sentence shows experience, preference, or judgment

Pattern:
- the prose refuses to commit
- it sounds safe but not useful

Fix:
- commit when the evidence supports it
- name the tradeoff
- say what you would do and why

## Category 9 - Tell-Tale Formatting

Signals:
- bold keyword plus colon on every bullet
- nested headings for tiny sections
- tables for two or three simple items
- every section has the same shape

Pattern:
- formatting creates the illusion of structure
- the page looks organized before the thinking is clear

Fix:
- use paragraphs for connected thought
- keep bullets for scan-worthy lists
- remove decorative bolding
- let section structure follow the content

## Category 10 - Lexical Tells

Frequent phrases:
actionable insights, meaningful outcomes, deep dive, unlock, game-changer,
North Star, pain points, paradigm shift, tapestry, testament to, at its core,
delve into, foster a culture of, drive alignment, robust and scalable,
seamless integration.

Pattern:
- familiar phrase does the work of a fresh observation
- the reader recognizes the sentence before finishing it

Fix:
- replace with a specific claim
- use plain words
- name the object, action, and consequence

## Scoring

Use the severity scale in `detector-settings.md`. The rubric identifies which
patterns fired; the settings file controls how many flags become Low, Medium, or
High risk.
