from typing import Literal, Optional

from fastapi import APIRouter, HTTPException

from app import models, schemas
from app.auth import db_dependency, user_dependency

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_own_transaction(transaction_id: int, db, user):
    txn = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.id == transaction_id,
            models.Transaction.owner_id == user.id,
        )
        .first()
    )
    if txn is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn


@router.post("", response_model=schemas.TransactionOut, status_code=201)
def create_transaction(payload: schemas.TransactionCreate, db: db_dependency, user: user_dependency):
    txn = models.Transaction(**payload.model_dump(), owner_id=user.id)
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


@router.get("", response_model=list[schemas.TransactionOut])
def get_all_transactions(db: db_dependency, user: user_dependency):
    return db.query(models.Transaction).filter(models.Transaction.owner_id == user.id).all()


# Must stay ABOVE "/{transaction_id}", otherwise "filter" is read as an id
@router.get("/filter", response_model=list[schemas.TransactionOut])
def filter_transactions(
    db: db_dependency,
    user: user_dependency,
    type: Optional[Literal["income", "expense"]] = None,
    category: Optional[str] = None,
    minimum_amount: Optional[float] = None,
    maximum_amount: Optional[float] = None,
):
    query = db.query(models.Transaction).filter(models.Transaction.owner_id == user.id)

    if type is not None:
        query = query.filter(models.Transaction.type == type)
    if category is not None:
        query = query.filter(models.Transaction.category.ilike(category))
    if minimum_amount is not None:
        query = query.filter(models.Transaction.amount >= minimum_amount)
    if maximum_amount is not None:
        query = query.filter(models.Transaction.amount <= maximum_amount)

    return query.all()


@router.get("/{transaction_id}", response_model=schemas.TransactionOut)
def get_transaction(transaction_id: int, db: db_dependency, user: user_dependency):
    return get_own_transaction(transaction_id, db, user)


@router.put("/{transaction_id}", response_model=schemas.TransactionOut)
def update_transaction(
    transaction_id: int,
    payload: schemas.TransactionUpdate,
    db: db_dependency,
    user: user_dependency,
):
    txn = get_own_transaction(transaction_id, db, user)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(txn, key, value)
    db.commit()
    db.refresh(txn)
    return txn


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: db_dependency, user: user_dependency):
    txn = get_own_transaction(transaction_id, db, user)
    db.delete(txn)
    db.commit()
    return {"message": "Transaction deleted successfully"}