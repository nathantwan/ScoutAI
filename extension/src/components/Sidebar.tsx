import React, { useState, useEffect } from 'react';
import { X, RefreshCw, AlertCircle, CheckCircle, TrendingUp, Shield } from 'lucide-react';
import { Recommendation, DraftState } from '../types';
import { api } from '../utils/api';
import { draftDetector } from '../utils/draft-detector';
import RosterSummary from './RosterSummary';
import RecommendationCard from './RecommendationCard';
import LoadingSpinner from './LoadingSpinner';

interface SidebarProps {
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ onClose }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [draftState, setDraftState] = useState<DraftState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const fetchRecommendations = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Extract draft state from the page
      const state = await draftDetector.extractDraftState();
      if (!state) {
        setError('No draft detected on this page');
        setIsLoading(false);
        return;
      }

      setDraftState(state);

      // Get recommendations from API
      const response = await api.getRecommendations({
        current_pick: state.current_pick,
        current_round: state.current_round,
        user_roster: state.user_roster,
        available_players: state.available_players
      });

      setRecommendations(response.recommendations);
      setLastUpdated(new Date());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch recommendations');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const handleRefresh = () => {
    fetchRecommendations();
  };

  const getRiskColor = (riskLevel: string) => {
    switch (riskLevel) {
      case 'low':
        return 'text-green-600 bg-green-100';
      case 'medium':
        return 'text-yellow-600 bg-yellow-100';
      case 'high':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="fixed top-0 right-0 h-full w-96 bg-white shadow-2xl border-l border-gray-200 z-50 overflow-y-auto">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <TrendingUp className="w-6 h-6" />
            <h1 className="text-xl font-bold">ScoutAI</h1>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:text-gray-200 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        <p className="text-sm text-primary-100 mt-1">
          Fantasy Football Draft Assistant
        </p>
      </div>

      {/* Content */}
      <div className="p-4 space-y-4">
        {/* Status Bar */}
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center space-x-2">
            {draftState && (
              <span className="text-gray-600">
                Round {draftState.current_round}, Pick {draftState.current_pick}
              </span>
            )}
          </div>
          <button
            onClick={handleRefresh}
            disabled={isLoading}
            className="flex items-center space-x-1 text-primary-600 hover:text-primary-700 disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3">
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 text-red-500" />
              <span className="text-red-700 text-sm">{error}</span>
            </div>
          </div>
        )}

        {/* Loading State */}
        {isLoading && <LoadingSpinner />}

        {/* Roster Summary */}
        {draftState && !isLoading && (
          <RosterSummary roster={draftState.user_roster} />
        )}

        {/* Recommendations */}
        {!isLoading && !error && recommendations.length > 0 && (
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <Shield className="w-5 h-5 text-primary-600" />
              <h2 className="text-lg font-semibold text-gray-800">
                Top Recommendations
              </h2>
            </div>
            
            {recommendations.map((recommendation, index) => (
              <RecommendationCard
                key={`${recommendation.player.name}-${index}`}
                recommendation={recommendation}
                rank={index + 1}
              />
            ))}
          </div>
        )}

        {/* Last Updated */}
        {lastUpdated && (
          <div className="text-xs text-gray-500 text-center pt-4 border-t border-gray-100">
            Last updated: {lastUpdated.toLocaleTimeString()}
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar; 