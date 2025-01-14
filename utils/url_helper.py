from faker import Faker

def get_random_category_url(base_url="https://www.varoom.com/all/"):
    """
    Generates a random category URL by appending a random country to the base URL.

    Args:
        base_url (str): The base URL for the category page.

    Returns:
        str: A complete category page URL with a random country.
    """
    faker = Faker()
    country = faker.country().replace(" ", "-").lower()  # Replace spaces with dashes for URL compatibility
    return f"{base_url}{country}"
