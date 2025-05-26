from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ..services.enquiry_service import save_enquiry_data

router = APIRouter()

@router.post("/enquiry")
async def submit_enquiry(
    email_to: str = Form(...),
    subject: str = Form(...),
    email_address: str = Form(...),
    company_name: str = Form(None),
    contact_number: str = Form(None),
    description: str = Form(None),
    attachment: UploadFile = File(None)
):
    try:
        file_data = await attachment.read() if attachment else None
        save_enquiry_data(email_to, subject, email_address, company_name, contact_number, description, file_data)
        return {"message": "Enquiry submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
