"""Unit tests for the Morning Greeting Agent system prompt."""
import os
import sys

import pytest

# Make app importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))


def test_get_system_prompt_returns_non_empty_string():
    """get_system_prompt() must return a non-empty string."""
    from agent import get_system_prompt
    prompt = get_system_prompt()
    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_get_system_prompt_contains_greeting_role():
    """System prompt must describe the agent as a greeting agent."""
    from agent import get_system_prompt
    prompt = get_system_prompt()
    assert "Morning Greeting Agent" in prompt


def test_get_system_prompt_contains_personalization_instruction():
    """System prompt must instruct the agent to address user by name."""
    from agent import get_system_prompt
    prompt = get_system_prompt()
    assert "name" in prompt.lower()


def test_get_system_prompt_contains_variety_instruction():
    """System prompt must instruct the agent to vary the greeting."""
    from agent import get_system_prompt
    prompt = get_system_prompt()
    assert "vary" in prompt.lower() or "different" in prompt.lower()


def test_get_system_prompt_contains_length_constraint():
    """System prompt must specify a short greeting (1-3 sentences)."""
    from agent import get_system_prompt
    prompt = get_system_prompt()
    assert "1-3 sentences" in prompt or "short" in prompt.lower()


def test_get_system_prompt_contains_security_guardrails():
    """System prompt must include security/guardrail instructions."""
    from agent import get_system_prompt
    prompt = get_system_prompt()
    assert "IMPORTANT" in prompt or "fabricate" in prompt.lower()
