---
title: "I stopped using AI chat to build software. I built an engineering team instead."
published: true
tags: ai, softwareengineering, opensource, productivity
---

Most AI coding tools have one structural flaw: the same model writes the code and then announces it's done.

The writer is the judge. Ask it to "verify your work" and it summarizes its own output back to you. That's not verification — that's a closed loop.

So I built something different: a portable, multi-agent AI coding team that lives in a single folder, separates the builder from the judge, and ships with an experience memory that compounds over time. It's open source. Let me walk you through the parts that actually work.

## 1. Implementation and acceptance are different jobs

In my setup, no agent gets to declare a task complete.

The implementer (AgentB or AgentD) produces **evidence**: tests it ran, endpoints it probed, a browser it walked, screenshots it captured. A separate role — the orchestrator (AgentA) — reviews that evidence and runs its own deterministic checks (compile, unit tests, exit codes, file existence).

No evidence, no delivery.

Real proof this works: during a six-phase industrial energy-monitoring build, the *visual-acceptance* agent — a completely separate vision model running out-of-band from the main conversation — caught a silent bug that the coding agent had shipped and been proud of.

The bug: a ranking chart rendered inside a `v-if`-controlled container. Switch the analysis period → Vue tears down the DOM node → chart goes blank and never recovers. The coding agent had tested that the chart *appeared* and called it done. The visual agent walked the actual rendered pages across three breakpoints, saw the blank chart, named the root cause, and proposed the fix.

The agent that wrote the code never would have caught its own omission. Independent acceptance caught a first-class bug. That's the business case on one slide.

## 2. Work orders, not chat history

The single biggest token waste in multi-agent setups is forwarding the entire conversation to a sub-agent. I don't do that.

When the orchestrator dispatches work, the sub-agent receives only:

- the work-order path
- the project path
- explicit scope of files it may modify
- the list of files it actually needs
- acceptance conditions

No conversation history. The sub-agent reads the order, does the work, and returns only: files changed, test results, residual risks. Never the full code, never a chat recap.

This isn't a micro-optimization — it's what makes parallelism safe. Two agents working in the same repo never step on each other's context, and the token bill stays flat no matter how long the human conversation gets.

## 3. Model routing: the anti-lock-in design

I don't assume one model. Every task routes to the model that fits it, from a pool you own. Here's my current table:

| Job | Model | Why |
|---|---|---|
| Everyday coding | cheap, fast | Low cost, high volume |
| Architecture / critical logic | strong | Worth the premium on the hard 20% |
| Bulk reading / log triage | cheap, fast | Pure grunt work |
| Visual / screenshot acceptance | vision model | Steady image reading |
| Parallel second implementer | *different* model than the first | Two identical models make the same mistake twice |

That last row is the one people miss. When two agents work in parallel, I deliberately give them **different models** — two identical models given the same ambiguous task will confidently produce the same wrong answer. A differently-brained implementer is a real cross-check.

Because the routing table is just a file, the two biggest buyer fears disappear:

- **Price changes?** Edit one line. Not locked to a vendor's pricing.
- **Switch IDEs?** Swap the adapter. The team, rules, memory, and acceptance discipline travel with it.

I currently run across five platforms (Codex, Google Antigravity, TraeCode, Claude Code, WorkBuddy) from the same folder. Two of them are marked "not officially verified" on purpose — I'd rather tell you what I haven't proven than let you assume I have.

## 4. Failure is a first-class citizen

Every "robust AI system" writeup assumes the models behave. Mine don't. Three rules keep it honest:

1. **Probe once, then decide.** Not "retry three times and hang."
2. **A failed external call is not a result.** Fall back to the built-in model; the orchestrator must re-decide.
3. **Three strikes, stop and ask.** Two failures → swap model or role. Three failures → stop dispatching, report to human.

And one honesty rule: when a platform lacks true sub-agent isolation, the team says *"sequential fallback: role simulation"* out loud, in the work order and the final answer. If AgentB didn't actually deliver, the report does not say "AgentB complete."

## 5. The memory that compounds

The deepest difference between "a tool that calls an API" and "a team" is this: **the team gets better the longer you use it.**

After every accepted task, the orchestrator checks whether anything new and *stable* happened:

- New user preference? → `user-preferences.md`
- New pitfall or reusable debugging path? → `defect-patterns.md` / `effective-solutions.md`
- Confirmed architecture decision? → `technical-decisions.md`
- Milestone? → `project-history.md`

If all four are no, nothing is written. Only stable, reusable conclusions. Each entry targets under 300 chars, each category capped at 40 entries / 8,000 chars. When a cap is hit, the original stays untouched — new conclusions overflow into a dated attachment file, never deleted or compressed to make room. Preserving memory faithfully beats keeping it tidy.

After one month, the team knows your routing preferences and UI conventions. After three months, it knows your defect patterns and data-modeling decisions. After a year, it's the equivalent of an engineer who has actually worked on your system — and that knowledge travels with the folder.

## What this is not

- Not a chatbot with extra steps.
- Not a claim that any one model is best. It's a routing *policy*.
- Not verified on every platform. Two of five are unverified.
- Not a magic cost saver. It's a discipline that keeps context bounded.

## Try it

Everything above is open source, standard-library-only Python, no third-party deps:

**[davececec/Portable-AI-Team](https://github.com/davececec/Portable-AI-Team)**

The routing table, work-order templates, and acceptance rules live in `AI-Team/policies/` and `AI-Team/templates/`. The full methodology write-up is in the repo under `docs/articles/`.

If you take one thing from this post: **make the builder and the judge different roles, and require evidence before acceptance.** Everything else is optimization on top of that.
