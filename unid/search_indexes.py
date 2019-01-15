import datetime
from haystack import indexes
from .models import Note, uploadContents


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name='search/note_text.txt')
    author = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Note

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class uploadContentsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name='search/uploadcontents_text.txt')
    writer = indexes.CharField(model_attr='writeremail')
    pub_date = indexes.DateTimeField(model_attr='last_modified')

    def get_model(self):
        return uploadContents

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()



