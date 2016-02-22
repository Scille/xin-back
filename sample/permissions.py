"""
This module centralize all the action-needs/permissions used for the
access rights policy
"""

from xin_back.policy import PolicyTree


POLICIES = PolicyTree({
    'history': 'see',
    'user': ('create', 'modify', 'see'),
    # TODO: complete me !
})
