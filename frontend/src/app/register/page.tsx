'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { authApi } from '@/services/api';

export default function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [step, setStep] = useState<'register' | 'verify'>('register');
  const [verificationCode, setVerificationCode] = useState('');
  const router = useRouter();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await authApi.register({
        email,
        password,
        full_name: fullName,
        phone_number: phoneNumber
      });
      
      // If phone was provided, go to verification step
      if (phoneNumber) {
        setStep('verify');
      } else {
        router.push('/login');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifySMS = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await authApi.verifySMS(email, verificationCode);
      router.push('/login');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Verification failed');
    } finally {
      setLoading(false);
    }
  };

  const handleResendSMS = async () => {
    setLoading(true);
    setError('');

    try {
      await authApi.resendSMS(email);
      setError('');
      alert('Verification code resent to your phone');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to resend code');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-center">🎯 CareOps</h1>
          <p className="text-center text-gray-600 mt-2">
            {step === 'register' ? 'Create Your Account' : 'Verify Your Phone'}
          </p>
        </div>

        {step === 'register' ? (
          <form onSubmit={handleRegister} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700">Full Name</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Minimum 6 characters"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Phone Number (Optional)</label>
              <input
                type="tel"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                placeholder="+1234567890"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500"
              />
              <p className="text-xs text-gray-500 mt-1">Include country code (e.g., +1)</p>
            </div>

            {error && <p className="text-red-600 text-sm bg-red-50 p-3 rounded">{error}</p>}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 rounded-md font-medium hover:bg-blue-700 disabled:opacity-50 transition"
            >
              {loading ? 'Creating account...' : 'Register'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleVerifySMS} className="space-y-6">
            <div className="bg-blue-50 p-4 rounded-md">
              <p className="text-sm text-gray-700">
                We've sent a verification code to <strong>{phoneNumber}</strong>
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Verification Code</label>
              <input
                type="text"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value)}
                placeholder="000000"
                maxLength={6}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 text-center text-2xl tracking-widest"
                required
              />
            </div>

            {error && <p className="text-red-600 text-sm bg-red-50 p-3 rounded">{error}</p>}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 rounded-md font-medium hover:bg-blue-700 disabled:opacity-50 transition"
            >
              {loading ? 'Verifying...' : 'Verify Phone'}
            </button>

            <button
              type="button"
              onClick={handleResendSMS}
              disabled={loading}
              className="w-full text-blue-600 py-2 font-medium hover:text-blue-700 disabled:opacity-50"
            >
              Didn't receive code? Resend
            </button>
          </form>
        )}

        <p className="text-center text-sm text-gray-600">
          Already have an account? <a href="/login" className="text-blue-600 hover:text-blue-700">Login</a>
        </p>
      </div>
    </div>
  );
}
