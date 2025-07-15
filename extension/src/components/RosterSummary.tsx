import React from 'react';
import { Users, UserCheck } from 'lucide-react';
import { Roster } from '../types';

interface RosterSummaryProps {
  roster: Roster;
}

const RosterSummary: React.FC<RosterSummaryProps> = ({ roster }) => {
  const positions = [
    { key: 'QB', label: 'QB', color: 'bg-blue-100 text-blue-800' },
    { key: 'RB', label: 'RB', color: 'bg-green-100 text-green-800' },
    { key: 'WR', label: 'WR', color: 'bg-purple-100 text-purple-800' },
    { key: 'TE', label: 'TE', color: 'bg-orange-100 text-orange-800' },
    { key: 'K', label: 'K', color: 'bg-gray-100 text-gray-800' },
    { key: 'DST', label: 'DST', color: 'bg-red-100 text-red-800' }
  ];

  const totalPlayers = Object.values(roster).reduce((sum, players) => sum + players.length, 0);

  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <div className="flex items-center space-x-2 mb-3">
        <Users className="w-5 h-5 text-gray-600" />
        <h3 className="text-lg font-semibold text-gray-800">Your Roster</h3>
        <span className="text-sm text-gray-500">({totalPlayers} players)</span>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {positions.map(({ key, label, color }) => {
          const players = roster[key as keyof Roster];
          const count = players.length;
          
          return (
            <div key={key} className="bg-white rounded-lg p-3 border border-gray-200">
              <div className="flex items-center justify-between mb-2">
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${color}`}>
                  {label}
                </span>
                <span className="text-sm font-medium text-gray-700">
                  {count}
                </span>
              </div>
              
              {players.length > 0 ? (
                <div className="space-y-1">
                  {players.slice(0, 2).map((player, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <UserCheck className="w-3 h-3 text-green-500" />
                      <span className="text-xs text-gray-600 truncate">
                        {player}
                      </span>
                    </div>
                  ))}
                  {players.length > 2 && (
                    <span className="text-xs text-gray-500">
                      +{players.length - 2} more
                    </span>
                  )}
                </div>
              ) : (
                <div className="text-xs text-gray-400 italic">
                  No players drafted
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Roster Analysis */}
      <div className="mt-4 pt-3 border-t border-gray-200">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-600">Roster Strength:</span>
          <span className="font-medium text-gray-800">
            {totalPlayers >= 8 ? 'Strong' : totalPlayers >= 5 ? 'Moderate' : 'Weak'}
          </span>
        </div>
        
        <div className="mt-2 text-xs text-gray-500">
          {totalPlayers < 5 && 'Consider drafting more players'}
          {totalPlayers >= 5 && totalPlayers < 8 && 'Good foundation, continue building'}
          {totalPlayers >= 8 && 'Strong roster, focus on best available'}
        </div>
      </div>
    </div>
  );
};

export default RosterSummary; 