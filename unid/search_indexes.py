import datetime
from haystack import indexes
from .models import Note, uploadContents, Post


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True, template_name='search/note_text.txt')
    author = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Note

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class uploadContentsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True, template_name='search/uploadcontents_text.txt')
    writer = indexes.CharField(model_attr='writeremail')
    pub_date = indexes.DateTimeField(model_attr='last_modified')
    content_auto = indexes.EdgeNgramField(model_attr='title')
    def get_model(self):
        return uploadContents

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True, template_name='search/informations_text.txt')
    writer = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='last_modified')
    content_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


