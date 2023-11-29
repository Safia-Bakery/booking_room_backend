from fastapi import FastAPI
from routers.api import router


app = FastAPI(
    title="Book Meeting"
)
# metadata.create_all(engine)
# app.state.database = database


# @app.on_event("startup")
# async def startup() -> None:
#     database_ = app.state.database
#     if not database_.is_connected:
#         await database_.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown() -> None:
#     database_ = app.state.database
#     if database_.is_connected:
#         await database_.disconnect()


app.include_router(router)
