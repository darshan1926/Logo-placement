from fastapi import APIRouter

router = APIRouter(
    tags=["ping"],
)


@router.get("/", include_in_schema=False)
def read_root():
    return "Welcome: IMAGE MANIPULATION PROJECT : )"


@router.get("/ping")
def ping_app():
    return True