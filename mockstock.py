from app import app, db
from app.models import  Stock ,Portfolio , User, Transaction, UserStock



# Adds context to the python interpreter, allowing for ease of database usage
@app.shell_context_processor
def make_shell_context():
    """
    Returns: models for the database to use with the context.
    """
    return {'db': db, 'User': User, 'Portfolio': Portfolio, 'Stock': Stock, 'Transaction': Transaction, 'UserStock':UserStock}
