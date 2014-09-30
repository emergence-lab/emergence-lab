from django.contrib.contenttypes.models import ContentType

from actstream.models import target_stream


_operator_contentid = ContentType.objects.get(name='operator').id


def project_stream(project):
    """
    Filters the activity stream to return any item for the specified project.
    """
    return target_stream(project)


def operator_project_stream(operator, project):
    """
    Filters the activity stream to return items the operator has done
    for the specified project.
    """
    return project_stream(project).filter(actor_content_type_id=_operator_contentid,
                                          actor_object_id=operator.id)


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


def operator_investigation_stream(operator, investigation):
    """
    Filters the activity stream to return items the operator has done
    for the specified investigation.
    """
    project = investigation.project
    stream = operator_project_stream(operator, project)
    return [item for item in stream
            if item.data is not None
            and item.data.get('investigation', 0) == investigation.id]
