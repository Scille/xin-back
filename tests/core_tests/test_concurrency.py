import pytest

from core.core_app import CoreApp
from core.model_util import (VersionedDocument, fields)
from core.concurrency import ConcurrencyError

# This do not test the concurrency handler need to setup a small app


class ConcurrencyTestApp:

    def __init__(self):
        self.app = CoreApp("TestDecode")
        self.app.bootstrap()

    def get(self):
        return self.app


def test_concurrency():
    class Doc(VersionedDocument):
        field = fields.StringField()
    app = ConcurrencyTestApp().get()
    with app.app_context():
        doc = Doc(field="v1")
        doc.save()
        assert doc.doc_version == 1
        doc_concurrent = Doc.objects(field="v1").first()
        assert doc_concurrent
        doc.field = "v2"
        doc_concurrent.field = "v2_alternate"
        doc_concurrent.save()
        assert doc_concurrent.doc_version == 2
        with pytest.raises(ConcurrencyError):
            doc.save()
        doc.reload()
        assert doc.field == doc_concurrent.field
        assert doc.doc_version == 2
