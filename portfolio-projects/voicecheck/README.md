# VoiceCheck

VoiceCheck is an agent-readable prose QA toolkit for finding writing that
sounds generic, over-processed, or AI-shaped.

It is not an AI detector. It does not claim to identify who wrote a draft.
Instead, it gives writers a practical review system for visible prose patterns:
filler openings, lifeless verbs, decorative adjectives, formulaic contrast,
condensed expert prose, mechanical rhythm, generic closers, and formatting that
looks more organized than the thinking underneath it.

## What It Does

- Runs quick flag checks on pasted prose.
- Produces detailed audits with exact excerpts and rewrite suggestions.
- Rewrites text while preserving the user's facts, claims, and domain detail.
- Helps agents produce prose that sounds clear, specific, and human without
  becoming casual or vague.
- Centralizes customization in one settings file.

## Why It Exists

AI-assisted writing often fails in two opposite ways. Some drafts become generic
and padded. Others become compressed expert prose: long noun chains,
comma-packed capability catalogs, and scope-setting phrases that sound sharp
once but robotic after repeated use.

VoiceCheck treats both as quality problems. The goal is not to make every piece
sound informal. The goal is to preserve judgment, specificity, and voice.

## Package Structure

```text
VoiceCheck/
  AGENTS.md
  README.md
  voicecheck-settings.md
  references/
    prose-quality-rubric.md
  examples/
    sample-input.md
    sample-audit.md
    sample-rewrite.md
```

## Quick Start

Use the folder as an agent project or copy its contents into a supported AI
workspace.

1. Put `AGENTS.md`, `voicecheck-settings.md`, and `references/` in the project.
2. Paste prose into the agent chat.
3. Ask for one of the supported modes:
   - `/voicecheck`
   - `flag check`
   - `audit this`
   - `rewrite using VoiceCheck`
   - `produce this in a natural voice`

Examples are optional. They show the intended output style but are not required
for normal use.

## Modes

Flag Check:
Returns risk level, flag count, categories fired, exact excerpts, and one
priority fix.

Audit:
Ranks findings by severity and gives suggested rewrites for each issue.

Rewrite:
Returns revised prose first, preserving meaning and factual claims.

Produce:
Uses the rubric silently while drafting new prose.

## Customization

All behavior settings live in `voicecheck-settings.md`:

- default mode
- rewrite strength
- protected content
- condensed prose thresholds
- contrast phrase policy
- output preferences
- severity scale

The rubric file defines the pattern library. The agent guide tells the agent
when to load which files.

## Example Use

```text
/voicecheck

This is not just a reporting process, it is a comprehensive operating cadence
that leverages stakeholder alignment, governance, prioritization, visibility,
decision quality, and execution discipline to drive meaningful outcomes.
```

VoiceCheck should flag formulaic contrast, vague verbs, decorative abstraction,
and compressed comma-heavy prose. A better rewrite would name the practical
function of the process and split the crowded sentence.

## Responsible Use

VoiceCheck should not be used to accuse a writer of using AI. Many flagged
patterns also appear in human business writing, especially rushed executive
drafts, consulting prose, and technical documentation.

Use it as a writing quality gate: identify weak patterns, preserve the real
thinking, and improve the draft.

## Suggested GitHub Metadata

Repository description:

> Agent-readable prose QA toolkit for finding AI-shaped writing patterns and
> rewriting drafts into clearer, more specific human prose.

Suggested topics:

```text
writing
prose
ai-writing
prompt-engineering
editing
style-guide
agent-workflow
quality-assurance
portfolio-project
```
