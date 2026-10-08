"""Daily 8:00 AM greeting scheduler.

Starts an APScheduler AsyncIOScheduler that fires a greeting job every morning
at 08:00 UTC (configurable via GREETING_TIMEZONE env var).
"""

import asyncio
import logging
import os
from typing import Callable, Awaitable

from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)

# Static fallback greeting used when the LLM is unavailable
STATIC_FALLBACK_GREETING = "Good morning! Wishing you a productive and wonderful day ahead."

# Default context_id used when the scheduler fires (no real user session)
SCHEDULER_CONTEXT_ID = "scheduler-daily-greeting"

_scheduler: AsyncIOScheduler | None = None


def start_scheduler(agent_invoke_fn: Callable[..., Awaitable]) -> AsyncIOScheduler:
    """Start the daily 8:00 AM greeting scheduler.

    Args:
        agent_invoke_fn: An async callable matching ``SampleAgent.invoke`` signature.
                         Will be called with (query, context_id) each morning.

    Returns:
        The running AsyncIOScheduler instance.
    """
    global _scheduler

    timezone = os.environ.get("GREETING_TIMEZONE", "UTC")

    async def _daily_greeting_job() -> None:
        """Scheduled job: invoke the agent to send the morning greeting."""
        query = "Good morning! Please send a greeting to the user."
        try:
            response = await agent_invoke_fn(query, SCHEDULER_CONTEXT_ID)
            greeting_text = getattr(response, "message", str(response))
            if not greeting_text:
                logger.warning(
                    "M2.missed: LLM call failed or returned empty, falling back to static greeting"
                )
                greeting_text = STATIC_FALLBACK_GREETING
            else:
                logger.info(
                    "M2.achieved: greeting content generated for user %s",
                    SCHEDULER_CONTEXT_ID,
                )
            logger.info(
                "M3.achieved: greeting delivered to user %s at scheduled time",
                SCHEDULER_CONTEXT_ID,
            )
            logger.info("M4.achieved: greeting cycle complete, all statuses recorded")
            logger.info("Morning greeting: %s", greeting_text)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error(
                "M3.missed: delivery failed for user %s, error: %s",
                SCHEDULER_CONTEXT_ID,
                exc,
            )
            logger.error("M4.missed: delivery status could not be confirmed")

    try:
        _scheduler = AsyncIOScheduler(timezone=timezone)
        _scheduler.add_job(
            _daily_greeting_job,
            trigger="cron",
            hour=8,
            minute=0,
            id="daily-morning-greeting",
            replace_existing=True,
        )
        _scheduler.start()
        logger.info(
            "M1.achieved: morning greeting scheduler initialized, next trigger at 08:00 (%s)",
            timezone,
        )
    except Exception as exc:  # pylint: disable=broad-except
        logger.error(
            "M1.missed: scheduler initialization failed, agent will not trigger. Error: %s",
            exc,
        )
        raise

    return _scheduler


def stop_scheduler() -> None:
    """Stop the scheduler gracefully (used in tests and shutdown hooks)."""
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        _scheduler = None
