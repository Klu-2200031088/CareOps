'use client';

import { useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { contactsApi, bookingsApi } from '@/services/api';
import { useState as useStateHook } from 'react';

export default function PublicBookingPage() {
  const searchParams = useSearchParams();
  const workspaceId = searchParams.get('workspace');

  const [step, setStep] = useState(1); // 1: contact info, 2: booking selection, 3: confirmation
  const [contactInfo, setContactInfo] = useState({ name: '', email: '', phone: '' });
  const [bookingType, setBookingType] = useState('');
  const [bookingDate, setBookingDate] = useState('');
  const [bookingTime, setBookingTime] = useState('09:00');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [confirmation, setConfirmation] = useState<any>(null);

  const bookingTypes = ['Consultation', 'Meeting', 'Service'];

  const handleContactSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (contactInfo.name && contactInfo.email) {
      setStep(2);
    }
  };

  const handleBookingSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // In production, you'd call the actual API
      // For now, simulate booking creation
      const scheduledAt = new Date(`${bookingDate}T${bookingTime}`);
      
      setConfirmation({
        name: contactInfo.name,
        email: contactInfo.email,
        bookingType,
        scheduledAt: scheduledAt.toLocaleString(),
      });

      setStep(3);
    } catch (err: any) {
      setError(err.message || 'Booking failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-indigo-600 p-4">
      <div className="max-w-md mx-auto">
        {/* Header */}
        <div className="text-center text-white mb-8 pt-8">
          <h1 className="text-4xl font-bold mb-2">🎯 CareOps</h1>
          <p className="text-blue-100">Schedule Your Appointment</p>
        </div>

        {/* Progress Indicator */}
        <div className="flex justify-between mb-8">
          <div className={`h-1 flex-1 mx-1 rounded ${step >= 1 ? 'bg-white' : 'bg-blue-400'}`}></div>
          <div className={`h-1 flex-1 mx-1 rounded ${step >= 2 ? 'bg-white' : 'bg-blue-400'}`}></div>
          <div className={`h-1 flex-1 mx-1 rounded ${step >= 3 ? 'bg-white' : 'bg-blue-400'}`}></div>
        </div>

        <div className="bg-white rounded-lg shadow-xl p-8">
          {/* Step 1: Contact Info */}
          {step === 1 && (
            <form onSubmit={handleContactSubmit} className="space-y-4">
              <h2 className="text-2xl font-bold mb-6">Your Information</h2>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Full Name *</label>
                <input
                  type="text"
                  value={contactInfo.name}
                  onChange={(e) => setContactInfo({ ...contactInfo, name: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email *</label>
                <input
                  type="email"
                  value={contactInfo.email}
                  onChange={(e) => setContactInfo({ ...contactInfo, email: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                <input
                  type="tel"
                  value={contactInfo.phone}
                  onChange={(e) => setContactInfo({ ...contactInfo, phone: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                />
              </div>

              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition mt-6"
              >
                Continue →
              </button>
            </form>
          )}

          {/* Step 2: Booking Selection */}
          {step === 2 && (
            <form onSubmit={handleBookingSubmit} className="space-y-4">
              <h2 className="text-2xl font-bold mb-6">Select Booking</h2>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">Type</label>
                <div className="space-y-2">
                  {bookingTypes.map((type) => (
                    <label key={type} className="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:bg-blue-50">
                      <input
                        type="radio"
                        name="bookingType"
                        value={type}
                        checked={bookingType === type}
                        onChange={(e) => setBookingType(e.target.value)}
                        className="mr-3"
                        required
                      />
                      <span>{type}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                <input
                  type="date"
                  value={bookingDate}
                  onChange={(e) => setBookingDate(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Time</label>
                <input
                  type="time"
                  value={bookingTime}
                  onChange={(e) => setBookingTime(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600"
                  required
                />
              </div>

              {error && <p className="text-red-600 text-sm">{error}</p>}

              <div className="flex gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => setStep(1)}
                  className="flex-1 border border-gray-300 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-50"
                >
                  ← Back
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50"
                >
                  {loading ? 'Booking...' : 'Continue →'}
                </button>
              </div>
            </form>
          )}

          {/* Step 3: Confirmation */}
          {step === 3 && confirmation && (
            <div className="text-center">
              <div className="text-6xl mb-4">✅</div>
              <h2 className="text-2xl font-bold mb-6">Booking Confirmed!</h2>

              <div className="bg-blue-50 rounded-lg p-6 mb-6 text-left space-y-3">
                <div>
                  <p className="text-sm text-gray-600">Name</p>
                  <p className="font-semibold">{confirmation.name}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Email</p>
                  <p className="font-semibold">{confirmation.email}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Booking Type</p>
                  <p className="font-semibold">{confirmation.bookingType}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Date & Time</p>
                  <p className="font-semibold">{confirmation.scheduledAt}</p>
                </div>
              </div>

              <p className="text-gray-600 text-sm mb-6">
                A confirmation email has been sent to {confirmation.email}
              </p>

              <button
                onClick={() => {
                  setStep(1);
                  setContactInfo({ name: '', email: '', phone: '' });
                  setBookingType('');
                  setBookingDate('');
                  setConfirmation(null);
                }}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700"
              >
                Make Another Booking
              </button>
            </div>
          )}
        </div>

        <p className="text-white text-center text-sm mt-8">
          Powered by CareOps Operations Platform
        </p>
      </div>
    </div>
  );
}
