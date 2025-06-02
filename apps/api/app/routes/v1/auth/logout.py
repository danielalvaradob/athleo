from fastapi import APIRouter, Response

router = APIRouter()

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully."}