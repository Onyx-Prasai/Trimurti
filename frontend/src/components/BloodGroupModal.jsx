import React, { useState } from 'react';

const BLOOD_GROUPS = [
  'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'
];

export default function BloodGroupModal({ isOpen, onClose, onSubmit }) {
  const [selectedBloodGroup, setSelectedBloodGroup] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!selectedBloodGroup) {
      alert('Please select a blood group');
      return;
    }

    setLoading(true);
    try {
      // Call the onSubmit callback with the selected blood group
      await onSubmit(selectedBloodGroup);
      setSelectedBloodGroup('');
    } catch (error) {
      console.error('Error submitting blood group:', error);
      alert('Failed to save blood group. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDoItLater = () => {
    setSelectedBloodGroup('');
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 px-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 animate-slideIn">
        {/* Header */}
        <div className="text-center mb-6">
          <div className="flex justify-center mb-4">
            <svg className="w-16 h-16 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M12 6.253v13m0-13C6.5 9.5 2 9.5 2 15.5S6.5 22 12 22s10-4.5 10-10.5S17.5 9.5 12 6.253zm0 0C6.5 2.5 2 2.5 2 8.5S6.5 15 12 15s10-4.5 10-10.5S17.5 2.5 12 6.253z"
              />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">What's Your Blood Group?</h2>
          <p className="text-gray-600 text-sm">
            Knowing your blood group helps us connect you with those who need you most
          </p>
        </div>

        {/* Blood Group Options */}
        <div className="mb-8">
          <div className="grid grid-cols-4 gap-3">
            {BLOOD_GROUPS.map((group) => (
              <button
                key={group}
                onClick={() => setSelectedBloodGroup(group)}
                className={`py-3 px-2 rounded-lg font-bold text-sm transition-all duration-200 ${
                  selectedBloodGroup === group
                    ? 'bg-red-600 text-white shadow-lg scale-105'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {group}
              </button>
            ))}
          </div>
        </div>

        {/* Buttons */}
        <div className="space-y-3">
          <button
            onClick={handleSubmit}
            disabled={loading || !selectedBloodGroup}
            className={`w-full py-3 px-4 rounded-lg font-semibold text-white transition-all duration-200 ${
              loading || !selectedBloodGroup
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-red-600 hover:bg-red-700 active:scale-95'
            }`}
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Saving...
              </div>
            ) : (
              'Submit'
            )}
          </button>

          <button
            onClick={handleDoItLater}
            disabled={loading}
            className="w-full py-3 px-4 rounded-lg font-semibold text-gray-700 bg-gray-100 hover:bg-gray-200 transition-all duration-200 disabled:opacity-50"
          >
            Do It Later
          </button>
        </div>

        {/* Info Message */}
        <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-xs text-blue-700 text-center">
            💡 You can update your blood group anytime from your profile settings
          </p>
        </div>
      </div>
    </div>
  );
}
