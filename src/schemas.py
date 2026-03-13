from typing import List, Optional
from pydantic import BaseModel, Field

NA = "Not Available"

class PropertyDetails(BaseModel):
    customer_name: str = NA
    address: str = NA
    property_type: str = NA
    floors: str = NA
    inspection_date: str = NA
    inspected_by: str = NA

class AreaObservation(BaseModel):
    area: str
    inspection_observations: List[str] = Field(default_factory=list)
    thermal_evidence: List[str] = Field(default_factory=list)
    supporting_images: List[str] = Field(default_factory=list)
    confidence: str = NA

class ThermalFinding(BaseModel):
    image_id: str = NA
    hotspot_c: Optional[float] = None
    coldspot_c: Optional[float] = None
    delta_c: Optional[float] = None
    emissivity: Optional[float] = None
    interpretation: str = NA
    mapped_area: str = NA

class RootCauseItem(BaseModel):
    cause: str
    evidence: List[str] = Field(default_factory=list)
    confidence: str = NA

class SeverityAssessment(BaseModel):
    level: str = NA
    reasoning: List[str] = Field(default_factory=list)

class DDRReport(BaseModel):
    property_details: PropertyDetails
    property_issue_summary: str = NA
    area_wise_observations: List[AreaObservation] = Field(default_factory=list)
    thermal_analysis_findings: List[ThermalFinding] = Field(default_factory=list)
    probable_root_cause: List[RootCauseItem] = Field(default_factory=list)
    severity_assessment: SeverityAssessment = Field(default_factory=SeverityAssessment)
    recommended_actions: List[str] = Field(default_factory=list)
    additional_notes: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    conflicts: List[str] = Field(default_factory=list)
