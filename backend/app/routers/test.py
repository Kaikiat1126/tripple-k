from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.get("/test/", tags=["test"])
async def test_root():
    return {"message": "Test API Router"}