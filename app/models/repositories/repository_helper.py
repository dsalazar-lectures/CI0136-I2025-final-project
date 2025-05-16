def safe_execute(func, fallback=None, context=""):
    """
    Helper function to safely execute a function with error handling.

    Args:
        func (callable): The function to execute.
        fallback (any): The value to return if an exception occurs.
        context (str): Optional context to print in the error message.

    Returns:
        The result of the function if no exception occurs, otherwise the fallback value.
    """
    try:
        return func()
    except Exception as e:
        print(f"[RepositoryHelper]{context} Error: {e}")
        return fallback
