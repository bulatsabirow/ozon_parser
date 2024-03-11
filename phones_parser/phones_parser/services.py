def xpath_lookup_filter(value: str) -> str:
    """
    Looks up required HTML snippets by using its inner content (text() attribute in XPath)
    """
    return f"//dt[span[contains(text(), '{value}')]]/following-sibling::dd"
