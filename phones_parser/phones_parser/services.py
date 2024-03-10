def xpath_lookup_filter(value: str) -> str:
    return f"//dt[span[contains(text(), '{value}')]]/following-sibling::dd"