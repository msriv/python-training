class BigqueryStorage:
    def connect(self):
        return "Bigquery connection successful"

class RedisStorage:
    def connect(self):
        return "Redis storage successful"


class StorageFactory:
    def __init__(self, Storage):
        self.storage = Storage()

    def connect_storage(self):
        return self.storage.connect()


if __name__ == "__main__":
    bq_storage_factory = StorageFactory(BigqueryStorage)
    redis_storage_factory = StorageFactory(RedisStorage)
    print(bq_storage_factory.connect_storage())
    print(redis_storage_factory.connect_storage())