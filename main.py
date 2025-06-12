from fastapi import FastAPI
from app.routers import item_data_router, login_router, enquiry, register,designation_router ,role_router,item_router,location_reg_router,equipment_reg_router,update_user_router, delete_user_router, update_item_router, delete_item_router,bookmark_router
from pyngrok import ngrok
import uvicorn
import nest_asyncio
from fastapi.middleware.cors import CORSMiddleware
from app.routers.location_router import router as location_router
from app.routers.user_router import router as user_router
from app.routers.equipment_router import router as equipment_router
from app.routers.notification_router import router as notification_router
from app.routers.current_status_router import router as current_status_router
from app.routers.sub_group_router import router as sub_group_router
from app.routers.my_profile import router as my_profile_router
from app.routers import remark_router, remark_data_router, remark_comment_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.include_router(item_data_router.router)
app.include_router(item_data_router.router)
app.include_router(equipment_router)
app.include_router(equipment_reg_router.router)
app.include_router(login_router.router)
app.include_router(enquiry.router)
app.include_router(location_router)
app.include_router(location_reg_router.router)
app.include_router(register.router)
app.include_router(user_router)
app.include_router(role_router.router)
app.include_router(designation_router.router)
app.include_router(item_router.router)
app.include_router(update_user_router.router)
app.include_router(delete_user_router.router)
app.include_router(update_item_router.router)
app.include_router(delete_item_router.router)
app.include_router(notification_router)
app.include_router(bookmark_router.router)
app.include_router(current_status_router)
app.include_router(sub_group_router)
app.include_router(my_profile_router)
app.include_router(remark_router.router)
app.include_router(remark_data_router.router)
app.include_router(remark_comment_router.router)



if __name__ == "__main__":
  port = 8000
  ngrok_tunnel = ngrok.connect(port)
  print('Public URL:', ngrok_tunnel.public_url)
  nest_asyncio.apply()
  uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)