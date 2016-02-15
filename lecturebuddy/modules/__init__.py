from lecturebuddy.modules.database.database import connectToDB
import ConfigParser

Config = ConfigParser.ConfigParser()

Config.read('lecturebuddy/protected/config.ini')

ADMIN_CODE = Config.get('flask', 'ADMIN_CODE')