# Classes for Redis objects associated with this app


class ActionItem(object):
    """
    Action items for each user. Associated with key
    users:<user_id>:action.items as ordered list.
    """
    created = ''
    comment = ''


class GitCredential(object):
    """
    Credentials for a user's Git account.
    Type is string with name users:<user_id>:git.credential
    """
    account_type = ''
