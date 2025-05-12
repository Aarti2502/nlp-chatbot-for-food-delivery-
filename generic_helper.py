import re

def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string

    return ""

def get_str_from_food_dict(food_dict: dict):
    result = ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
    return result


if __name__ == "main":
    print(extract_session_id("projects/mira-chatbot-for-food-del-cxoe/agent/sessions/11044347-aba6-49f2-432f-1572585fa369/contexts/ongoing-order"))
    pass