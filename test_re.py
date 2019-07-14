import re


"""
pattern = r"\bfix(s|es|d|ed)?\s*(#|issue|issues)?\s*\d+"
s = "This commit fixed "
print(re.search(pattern, s))
"""

s = """
    Do you    know \t?


    Yeah
    """

re.sub(r"\s+", " ", s)
print(s)
