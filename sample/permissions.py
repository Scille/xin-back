"""
This module centralize all the action-needs/permissions used for the
access rights policy
"""

from core.policy import PolicyTree


POLICIES = PolicyTree({
    'history': 'see',
    'user': ('create', 'modify', 'see'),
    # TODO: complete me !
})
