import os
import argparse
import json

import utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('TELEFONE', type=utils.validate_phone, help='Phone number(s), you can send one or more using this formats: 01234567891 or 01234567891,78945612348')
    parser.add_argument('DATA', type=utils.validate_date, help='Report date in format YYYY-MM-DDTHH:MM')
    parser.add_argument('--ENVIA_EMAIL', action='store_true', help='Flag to indicate if the report will be sent via email.')
    parser.add_argument('BRUTO', type=str, help='Path to the raw report file')

    args = parser.parse_args()

    phones = args.TELEFONE
    date = args.DATA
    send_email = args.ENVIA_EMAIL
    bruto_path = args.BRUTO

    print("Phones:", phones)
    print("Date:", date)
    print("Send email:", send_email)
    print("Bruto path:", bruto_path)

    with open(bruto_path, 'r', encoding="utf-8") as file:
        # Getting data from file
        raw_content = json.load(file)

    # Get users from database
    users = utils.get_users_from_db(phones)


    #  Generate report
    for user in users:
        
        # Send email
        if send_email is True:
            utils.send_email(user=user)


if __name__ == "__main__":
    main()
