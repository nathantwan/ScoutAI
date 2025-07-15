// API Types
export interface Player {
  name: string;
  position: 'QB' | 'RB' | 'WR' | 'TE' | 'K' | 'DST';
  team: string;
  adp?: number;
  projected_points?: number;
  bye_week?: number;
}

export interface Roster {
  QB: string[];
  RB: string[];
  WR: string[];
  TE: string[];
  K: string[];
  DST: string[];
}

export interface Recommendation {
  player: Player;
  confidence_score: number;
  predicted_points: number;
  boom_probability: number;
  value_over_replacement: number;
  explanation: string;
  risk_level: 'low' | 'medium' | 'high';
}

export interface DraftRequest {
  current_pick: number;
  current_round: number;
  user_roster: Roster;
  available_players: Player[];
  league_settings?: Record<string, any>;
}

export interface DraftResponse {
  recommendations: Recommendation[];
  roster_analysis?: Record<string, any>;
  draft_strategy?: string;
}

// Extension Types
export interface DraftState {
  current_pick: number;
  current_round: number;
  user_roster: Roster;
  available_players: Player[];
  platform: 'espn' | 'yahoo';
}

export interface ScoutAIState {
  isVisible: boolean;
  isLoading: boolean;
  recommendations: Recommendation[];
  draftState: DraftState | null;
  error: string | null;
} 