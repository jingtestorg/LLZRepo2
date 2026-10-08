"""Unit tests for the Morning Greeting scheduler."""
import asyncio
import logging
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

# Ensure APScheduler is importable from /tmp/packages
sys.path.insert(0, "/tmp/packages")


def test_static_fallback_greeting_is_defined():
    """STATIC_FALLBACK_GREETING must be a non-empty string."""
    from scheduler import STATIC_FALLBACK_GREETING
    assert isinstance(STATIC_FALLBACK_GREETING, str)
    assert len(STATIC_FALLBACK_GREETING) > 0
    assert "Good morning" in STATIC_FALLBACK_GREETING


@pytest.mark.asyncio
async def test_start_scheduler_registers_daily_job():
    """start_scheduler() must register a job with id 'daily-morning-greeting'."""
    from scheduler import start_scheduler, stop_scheduler

    mock_invoke = AsyncMock(return_value=MagicMock(message="Good morning!"))
    scheduler = start_scheduler(mock_invoke)
    try:
        job = scheduler.get_job("daily-morning-greeting")
        assert job is not None
        assert job.id == "daily-morning-greeting"
    finally:
        stop_scheduler()


@pytest.mark.asyncio
async def test_start_scheduler_logs_m1_achieved(caplog):
    """start_scheduler() must emit M1.achieved log on success."""
    from scheduler import start_scheduler, stop_scheduler

    mock_invoke = AsyncMock(return_value=MagicMock(message="Good morning!"))
    with caplog.at_level(logging.INFO, logger="scheduler"):
        scheduler = start_scheduler(mock_invoke)
        stop_scheduler()

    assert any("M1.achieved" in r.message for r in caplog.records)


def test_start_scheduler_logs_m1_missed_on_error(caplog):
    """start_scheduler() must emit M1.missed log on failure."""
    from scheduler import start_scheduler

    mock_invoke = AsyncMock(return_value=MagicMock(message="Hello!"))
    # Patch APScheduler to raise on start
    with patch("scheduler.AsyncIOScheduler") as MockScheduler:
        mock_instance = MagicMock()
        mock_instance.start.side_effect = RuntimeError("scheduler init error")
        MockScheduler.return_value = mock_instance

        with caplog.at_level(logging.ERROR, logger="scheduler"):
            with pytest.raises(RuntimeError):
                start_scheduler(mock_invoke)

    assert any("M1.missed" in r.message for r in caplog.records)


@pytest.mark.asyncio
async def test_daily_greeting_job_logs_m2_achieved(caplog):
    """The daily job must log M2.achieved when the LLM returns a greeting."""
    from scheduler import start_scheduler, stop_scheduler

    mock_invoke = AsyncMock(return_value=MagicMock(message="Good morning, sunshine!"))
    scheduler = start_scheduler(mock_invoke)

    try:
        job = scheduler.get_job("daily-morning-greeting")
        assert job is not None
        # Run the job function directly
        with caplog.at_level(logging.INFO, logger="scheduler"):
            await job.func()
    finally:
        stop_scheduler()

    assert any("M2.achieved" in r.message for r in caplog.records)
    assert any("M3.achieved" in r.message for r in caplog.records)
    assert any("M4.achieved" in r.message for r in caplog.records)


@pytest.mark.asyncio
async def test_daily_greeting_job_falls_back_on_empty_response(caplog):
    """The daily job must use the static fallback when LLM returns empty."""
    from scheduler import start_scheduler, stop_scheduler

    mock_invoke = AsyncMock(return_value=MagicMock(message=""))
    scheduler = start_scheduler(mock_invoke)

    try:
        job = scheduler.get_job("daily-morning-greeting")
        with caplog.at_level(logging.WARNING, logger="scheduler"):
            await job.func()
    finally:
        stop_scheduler()

    all_messages = " ".join(r.message for r in caplog.records)
    assert "M2.missed" in all_messages


@pytest.mark.asyncio
async def test_daily_greeting_job_logs_m3_missed_on_error(caplog):
    """The daily job must log M3.missed when the invoke call raises."""
    from scheduler import start_scheduler, stop_scheduler

    mock_invoke = AsyncMock(side_effect=RuntimeError("LLM unavailable"))
    scheduler = start_scheduler(mock_invoke)

    try:
        job = scheduler.get_job("daily-morning-greeting")
        with caplog.at_level(logging.ERROR, logger="scheduler"):
            await job.func()
    finally:
        stop_scheduler()

    assert any("M3.missed" in r.message for r in caplog.records)
    assert any("M4.missed" in r.message for r in caplog.records)
