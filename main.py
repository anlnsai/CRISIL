import json
import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
cache = {}


def cache_result(func):
    def wrapper(*args, **kwargs):
        global cache
        key = func.__name__ + str(args) + str(kwargs)
        try:
            if not cache:
                with open('cache.json', 'r') as f:
                    cache = json.load(f)
            if key in cache:
                return cache[key]
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        result = func(*args, **kwargs)
        with open('cache.json', 'w') as cache_file:
            cache[key] = result
            json.dump(cache, cache_file)

        return result

    return wrapper


BASE_URL = config.get("URL", "BaseURL")


def get_request(endpoint: str, dataFormat=True):
    url = BASE_URL + endpoint
    response = requests.get(url)
    response.raise_for_status()
    data = response

    if dataFormat:
        data = response.json()

    return data


def get_states_data() -> dict:
    return get_request("/api/v2/recipient/state/")


@cache_result
def get_state_data(fips_code: int) -> dict:
    return get_request(f"/api/v2/recipient/state/{fips_code}")


def get_fips_code(state_name: str) -> int:
    data = get_states_data()

    for state in data:
        if state.get('name') == state_name:
            return state.get('fips')

    raise ValueError(f"No FIPS code found for state:{state_name}")


@cache_result
def get_awards_data(fips_code: int, year: int) -> dict:
    return get_request(f"/api/v2/recipient/state/awards/{fips_code}/?fiscal_year={year}")


# What was the average loan amount to Texas in FY 2019?
def average_loan_amount(state: str, year: int) -> float:
    fips = get_fips_code(state)
    awards_data = get_awards_data(fips, year)
    total_loan_amount = 0
    total_loans = 0

    for award in awards_data:
        if award.get('type') == 'loans':
            total_loan_amount += award.get('amount')
            total_loans += 1
    if total_loans:
        return total_loan_amount / total_loans
    return total_loans


# Which state had the highest grant value per resident in the US in 2023?
def calculate_grant_value_per_resident(awards_data: dict, population: int) -> float:
    total_grant_amount = 0
    for award in awards_data:
        if award['type'] == 'grants':
            total_grant_amount += award['amount']
    if population:
        return total_grant_amount / population
    return population


def find_state_with_highest_grant_value_per_resident(year: int) -> str:
    states_data = get_states_data()
    highest_grant_value_per_resident = 0
    state_with_highest_grant_value_per_resident = ""
    for state in states_data:
        fips_code = state.get('fips')
        awards_data = get_awards_data(fips_code, year)
        population = get_state_data(fips_code).get('population')
        population = int(population) if population else 0
        grant_value_per_resident = calculate_grant_value_per_resident(awards_data, population)
        if grant_value_per_resident > highest_grant_value_per_resident:
            highest_grant_value_per_resident = grant_value_per_resident
            state_with_highest_grant_value_per_resident = state.get('name')

    return state_with_highest_grant_value_per_resident


# What is the total budget resources available versus the new awards distribution ratio for NASA in FY 2024?
@cache_result
def get_toptier_code(abbreviation: str) -> int:
    data = get_request("/api/v2/references/toptier_agencies/")

    for agency in data.get('results'):
        if agency.get('abbreviation') == abbreviation:
            return agency.get('toptier_code')

    raise ValueError(f"No top tier agency found for abbreviation:{abbreviation}")


@cache_result
def get_budgetary_resources(toptier_agency_code: int, year: int) -> float:
    data = get_request(f"/api/v2/agency/{toptier_agency_code}/budgetary_resources/")

    for row in data.get('agency_data_by_year'):
        if row.get('fiscal_year') == year:
            return row.get('total_budgetary_resources')
    return 0.0


@cache_result
def get_new_awards_distribution_ratio(toptier_agency_code: int, year: int) -> int:
    return get_request(
        f"/api/v2/agency/{toptier_agency_code}/awards/new/count/?fiscal_year={year}"
    ).get('new_award_count')


if __name__ == '__main__':
    print("The average loan amount to Texas in FY 2019 was:", average_loan_amount("Texas", 2019))
    print(find_state_with_highest_grant_value_per_resident(2023),
          "state had the highest grant value per resident in the US in 2023")

    nasa_code = get_toptier_code("NASA")
    total_budget_resources = get_budgetary_resources(nasa_code, 2024)
    new_awards_distribution_ratio = get_new_awards_distribution_ratio(nasa_code, 2024)
    print(f"The total budget resources available for NASA in FY 2024 is: {total_budget_resources}")
    print(f"The new awards distribution ratio for NASA in FY 2024 is: {new_awards_distribution_ratio}")
