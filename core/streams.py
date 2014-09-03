from django.contrib.contenttypes.models import ContentType

from actstream.models import actor_stream

from .models import operator, project, investigation


def project_stream(operator, project):
    """
    Filters the activity stream to return items the operator has done
    for the specified project.
    """
    project_content_id = ContentType.objects.get(name='project').id
    return actor_stream(operator).filter(target_content_type_id=project_content_id,
                                         target_object_id=project.id)

def investigation_stream(operator, investigation):
    """
    Filters the activity stream to return items the operator has done
    for the specified investigation.
    """
    project = investigation.project
    stream = project_stream(operator, project)
    return [item for item in stream if item.data.get('investigation', 0) == investigation.id]
