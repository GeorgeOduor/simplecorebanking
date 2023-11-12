
def check_balance(transactions):
    if transactions.exists():
        latest_balance = transactions.latest('id').transaction_balance
    else:
        latest_balance = 0
    return latest_balance
    

def new_trx_balance(model,client,transaction_type,transaction_amount):
        transactions = model.objects.filter(client_id=client)
        if transactions.exists():
            # get the latest balance 
            latest_balance = transactions.latest('transaction_date').transaction_balance
            # if trx is deposit,add else subtract
            if transaction_type == 'CREDIT':
                balance = latest_balance + transaction_amount
            else:
                balance = latest_balance - transaction_amount
            return balance
        else:
            return transaction_amount

def generate_account_id(prefix, model, id_field, total_digits=13):
    """
    Generates an account ID based on the provided prefix, model, and ID field.

    Args:
        prefix (str): The prefix for the account ID.
        model (Model): The model to query for the latest account ID.
        id_field (str): The field name of the ID in the model.
        total_digits (int, optional): The total number of digits in the account ID. Defaults to 13.

    Returns:
        str: The generated account ID.

    Raises:
        ValueError: If the prefix is empty.

    """
    # Ensure the prefix is not empty
    if not prefix:
        raise ValueError("Prefix cannot be empty")

    # Calculate the length of the numeric part of the account ID
    numeric_part_length = total_digits - len(prefix)

    # Find the latest account ID in the database
    last_account = model.objects.order_by('-' + id_field).first()

    if last_account:
        last_id = getattr(last_account, id_field)
        
        if last_id.startswith(prefix):
            # Extract the numeric part of the last ID and increment it
            numeric_part = last_id[len(prefix):]
            new_numeric_part = str(int(numeric_part) + 1).zfill(numeric_part_length)
            new_account_id = prefix + new_numeric_part
        else:
            # If the last ID has a different prefix, start from 1
            new_account_id = prefix + '1'.zfill(numeric_part_length)
    else:
        # If no accounts exist yet, start with '1'
        new_account_id = prefix + '1'.zfill(numeric_part_length)

    return new_account_id
