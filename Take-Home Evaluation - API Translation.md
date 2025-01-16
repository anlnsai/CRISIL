#### Instructions
For this take-home, you'll explore the given API surface to answer specific questions and propose enhancements for clarity and accessibility. Your task is to use the following subset of the API endpoints to address the questions below, followed by conceptualizing improvements to the API design.

#### API Subset:

1. **Agency Data**:
    
    - [`/api/v2/agency/<TOPTIER_AGENCY_CODE>/sub_agency/`](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/agency/toptier_code/sub_agency.md)
    - [`/api/v2/agency/<TOPTIER_AGENCY_CODE>/awards/new/count/`](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/agency/toptier_code/awards/new/count.md)
    - [`/api/v2/agency/<TOPTIER_AGENCY_CODE>/budgetary_resources/`](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/agency/toptier_code/budgetary_resources.md)
    - [`/api/v2/agency/<TOPTIER_AGENCY_CODE>/program_activity/`](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/agency/toptier_code/program_activity.md)
    - [`/api/v2/agency/<TOPTIER_AGENCY_CODE>/object_class/`](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/agency/toptier_code/object_class.md)
2. **State Data**:
    
    - [`/api/v2/recipient/state/`](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/recipient/state/fips.md)
    - [`/api/v2/recipient/state/awards/<FIPS>/`](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/recipient/state/awards/fips.md)
3. **References**:
    
    - [`/api/v2/references/toptier_agencies/`](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/references/toptier_agencies.md)
    - [`/api/v2/references/glossary/`](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/references/glossary.md)
    - [`/api/v2/references/naics/`](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/references/naics/code.md)
4. **Other/Contextual Data**:
    
    - [`/api/v2/disaster/overview/`](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/disaster/overview.md)
    - [`/api/v2/federal_accounts/<ACCOUNT_CODE>/`](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/federal_accounts/account_number.md)
#### Example:
**What sub-agencies report to the USDA, and what were their funding allocations in 2023?**
```python
import requests

def get_toptier_code_from_abbreviation(abbreviation):
	# Endpoint to get top tier agencies
	url = "https://api.usaspending.gov/api/v2/references/toptier_agencies/"
	response = requests.get(url)
	response.raise_for_status()
	data = response.json()
	
	# Loop through the list to find USDA's top tier agency code
	for agency in data['results']:
		if agency['abbreviation'] == abbreviation:
			return agency['toptier_code']
	
	raise ValueError(f"No top tier agency found for abbreviation:{abbreviation}")

def get_sub_agencies(toptier_agency_code, year=None):
	# Base URL for sub-agencies
	base_url = f"https://api.usaspending.gov/api/v2/agency/{toptier_agency_code}/sub_agency/"
	# If a year is provided, include it in the query parameters
	if year:
		params = {'fiscal_year': year}
		url = f"{base_url}?fiscal_year={year}"
	else:
		url = base_url
		response = requests.get(url)
		response.raise_for_status()
	return response.json()

  
usda_code = get_toptier_code_from_abbreviation("USDA")
usda_sub_agencies = get_sub_agencies(usda_code, year=2023)
for sub_agency in usda_sub_agencies["results"]:
	print(f {sub_agency['name']}\n{sub_agency['abbreviation']})\n{sub_agency['total_obligatins']}\n")
```
#### Questions:
1. **What was the average loan amount to Texas in FY 2019?**
    
2. **Which state had the highest grant value per resident in the US in 2023?**
    
3. **What is the total budget resources available versus the new awards distribution ratio for NASA in FY 2024?**
    

#### API Improvement Proposal:

Consider the questions above and reflect on how the API structure may be enhanced for better usability. Discuss the following:

1. **New Routes**: Propose new API endpoints or optimized paths that use the outputs of existing routes as inputs, making frequently asked queries more straightforward.
    
2. **Renaming Input Parameters**: Suggest renaming any input parameters that could be more intuitive or consistent across the API.
    
3. **Output Data Format Adjustments**: Recommend any changes to the output data format to ensure clarity and ease of use for clients consuming the API.
    
4. **Documentation Enhancements**: Identify areas in the existing API where documentation can be improved to clarify endpoint functionality and parameters.

No code is required for this section. Please share a list of suggested changes and brief descriptions of the reasoning behind them.

---

### Submission Guidelines:

Please provide your responses in a structured document, with each question and proposal clearly outlined. For the practical tasks, include any code you use to interact with the API and manipulate their responses. For the proposal, a brief explanation with examples is sufficient to illustrate your suggestions.

During our in-person discussion, you will have the opportunity to present your approach to addressing the queries and to share your proposed suggestions for enhancing the API.