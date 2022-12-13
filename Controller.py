from Model import *

class Controller:
    model : Model

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def save_company_info(self, data):
        self.model.save_company_info(data)

    def get_company_info(self):
        return self.model.get_company_info()

    def get_plant_info(self):
        return self.model.get_plant_info()

    def get_worker_info(self):
        return self.model.get_worker_info()

    def get_greenplaces_info(self):
        return self.model.get_greenplaces_info()

    def delete_worker(self, name):
        self.model.delete_worker(name)

    def add_worker(self, data):
        self.model.add_worker(data)

    def add_decorator(self, data):
        self.model.add_decorator(data)

    def add_park(self, name):
        self.model.add_park(name)

    def delete_park(self, id):
        self.model.delete_park(id)

    def add_zone(self, park_id):
        self.model.add_zone(park_id)

    def delete_zone(self, id):
        self.model.delete_zone(id)

    def add_plant(self, data):
        self.model.add_plant(data)

    def delete_plant(self, id):
        self.model.delete_plant(id)

    def delete_decorator(self, id):
        self.model.delete_decorator(id)

    def get_watering_info(self, type=None):
        return self.model.get_watering_info(type)

    def search_plants(self, type):
        return self.model.search_plants(type)

    def search_workers(self, date):
        return self.model.search_workers(date)