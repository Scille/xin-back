import pytest
from core.model_util import fields, HistorizedDocument
from core.concurrency import ConcurrencyError
from core_tests.common import BaseTest


class Document(HistorizedDocument):
    field = fields.StringField()


class TestHistorizedDocument(BaseTest):

    def test_history(self):
        doc = Document(field='first_version')
        doc.save()
        assert doc.doc_version == 1
        doc.field = 'new_version'
        doc.save()
        assert doc.doc_version == 2
        doc.delete()
        assert doc.doc_version == 2
        histories = Document._meta['history_cls'].objects().order_by('+date')
        assert len(histories) == 3
        assert histories[0].action == 'CREATE'
        assert histories[1].action == 'UPDATE'
        assert histories[2].action == 'DELETE'

    def test_concurrency(self):
        doc = Document(field='first_version')
        doc.save()
        assert doc.doc_version == 1
        doc.field = 'new_version'
        doc.save()
        assert doc.doc_version == 2
        doc_concurrent = Document.objects.get(pk=doc.pk)
        doc_concurrent.field = 'concurrent_version'
        doc_concurrent.save()
        assert doc_concurrent.doc_version == 3
        with pytest.raises(ConcurrencyError):
            doc.field = 'invalid_version'
            doc.save()
