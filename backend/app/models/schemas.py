from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum

class Position(str, Enum):
    """Fantasy football positions"""
    QB = "QB"
    RB = "RB"
    WR = "WR"
    TE = "TE"
    K = "K"
    DST = "DST"

class Player(BaseModel):
    """Player information"""
    name: str = Field(..., description="Player name")
    position: Position = Field(..., description="Player position")
    team: str = Field(..., description="Player team")
    adp: Optional[float] = Field(None, description="Average draft position")
    projected_points: Optional[float] = Field(None, description="Projected fantasy points")
    bye_week: Optional[int] = Field(None, description="Player bye week")

class Roster(BaseModel):
    """User's current roster"""
    QB: List[str] = Field(default_factory=list, description="Quarterbacks")
    RB: List[str] = Field(default_factory=list, description="Running backs")
    WR: List[str] = Field(default_factory=list, description="Wide receivers")
    TE: List[str] = Field(default_factory=list, description="Tight ends")
    K: List[str] = Field(default_factory=list, description="Kickers")
    DST: List[str] = Field(default_factory=list, description="Defense/Special teams")

class Recommendation(BaseModel):
    """Player recommendation with analysis"""
    player: Player = Field(..., description="Recommended player")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in recommendation (0-1)")
    predicted_points: float = Field(..., description="Predicted fantasy points")
    boom_probability: float = Field(..., ge=0.0, le=1.0, description="Probability of boom performance")
    value_over_replacement: float = Field(..., description="Value over replacement player")
    explanation: str = Field(..., description="Brief explanation of recommendation")
    risk_level: str = Field(..., description="Risk level: low, medium, high")

class DraftRequest(BaseModel):
    """Request for draft recommendations"""
    current_pick: int = Field(..., ge=1, description="Current pick number")
    current_round: int = Field(..., ge=1, description="Current draft round")
    user_roster: Roster = Field(..., description="User's current roster")
    available_players: List[Player] = Field(..., description="Available players to draft")
    league_settings: Optional[Dict] = Field(default_factory=dict, description="League settings (optional)")

class DraftResponse(BaseModel):
    """Response with draft recommendations"""
    recommendations: List[Recommendation] = Field(..., description="List of player recommendations")
    roster_analysis: Optional[Dict] = Field(None, description="Analysis of current roster needs")
    draft_strategy: Optional[str] = Field(None, description="Recommended draft strategy") 