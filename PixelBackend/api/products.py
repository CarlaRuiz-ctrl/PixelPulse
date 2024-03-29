from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from PixelBackend import schemas, models
from PixelBackend.database import get_db
from PixelBackend import OAuth

router = APIRouter()


@router.get("/products", response_model=list[schemas.Product])
def get_products(
    db: Session = Depends(get_db),
    current_user=Depends(OAuth.get_current_user),
    request: Request = None,
):
    """Get all products from the database.

    Args:
        db (Session): The database session.

    Returns:
        list[schemas.ProductResponse]: A list of all products in the database.
    """
    category = request.query_params.get("category")
    search_string = request.query_params.get("search_string")
    try:
        if search_string:
            products = (
                db.query(models.Product)
                .filter(models.Product.name.ilike(f"%{search_string}%"))
                .all()
            )
        elif not category:
            products = db.query(models.Product).all()
        else:
            products = db.query(models.Product).filter_by(category=category).all()

    except Exception:
        print("Error occurred while fetching products from the database.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while fetching products from the database.",
        )

    try:
        if not category:
            products = db.query(models.Product).all()
        else:
            products = db.query(models.Product).filter_by(category=category).all()

    except Exception:
        print("Error occurred while fetching products from the database.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while fetching products from the database.",
        )
    if not products:
        print("No products found in the database.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found in the database.",
        )

    return products
