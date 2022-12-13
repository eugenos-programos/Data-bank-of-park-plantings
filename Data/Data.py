import sqlite3, datetime
import os
import random
import numpy as np

class ObjectData():
    def __init__(self, db_file_name, create_command) -> None:
        self.db_file_name = db_file_name
        self.create_table_command = create_command

    def execute_sql_command(self, sql_command, params=()):
        sqliteConnection = sqlite3.connect(self.db_file_name)
        cursor = sqliteConnection.cursor()
        cursor.execute(sql_command, params)
        out = cursor.fetchall()
        sqliteConnection.commit()
        sqliteConnection.close()
        return out

    def build_table(self):
        self.execute_sql_command(self.create_table_command)

    def add_object(self):
        pass

    def edit_object(self):
        pass

    def delete_object(self):
        pass

class CompanyData(ObjectData):
    def __init__(self, db_file_name) -> None:
        sql_command_create_database = \
        """
        CREATE TABLE company (
            [name] [nvarchar](50) NOT NULL,
            [address] [nvarchar](100) NOT NULL
        );
        """
        super().__init__(db_file_name, sql_command_create_database)

    def build_table(self):
        super().build_table()
        self.execute_sql_command("INSERT INTO company VALUES ('My Company', 'Minsk, pr. Nezavisimosti, 1');")

    def get_company_info(self):
        return self.execute_sql_command("SELECT * FROM company")

    def set_company_info(self, data):
        self.execute_sql_command("UPDATE company SET name = ?, address = ?", data)

class WorkerData(ObjectData):
    def __init__(self, db_file_name) -> None:
        sql_create_worker_data_command = \
        """
        CREATE TABLE worker (
            [ID] [int] NOT NULL UNIQUE,
            [name] [nvarchar](50) NOT NULL,
            [telephone] [nvarchar](20) NOT NULL,
            [address] [nvarchar](100) NOT NULL,
            [birthdate] [DATE] NOT NULL
        );
        """
        super().__init__(db_file_name, sql_create_worker_data_command)

    def add_object(self, data):
        self.execute_sql_command("INSERT INTO worker VALUES (?, ?, ?, ?, ?)", data)

    def delete_object(self, id):
        if len(self.execute_sql_command("SELECT * FROM worker WHERE id = ?", (id, ))) == 0:
            raise ValueError("Worker with this id is not found")
        self.execute_sql_command("DELETE FROM worker WHERE ID = ?", (id, ))

    def get_objects(self, date):
        if date:
            return self.execute_sql_command("SELECT * FROM worker INNER JOIN watering ON worker.id = watering.id_worker WHERE substr(watering.watering_date, 0, 11) = ?", \
                (date, ))
        return self.execute_sql_command("SELECT * FROM worker")

class DecoratorData(ObjectData):
    def __init__(self, db_file_name) -> None:
        create_command = \
        """
        CREATE TABLE decorator (
            [ID] [int] NOT NULL UNIQUE,
            [name] [nvarchar](50) NOT NULL,
            [telephone] [nvarchar](25) NOT NULL,
            [address] [nvarchar](50) NOT NULL,
            [education] [nvarchar](100) NOT NULL,
            [university] [nvarchar](100) NOT NULL,
            [educ_type] [nvarchar](25) NOT NULL,
            [birthdate] [DATE] NOT NULL
        )
        """
        super().__init__(db_file_name, create_command)

    def add_object(self, data):
        self.execute_sql_command("INSERT INTO decorator VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)

    def delete_object(self, id):
        if len(self.execute_sql_command("SELECT * FROM decorator WHERE id = ?", (id, ))) == 0:
            raise ValueError("Decorator with this id is not found")
        self.execute_sql_command("DELETE FROM decorator WHERE id = ?", (id, ))

    def get_objects(self, date):
        if date:
            data = self.execute_sql_command("SELECT * FROM decorator INNER JOIN watering ON decorator.id = watering.id_decorator WHERE substr(watering.watering_date, 0, 11) = ?", \
                (date, ))
        else:
            data = self.execute_sql_command("SELECT * FROM decorator")
        new_data = []
        for obj in data:
            new_data.append(list(obj[:4]) + [obj[-1]])
        return new_data

class PlantData(ObjectData):
    def __init__(self, db_file_name) -> None:
        sql_create_plant_data_command = \
        """
        CREATE TABLE plant (
            [ID] [int] NOT NULL UNIQUE,
            [type] [nvarchar](15) NOT NULL,
            [watering_period] [int] NOT NULL,
            [disembarkation_date] [DATE] NOT NULL,
            [age] [int] NOT NULL,
            [zone_id] [int] NOT NULL,
            FOREIGN KEY (zone_id)
                REFERENCES zone(ID)
                ON DELETE CASCADE
        )
        """ 
        super().__init__(db_file_name, sql_create_plant_data_command)

    def delete_object(self, id):
        if len(self.execute_sql_command("SELECT * FROM plant WHERE id = ?", (id, ))) == 0:
            raise ValueError("Plant with this id is not found")
        self.execute_sql_command("DELETE FROM plant WHERE id = ?", (id, ))

    def add_object(self, data):
        watering_period = random.choice([1, 2, 3, 4, 5, 6, 7])
        if len(self.execute_sql_command("SELECT * FROM zone WHERE id = ?", (data[3], ))) == 0:
            raise ValueError("Zone with this id is not found")
        data = (data[0], data[1], watering_period, datetime.datetime.now(), data[2], data[3])
        self.execute_sql_command("INSERT INTO plant VALUES (?, ?, ?, ?, ?, ?)", data)

    def get_objects(self, type=None):
        if type:
            data = self.execute_sql_command("SELECT plant.ID, plant.type, plant.disembarkation_date,\
                    plant.age, zone.id, park.name FROM plant \
                    INNER JOIN zone ON zone.id = plant.zone_id INNER JOIN park ON zone.park_id = park.id \
                    WHERE plant.type = ?", (type, ))
        else:
            data = self.execute_sql_command("SELECT plant.ID, plant.type, plant.disembarkation_date,\
                    plant.age, zone.id, park.name FROM plant \
                    INNER JOIN zone ON zone.id = plant.zone_id INNER JOIN park ON zone.park_id = park.id")
        new_data = []
        for ind, obj in enumerate(data):
            new_data.append(list(obj))
            new_data[ind][2] = new_data[ind][2][:-7]
        return new_data


class ParkData(ObjectData):
    def __init__(self, db_file_name) -> None:
        sql_create_park_table_command = \
        """
        CREATE TABLE park  (
            [ID] INTEGER PRIMARY KEY AUTOINCREMENT,
            [name] [nvarchar](20) NOT NULL
        )
        """
        super().__init__(db_file_name, sql_create_park_table_command)

    def delete_object(self, id):
        if len(self.execute_sql_command("SELECT * FROM park WHERE ID = ?", (id, ))) == 0:
            raise ValueError("Park with this ID is not found")
        sql_remove_command = "DELETE FROM park WHERE id = ?"
        self.execute_sql_command(sql_remove_command, (id, ))

    def add_object(self, name):
        sql_add_command = "INSERT INTO park (name) VALUES (?)"
        self.execute_sql_command(sql_add_command, (name, ))

    def edit_object(self, id, new_name):
        sql_edit_command = "UPDATE park SET name = ? WHERE id = ?"
        self.execute_sql_command(sql_edit_command, (new_name, id))

    def get_objects(self):
        return self.execute_sql_command("SELECT * FROM park")

class ZoneData(ObjectData):
    def __init__(self, db_file_name) -> None:
        sql_create_zone_table_command = \
        """
        CREATE TABLE zone (
            [ID] INTEGER PRIMARY KEY AUTOINCREMENT,
            [park_id] INTEGER NOT NULL,
            FOREIGN KEY (park_id)
                REFERENCES park(ID)
                ON DELETE CASCADE
        )    
        """
        super().__init__(db_file_name, sql_create_zone_table_command)

    def add_object(self, park_id):
        if len(self.execute_sql_command("SELECT * FROM park WHERE id = ?", (park_id, ))) == 0:
            raise ValueError("Park with this id is not found")
        self.execute_sql_command("INSERT INTO zone (park_id) VALUES (?)", (park_id, ))

    def get_objects(self):
        return self.execute_sql_command("SELECT * FROM zone")

    def delete_object(self, id):
        if len(self.execute_sql_command("SELECT * FROM zone WHERE ID  = ?", (id, ))) == 0:
            raise ValueError("Zone with this ID is not found")
        self.execute_sql_command("DELETE FROM zone WHERE ID = ?", (id, ))

class WateringData(ObjectData):
    def __init__(self, db_file_name) -> None:
        create_command = \
        """
        CREATE TABLE watering (
            [id_plant] [int] NOT NULL,
            [watering_date] [DATE] NOT NULL,
            [watering_size] [INT] NOT NULL,
            [id_worker] [int] NOT NULL,
            [id_decorator] [int] NOT NULL,
            FOREIGN KEY (id_plant)
                REFERENCES plant(ID)
                ON DELETE CASCADE,
            FOREIGN KEY (id_worker)
                REFERENCES worker(ID)
                ON DELETE CASCADE,
            FOREIGN KEY (id_decorator)
                REFERENCES decorator(ID)
                ON DELETE CASCADE
        )
        """
        super().__init__(db_file_name, create_command)

    def add_object(self, data):
        id_plant = data[0]
        age = data[2]
        dis_date, period = self.execute_sql_command("SELECT disembarkation_date, watering_period FROM plant WHERE id = ?", (id_plant, ))[0]
        dis_date = dis_date[2:-7]
        dis_date = datetime.datetime.strptime(dis_date, '%y-%m-%d %H:%M:%S')
        for iter in range(3):
            watering_date = dis_date + datetime.timedelta(days=period) * (iter + 1)
            watering_size = round(1 / age + np.random.rand(), 2)
            decor_id = self.find_free_decorator(watering_date)
            worker_id = self.find_free_worker(watering_date)
            data = (id_plant, watering_date, watering_size, worker_id, decor_id)
            self.execute_sql_command("INSERT INTO watering VALUES (?, ?, ?, ?, ?)", data)

    def find_free_decorator(self, date):
        free_decor_ids = self.execute_sql_command("SELECT ID FROM decorator WHERE ID NOT IN (SELECT id_decorator FROM watering WHERE watering_date = ?)", (date, ))
        if len(free_decor_ids) > 0:
            decor_id = random.choice(free_decor_ids)[0]
        else:
            if len(self.execute_sql_command("SELECT ID FROM decorator")) == 0:
                decor_id = -1
            else:
                decor_id = random.choice(self.execute_sql_command("SELECT ID FROM decorator"))[0]
        return decor_id
        
    def find_free_worker(self, date):
        free_warker_ids = self.execute_sql_command("SELECT ID FROM worker WHERE ID NOT IN (SELECT id_worker FROM watering WHERE watering_date = ?)", (date, ))
        if len(free_warker_ids) > 0:
            warker_id = random.choice(free_warker_ids)[0]
        else:
            if len(self.execute_sql_command("SELECT ID FROM decorator")) == 0:
                warker_id = -1
            else:
                warker_id = random.choice(self.execute_sql_command("SELECT ID FROM decorator"))[0]
        return warker_id
        
    def get_objects(self, type):
        if type:
            return self.execute_sql_command("SELECT watering.* FROM watering INNER JOIN plant ON watering.id_plant = plant.id WHERE plant.type=?", (type, ))
        return self.execute_sql_command("SELECT * FROM watering")

class Data():

    objects_data : dict[str : ObjectData]
    db_file_name : str 

    def __init__(self) -> None:
        self.db_file_name = 'data.db'
        self.objects_data = {}

        self.objects_data['worker'] = WorkerData(self.db_file_name)
        self.objects_data['company'] = CompanyData(self.db_file_name)
        self.objects_data['plant'] = PlantData(self.db_file_name)
        self.objects_data['zone'] = ZoneData(self.db_file_name)
        self.objects_data['park'] = ParkData(self.db_file_name)
        self.objects_data['decorator'] = DecoratorData(self.db_file_name)
        self.objects_data['watering'] = WateringData(self.db_file_name)

    def create_database(self):
        if os.path.exists('data.db'):
            os.remove('data.db')
        for key in self.objects_data.keys():
            self.objects_data[key].build_table()

    def add_worker(self, data):
        self.objects_data['worker'].add_object(data)

    def delete_worker(self, id):
        self.objects_data['worker'].delete_object(id)

    def get_workers(self, type=None):
        workers = self.objects_data['worker'].get_objects(type)
        decorators = self.objects_data['decorator'].get_objects(type)
        return workers + decorators

    def get_company_info(self):
        return self.objects_data['company'].get_company_info()

    def set_company_info(self, data):
        self.objects_data['company'].set_company_info(data)

    def add_plant(self, data):
        self.objects_data['plant'].add_object(data)
        self.objects_data['watering'].add_object(data)

    def delete_plant(self, id):
        self.objects_data['plant'].delete_object(id)

    def get_plants(self, type=None):
        return self.objects_data['plant'].get_objects(type)

    def add_zone(self, park_id):
        self.objects_data['zone'].add_object(park_id)

    def get_all_zones(self):
        return self.objects_data['zone'].get_objects()

    def delete_zone(self, id):
        self.objects_data['zone'].delete_object(id)

    def add_park(self, name):
        self.objects_data['park'].add_object(name)

    def delete_park(self, id):
        self.objects_data['park'].delete_object(id)

    def edit_park(self, id, new_name):
        self.objects_data['park'].edit_object(id, new_name)

    def get_all_parks(self):
        return self.objects_data['park'].get_objects()

    def add_decorator(self, data):
        return self.objects_data['decorator'].add_object(data)

    def delete_decorator(self, id):
        return self.objects_data['decorator'].delete_object(id)

    def get_watering_info(self, type):
        return self.objects_data['watering'].get_objects(type)

if __name__ == '__main__':
    data = Data()
    data.create_database()
