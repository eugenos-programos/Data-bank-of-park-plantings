import sqlite3
import os

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
            [name] [nvarchar](50) NOT NULL,
            [telephone] [nvarchar](20) NOT NULL,
            [address] [nvarchar](100) NOT NULL
        );
        """
        super().__init__(db_file_name, sql_create_worker_data_command)

    def add_object(self, data):
        self.execute_sql_command("INSERT INTO worker VALUES (?, ?, ?, ?)", data)

    def delete_object(self, name):
        self.execute_sql_command("DELETE FROM worker WHERE name = ?", (name, ))

    def get_objects(self):
        return self.execute_sql_command("SELECT * FROM worker")

class PlantData(ObjectData):
    def __init__(self, db_file_name) -> None:
        sql_create_plant_data_command = \
        """
        CREATE TABLE plant (
            [ID] [int] NOT NULL,
            [type] [nvarchar](15) NOT NULL,
            [watering_date] [DATE] NOT NULL,
            [disembarkation_date] [DATE] NOT NULL,
            [watering_size] [int] NOT NULL
        )
        """ 
        super().__init__(db_file_name, sql_create_plant_data_command)

    def delete_object(self, id):
        self.execute_sql_command("DELETE FROM plant WHERE id = ?", (id, ))

    def add_object(self, data):
        self.execute_sql_command("INSERT INTO plant VALUES (?, ?, ?, ?, ?)", data)

    def get_objects(self):
        return self.execute_sql_command("SELECT * FROM plant")

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
        if len(self.execute_sql_command("SELECT * FROM perk WHERE ID  = ", (id,))) == 0:
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
        self.execute_sql_command("INSERT INTO zone (park_id) VALUES (?)", (park_id, ))

    def get_objects(self):
        return self.execute_sql_command("SELECT * FROM zone")

    def delete_object(self, id):
        if len(self.execute_sql_command("SELECT * FROM zone WHERE ID  = ", (id,))) == 0:
            raise ValueError("Zone with this ID is not found")
        self.execute_sql_command("DELETE FROM zone WHERE ID = ?", (id, ))


class Data():
    def __init__(self) -> None:
        self.db_file_name = 'data.db'
        self.objects_data = {}

        self.objects_data['worker'] = WorkerData(self.db_file_name)
        self.objects_data['company'] = CompanyData(self.db_file_name)
        self.objects_data['plant'] = PlantData(self.db_file_name)
        self.objects_data['zone'] = ZoneData(self.db_file_name)
        self.objects_data['park'] = ParkData(self.db_file_name)

    def create_database(self):
        if os.path.exists('data.db'):
            os.remove('data.db')
        for key in self.objects_data.keys():
            self.objects_data[key].build_table()

    def add_worker(self, data):
        self.objects_data['worker'].add_object(data)

    def delete_worker(self, name):
        self.objects_data['worker'].delete_object(name)

    def get_workers(self):
        return self.objects_data['worker'].get_objects()

    def get_company_info(self):
        return self.objects_data['company'].get_company_info()

    def set_company_info(self, data):
        self.objects_data['company'].set_company_info(data)

    def add_plant(self, data):
        self.objects_data['plant'].add_object(data)

    def delete_plant(self, id):
        self.objects_data['plant'].delete_object(id)

    def get_plants(self):
        return self.objects_data['plant'].get_objects()

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

if __name__ == '__main__':
    data = Data()
    data.create_database()