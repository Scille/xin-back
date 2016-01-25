from core.core_app import CoreApp


class BaseTest:

    @classmethod
    def _clean_db(cls):
        cls.app.db.connection.drop_database(
            cls.app.extensions['mongoengine'][cls.app.db]['conn'].get_default_database().name)

    @classmethod
    def setup_class(cls, config=None):
        """
        Initialize flask app and configure it with a clean test database
        """

        app = CoreApp(__name__)
        app.testing = True
        test_config = {
            'TESTING': True,
            'MONGODB_HOST': 'mongodb://localhost:27017/test',
            'TOKEN_FRESHNESS_VALIDITY': 100000,
            'TOKEN_VALIDITY': 100000,
            'SECRET_KEY': "testUltraSecretKey"
        }

        test_config.update(config or {})

        app.config.update(test_config)
        app.bootstrap()

        cls.app = app
        cls.ctx = app.app_context()
        cls.ctx.push()
        cls._clean_db()

    @classmethod
    def teardown_class(cls):
        cls.ctx.pop()
