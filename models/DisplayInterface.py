import json


class ApplicationState:
    """ Класс хранит переменные состояния приложения """

    def __init__(self):
        self.host = None
        self.start_offset = None
        self.end_offset = None
        self.result_data = None  # Данные из 'crpt.billing.operation.sync'
        self.unpaid_values = None  # Данные из 'crpt.billing.skipped.backup'
        self.once_again = None  # Повторить поиск
        self.data_for_file = ''  # Хранит форматированый вывод для записи в фаил

    def save_in_file(self):
        with open('result-out.txt', 'w+') as f:
            self._erase_file(f)
            f.write(self.data_for_file)

        print('\n\nThe search results are saved to a file "result-out.txt"\n')

    @staticmethod
    def _erase_file(file):
        if file.read() != '':
            file.write('')


class DisplayInterface(ApplicationState):
    """ Предоставляет методы для работы с интерфейсом приложения """

    def __init__(self):
        super().__init__()
        self._welcome_message()
        self._input_host()
        self._input_start_offset()
        self._input_end_offset()

    @staticmethod
    def create():
        return DisplayInterface()

    @staticmethod
    def _welcome_message():
        print(logo + '\n')

    def _input_host(self):
        self.host = input('Kafka Host(no port):\n>>> ') + ':9092'
        if self.host == ':9092':
            self.host = input('kafka host(no port):\n>>> ') + ':9092'

    def _input_start_offset(self):
        try:
            self.start_offset = int(input('start offset:\n>>> '))
        except ValueError:
            print('Error! Это не число.')

    def _input_end_offset(self):
        try:
            self.end_offset = int(input('end offset:\n>>> '))
        except ValueError:
            print('Error! Это не число.')

    def display_result(self) -> None:
        """ Ф-ия выводит в нужном для OffsetExplorer виде данные для переотправки """

        try:
            for item in self.result_data:
                result_string = f'{item[0]}={json.dumps(item[1])}'
                self.data_for_file += str(result_string) + '\n'
                print(result_string)

        except TypeError as ex:
            print(ex)
            pass

    @staticmethod
    def _print_error_message(message):
        print(message)

    def again(self):
        response = input('Again?(y/n):\n>>> ')

        if response == 'y':
            self.once_again = True
        else:
            self.once_again = False


logo = """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░██████████████████████████████████████░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░██████░░██████░░██████░░██████░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░██░░░░░░██░░██░░██░░██░░░░██░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░██░░░░░░██████░░██████░░░░██░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░██░░░░░░████░░░░██░░░░░░░░██░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░██████░░██░░██░░██░░░░░░░░██░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░██████████████████████████████████████░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ unpaid-parser ver 0.1"""
