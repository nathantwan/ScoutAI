import React from 'react';

const LoadingSpinner: React.FC = () => {
  return (
    <div className="flex items-center justify-center py-8">
      <div className="flex flex-col items-center space-y-3">
        <div className="relative">
          <div className="w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
        </div>
        <div className="text-sm text-gray-600">Analyzing draft...</div>
      </div>
    </div>
  );
};

export default LoadingSpinner; 