#!/usr/bin/env python3
"""
phoneinfo - Look up info about a phone number from the terminal.

Usage:
    phoneinfo +260972693740
    phoneinfo 260972693740      # '+' is optional if the country code is included
    phoneinfo 0972693740 --region ZM   # local format needs a region
"""

import argparse
import sys

import phonenumbers
from phonenumbers import geocoder, carrier, timezone

TYPE_NAMES = {
    phonenumbers.PhoneNumberType.MOBILE: "Mobile",
    phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
    phonenumbers.PhoneNumberType.TOLL_FREE: "Toll Free",
    phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
    phonenumbers.PhoneNumberType.SHARED_COST: "Shared Cost",
    phonenumbers.PhoneNumberType.VOIP: "VoIP",
    phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
    phonenumbers.PhoneNumberType.PAGER: "Pager",
    phonenumbers.PhoneNumberType.UAN: "UAN",
    phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail",
    phonenumbers.PhoneNumberType.UNKNOWN: "Unknown",
}


def smart_parse(raw_number: str, region: str | None):
    """
    Try to parse a phone number even if the user didn't type a leading '+'.

    Order of attempts:
    1. As typed (handles '+2609...' and '002609...' style input).
    2. With '+' added in front (handles '2609...' - full number, missing '+').
    3. Using --region, if given (handles local-format numbers like '0972...').

    Returns the first result that parses as VALID. If nothing parses as
    valid, falls back to returning the first result that at least parses
    without error, so we can still report why it's invalid.
    """
    candidate = raw_number.strip()
    if candidate.startswith("00"):
        candidate = "+" + candidate[2:]

    attempts = []
    if candidate.startswith("+"):
        attempts.append((candidate, None))
    else:
        attempts.append(("+" + candidate, None))  # assume country code, missing '+'
        if region:
            attempts.append((candidate, region))  # local number + region

    first_parsed = None
    last_error = None
    for text, reg in attempts:
        try:
            parsed = phonenumbers.parse(text, reg)
        except phonenumbers.NumberParseException as e:
            last_error = e
            continue
        if first_parsed is None:
            first_parsed = parsed
        if phonenumbers.is_valid_number(parsed):
            return parsed

    if first_parsed is not None:
        return first_parsed
    raise last_error


def lookup(raw_number: str, region: str | None) -> int:
    try:
        number = smart_parse(raw_number, region)
    except phonenumbers.NumberParseException as e:
        print(f"Error parsing '{raw_number}': {e}", file=sys.stderr)
        print(
            "Tip: for local numbers (no country code), pass "
            "--region with a 2-letter country code (e.g. --region ZM).",
            file=sys.stderr,
        )
        return 1

    valid = phonenumbers.is_valid_number(number)
    possible = phonenumbers.is_possible_number(number)
    number_type = phonenumbers.number_type(number)

    e164 = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
    international = phonenumbers.format_number(
        number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
    )

    print(f"Number:        {e164}")
    print(f"Formatted:     {international}")
    print(f"Valid number:  {valid}")
    if not valid:
        print(f"Possible:      {possible}")
    print(f"Country:       {geocoder.description_for_number(number, 'en') or 'Unknown'}")
    print(f"Carrier:       {carrier.name_for_number(number, 'en') or 'Unknown'}")
    tzs = timezone.time_zones_for_number(number)
    print(f"Timezone:      {', '.join(tzs) if tzs else 'Unknown'}")
    print(f"Type:          {TYPE_NAMES.get(number_type, 'Other')}")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="phoneinfo",
        description="Look up validity, carrier, country, timezone, and type for a phone number.",
    )
    parser.add_argument(
        "number",
        help="Phone number to look up, e.g. +260972693740 or just 260972693740",
    )
    parser.add_argument(
        "-r",
        "--region",
        default=None,
        help=(
            "2-letter region code to assume if the number has no country code "
            "(e.g. ZM for Zambia, US for United States)"
        ),
    )
    args = parser.parse_args()
    return lookup(args.number, args.region)


if __name__ == "__main__":
    sys.exit(main())
