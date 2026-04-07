# Copyright (c) 2026. All rights reserved.
# Customer Support Ticket Resolution Environment for OpenEnv

"""
AI-Powered Customer Support Ticket Resolution Environment.

A realistic simulation environment where an AI agent learns to handle
customer support tickets end-to-end using the OpenEnv framework.
"""

from env.models import SupportAction, SupportObservation, SupportState, SupportReward
from env.graders import grade_easy, grade_medium, grade_hard

__all__ = [
    "SupportAction",
    "SupportObservation",
    "SupportState",
    "SupportReward",
    "grade_easy",
    "grade_medium",
    "grade_hard",
]
