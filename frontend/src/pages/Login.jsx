import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import BloodGroupModal from '../components/BloodGroupModal';

export default function Login({ setIsAuthenticated }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showBloodGroupModal, setShowBloodGroupModal] = useState(false);
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        setUserData(data);
        setIsAuthenticated(true);
        setShowBloodGroupModal(true);
      } else {
        setError(data.detail || 'Login failed. Please try again.');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleBloodGroupSubmit = async (bloodGroup) => {
    try {
      const token = localStorage.getItem('token');

      const response = await fetch('/api/donor-profile/update-blood-group/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify({ blood_group: bloodGroup }),
      });

      // Keep localStorage user in sync so Profile shows the correct value immediately
      let savedBloodGroup = bloodGroup;
      try {
        const data = await response.json();
        if (data?.blood_group) savedBloodGroup = data.blood_group;
      } catch {
        // ignore JSON parse errors; we'll still use the selected value
      }

      const existingUser = JSON.parse(localStorage.getItem('user') || '{}');
      localStorage.setItem(
        'user',
        JSON.stringify({
          ...existingUser,
          blood_group: savedBloodGroup,
        })
      );
    } finally {
      setShowBloodGroupModal(false);
      navigate('/dashboard');
    }
  };

  return (
    <>
      <BloodGroupModal
        isOpen={showBloodGroupModal}
        onClose={() => {
          setShowBloodGroupModal(false);
          navigate('/dashboard');
        }}
        onSubmit={handleBloodGroupSubmit}
      />

      <div className="bg-gray-50 min-h-screen flex items-center justify-center px-4">
        <div className="w-full max-w-6xl grid md:grid-cols-2 gap-8 items-center">

          {/* LEFT SIDE */}
          <div className="hidden md:block bg-gradient-to-r from-red-600 to-red-400 text-white rounded-3xl p-12 shadow-2xl">
            <h1 className="text-4xl font-bold">Blood Hub Nepal</h1>
            <p className="mt-4">Save Lives, One Drop at a Time</p>
          </div>

          {/* RIGHT SIDE */}
          <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12">
            <h2 className="text-3xl font-bold mb-6">Welcome Back</h2>

            {error && (
              <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 mb-6">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full p-3 border rounded-xl"
                required
              />

              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full p-3 border rounded-xl"
                required
              />

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-red-600 text-white rounded-xl"
              >
                {loading ? 'Signing In...' : 'Sign In'}
              </button>
            </form>
          </div>

        </div>
      </div>
    </>
  );
}
