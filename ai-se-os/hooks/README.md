# AI-SE OS Hooks

This directory documents hook points that AI agents and future runtime adapters can use to auto-load AI-SE OS.

The current implementation is documentation-first:

- root instruction shims tell common AI coding tools to boot from `.ai_os`
- `.ai_os/docs/40_AGENT_DISCOVERY_AND_HOOKS.md` defines the canonical trigger contract
- future Level 4 runtimes may add executable hook adapters here

No file in this directory should perform privileged actions without the policy enforcement rules in `../docs/25_POLICY_ENFORCEMENT.md`.

