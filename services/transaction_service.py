from repositories import transaction_repo


def get_all(account_id: int) -> list[dict]:
    """Returns all transactions for an account, newest first"""
    return transaction_repo.get_all(account_id)


def filter_by_date(account_id: int, date: str) -> list[dict]:
    """
    Returns transactions on a specific date
    date format: YYYY-MM-DD
    """
    return transaction_repo.filter_by_date(account_id, date)


def filter_by_range(account_id: int, start_date: str, end_date: str) -> list[dict]:
    """
    Returns transactions between two dates (inclusive)
    Date format: YYYY-MM-DD
    """
    if start_date > end_date:
        return []
    return transaction_repo.filter_by_range(account_id, start_date, end_date)


def filter_by_type(account_id: int, type_: str) -> list[dict]:
    """
    Returns transactions of a given type
    type_: 'deposit', 'withdrawal', or 'transfer'
    """
    valid_types = ("deposit", "withdrawal", "transfer")
    if type_ not in valid_types:
        raise ValueError(f"Invalid type '{type_}'. Must be one of: {valid_types}")
    return transaction_repo.filter_by_type(account_id, type_)


def filter_by_category(account_id: int, category_name: str) -> list[dict]:
    """Returns transactions belonging to a given category (e.g. 'food', 'leisure')"""
    return transaction_repo.filter_by_category(account_id, category_name)


def sort_by_amount(account_id: int, order: str = "asc") -> list[dict]:
    """
    Returns all transactions sorted by amount
    order: 'asc' or 'desc'
    """
    if order not in ("asc", "desc"):
        raise ValueError("order must be 'asc' or 'desc'")
    return transaction_repo.sort_by_amount(account_id, order)


def get_by_month(account_id: int, year: int, month: int) -> list[dict]:
    """Returns all transactions for a specific month and year"""
    return transaction_repo.get_by_month(account_id, year, month)