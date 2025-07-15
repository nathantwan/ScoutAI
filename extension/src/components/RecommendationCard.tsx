import React from 'react';
import { TrendingUp, AlertTriangle, CheckCircle, Target } from 'lucide-react';
import { Recommendation } from '../types';

interface RecommendationCardProps {
  recommendation: Recommendation;
  rank: number;
}

const RecommendationCard: React.FC<RecommendationCardProps> = ({ recommendation, rank }) => {
  const { player, confidence_score, predicted_points, boom_probability, value_over_replacement, explanation, risk_level } = recommendation;

  const getConfidenceColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getRiskIcon = (risk: string) => {
    switch (risk) {
      case 'low':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'medium':
        return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
      case 'high':
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
      default:
        return <Target className="w-4 h-4 text-gray-500" />;
    }
  };

  const getPositionColor = (position: string) => {
    switch (position) {
      case 'QB':
        return 'bg-blue-100 text-blue-800';
      case 'RB':
        return 'bg-green-100 text-green-800';
      case 'WR':
        return 'bg-purple-100 text-purple-800';
      case 'TE':
        return 'bg-orange-100 text-orange-800';
      case 'K':
        return 'bg-gray-100 text-gray-800';
      case 'DST':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <div className="w-6 h-6 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center text-xs font-bold">
            {rank}
          </div>
          <div>
            <h4 className="font-semibold text-gray-900">{player.name}</h4>
            <div className="flex items-center space-x-2">
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPositionColor(player.position)}`}>
                {player.position}
              </span>
              <span className="text-xs text-gray-500">{player.team}</span>
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-1">
          {getRiskIcon(risk_level)}
          <span className="text-xs text-gray-500 capitalize">{risk_level} risk</span>
        </div>
      </div>

      {/* Confidence Score */}
      <div className="mb-3">
        <div className="flex items-center justify-between mb-1">
          <span className="text-sm text-gray-600">Confidence</span>
          <span className={`text-sm font-medium ${getConfidenceColor(confidence_score)}`}>
            {Math.round(confidence_score * 100)}%
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-primary-500 h-2 rounded-full transition-all duration-300"
            style={{ width: `${confidence_score * 100}%` }}
          />
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-3 mb-3">
        <div className="bg-gray-50 rounded p-2">
          <div className="text-xs text-gray-500">Projected Points</div>
          <div className="font-semibold text-gray-900">{Math.round(predicted_points)}</div>
        </div>
        
        <div className="bg-gray-50 rounded p-2">
          <div className="text-xs text-gray-500">Boom Probability</div>
          <div className="font-semibold text-gray-900">{Math.round(boom_probability * 100)}%</div>
        </div>
        
        <div className="bg-gray-50 rounded p-2">
          <div className="text-xs text-gray-500">Value Over Replacement</div>
          <div className="font-semibold text-gray-900">{Math.round(value_over_replacement)}</div>
        </div>
        
        <div className="bg-gray-50 rounded p-2">
          <div className="text-xs text-gray-500">ADP</div>
          <div className="font-semibold text-gray-900">
            {player.adp ? Math.round(player.adp) : 'N/A'}
          </div>
        </div>
      </div>

      {/* Explanation */}
      <div className="bg-blue-50 border border-blue-200 rounded p-3">
        <div className="flex items-start space-x-2">
          <TrendingUp className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" />
          <p className="text-sm text-blue-800">{explanation}</p>
        </div>
      </div>
    </div>
  );
};

export default RecommendationCard; 