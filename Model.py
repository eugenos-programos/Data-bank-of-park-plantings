import re
from Data.Data import Data

class Model:
    def __init__(self):
        self.data = Data()

    def save_company_info(self, data):
        self.data.set_company_info(data)

    def get_company_info(self):
        return self.data.get_company_info()[0]

    def get_plant_info(self):
        return self.data.get_plants()

    def get_worker_info(self):
        return self.data.get_workers()

    def get_greenplaces_info(self):
        return self.data.get_all_parks()

    def delete_worker(self, id):
        self.data.delete_worker()

    def add_worker(self, data):
        self.data.add_worker(data)

    def add_decorator(self, data):
        self.data.add_decorator(data)

    def add_park(self, name):
        self.data.add_park(name)

    def delete_park(self, id):
        self.data.delete_park(id)

    def add_zone(self, park_id):
        self.data.add_zone(park_id)

    def delete_zone(self, id):
        self.data.delete_zone(id)

if __name__ == '__main__':
    print(Model().data.get_all_parks())