from flask_script import Manager
#from flask_migrate import Migrate, MigrateCommand

from app import create_app

app = create_app('development')
#migrate = Migrate(app, db)
manager = Manager(app)

#manager.add_command('db', MigrateCommand)

    
@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()