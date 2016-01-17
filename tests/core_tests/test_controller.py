from mongoengine import ValidationError as MongoValidationError

from core.model_util import (Document, HistorizedDocument, BaseController,
                             ControlledDocument, VersionedDocument, fields)
from core.concurrency import ConcurrencyError
from core.core_app import CoreApp


class ControllerTestApp:

    def __init__(self):
        self.app = CoreApp("TestController")
        self.app.bootstrap()

    def get(self):
        return self.app


def test_controller():
    def controller_factory(document):
        router = {
            'ready': ReadyController,
            'fired': FiredController,
            'reloading': ReloadingController
        }
        return router[document.status](document)

    class ReadyController(BaseController):

        def state(self):
            return "%s is ready to fire" % self.document.name

        def fire(self):
            self.document.status = 'fired'
            self.document.save()

    class FiredController(BaseController):

        def state(self):
            return "%s is empty" % self.document.name

        def reload(self):
            self.document.status = 'reloading'
            self.document.save()

    class ReloadingController(BaseController):

        def state(self):
            return "%s is reloading..." % self.document.name

        def done(self):
            self.document.status = 'ready'
            self.document.save()

    class Gun(ControlledDocument):
        meta = {'controller_cls': controller_factory}
        name = fields.StringField(required=True)
        status = fields.StringField(choices=['ready', 'fired', 'reloading'], required=True)
    app = ControllerTestApp().get()
    with app.app_context():
        doc = Gun(name='gun-1', status='ready')
        doc.save()
        assert isinstance(doc.controller, ReadyController)
        assert hasattr(doc.controller, 'fire')
        assert doc.controller.state() == 'gun-1 is ready to fire'
        doc.controller.fire()
        assert isinstance(doc.controller, FiredController)
        assert doc.controller.state() == 'gun-1 is empty'
        doc.controller.reload()
        assert isinstance(doc.controller, ReloadingController)
        doc.controller.done()


def test_dualinheritance():
    class DualInheritanceController(BaseController):

        def make_v2(self):
            self.document.field = 'v2'
            self.document.save()

    class DualInheritanceDoc(ControlledDocument, HistorizedDocument):
        meta = {'controller_cls': DualInheritanceController}
        field = fields.StringField()
    app = ControllerTestApp().get()
    with app.app_context():
        doc = DualInheritanceDoc(field='v1')
        doc.save()
        # Make sure we have both history and controller functionalities
        assert isinstance(doc.controller, DualInheritanceController)
        doc.controller.make_v2()
        assert hasattr(doc, 'get_history')
        history = doc.get_history()
        assert history.count() == 2
