"""
Resume Intelligence Router
Simplified API endpoints - business logic delegated to services
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from ..db import get_db, Candidate
from ..schemas.resume import ParsedResume, ExtractedField
from ..services import ResumeParser

router = APIRouter(prefix="/api/resume", tags=["Resume Intelligence"])

# Service instance
parser = ResumeParser()


@router.post("/parse", response_model=ParsedResume)
async def parse_resume(file: UploadFile = File(...)):
    """
    Parse an uploaded resume (PDF/DOCX) and extract structured data.
    Returns confidence scores for each extracted field.
    """
    # Validate file type
    allowed_types = {
        "application/pdf": "pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx"
    }
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Please upload PDF or DOCX."
        )
    
    # Read and extract text
    content = await file.read()
    file_type = allowed_types[file.content_type]
    
    try:
        if file_type == "pdf":
            text = parser.extract_text_from_pdf(content)
        else:
            text = parser.extract_text_from_docx(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")
    
    if not text or len(text.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="Could not extract sufficient text from the document."
        )
    
    # Extract all fields using service
    parsed = {
        'full_name': parser.extract_name(text),
        'email': parser.extract_email(text),
        'phone': parser.extract_phone(text),
        'location': parser.extract_location(text),
        'current_role': ExtractedField(value="", confidence=0, source="Not implemented", needs_review=True),
        'years_of_experience': parser.extract_experience_years(text),
        'skills': parser.extract_skills(text),
        'education': [],
        'work_experience': [],
    }
    
    overall_confidence = parser.calculate_overall_confidence(parsed)
    
    return ParsedResume(
        **parsed,
        overall_confidence=overall_confidence,
        raw_text=text[:2000]
    )


@router.post("/save/{candidate_id}")
async def save_parsed_profile(
    candidate_id: int,
    profile: ParsedResume,
    db: Session = Depends(get_db)
):
    """Save or update a parsed profile to the database."""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        candidate = Candidate(
            full_name=profile.full_name.value,
            email=profile.email.value,
            phone=profile.phone.value,
            location=profile.location.value,
            current_role=profile.current_role.value,
            years_of_experience=profile.years_of_experience.value,
            raw_resume_text=profile.raw_text,
            confidence_scores={
                'full_name': profile.full_name.confidence,
                'email': profile.email.confidence,
                'overall': profile.overall_confidence
            }
        )
        db.add(candidate)
    else:
        candidate.full_name = profile.full_name.value
        candidate.email = profile.email.value
        candidate.phone = profile.phone.value
        candidate.location = profile.location.value
        candidate.years_of_experience = profile.years_of_experience.value
    
    db.commit()
    db.refresh(candidate)
    
    return {"message": "Profile saved successfully", "candidate_id": candidate.id}
