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

    with open(args.BRUTO, 'r', encoding="utf-8") as file:
        # Getting data from file
        raw_content = json.load(file)

    # Get users from database
    users = utils.get_users_from_db(args.TELEFONE)

    #  Generate report
    for user in users:
        report = utils.generate_pdf_report(raw_content, user, args.DATA)
        # Send email
        if args.ENVIA_EMAIL is True:
            utils.send_email(user=user, report=report, date=args.DATA)


if __name__ == "__main__":
    main()
