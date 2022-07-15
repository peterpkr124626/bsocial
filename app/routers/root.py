from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Root"])


@router.get("/")
def display_message():
    return {"message": "Welcome to BSocial created by Shubham Patel."}
