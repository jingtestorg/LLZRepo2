# Morning Greeting Agent

AI agent that greets users every morning at 8:00 AM.

## Business challenge

Employees lack a consistent, automated daily touchpoint at the start of their workday. A scheduled AI agent should send a friendly "hello" greeting to users every morning at 8:00 AM to foster engagement and prompt a productive start to the day.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| On-time start-of-day productivity | — | Measurable improvement in daily task start times | — | Employee daily workflow | user |
| Daily morale / positive work culture | — | Positive sentiment from daily greeting interaction | — | Employee experience management | user |

## Key Milestones

1. **Agent scheduled** — Agent is configured and running on a daily 8:00 AM schedule.
2. **Greeting delivered** — Agent successfully sends a hello message to the target user(s) each morning.
3. **Personalization active** — Agent addresses users by name or with context-aware content.
4. **Delivery confirmed** — System confirms message delivery with no failures.

## Business Architecture (RBA)

### End-to-End Process

Recruit to Retire for Internal Workforce

### Process Hierarchy

```
Recruit to Retire for Internal Workforce (E2E)
└── Manage Workforce (internal workforce)
    └── Manage employee experience (internal workforce) (BPS-392_001)
        └── Enrich employee experience
```

### Summary

Automated daily morning greetings map to the "Manage employee experience" sub-process in the Recruit to Retire E2E, enriching employee experience through regular, automated morning communications.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
| ---------------------- | ----------------------- | ---------- | ----------------- | ------------------ | ------------------ | ------------------- | ---- | ------------------- |
| Schedule daily 8:00 AM greeting | — | — | — | — | — | — | Yes | No standard SAP API for scheduled personal greetings; custom agent required |
| Deliver greeting message to user | SAP SuccessFactors Work Zone (SC4289) | — | — | — | — | — | Maybe | Work Zone supports employee communications; custom agent can deliver via chat/notification |
| Personalized greeting content | — | — | — | — | — | — | Yes | AI agent generates personalized greeting using LLM |

### Key findings
- No standard SAP API or MCP server directly supports a scheduled daily greeting agent.
- SAP SuccessFactors Work Zone covers workforce engagement but does not provide a scheduling + greeting API.
- A custom Python AI agent with a built-in scheduler (e.g., APScheduler or cron trigger) is the recommended approach.
- The agent will use LLM capabilities to generate friendly, personalized morning greetings.
- This is a fully custom solution with no reusable standard SAP asset for the core scheduling + greeting function.

## Recommendations

### Morning Greeting AI Agent

#### Executive Summary

Custom Python AI agent with daily 8AM scheduler for user greetings.

#### Recommended Solution

A pro-code Python AI agent (A2A protocol) that runs on a daily schedule at 8:00 AM. The agent uses an internal scheduler to trigger at the configured time and sends a personalized "hello" greeting to users. The greeting content is generated using an LLM to keep it friendly and varied each day.

#### Recommended solution category

AI Agent

#### Intent fit
85%
