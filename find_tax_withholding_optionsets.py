from bs4 import BeautifulSoup
import requests

american_states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
                   "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
                   "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
                   "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",
                   "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee",
                   "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming",
                   "Washington DC", "Puerto Rico", "American Samoa", "Guam", "Northern Mariana Islands", "US Virgin Islands"]


def soup_session(link):
    """BeautifulSoup session"""
    session = requests.Session()
    tax_withholding_link = session.get(link)
    soup = BeautifulSoup(tax_withholding_link.content, 'html.parser')
    return soup


def get_all_possible_optionset_values():
    possible_optionsets = []
    state_optionset_mapping = {}
    for state in american_states:
        state_optionset_mapping[state] = []

    for state in american_states:
        soup = soup_session("https://www.paycheckcity.com/calculator/dualsalary/" + state.lower().replace(" ", "-"))
        for div in soup.find_all('div', attrs={'class': 'input-wrapper'}):
            for state_optionsets in div.find_all('select',
                                                 id=lambda value: value and value.startswith("DynamicForm-1stateInfo")):
                for option in state_optionsets.find_all('option'):
                    option_found = option.text.strip().lower()
                    if option_found == 'yes' or option_found == 'no':
                        continue
                    if option_found not in possible_optionsets:
                        possible_optionsets.append(option_found)

                    state_optionset_mapping[state].append(option_found)

    print(state_optionset_mapping)
    print(possible_optionsets)
    print(len(possible_optionsets))


if __name__ == '__main__':
    get_all_possible_optionset_values()
