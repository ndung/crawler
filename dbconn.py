import pymongo

client = pymongo.MongoClient('192.168.46.3', 27017)
db = client.twitter_politician
table = "media_online"
db[table].create_index([("url", pymongo.DESCENDING)], unique=True)

class DBConn:

    def save(self, obj):
        try:
            db.media_online.insert_one(obj)
        except pymongo.errors.DuplicateKeyError:
            pass
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)