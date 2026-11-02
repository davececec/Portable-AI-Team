# How We Run an AI Engineering Team

*Not another AI coding assistant. A playbook for treating AI agents like a real engineering team — with work orders, independent acceptance, model routing, and a memory that compounds. Built on and shipped with [Portable AI Team](../../README.md), an open-source, single-folder multi-agent framework.*

---

Most AI coding tools share one structural flaw: the same model writes the code and then announces, on its own authority, that it is done. The writer is also the judge. Ask ten tools to "verify your work" and nine will summarize their own output back to you and call it verification.

That is not engineering. Engineering separates the person who builds from the person who signs off. So we built a team around that single idea, and then spent a couple of months running it on a real industrial project to see what actually holds up. This is what we learned.

## The one rule that changes everything: implementation and acceptance are different jobs

In our setup, no agent gets to declare a task complete. The agent that wrote the code (AgentB, or its parallel counterpart AgentD) produces *evidence*: tests it ran, endpoints it probed, a browser it walked, screenshots it captured. A separate role — AgentA, the orchestrator — reviews that evidence and runs its own deterministic checks (compile, unit tests, exit codes, file existence) before anything is marked delivered.

No evidence, no delivery. The writer and the judge are different minds, sometimes different models. This is the one design decision I would defend hardest, because it is the one that is easiest for a human to understand and the one the market most rarely sees.

A concrete proof point: during a six-phase energy-monitoring build, the visual-acceptance agent (a separate vision model, running out-of-band from the main conversation) caught a real, silent bug that the coding agent had shipped and been proud of.

**The bug:** a ranking chart rendered inside a `v-if`-controlled container. When the user switched the analysis period, Vue tore down the DOM node. The chart was gone — not re-rendered, not recovered, just blank. The coding agent had written the chart, tested that it *appeared* initially, and reported success. The visual agent, walking the actual rendered pages across three breakpoints, saw the blank chart after a period switch, named the root cause (the `v-if` unmount), and proposed the fix. We added a DOM-consistency check in the chart composable and re-verified across seven scenarios with zero console errors.

The point is not "vision models are great." The point is that *the agent that wrote the code never would have caught its own omission*, because it was not looking at the rendered result the way a user would. Independent acceptance caught a first-class bug. That is the whole business case on one slide.

## Work orders, not chat history

The second decision is about context. The single biggest token waste in multi-agent setups is forwarding the entire conversation to a sub-agent. We don't do that.

When AgentA dispatches work to AgentB or AgentD, the sub-agent receives only:

- the work-order path
- the project path
- the explicit scope of files it may modify
- the list of files it actually needs
- the acceptance conditions

That's it. No conversation history, no "here's everything we discussed so far." The work order is a compact, structured file (a micro template for tiny tasks, a standard template for real ones). The sub-agent reads it, does the work, and returns only: the files it changed, the test results, and the residual risks. Never the full code, never a recap of the chat.

This sounds like a micro-optimization. It isn't. It is what makes parallelism safe: two agents working in the same repo never step on each other's context, and the token bill stays flat no matter how long the human conversation gets.

## Model routing: the anti-lock-in design

Here is the part that matters most to anyone who buys software. We do **not** assume one model. Every task is routed to the model that fits it, from a configurable pool, and the routing table is a file you own.

Our current routing table, distilled from weeks of real runs:

| Job | Model we route to | Why |
|---|---|---|
| Everyday execution / coding | cheap, fast model | Low cost, high volume |
| Architecture, critical business logic, risky migrations | strong model | Worth the premium on the hard 20% |
| Bulk reading / log triage / big file scans | cheap fast model | Pure grunt work, short sessions |
| Visual / screenshot / chart acceptance | a dedicated vision model | Steady image reading, few false alarms |
| Parallel second implementer | a *different* model than the first | Two identical models tend to make the same mistake twice |

The last row is the one people miss. When two agents work in parallel, we deliberately give them **different models**, because two identical models given the same ambiguous task will confidently produce the same wrong answer. A second, differently-brained implementer is a real cross-check.

And because the routing table is just a file, the two biggest buyer fears disappear:

- **A model price changes?** Edit one line in the table. You are not locked to a vendor's pricing.
- **You want to switch IDEs or hosts?** Swap the adapter. The team, its rules, its memory, and its acceptance discipline travel with it.

We currently run across five platforms — Codex, Google Antigravity, TraeCode, Claude Code, and WorkBuddy — from the same folder. The two newest are marked "not officially verified" in the docs, on purpose. We would rather tell you what we have not proven than let you assume we have.

## Failure is a first-class citizen

Every "robust AI system" writeup quietly assumes the models behave. Ours do not, and we stopped pretending they would. The discipline lives in three rules:

1. **Probe once, then decide.** Before the first dispatch we probe external model availability once. If a channel fails with a known protocol error, we classify it as an environment limit and degrade gracefully — we do not blindly retry three times and hang, which is exactly what a naive implementation does.

2. **A failed external call is not a result.** If an external API times out or errors, the result is marked failed and we fall back to the built-in model. Crucially, the orchestrator must *re-decide*. It is not allowed to treat the external model's partial reply as acceptance.

3. **Three strikes, stop and ask.** The same task failing twice may trigger a model or role swap. Failing three times, the orchestrator stops dispatching entirely and reports the blockage to a human with options. No infinite retry loops, no silent degradation.

There is a parallel rule for honesty: when a platform lacks true sub-agent isolation, the team says *"sequential fallback: role simulation"* out loud, in the work order and the final answer. It lists which roles ran on which models, whether context isolation was real or simulated, and what was left unverified. If AgentB did not actually deliver, the report does not say "AgentB complete."

This is the part that builds trust. A team is most credible not at its best moment but at its worst: what it tried, what failed, how it found out, and what it changed. We keep the failures in the changelog on purpose.

## The compounding asset: a memory that appreciates

The deepest difference between "a tool that calls an API" and "a team" is this: **the team gets better the longer you use it, and the tool does not.**

After every accepted task, the orchestrator checks — without a dedicated model call — whether anything new and *stable* happened:

- A new user preference? → `user-preferences.md`
- A new pitfall or a reusable debugging path? → `defect-patterns.md` / `effective-solutions.md`
- A confirmed architecture or data-semantics decision? → `technical-decisions.md`
- A milestone? → `project-history.md`

If the answer to all four is no, nothing is written. We do not bloat the memory with project summaries, business source, secrets, or raw logs — only stable, reusable conclusions, each targeting under 300 characters, each category capped at 40 entries / 8,000 characters. When a cap is reached, we never delete or rewrite old memories to make space: the original stays verbatim, and new conclusions overflow into a dated attachment file (`memory/attachments/YYYY-MM-DD-topic.md`) with a lightweight pointer added to the index. If we are not sure whether something is a duplicate or how to categorize it, we keep the original and mark it for review. Preserving memory faithfully matters more than keeping it tidy.

The practical consequence: after one month, the team has your routing preferences and your UI conventions. After three months, it has your defect patterns and your data-modeling decisions. After a year, it has accumulated the equivalent of an engineer who has actually worked on your system — and that knowledge *travels with the folder* when you move to a new project. A raw API call has no such curve. This is the "compounding" we put on the cover of the deck, and it is the reason the honest comparison is "use it for three months versus three years."

We ship a desensitized snapshot of this seed memory so a new install starts with prior art instead of a blank slate — but it is never auto-merged into your live memory, so it can't pollute your project.

## What this is not

Let's be precise about scope, because the vague kind of this category is full of vaporware:

- It is **not** a chatbot with extra steps. It is a set of roles, files, and discipline.
- It is **not** a claim that any specific model is the best. It is a routing *policy* over whichever models you already have.
- It is **not** verified to work flawlessly on every platform. Two of our five adapters are explicitly marked unverified.
- It is **not** a magic cost saver. It is a *discipline* that keeps context and retries bounded, which is what makes the token bill predictable.

## The part we are open-sourcing first

We believe the methodology — the work-order structure, the acceptance rules, the routing table, the degradation discipline — is the part of this with the widest value, and it is platform-agnostic. So that is what is open. The framework, the adapters, the policies, the templates, and the doctor self-check are all in the repo and run on a standard-library-only Python install with no third-party dependencies.

The memory itself — your specific accumulated experience — is yours. It stays in your folder, it is git-ignored, and it never ships to a third party. You can carry the team into any project with one double-click, merge two teams' experience into one, and take it away again when you are done.

If you run AI agents in production, the single most useful thing you can steal from this post is the first section: **make the builder and the judge different roles, and require evidence before acceptance.** Everything else is optimization on top of that.

The code is at [davececec/Portable-AI-Team](https://github.com/davececec/Portable-AI-Team). The full routing table, the work-order templates, and the acceptance rules are in `AI-Team/policies/` and `AI-Team/templates/` — read them before you read this post again.
