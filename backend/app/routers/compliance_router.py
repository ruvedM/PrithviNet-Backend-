# Compliance API Endpoints
import os
import json
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional
from ..schemas.compliance_schema import ComplianceReport
from ..services.compliance_service import analyze_compliance, generate_notice

router = APIRouter()

STORAGE_DIR = "industry_reports"

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

@router.post("/upload-compliance")
async def upload_compliance(
    industry_name: str = Form(...),
    industry_type: str = Form(...),
    location: str = Form(...),
    air: Optional[str] = Form(None),
    water: Optional[str] = Form(None),
    heavy_metals: Optional[str] = Form(None),
    noise: Optional[str] = Form(None),
    waste: Optional[str] = Form(None),
    emissions: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    try:
        report_data = {
            "industry_name": industry_name,
            "industry_type": industry_type,
            "location": location,
            "air": json.loads(air) if air else {},
            "water": json.loads(water) if water else {},
            "heavy_metals": json.loads(heavy_metals) if heavy_metals else {},
            "noise": json.loads(noise) if noise else {},
            "waste": json.loads(waste) if waste else {},
            "emissions": json.loads(emissions) if emissions else {}
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in parameters")

    if file:
        content = await file.read()
        try:
            file_data = json.loads(content)
            # Merge file data into report_data
            for key in ["air", "water", "heavy_metals", "noise", "waste", "emissions"]:
                if key in file_data:
                    report_data[key].update(file_data[key])
        except json.JSONDecodeError:
            # If not JSON, maybe it's CSV? For now let's assume JSON as requested or manual entry.
            pass

    analysis, score = analyze_compliance(report_data)
    notice = generate_notice(report_data, analysis, score)

    # Storage
    industry_dir = os.path.join(STORAGE_DIR, industry_name.replace(" ", "_"))
    if not os.path.exists(industry_dir):
        os.makedirs(industry_dir)
    
    with open(os.path.join(industry_dir, "compliance_report.json"), "w") as f:
        json.dump({"report": report_data, "analysis": analysis, "score": score, "notice": notice}, f, indent=4)

    return notice

@router.get("/authority/compliance-reports")
def get_compliance_reports():
    reports = []
    if not os.path.exists(STORAGE_DIR):
        return reports
    
    for industry_name in os.listdir(STORAGE_DIR):
        report_path = os.path.join(STORAGE_DIR, industry_name, "compliance_report.json")
        if os.path.exists(report_path):
            with open(report_path, "r") as f:
                data = json.load(f)
                notice = data.get("notice", {})
                reports.append({
                    "industry": notice.get("industry", industry_name),
                    "compliance_score": notice.get("compliance_score", 0),
                    "violations": notice.get("violations", []),
                    "recommendations": notice.get("recommendations", []),
                    "status": notice.get("status", "Pending"),
                    "report_date": "2024-03-20" # Placeholder
                })
    return reports

@router.get("/authority/violations")
def get_violations():
    reports = get_compliance_reports()
    return [r for r in reports if r["status"] == "Non-Compliant"]

@router.post("/send-notice")
def send_notice(notice: dict):
    # Simulate sending notice (log)
    print(f"Notice sent to {notice['industry']}: {notice}")
    return {"status": "Notice sent", "notice": notice}
