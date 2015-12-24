import datetime
from haystack import indexes
from models import Process


class ProcessIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True,
                             use_template=True,
                            #  model_attr='comment'
                             )
    user = indexes.CharField(model_attr='user')
    type = indexes.CharField(model_attr='type')
    legacy_identifier = indexes.CharField(model_attr='legacy_identifier')
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return Process

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())
