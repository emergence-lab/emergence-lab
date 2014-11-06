from django.contrib.contenttypes.models import ContentType

from actstream.models import target_stream


_user_contentid = ContentType.objects.get(name='user').id


def project_stream(project):
    """
    Filters the activity stream to return any item for the specified project.
    """
    return target_stream(project)


def user_project_stream(user, project):
    """
    Filters the activity stream to return items the user has done
    for the specified project.
    """
    return project_stream(project).filter(actor_content_type_id=_user_contentid,
                                          actor_object_id=user.id)


def investigation_stream(investigation):
    """
    Filters the activity stream to return any item for the specified
    investigation.
    """
    project = investigation.project
    stream = project_stream(project)
    return [item for item in stream
            if item.data is not None
            and item.data.get('investigation', 0) == investigation.id]


def user_investigation_stream(user, investigation):
    """
    Filters the activity stream to return items the user has done
    for the specified investigation.
    """
    project = investigation.project
    stream = user_project_stream(user, project)
    return [item for item in stream
            if item.data is not None
            and item.data.get('investigation', 0) == investigation.id]
