import re

def extract_numbers(text: str):
    '''
        Extracts numbers from the string
    '''
    matches = re.findall(r'\d+', text)
    return [int(num) for num in matches]


if __name__ == "__main__":
    S = "The mangoes cost Rs.25 and oranges cost Rs.400"
    print(extract_numbers(S))
