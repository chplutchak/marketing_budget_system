from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class RDInitiative(Base):
    __tablename__ = "rd_initiatives"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Stage tracking
    stage = Column(String(50), nullable=False, default="feasibility")  
    # feasibility, validation, development, launch_prep, launched, on_hold, cancelled
    
    # Business case
    target_market = Column(Text, nullable=True)  # Who is this for?
    market_size_estimate = Column(Float, nullable=True)  # TAM estimate
    target_price = Column(Float, nullable=True)
    target_margin = Column(Float, nullable=True)  # %
    
    # Timeline
    start_date = Column(Date, nullable=True)
    target_launch_date = Column(Date, nullable=True)
    actual_launch_date = Column(Date, nullable=True)
    
    # Status
    is_active = Column(String(20), default="active")
    priority = Column(String(20), default="medium")  # low, medium, high, critical
    
    # Owners
    lead_owner = Column(String(100), nullable=True)  # Primary person responsible
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    feasibility = relationship("RDFeasibility", back_populates="initiative", uselist=False)
    customer_interests = relationship("RDCustomerInterest", back_populates="initiative", cascade="all, delete-orphan")
    samples = relationship("RDSample", back_populates="initiative", cascade="all, delete-orphan")
    contacts = relationship("RDContact", back_populates="initiative", cascade="all, delete-orphan")
    milestones = relationship("RDMilestone", back_populates="initiative", cascade="all, delete-orphan")
    roi_data = relationship("RDROI", back_populates="initiative", uselist=False)
    
    def __repr__(self):
        return f"<RDInitiative(name='{self.name}', stage='{self.stage}')>"


class RDFeasibility(Base):
    __tablename__ = "rd_feasibility"
    
    id = Column(Integer, primary_key=True, index=True)
    initiative_id = Column(Integer, ForeignKey("rd_initiatives.id"), nullable=False, unique=True)
    
    # Manufacturing analysis
    is_manufacturable = Column(String(20), nullable=True)  # yes, no, needs_research
    manufacturing_complexity = Column(String(20), nullable=True)  # low, medium, high
    estimated_lead_time_days = Column(Integer, nullable=True)
    moq = Column(Integer, nullable=True)  # Minimum order quantity
    
    # Cost analysis
    estimated_cogs = Column(Float, nullable=True)  # Cost of goods sold per unit
    estimated_development_cost = Column(Float, nullable=True)  # One-time R&D cost
    estimated_sample_cost = Column(Float, nullable=True)  # Cost per sample unit
    
    # Supply chain
    material_constraints = Column(Text, nullable=True)
    supplier_identified = Column(String(20), nullable=True)  # yes, no, partial
    
    # Regulatory
    regulatory_requirements = Column(Text, nullable=True)
    regulatory_status = Column(String(50), nullable=True)
    
    # Notes
    feasibility_notes = Column(Text, nullable=True)
    last_reviewed_date = Column(Date, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    initiative = relationship("RDInitiative", back_populates="feasibility")
    
    def __repr__(self):
        return f"<RDFeasibility(initiative_id={self.initiative_id}, manufacturable='{self.is_manufacturable}')>"


class RDCustomerInterest(Base):
    __tablename__ = "rd_customer_interest"
    
    id = Column(Integer, primary_key=True, index=True)
    initiative_id = Column(Integer, ForeignKey("rd_initiatives.id"), nullable=False)
    
    # Customer info
    customer_name = Column(String(255), nullable=False)
    contact_person = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    
    # Interest tracking
    interest_level = Column(String(20), nullable=False, default="interested")  
    # interested, highly_interested, committed, testing, ordered, not_interested
    
    # Historical context
    has_order_history = Column(String(20), nullable=True)  # yes, no
    historical_order_volume = Column(Float, nullable=True)  # $ value
    similar_products_ordered = Column(Text, nullable=True)
    
    # Engagement
    first_contact_date = Column(Date, nullable=True)
    last_contact_date = Column(Date, nullable=True)
    next_follow_up_date = Column(Date, nullable=True)
    
    # Sample status
    sample_requested = Column(String(20), default="no")  # yes, no, sent
    sample_sent_date = Column(Date, nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    initiative = relationship("RDInitiative", back_populates="customer_interests")
    
    def __repr__(self):
        return f"<RDCustomerInterest(customer='{self.customer_name}', interest='{self.interest_level}')>"


class RDSample(Base):
    __tablename__ = "rd_samples"
    
    id = Column(Integer, primary_key=True, index=True)
    initiative_id = Column(Integer, ForeignKey("rd_initiatives.id"), nullable=False)
    
    # Sample details
    sample_type = Column(String(100), nullable=False)  # trial_batch, demo_sample, validation_sample
    recipient_name = Column(String(255), nullable=False)
    recipient_company = Column(String(255), nullable=True)
    
    # Logistics
    quantity = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)
    ship_date = Column(Date, nullable=True)
    tracking_number = Column(String(255), nullable=True)
    
    # Cost
    sample_cost = Column(Float, nullable=False, default=0.0)
    shipping_cost = Column(Float, nullable=True)
    
    # Follow-up
    follow_up_date = Column(Date, nullable=True)
    feedback_received = Column(String(20), default="no")  # yes, no, pending
    feedback_notes = Column(Text, nullable=True)
    
    # Conversion
    converted_to_order = Column(String(20), default="pending")  # yes, no, pending
    order_value = Column(Float, nullable=True)
    order_date = Column(Date, nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    initiative = relationship("RDInitiative", back_populates="samples")
    
    def __repr__(self):
        return f"<RDSample(recipient='{self.recipient_name}', cost=${self.sample_cost})>"


class RDContact(Base):
    __tablename__ = "rd_contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    initiative_id = Column(Integer, ForeignKey("rd_initiatives.id"), nullable=False)
    
    # Contact details
    contact_date = Column(Date, nullable=False)
    contact_type = Column(String(50), nullable=False)  # email, call, meeting, convention, demo
    contact_person = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    
    # Who from UTAK
    utak_contact = Column(String(255), nullable=True)  # Who from your team
    department = Column(String(100), nullable=True)  # sales, marketing, ops, manufacturing
    
    # Details
    subject = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    outcome = Column(String(100), nullable=True)  # positive, neutral, negative, needs_follow_up
    
    # Next steps
    next_action = Column(Text, nullable=True)
    next_action_date = Column(Date, nullable=True)
    next_action_owner = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    initiative = relationship("RDInitiative", back_populates="contacts")
    
    def __repr__(self):
        return f"<RDContact(date={self.contact_date}, type='{self.contact_type}')>"


class RDMilestone(Base):
    __tablename__ = "rd_milestones"
    
    id = Column(Integer, primary_key=True, index=True)
    initiative_id = Column(Integer, ForeignKey("rd_initiatives.id"), nullable=False)
    
    # Milestone details
    milestone_name = Column(String(255), nullable=False)
    milestone_type = Column(String(50), nullable=False)  
    # feasibility_complete, samples_ready, validation_done, launch_materials_ready, launched
    
    # Timeline
    target_date = Column(Date, nullable=True)
    actual_date = Column(Date, nullable=True)
    
    # Status
    status = Column(String(50), nullable=False, default="not_started")  
    # not_started, in_progress, completed, delayed, blocked
    
    # Ownership
    owner = Column(String(255), nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    blockers = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    initiative = relationship("RDInitiative", back_populates="milestones")
    
    def __repr__(self):
        return f"<RDMilestone(name='{self.milestone_name}', status='{self.status}')>"


class RDROI(Base):
    __tablename__ = "rd_roi"
    
    id = Column(Integer, primary_key=True, index=True)
    initiative_id = Column(Integer, ForeignKey("rd_initiatives.id"), nullable=False, unique=True)
    
    # Investment
    total_development_cost = Column(Float, nullable=True, default=0.0)
    total_sample_cost = Column(Float, nullable=True, default=0.0)
    total_marketing_cost = Column(Float, nullable=True, default=0.0)
    total_other_costs = Column(Float, nullable=True, default=0.0)
    
    # Returns
    total_revenue = Column(Float, nullable=True, default=0.0)
    total_orders = Column(Integer, nullable=True, default=0)
    
    # Calculated fields
    total_investment = Column(Float, nullable=True, default=0.0)  # Sum of all costs
    roi_percentage = Column(Float, nullable=True)  # (revenue - investment) / investment * 100
    
    # Conversion metrics
    samples_sent_count = Column(Integer, nullable=True, default=0)
    samples_converted_count = Column(Integer, nullable=True, default=0)
    conversion_rate = Column(Float, nullable=True)  # %
    
    # Notes
    notes = Column(Text, nullable=True)
    last_calculated_date = Column(Date, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    initiative = relationship("RDInitiative", back_populates="roi_data")
    
    def __repr__(self):
        return f"<RDROI(initiative_id={self.initiative_id}, roi={self.roi_percentage}%)>"