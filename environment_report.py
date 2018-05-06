from multiprocessing import Manager, Process
from tpf_60 import sensing
from stat_calc import calc_statistics

class EnvironmentReport:
    
    def __init__(self, image_file=None, manager=None, data_polling_time=None, data_limit=None, data_timeout=None):
        
        if not manager:
            manager = Manager()
            
        self.temperature_data = manager.list()
        self.pressure_data = manager.list()
        self.humidity_data = manager.list()
    
        self.temperature_statistics = manager.dict()
        self.pressure_statistics = manager.dict()
        self.humidity_statistics = manager.dict()
        
        self.data_polling = data_polling_time
        self.data_timeout = data_timeout
        self.data_limit = data_limit
    
        self.calculate_condition = manager.Condition()
    
        self.image_file = image_file
        
    def setup(self):
        sensor = Process(target=sensing, args=(self.temperature_data, self.pressure_data,
                                               self.humidity_data, self.data_polling,
                                               self.data_limit, self.data_timeout,
                                               self.calculate_condition), daemon=True)
        sensor.start()

        calc_stat = Process(target=calc_statistics, kwargs=dict(temperature_data=self.temperature_data,
                                                                temperature_statistics=self.temperature_statistics,
                                                                pressure_data=self.pressure_data,
                                                                pressure_statistics=self.pressure_statistics,
                                                                humidity_data=self.humidity_data,
                                                                humidity_statistics=self.humidity_statistics,
                                                                condition_flag=self.calculate_condition),
                                                                daemon=True)
        calc_stat.start()