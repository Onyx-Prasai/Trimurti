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
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      const data = await response.json();
      console.log('Login response:', data);

      if (response.ok) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        setUserData(data);
        setIsAuthenticated(true);
        
        // Show blood group modal instead of navigating immediately
        setShowBloodGroupModal(true);
      } else {
        setError(data.detail || 'Login failed. Please try again.');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleBloodGroupSubmit = async (bloodGroup) => {
    try {
      const token = localStorage.getItem('token');
      
      // Update user's blood group in the backend
      const response = await fetch('/api/donor-profile/update-blood-group/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`,
        },
        body: JSON.stringify({
          blood_group: bloodGroup,
        }),
      });

      if (response.ok) {
        console.log('Blood group saved successfully');
        setShowBloodGroupModal(false);
        navigate('/dashboard');
      } else {
        console.error('Failed to save blood group');
        alert('Failed to save blood group. Proceeding anyway...');
        setShowBloodGroupModal(false);
        navigate('/dashboard');
      }
    } catch (error) {
      console.error('Error saving blood group:', error);
      // Proceed even if saving fails
      setShowBloodGroupModal(false);
      navigate('/dashboard');
    }
  };

  return (
    <>
      <div>Hello World</div>
    </>
  );
}