from fastapi import APIRouter
from database import mongo_connection

router = APIRouter(
    prefix="/update",
    tags=["update"],
    responses={404: {"description": "Not found"}},
)


# update the status of the window
@router.put("/{isOpen}", status_code=205)
def root(isOpen: bool):
    """
    upgrade status of isOpen table in database
    """
    is_open = mongo_connection["Record"].find_one(
        {"isCommand": True}, {"isCommand": False, "_id": False}
    )["isOpen"]

    if is_open is isOpen:
        return {"message": f"already update command to {isOpen}"}

    mongo_connection["Record"].update_one(
        {"isCommand": True}, {"$set": {"isOpen": isOpen}}
    )
    return {"message": f"already set command to {isOpen}"}
