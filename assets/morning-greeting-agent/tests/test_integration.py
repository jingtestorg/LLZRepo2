"""Integration test for the Morning Greeting Agent end-to-end flow."""
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
sys.path.insert(0, "/tmp/packages")

# Set IBD_TESTING before any agent imports
os.environ.setdefault("IBD_TESTING", "true")


@pytest.mark.asyncio
async def test_agent_invoke_returns_greeting():
    """Full end-to-end: invoke the agent and assert it returns a greeting string."""
    # Mock the LLM to return a canned response
    canned_response = "Good morning! Today is a beautiful day to be productive."

    # Build a fake LangGraph result
    fake_message = MagicMock()
    fake_message.content = canned_response
    fake_result = {"messages": [fake_message]}

    with patch("agent.SampleAgent._invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = fake_result

        from agent import SampleAgent
        agent = SampleAgent()

        response = await agent.invoke(
            query="Good morning! Please send a greeting to the user.",
            context_id="test-context-001",
        )

    assert response.status == "completed"
    assert isinstance(response.message, str)
    assert len(response.message) > 0
    assert response.message == canned_response


@pytest.mark.asyncio
async def test_agent_invoke_uses_fallback_on_empty_llm_response():
    """When LLM returns empty content, agent should use the static fallback."""
    fake_message = MagicMock()
    fake_message.content = ""
    fake_result = {"messages": [fake_message]}

    with patch("agent.SampleAgent._invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = fake_result

        from agent import SampleAgent
        agent = SampleAgent()

        response = await agent.invoke(
            query="Good morning! Please send a greeting to the user.",
            context_id="test-context-002",
        )

    assert response.status == "completed"
    assert "Good morning" in response.message


@pytest.mark.asyncio
async def test_agent_stream_yields_processing_then_result():
    """stream() must yield a 'Processing...' chunk first, then the final result."""
    canned_response = "Rise and shine! Have an amazing day."
    fake_message = MagicMock()
    fake_message.content = canned_response
    fake_result = {"messages": [fake_message]}

    with patch("agent.SampleAgent._invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = fake_result

        from agent import SampleAgent
        agent = SampleAgent()

        chunks = []
        async for chunk in agent.stream(
            query="Good morning! Please send a greeting to the user.",
            context_id="test-context-003",
        ):
            chunks.append(chunk)

    assert len(chunks) >= 2
    assert chunks[0]["is_task_complete"] is False
    assert chunks[0]["content"] == "Processing..."
    final = chunks[-1]
    assert final["is_task_complete"] is True
    assert final["content"] == canned_response


@pytest.mark.asyncio
async def test_agent_handles_exception_gracefully():
    """When _invoke_with_fallback raises, stream() must yield an error response."""
    with patch("agent.SampleAgent._invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.side_effect = RuntimeError("AI Core unavailable")

        from agent import SampleAgent
        agent = SampleAgent()

        chunks = []
        async for chunk in agent.stream(
            query="Good morning!",
            context_id="test-context-004",
        ):
            chunks.append(chunk)

    final = chunks[-1]
    assert final["is_task_complete"] is True
    assert "error" in final["content"].lower() or "encountered" in final["content"].lower()
