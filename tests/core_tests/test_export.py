from core.tools import Export, ExportError
from core.core_app import CoreApp
from core.model_util import (Document, VersionedDocument, fields)

from common import BaseTest

# idea here create a fake document (should be common) to insert in database, with a certain number of key
# insert a certain number of this document in db
# exoport if at the csv format


class DocTest(VersionedDocument):
    name = fields.StringField()
    lastName = fields.StringField()


class TestCoreToolsExport(BaseTest):

    def test_export_noDocument(self):
        DocTest.drop_collection()
        export = Export(DocTest)
        result = export.csvFormat(['name', 'lastName'])
        assert result == "name,lastName\r\n"

    def test_export_OneDocument(self):
        DocTest.drop_collection()
        document1 = DocTest()
        document1.name = "John"
        document1.lastName = "Doe"
        document1.save()
        export = Export(DocTest)
        result = export.csvFormat(['name', 'lastName'])
        assert result == "name,lastName\r\nJohn,Doe\r\n"

    def test_export_document_multipleDocument(self):
        DocTest.drop_collection()
        document1 = DocTest()
        document1.name = "John"
        document1.lastName = "Doe"
        document1.save()
        document2 = DocTest()
        document2.name = "Matthieu"
        document2.lastName = "Martin"
        document2.save()
        export = Export(DocTest)
        result = export.csvFormat(['name', 'lastName'])
        assert result == "name,lastName\r\nJohn,Doe\r\nMatthieu,Martin\r\n"

    def test_export_document_with_wrong_attribute(self):
        DocTest.drop_collection()
        document1 = DocTest()
        document1.name = "John"
        document1.lastName = "Doe"
        document1.save()
        export = Export(DocTest)
        result = export.csvFormat(['name', 'lastName', 'age'])
        assert result == "name,lastName,age\r\nJohn,Doe,\r\n"

    def test_export_WrongTypeOfDocument(self):
        DocTest.drop_collection()

        class DocTestNotMongo():
            name = fields.StringField()
            lastName = fields.StringField()

        catch = False
        try:
            export = Export(DocTestNotMongo)
        except ExportError:
            catch = True
        assert catch
