from urllib.parse import urlparse, parse_qs

country_mapping = {
    "US": "United States",
    "CA": "Canada",
    "DE": "Germany",
    "GB": "United Kingdom",
    "FR": "France",
    "NL": "Netherlands",
    "ID": "Indonesia",
    "VN": "Vietnam",
    "SG": "Singapore",
    "JP": "Japan",
    "KR": "South Korea",
    "BR": "Brazil",
    "AR": "Argentina",
    "ZA": "South Africa",
    "KE": "Kenya",
    "AU": "Australia",
    "AE": "United Arab Emirates",
    "SA": "Saudi Arabia"
}

country_short_to_region = {
    "AF": "Asia",
    "AX": "Europe",
    "AL": "Europe",
    "DZ": "Africa",
    "AS": "Oceania",
    "AD": "Europe",
    "AO": "Africa",
    "AI": "North America",
    "AQ": "Antarctica",
    "AG": "North America",
    "AR": "South America",
    "AM": "Asia",
    "AW": "North America",
    "AU": "Oceania",
    "AT": "Europe",
    "AZ": "Asia",
    "BS": "North America",
    "BH": "Asia",
    "BD": "Asia",
    "BB": "North America",
    "BY": "Europe",
    "BE": "Europe",
    "BZ": "North America",
    "BJ": "Africa",
    "BM": "North America",
    "BT": "Asia",
    "BO": "South America",
    "BA": "Europe",
    "BW": "Africa",
    "BV": "Antarctica",
    "BR": "South America",
    "IO": "Asia",
    "BN": "Asia",
    "BG": "Europe",
    "BF": "Africa",
    "BI": "Africa",
    "KH": "Asia",
    "CM": "Africa",
    "CA": "North America",
    "CV": "Africa",
    "KY": "North America",
    "CF": "Africa",
    "TD": "Africa",
    "CL": "South America",
    "CN": "Asia",
    "CX": "Asia",
    "CC": "Asia",
    "CO": "South America",
    "KM": "Africa",
    "CG": "Africa",
    "CD": "Africa",
    "CK": "Oceania",
    "CR": "North America",
    "CI": "Africa",
    "HR": "Europe",
    "CU": "North America",
    "CY": "Asia",
    "CZ": "Europe",
    "DK": "Europe",
    "DJ": "Africa",
    "DM": "North America",
    "DO": "North America",
    "EC": "South America",
    "EG": "Africa",
    "SV": "North America",
    "GQ": "Africa",
    "ER": "Africa",
    "EE": "Europe",
    "ET": "Africa",
    "FK": "South America",
    "FO": "Europe",
    "FJ": "Oceania",
    "FI": "Europe",
    "FR": "Europe",
    "GF": "South America",
    "PF": "Oceania",
    "TF": "Antarctica",
    "GA": "Africa",
    "GM": "Africa",
    "GE": "Asia",
    "DE": "Europe",
    "GH": "Africa",
    "GI": "Europe",
    "GR": "Europe",
    "GL": "North America",
    "GD": "North America",
    "GP": "North America",
    "GU": "Oceania",
    "GT": "North America",
    "GG": "Europe",
    "GN": "Africa",
    "GW": "Africa",
    "GY": "South America",
    "HT": "North America",
    "HM": "Antarctica",
    "VA": "Europe",
    "HN": "North America",
    "HK": "Asia",
    "HU": "Europe",
    "IS": "Europe",
    "IN": "Asia",
    "ID": "Asia",
    "IR": "Asia",
    "IQ": "Asia",
    "IE": "Europe",
    "IM": "Europe",
    "IL": "Asia",
    "IT": "Europe",
    "JM": "North America",
    "JP": "Asia",
    "JE": "Europe",
    "JO": "Asia",
    "KZ": "Asia",
    "KE": "Africa",
    "KI": "Oceania",
    "KP": "Asia",
    "KR": "Asia",
    "KW": "Asia",
    "KG": "Asia",
    "LA": "Asia",
    "LV": "Europe",
    "LB": "Asia",
    "LS": "Africa",
    "LR": "Africa",
    "LY": "Africa",
    "LI": "Europe",
    "LT": "Europe",
    "LU": "Europe",
    "MO": "Asia",
    "MK": "Europe",
    "MG": "Africa",
    "MW": "Africa",
    "MY": "Asia",
    "MV": "Asia",
    "ML": "Africa",
    "MT": "Europe",
    "MH": "Oceania",
    "MQ": "North America",
    "MR": "Africa",
    "MU": "Africa",
    "YT": "Africa",
    "MX": "North America",
    "FM": "Oceania",
    "MD": "Europe",
    "MC": "Europe",
    "MN": "Asia",
    "ME": "Europe",
    "MS": "North America",
    "MA": "Africa",
    "MZ": "Africa",
    "MM": "Asia",
    "NA": "Africa",
    "NR": "Oceania",
    "NP": "Asia",
    "NL": "Europe",
    "AN": "North America",
    "NC": "Oceania",
    "NZ": "Oceania",
    "NI": "North America",
    "NE": "Africa",
    "NG": "Africa",
    "NU": "Oceania",
    "NF": "Oceania",
    "MP": "Oceania",
    "NO": "Europe",
    "OM": "Asia",
    "PK": "Asia",
    "PW": "Oceania",
    "PS": "Asia",
    "PA": "North America",
    "PG": "Oceania",
    "PY": "South America",
    "PE": "South America",
    "PH": "Asia",
    "PN": "Oceania",
    "PL": "Europe",
    "PT": "Europe",
    "PR": "North America",
    "QA": "Asia",
    "RE": "Africa",
    "RO": "Europe",
    "RU": "Europe",
    "RW": "Africa",
    "BL": "North America",
    "SH": "Africa",
    "KN": "North America",
    "LC": "North America",
    "MF": "North America",
    "PM": "North America",
    "VC": "North America",
    "WS": "Oceania",
    "SM": "Europe",
    "ST": "Africa",
    "SA": "Asia",
    "SN": "Africa",
    "RS": "Europe",
    "SC": "Africa",
    "SL": "Africa",
    "SG": "Asia",
    "SK": "Europe",
    "SI": "Europe",
    "SB": "Oceania",
    "SO": "Africa",
    "ZA": "Africa",
    "GS": "Antarctica",
    "ES": "Europe",
    "LK": "Asia",
    "SD": "Africa",
    "SR": "South America",
    "SJ": "Europe",
    "SZ": "Africa",
    "SE": "Europe",
    "CH": "Europe",
    "SY": "Asia",
    "TW": "Asia",
    "TJ": "Asia",
    "TZ": "Africa",
    "TH": "Asia",
    "TL": "Asia",
    "TG": "Africa",
    "TK": "Oceania",
    "TO": "Oceania",
    "TT": "North America",
    "TN": "Africa",
    "TR": "Asia",
    "TM": "Asia",
    "TC": "North America",
    "TV": "Oceania",
    "UG": "Africa",
    "UA": "Europe",
    "AE": "Asia",
    "GB": "Europe",
    "US": "North America",
    "UM": "Oceania",
    "UY": "South America",
    "UZ": "Asia",
    "VU": "Oceania",
    "VE": "South America",
    "VN": "Asia",
    "VG": "North America",
    "VI": "North America",
    "WF": "Oceania",
    "EH": "Africa",
    "YE": "Asia",
    "ZM": "Africa",
    "ZW": "Africa"
}


def extract_url_params(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    return query_params

