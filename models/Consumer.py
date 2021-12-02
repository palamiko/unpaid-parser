import json

from kafka import TopicPartition, KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from kafka.errors import NoBrokersAvailable
from kafka.structs import OffsetAndTimestamp
from munch import DefaultMunch

from ValueModels import ValueCharge, ValuePayment


class Consumer:

    def __init__(self, host):
        self._host = host
        self._undefined = object()

        try:
            self.consumer = KafkaConsumer(
                bootstrap_servers=[self._host],
                value_deserializer=lambda m: json.loads(m.decode('ascii')))

        except NoBrokersAvailable:
            print('Error! Хост не доступен.')

    def find_unsent_messages(self, start_offset, end_offset) -> list[ValueCharge]:
        """ Ф-ия вытаскивает сообщения с did из топика 'crpt.billing.skipped.backup',
            принемает начальный и конечный офсет сообщений """

        tp_skipped_backup = TopicPartition(topic='crpt.billing.skipped.backup', partition=0)
        list_charge: list[ValueCharge] = []

        self.consumer.assign([tp_skipped_backup])
        self.consumer.seek(tp_skipped_backup, offset=start_offset)  # 427

        for messages in self.consumer:
            messages: ConsumerRecord

            # Парсит сообщение в класс
            value_charge: ValueCharge = DefaultMunch.fromDict(messages.value, self._undefined)

            list_charge.append(value_charge)

            if messages.offset == end_offset:
                break

        return list_charge

    def get_resent_values(self, start_timestamp: int, list_charge: list[ValueCharge]) -> list[list]:
        """ Функция выполняет поиск значений в топике 'crpt.billing.operation.sync'
            которые не были доставлены в ониму путем сравнения DID в списке сообщений
            который был получен из топика 'crpt.billing.skipped.backup', на вход принемает
            начальный timestamp с которог начинать поиск и список неотправленных DID """

        tp_operation_sync = TopicPartition(topic='crpt.billing.operations.sync', partition=0)
        list_payment: list[list] = []

        self.consumer.assign([tp_operation_sync])
        # Получает первый офсет из 'crpt.billing.operation.sync' за дату инцендента
        dict_offset_timestamp: dict[TopicPartition, OffsetAndTimestamp] \
            = self.consumer.offsets_for_times({tp_operation_sync: start_timestamp})

        # Получает OffsetAndTimestamp из dict
        offset_timestamp = dict_offset_timestamp.get(tp_operation_sync)

        self.consumer.seek(partition=tp_operation_sync, offset=offset_timestamp.offset)

        # Перебираем сообщения в топике
        for message in self.consumer:
            message: ConsumerRecord

            key = message.key.decode('UTF-8')
            # Парсит сообщение в класс
            value_payment: ValuePayment = DefaultMunch.fromDict(message.value, self._undefined)

            # Перебираем сообщения найденные в 'crpt.billing.skipped.backup' для сравнения с "operation.sync"
            for one_charge in list_charge:
                try:
                    # Если did сообщений совпадает, добавляем тело платежа в список
                    if value_payment.charge.id == one_charge.charge.id:

                        # Добавление в список платежей list, в котором ключ и значение
                        list_payment.append([key, value_payment])

                        # Если колличиство сообщений из первого топика равно второму то конец поиска
                        if len(list_charge) == len(list_payment):
                            self.consumer.close()
                            break

                except AttributeError:
                    pass

        return list_payment
