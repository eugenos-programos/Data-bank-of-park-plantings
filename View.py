from tkinter import ttk
import tkinter as tk
from Controller import Controller

def bind_textbox(frame, def_text, size=(1, 10), save_text=True):
    textbox = tk.Text(frame, height=size[0], width=size[1])
    textbox.insert(tk.END, def_text)
    if save_text:
        def default(event):
            current = textbox.get('1.0', tk.END)
            if current[:-1] == def_text:
                textbox.delete('1.0', tk.END)
            elif current == '\n':
                textbox.insert('1.0', def_text)

        textbox.bind("<FocusIn>", default)
        textbox.bind("<FocusOut>", default)

    return textbox

def create_table(frame, data, col_names):
    for col_index, col_name in enumerate(col_names):
            entry = ttk.Entry(frame, width=20, font=('Arial', 16, 'bold'))
            entry.grid(row=0, column=col_index)
            entry.insert(tk.END, col_name)

    for row_index in range(1, len(data) + 1):
        for col_index in range(len(col_names)):
            entry = ttk.Entry(frame, width=20, font=('Arial', 16,' bold'))
            entry.grid(row=row_index, column=col_index)
            entry.insert(tk.END, data[row_index - 1][col_index])
    return entry

class View():

    controller : Controller

    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.grid(row=10, column=0, padx=80, pady=160)
        self.start_menu()

    def start_menu(self):
        self.clean_up_frame()
        self.parent.title('Банк данных насаждений парков')

        self.company_info_but = ttk.Button(self.frame, text='Управление информацией о фирме', command=self.company_info)
        self.park_and_zones_info_but = ttk.Button(self.frame, text='Управление инф. о зонах и парках', command=self.parks_info_managing)
        self.plant_info_but = ttk.Button(self.frame, text='Управление информацией о растениях', command=self.plants_info_managing)
        self.workers_info_but = ttk.Button(self.frame, text='Управение информацией о служащих', command=self.workers_info_managing)
        self.decorator_info_but = ttk.Button(self.frame, text='Управление информацией о декораторах', command=self.decorator_info_managing)
        self.see_greenplaces_but = ttk.Button(self.frame, text='Просмотр информации о насаждениях', command=self.see_greenplaces_info)
        self.see_workers_but = ttk.Button(self.frame, text='Просмотр списка сотрудников по дате', command=self.see_workers_info)
        self.see_plants_but = ttk.Button(self.frame, text='Просмотр инф. о растениях и плану полива', command=self.see_plants_info)
        self.exit_but = ttk.Button(self.frame, text='Выход', command=self.exit)

        self.company_info_but.grid(row=1, column=0, sticky='ew', pady=10)
        self.park_and_zones_info_but.grid(row=2, column=0, sticky='ew', pady=10)
        self.plant_info_but.grid(row=3, column=0, sticky='ew', pady=10)
        self.workers_info_but.grid(row=4, column=0, sticky='ew', pady=10)
        self.decorator_info_but.grid(row=5, column=0, sticky='ew', pady=10)
        self.see_greenplaces_but.grid(row=6, column=0, sticky='ew', pady=10)
        self.see_workers_but.grid(row=7, column=0, sticky='ew', pady=10)
        self.see_plants_but.grid(row=8, column=0, sticky='ew', pady=10)
        self.exit_but.grid(row=9, column=0, sticky='ew', pady=25)

    def company_info(self):
        self.clean_up_frame()
        self.parent.title('Информация о фирме')
        name, address = self.controller.get_company_info()

        self.name_label = ttk.Label(self.frame, text='Name:')
        self.name_label.grid(row=1, column=0, pady=5)
        self.address_label = ttk.Label(self.frame, text='Address:')
        self.address_label.grid(row=3, column=0, pady=5)
        self.company_name = bind_textbox(self.frame, name, (2, 30), False)
        self.company_name.grid(row=1, column=1, pady=5)
        self.company_address = bind_textbox(self.frame, address, (2, 30), False)
        self.company_address.grid(row=3, column=1, pady=5)

        self.save_comp_but = ttk.Button(self.frame, text='Сохранить новую информацию', command=self.save_company_info)
        self.save_comp_but.grid(row=4, column=1, pady=15)

    def save_company_info(self):
        name = self.company_name.get('1.0', tk.END)[:-1]
        address = self.company_address.get('1.0', tk.END)[:-1]
        data = (name, address)
        self.controller.save_company_info(data)
        self.clean_up_frame()
        self.start_menu()

    def see_workers_info(self):
        self.clean_up_frame()
        data = self.controller.get_worker_info()
        self.parent.title('Найти информацию о работниках')
        col_names = ['Статус', 'ФИО', 'Адрес', 'Телефон', 'Дата Рождения']
        create_table(self.frame, data, col_names)
        self.date_box = bind_textbox(self.frame, 'Введите дату...', size=(2, 30))
        self.date_box.grid(row=len(data) + 2, column=1, pady=20)
        ttk.Button(self.frame, text='Искать рабочих', command=self.search_workers).grid(row=len(data) + 2, column=4, pady=20)
        ttk.Button(self.frame, text='Выйти в главное меню', command=self.start_menu).grid(row=len(data) + 3, column=1, pady=20)

    def search_workers(self):
        date = self.date_box.get('1.0', tk.END)[:-1]
        self.clean_up_frame()
        data = self.controller.search_workers(date)
        col_names = ['Статус', 'ФИО', 'Адрес', 'Телефон']
        create_table(self.frame, data, col_names)
        self.date_box = bind_textbox(self.frame, 'Введите дату...', size=(2, 30))
        self.date_box.grid(row=len(data) + 2, column=1, pady=20)
        ttk.Button(self.frame, text='Искать высадку', command=self.search_workers).grid(row=len(data) + 2, column=4, pady=20)
        ttk.Button(self.frame, text='Выйти в главное меню', command=self.start_menu).grid(row=len(data) + 3, column=1, pady=20)

    def see_plants_info(self):
        self.clean_up_frame()
        data = self.controller.get_watering_info()
        self.parent.title('Режимы полива растений')
        col_names = ['ID растения', 'Дата полива', 'Размер полива', 'ИД работника', 'ИД декоратора']
        create_table(self.frame, data, col_names)
        self.plant_type = bind_textbox(self.frame, 'Введите вид...', size=(2, 30))
        self.plant_type.grid(row=len(data) + 2, column=1, pady=20)
        ttk.Button(self.frame, text='Искать растения', command=self.watering_search).grid(row=len(data) + 2, column=4, pady=20)
        ttk.Button(self.frame, text='Выйти в главное меню', command=self.start_menu).grid(row=len(data) + 3, column=1, pady=20)

    def watering_search(self):
        type = self.plant_type.get('1.0', tk.END)[:-1]
        self.clean_up_frame()
        data = self.controller.get_watering_info(type)
        self.parent.title('Режимы полива растений')
        col_names = ['ID растения', 'Дата полива', 'Размер полива', 'ИД работника', 'ИД декоратора']
        create_table(self.frame, data, col_names)
        self.plant_type = bind_textbox(self.frame, 'Введите вид...', size=(2, 30))
        self.plant_type.grid(row=len(data) + 2, column=1, pady=20)
        ttk.Button(self.frame, text='Искать растения', command=self.watering_search).grid(row=len(data) + 2, column=4, pady=20)
        ttk.Button(self.frame, text='Выйти в главное меню', command=self.start_menu).grid(row=len(data) + 3, column=1, pady=20)

    def workers_info_managing(self):
        self.clean_up_frame()
        self.id_delete_work = bind_textbox(self.frame, 'Введите ИД удаляемого рабочего....', size=(2, 25))
        self.id_delete_work.grid(row=0, column=0)
        self.del_work_out = None
        ttk.Button(self.frame, text='Удалить', command=self.delete_worker).grid(row=5, column=0, pady=10)

        self.status_new_work = bind_textbox(self.frame, 'ИД нового рабочего...', size=(2, 30))
        self.status_new_work.grid(row=0, column=2)
        self.name_new_work = bind_textbox(self.frame, 'Имя нового рабочего...', (2, 30))
        self.name_new_work.grid(row=1, column=2)
        self.tel_new_work = bind_textbox(self.frame, 'Телефон нового рабочего...', (2, 30))
        self.tel_new_work.grid(row=3, column=2)
        self.address_new_work = bind_textbox(self.frame, 'Адрес нового рабочего...', (2, 30))
        self.address_new_work.grid(row=4, column=2)
        self.birth_work = bind_textbox(self.frame, 'Дата рождения рабочего...', (2, 30))
        self.birth_work.grid(row=5, column=2)
        self.add_work_out = None
        ttk.Button(self.frame, text='Добавить', command=self.add_new_worker).grid(row=6, column=2)
        ttk.Button(self.frame, text='Выйти в меню', command=self.start_menu).grid(row=8, column=1, pady=60)

    def decorator_info_managing(self):
        self.clean_up_frame()
        self.id_delete_work = bind_textbox(self.frame, 'Введите ИД удаляемого декоратора....', size=(2, 25))
        self.id_delete_work.grid(row=0, column=0)
        self.del_decor_out = None
        ttk.Button(self.frame, text='Удалить', command=self.delete_decorator).grid(row=6, column=0, pady=20)

        self.id_new_decor = bind_textbox(self.frame, 'Ид нового декоратора...', (2, 30))
        self.id_new_decor.grid(row=0, column=2)

        self.name_new_decor = bind_textbox(self.frame, 'Имя нового декоратора...', (2, 30))
        self.name_new_decor.grid(row=1, column=2)

        self.tel_new_decor = bind_textbox(self.frame, 'Телефон нового декоратора...', (2, 30))
        self.tel_new_decor.grid(row=2, column=2)

        self.address_new_decor = bind_textbox(self.frame, 'Адрес нового декоратора...', (2, 30))
        self.address_new_decor.grid(row=3, column=2)

        self.educ_new_decor = bind_textbox(self.frame, 'Образование декоратора...', (2, 30))
        self.educ_new_decor.grid(row=4, column=2)

        self.univer_new_decor = bind_textbox(self.frame, 'ВУЗ декоратора...', (2, 30))
        self.univer_new_decor.grid(row=5, column=2)

        self.educ_type_new_decor = bind_textbox(self.frame, 'Тип образования декоратора...', (2, 30))
        self.educ_type_new_decor.grid(row=6, column=2) 

        self.birthdate_decor = bind_textbox(self.frame, 'Рождение декоратора...', (2, 30))
        self.birthdate_decor.grid(row=7, column=2) 
        self.add_decor_out = None
        ttk.Button(self.frame, text='Добавить', command=self.add_new_decorator).grid(row=8, column=2)
        ttk.Button(self.frame, text='Выйти в меню', command=self.start_menu).grid(row=9, column=1, pady=60)

    def add_new_decorator(self):
        if self.add_decor_out:
            self.add_decor_out.destroy()
        try:
            id = int(self.id_new_decor.get('1.0', tk.END))
            name = self.name_new_decor.get('1.0', tk.END)[:-1]
            tel = self.tel_new_decor.get('1.0', tk.END)[:-1]
            address = self.address_new_decor.get('1.0', tk.END)[:-1]
            educ = self.educ_new_decor.get('1.0', tk.END)[:-1]
            unver = self.univer_new_decor.get('1.0', tk.END)[:-1]
            educ_type = self.educ_type_new_decor.get('1.0', tk.END)[:-1]
            birthdate = self.birthdate_decor.get('1.0', tk.END)[:-1]
            data = (id, name, tel, address, educ, unver, educ_type, birthdate)
            self.controller.add_decorator(data)
        except Exception as exc:
            self.add_decor_out = tk.Label(self.frame, text=exc, fg='#f60404')
            self.add_decor_out.grid(row=9, column=2, pady=10)
        else:
            self.add_decor_out = tk.Label(self.frame, text='Worker is added', fg='#008000')
            self.add_decor_out.grid(row=9, column=2, pady=10)

    def delete_decorator(self):
        if self.del_decor_out:
            self.del_decor_out.destroy()
        try:
            id = int(self.id_delete_work.get('1.0', tk.END))
            self.controller.delete_decorator(id)
        except Exception as exc:
            self.del_decor_out = tk.Label(self.frame, text=exc, fg='#f60404')
            self.del_decor_out.grid(row=3, column=0, pady=10)
        else:
            self.del_decor_out = tk.Label(self.frame, text=f'Decorator deleted', fg='#008000')
            self.del_decor_out.grid(row=3, column=0, pady=10)

    def parks_info_managing(self):
        self.clean_up_frame()
        self.id_delete_park = bind_textbox(self.frame, 'Ид парка для удаления....', size=(2, 25))
        self.id_delete_park.grid(row=0, column=0)
        self.del_park_out = None
        ttk.Button(self.frame, text='Удалить', command=self.delete_park).grid(row=1, column=0, pady=10)

        self.id_delete_zone = bind_textbox(self.frame, 'Ид зоны для удаления....', size=(2, 25))
        self.id_delete_zone.grid(row=3, column=0)
        self.del_zone_out = None
        ttk.Button(self.frame, text='Удалить', command=self.delete_zone).grid(row=6, column=0, pady=10)

        self.id_add_zone = bind_textbox(self.frame, 'Ид парка для добавления зоны...', size=(2, 25))
        self.id_add_zone.grid(row=0, column=2, padx=20)
        self.add_park_out = None

        self.add_zone_out = None
        self.name_add_park = bind_textbox(self.frame, 'Имя нового парка...', size=(2, 25))
        self.name_add_park.grid(row=0, column=3, padx=20)

        ttk.Button(self.frame, text='Добавить зону', command=self.add_zone).grid(row=1, column=2, pady=15)
        ttk.Button(self.frame, text='Добавить парк', command=self.add_park).grid(row=1, column=3, pady=15)

        ttk.Button(self.frame, text='Выйти в меню', command=self.start_menu).grid(row=7, column=1, pady=15)

    def add_park(self):
        if self.add_park_out:
            self.add_park_out.destroy()
        try:
            name = self.name_add_park.get('1.0', tk.END)[:-1]
            self.controller.add_park(name)
        except Exception as exc:
            self.add_park_out = tk.Label(self.frame, text=exc, fg='#f60404')
            self.add_park_out.grid(row=2, column=3, pady=10)
        else:
            self.add_plant_out = tk.Label(self.frame, text='Park is added', fg='#008000')
            self.add_plant_out.grid(row=2, column=3, pady=10)

    def add_zone(self):
        if self.add_zone_out:
            self.add_zone_out.destroy()
        try:
            id = int(self.id_add_zone.get('1.0', tk.END)[:-1])
            self.controller.add_zone(id)
        except Exception as exc:
            self.add_zone_out = tk.Label(self.frame, text=exc, fg='#f60404')
            self.add_zone_out.grid(row=2, column=2, pady=10)
        else:
            self.add_zone_out = tk.Label(self.frame, text='Zone is added', fg='#008000')
            self.add_zone_out.grid(row=2, column=2, pady=15)

    def delete_park(self):
        if self.del_park_out:
            self.del_park_out.destroy()
        try:
            id = int(self.id_delete_park.get('1.0', tk.END))
            self.controller.delete_park(id)
        except Exception as exc:
            self.del_park_out = tk.Label(self.frame, text=exc, fg='#f60404')
            self.del_park_out.grid(row=2, column=0, pady=10)
        else:
            self.del_park_out = tk.Label(self.frame, text='Park is deleted', fg='#008000')
            self.del_park_out.grid(row=2, column=0, pady=10)

    def delete_zone(self):
        if self.del_zone_out:
            self.del_zone_out.destroy()
        try:
            id = int(self.id_delete_zone.get('1.0', tk.END))
            self.controller.delete_zone(id)
        except Exception as exc:
            self.del_zone_out = tk.Label(self.frame, text=exc, fg='#f60404')
            self.del_zone_out.grid(row=7, column=0, pady=10)
        else:
            self.del_zone_out = tk.Label(self.frame, text='Zone is deleted', fg='#008000')
            self.del_zone_out.grid(row=7, column=0, pady=10)
    
    def plants_info_managing(self):
        self.clean_up_frame()
        self.id_delete_plant = bind_textbox(self.frame, 'Введите ид растения....', size=(2, 25))
        self.id_delete_plant.grid(row=0, column=0)
        self.del_plant_out = None
        ttk.Button(self.frame, text='Удалить', command=self.delete_plant).grid(row=5, column=0, pady=10)

        self.id_new_plant = bind_textbox(self.frame, 'Ид нового растения...', size=(2, 30))
        self.id_new_plant.grid(row=0, column=2)
        self.type_plant = bind_textbox(self.frame, 'Тип нового растения...', (2, 30))
        self.type_plant.grid(row=1, column=2)
        self.age_plant = bind_textbox(self.frame, 'Возраст растения...', (2, 30))
        self.age_plant.grid(row=3, column=2)
        self.zone_id_plant = bind_textbox(self.frame, 'Ид зоны растения...', (2, 30))
        self.zone_id_plant.grid(row=4, column=2)
        self.add_plant_out = None
        ttk.Button(self.frame, text='Добавить', command=self.add_new_plant).grid(row=5, column=2)
        ttk.Button(self.frame, text='Выйти в меню', command=self.start_menu).grid(row=7, column=1, pady=60)

    def add_new_plant(self):
        if self.add_plant_out:
            self.add_plant_out.destroy()
        try:
            id = int(self.id_new_plant.get('1.0', tk.END))
            type = self.type_plant.get('1.0', tk.END)[:-1]
            age = int(self.age_plant.get('1.0', tk.END))
            zone_id = int(self.zone_id_plant.get('1.0', tk.END))
            data = (id, type, age, zone_id)
            self.controller.add_plant(data)
        except Exception as exc:
            self.add_plant_out = tk.Label(self.frame, text=exc, fg='#f60404')
            self.add_plant_out.grid(row=6, column=2, pady=10)
        else:
            self.add_plant_out = tk.Label(self.frame, text='Plant is added', fg='#008000')
            self.add_plant_out.grid(row=6, column=2, pady=10)

    def delete_plant(self):
        if self.del_plant_out:
            self.del_plant_out.destroy()
        try:
            id = int(self.id_delete_plant.get('1.0', tk.END))
            self.controller.delete_plant(id)
        except Exception as exc:
            self.del_plant_out = tk.Label(self.frame, text=exc, fg='#f60404')
            self.del_plant_out.grid(row=3, column=0, pady=10)
        else:
            self.del_plant_out = tk.Label(self.frame, text=f'Plant is deleted', fg='#008000')
            self.del_plant_out.grid(row=3, column=0, pady=10)

    def add_new_worker(self):
        if self.add_work_out:
            self.add_work_out.destroy()
        try:
            id = int(self.status_new_work.get('1.0', tk.END))
            name = self.name_new_work.get('1.0', tk.END)[:-1]
            tel = self.tel_new_work.get('1.0', tk.END)[:-1]
            address = self.address_new_work.get('1.0', tk.END)[:-1]
            birthdate = self.birth_work.get('1.0', tk.END)[:-1]
            data = (id, name, tel, address, birthdate)
            self.controller.add_worker(data)
        except Exception as exc:
            self.add_work_out = tk.Label(self.frame, text=exc, fg='#f60404')
            self.add_work_out.grid(row=7, column=2, pady=10)
        else:
            self.add_work_out = tk.Label(self.frame, text='Worker is added', fg='#008000')
            self.add_work_out.grid(row=7, column=2, pady=10)
    
    def delete_worker(self):
        if self.del_work_out:
            self.del_work_out.destroy()
        try:
            id = int(self.id_delete_work.get('1.0', tk.END))
            self.controller.delete_worker(id)
        except Exception as exc:
            self.del_work_out = tk.Label(self.frame, text=exc, fg='#f60404')
            self.del_work_out.grid(row=3, column=0, pady=10)
        else:
            self.del_work_out = tk.Label(self.frame, text=f'Worker is deleted', fg='#008000')
            self.del_work_out.grid(row=3, column=0, pady=10)

    def see_greenplaces_info(self):
        self.clean_up_frame()
        data = self.controller.get_greenplaces_info()
        self.parent.title('Найти информацию о насаждениях')
        col_names = ['ID', 'Вид', 'Дата высадки', 'Возраст', 'Зона', 'Парк']
        create_table(self.frame, data, col_names)
        self.plant_type = bind_textbox(self.frame, 'Введите вид...', size=(2, 30))
        self.plant_type.grid(row=len(data) + 2, column=1, pady=20)
        ttk.Button(self.frame, text='Искать высадку', command=self.search_plants).grid(row=len(data) + 2, column=4, pady=20)
        ttk.Button(self.frame, text='Выйти в главное меню', command=self.start_menu).grid(row=len(data) + 3, column=1, pady=20)

    def search_plants(self):
        plant_type_text = self.plant_type.get('1.0', tk.END)[:-1]
        self.clean_up_frame()
        data = self.controller.search_plants(plant_type_text)
        col_names = ['ID', 'Вид', 'Дата высадки', 'Возраст', 'Зона', 'Парк']
        create_table(self.frame, data, col_names)
        self.plant_type = bind_textbox(self.frame, 'Введите вид...', size=(2, 30))
        self.plant_type.grid(row=len(data) + 2, column=1, pady=20)
        ttk.Button(self.frame, text='Искать высадку', command=self.search_plants).grid(row=len(data) + 2, column=4, pady=20)
        ttk.Button(self.frame, text='Выйти в главное меню', command=self.start_menu).grid(row=len(data) + 3, column=1, pady=20)

    def set_controller(self, controller):
        self.controller = controller

    def exit(self):
        self.frame.destroy()
        exit(0)

    def clean_up_frame(self):
        for widg in self.frame.winfo_children():
            widg.destroy()


