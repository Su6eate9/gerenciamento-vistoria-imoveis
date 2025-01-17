def find_by_id_orm(model, id):
    """
    Busca um registro por ID usando SQLAlchemy.
    """
    return model.query.get(id)
