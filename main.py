import sys

from models.Consumer import Consumer
from models.DisplayInterface import DisplayInterface

if __name__ == "__main__":
    while True:
        app_state = DisplayInterface.create()
        consumer = Consumer(host=app_state.host)

        app_state.unpaid_values = consumer.find_unsent_messages(
            start_offset=app_state.start_offset, end_offset=app_state.end_offset)
        app_state.result_data = consumer.get_resent_values(
            start_timestamp=app_state.unpaid_values[0].charge.date, list_charge=app_state.unpaid_values)

        app_state.display_result()

        if app_state.data_for_file != '':
            app_state.save_in_file()

        app_state.again()

        if app_state.once_again:
            pass
        else:
            consumer.consumer.unsubscribe()
            break
    sys.exit(0)
