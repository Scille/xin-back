"""
This module centralize all the action-needs/permissions used for the
access rights policy
"""

from scille_core_back.policy import PolicyTree


POLICIES = PolicyTree({
    'history': 'see',
    'user': ('create', 'modify', 'see'),
    # TODO: complete me !
})
