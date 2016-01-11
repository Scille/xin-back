#! /usr/bin/env python3

from flask import current_app
from flask.ext.script import Manager, Server, Shell
from mongopatcher.extensions.flask import init_patcher, patcher_manager

from core.managers import solr_manager_factory
from sample import bootstrap_app, model


app = bootstrap_app()


class BootstrappedShell(Shell):

    def __init__(self, *args, **kwargs):

        def make_context():
            context = {'db': current_app.db, 'solr': current_app.solr}
            for elem in ('User', ):
                exec("from sample.model import %s" % elem)
                context[elem] = eval(elem)
            print('Context vars: %s' % ', '.join(context.keys()))
            return context
        super().__init__(*args, make_context=make_context, **kwargs)


manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("shell", BootstrappedShell())
manager.add_command("solr", solr_manager_factory((model.User, )))

init_patcher(app, app.db.connection.get_default_database())
manager.add_command("datamodel", patcher_manager)


if __name__ == "__main__":
    manager.run()
