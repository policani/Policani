# AI Prose-Pattern Detector Settings

This is the single customization file for AI Prose-Pattern Detector. Change
behavior here, not inside `AGENTS.md` or the rubric.

## Product Stance

AI Prose-Pattern Detector reviews prose patterns associated with AI-likeness. It
does not decide whether a person or model wrote the text. Its job is to help a
capable writer keep judgment, specificity, and voice while removing generic
AI-shaped habits.

## Default Behavior

- Default mode: Flag Check
- Default audience: professional generalist
- Default rewrite strength: medium
- Default risk threshold: 3 or more meaningful flags means the text should be
  revised before external use.
- Default tone goal: clear, grounded, specific, and human without becoming
  casual filler.

## Rewrite Strength

Light:
- Remove obvious filler and repeated tells.
- Keep structure mostly intact.
- Use when the text is already strong or politically sensitive.

Medium:
- Tighten rhythm, replace vague phrasing, split over-condensed sentences, and
  vary paragraph shape.
- Use for most professional writing.

Heavy:
- Rebuild the passage around the real point, audience, and proof.
- Use when the text is generic, over-polished, or structurally wrong.

## Protected Content

Preserve these unless the user explicitly asks to change them:

- names, dates, titles, company names, and product names
- numbers, metrics, legal terms, compliance language, and quoted text
- links, citations, code blocks, command examples, and Markdown tables
- deliberate terminology that belongs to the user's field
- claims that would require fact-checking before changing

## Priority Signals

Treat these as high-priority detector signals:

- filler openings that delay the point
- decorative adjectives and lifeless verbs
- repeated "not X, it is Y" or "not just X but also Y" contrast framing
- comma-heavy capability stacks with five or more compressed ideas
- noun chains that hide the actor, action, or decision
- uniform sentence rhythm across a paragraph
- generic closers that restate the obvious
- formatting symmetry that makes a draft feel machine-shaped

## Condensed Prose Thresholds

Flag a sentence when one or more are true:

- it contains five or more comma-separated capabilities, methods, or outcomes
- it chains four or more abstract nouns without a concrete actor or verb
- it uses multiple slash pairs or stacked compound labels to avoid choosing
  clearer words
- it asks one sentence to carry strategy, execution, governance, risk, and
  impact at the same time

When fixing condensed prose, do not simply shorten it. Split the sentence, name
the actor, choose the main claim, and move secondary detail into a follow-up
sentence or remove it.

## Contrast Phrase Policy

Scope-setting contrast can be useful. Do not ban it outright. Flag it when:

- "not X, it is Y" appears more than once in a piece
- the contrast is decorative rather than clarifying
- the second half merely upgrades the first half with a bigger abstraction
- the sentence sounds like positioning copy instead of a human explanation

Preferred fixes:

- state the positive claim directly
- use "the better distinction is..."
- use "the practical question is..."
- split scope from rationale
- replace false contrast with a concrete example

## Output Preferences

Flag Check:
- concise bullets
- exact excerpts
- one priority fix

Audit:
- ranked findings
- representative examples for repeated issues
- rewrite suggestion for each finding

Rewrite:
- revised text first
- optional short note after the rewrite

Produce:
- final prose only
- no rule narration unless requested

## Severity Scale

Low:
- 0-2 minor flags
- the text has a clear point and human judgment

Medium:
- 3-5 flags or one repeated pattern
- the text is usable but should be revised

High:
- 6 or more flags, heavy generic phrasing, or dense compression that obscures
  meaning
- revise before external use
