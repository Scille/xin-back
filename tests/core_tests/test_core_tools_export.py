from core.tools import Export, ExportError
from core.core_app import CoreApp
from core.model_util import (Document, VersionedDocument, fields)

# idea here create a fake document (should be common) to insert in database, with a certain number of key
# insert a certain number of this document in db
# exoport if at the csv format


class ExportTestApp:

    def __init__(self):
        self.app = CoreApp("TestExport")
        self.app.bootstrap()
        with self.app.app_context():
            self.app.db.connect('test')
            self.app.db.connection.drop_database('test')

    def get(self):
        return self.app


class DocTest(VersionedDocument):
    name = fields.StringField()
    lastName = fields.StringField()


def test_export_noDocument():
    app = ExportTestApp().get()
    with app.app_context():
        export = Export(DocTest)
        result = export.csvFormat(['name', 'lastName'])
        assert result == "name,lastName\r\n"


def test_export_OneDocument():
    app = ExportTestApp().get()
    with app.app_context():
        document1 = DocTest()
        document1.name = "John"
        document1.lastName = "Doe"
        document1.save()
        export = Export(DocTest)
        result = export.csvFormat(['name', 'lastName'])
        assert result == "name,lastName\r\nJohn,Doe\r\n"


def test_export_document_multipleDocument():
    app = ExportTestApp().get()
    with app.app_context():
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


def test_export_document_with_wrong_attribute():
    app = ExportTestApp().get()
    with app.app_context():
        document1 = DocTest()
        document1.name = "John"
        document1.lastName = "Doe"
        document1.save()
        export = Export(DocTest)
        result = export.csvFormat(['name', 'lastName', 'age'])
        assert result == "name,lastName,age\r\nJohn,Doe,\r\n"


def test_export_WrongTypeOfDocument():
    app = ExportTestApp().get()
    with app.app_context():
        class DocTestNotMongo():
            name = fields.StringField()
            lastName = fields.StringField()

        catch = False
        try:
            export = Export(DocTestNotMongo)
        except ExportError:
            catch = True
        assert catch
