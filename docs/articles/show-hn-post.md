# Show HN: Portable AI Team — a multi-agent coding team in a single folder

*(This is the launch comment to post as the first reply when you submit the repo. Keep it under ~400 words; HN penalizes self-promo that reads like marketing.)*

---

Hi HN — I built a portable multi-agent AI coding team that lives in a single folder and treats AI agents like a real engineering team: separate roles, work orders instead of chat history, and independent acceptance.

The core idea is simple: **the agent that writes the code is not the agent that decides it's done.**

In my setup, the implementer produces evidence (tests run, endpoints probed, browser walked, screenshots captured) and a separate orchestrator reviews that evidence plus deterministic checks (compile, exit codes, file existence) before marking delivery. No evidence, no delivery.

Why this matters — a real example from a six-phase industrial energy-monitoring build:

The coding agent shipped a ranking chart and reported success. The chart was rendered inside a `v-if`-controlled container; when the user switched the analysis period, Vue tore down the DOM node and the chart went blank, unrecoverable. The coding agent had only verified the chart *appeared*. A separate vision-model agent, walking the actual rendered pages out-of-band from the main conversation, caught the bug, identified the root cause, and proposed the fix.

The writer never would have caught its own omission.

Other things the framework does:

- **Work orders, not chat history.** Sub-agents receive only the order path, project path, allowed file scope, needed files, and acceptance conditions. Token bill stays flat no matter how long the conversation gets.
- **Model routing as a config file.** Every task routes to the model that fits it. Two parallel implementers deliberately get *different* models, because identical models make the same mistake twice.
- **Failure discipline.** Probe once, not blind retries. A failed external call is not a result. Three consecutive failures → stop and ask a human.
- **A memory that compounds.** Stable conclusions accumulate per-category (defect patterns, technical decisions, user preferences) with caps that overflow into dated attachment files rather than deleting old memories, and travel with the folder.

It runs on standard-library-only Python (no third-party deps), currently supports five platforms (Codex, Google Antigravity, TraeCode, Claude Code, WorkBuddy — the last two explicitly marked unverified), and is open source:

https://github.com/davececec/Portable-AI-Team

The full methodology write-up (with the ECharts bug story) is in the repo under `docs/articles/how-we-run-an-ai-engineering-team.md`.

Happy to answer questions about the acceptance rules, the routing table, or what didn't work.
