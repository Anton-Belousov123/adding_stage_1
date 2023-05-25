import time

import db
import ozon


def main():
    table_name = 'oleg'
    while True:
        table_name = 'kamran' if table_name == 'oleg' else 'oleg'
        element = db.get_element(table_name)

        if element is None:  # If not elements in order
            table_name = 'kamran' if table_name == 'oleg' else 'oleg'
            element = db.get_element(table_name)
            if element is None:
                time.sleep(60)
                continue

        if ozon.test_upload_is_ok(element[0], element[1], element[2]):
            ozon.upload_to_main(element[0], element[1], element[2], table_name)
            db.change_status(table_name, element, 'uploaded_by_copy')
        else:
            db.change_status(table_name, element, 'upload_error_by_copy')


if __name__ == '__main__':
    main()
