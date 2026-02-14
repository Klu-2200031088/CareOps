'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore, useWorkspaceStore } from '@/services/store';
import { workspaceApi, bookingsApi, inboxApi, contactsApi } from '@/services/api';
import { format } from 'date-fns';

export default function WorkspaceSetupPage() {
  const { token } = useAuthStore();
  const { currentWorkspace, setWorkspace } = useWorkspaceStore();
  const [step, setStep] = useState(1); // 1: setup, 2: preview
  const [bookingTypes, setBookingTypes] = useState<any[]>([]);
  const [newBooking, setNewBooking] = useState({ booking_type: '', duration_minutes: 60 });
  const [contacts, setContacts] = useState<any[]>([]);
  const [newContact, setNewContact] = useState({ name: '', email: '', phone: '' });
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  useEffect(() => {
    if (!token || !currentWorkspace) {
      router.push('/workspaces');
      return;
    }
    loadWorkspaceData();
  }, [token, currentWorkspace, router]);

  const loadWorkspaceData = async () => {
    try {
      const contactsRes = await contactsApi.list(token!, currentWorkspace.id);
      setContacts(contactsRes.data);

      const bookingsRes = await bookingsApi.list(token!, currentWorkspace.id);
      setBookingTypes(bookingsRes.data);
    } catch (error) {
      console.error('Failed to load workspace data:', error);
    }
  };

  const handleAddBooking = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newBooking.booking_type.trim()) return;

    setLoading(true);
    try {
      // Create a dummy contact first
      const contactRes = await contactsApi.create(token!, currentWorkspace.id, {
        name: 'Booking Type Demo',
        email: 'demo@example.com'
      });

      const bookingRes = await bookingsApi.create(
        token!,
        currentWorkspace.id,
        contactRes.data.id,
        {
          ...newBooking,
          scheduled_at: new Date().toISOString()
        }
      );

      setBookingTypes([...bookingTypes, bookingRes.data]);
      setNewBooking({ booking_type: '', duration_minutes: 60 });
    } catch (error) {
      console.error('Failed to add booking:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddContact = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await contactsApi.create(token!, currentWorkspace.id, newContact);
      setContacts([...contacts, res.data]);
      setNewContact({ name: '', email: '', phone: '' });
    } catch (error) {
      console.error('Failed to add contact:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleActivate = async () => {
    try {
      await workspaceApi.activate(token!, currentWorkspace.id);
      setWorkspace({ ...currentWorkspace, is_active: true });
      router.push('/dashboard');
    } catch (error) {
      console.error('Failed to activate workspace:', error);
    }
  };

  if (!currentWorkspace) return <div className="p-8">Loading...</div>;

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">Setup: {currentWorkspace.name}</h1>
        <p className="text-gray-600 mb-8">Configure your workspace to get started</p>

        <div className="flex gap-4 mb-8">
          <button
            onClick={() => setStep(1)}
            className={`px-4 py-2 rounded-md font-medium ${
              step === 1 ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 border'
            }`}
          >
            Setup
          </button>
          <button
            onClick={() => setStep(2)}
            className={`px-4 py-2 rounded-md font-medium ${
              step === 2 ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 border'
            }`}
          >
            Preview
          </button>
        </div>

        {step === 1 ? (
          <div className="space-y-6">
            {/* Add Booking Types */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold mb-4">📅 Booking Types</h2>
              <form onSubmit={handleAddBooking} className="space-y-4">
                <div className="flex gap-4">
                  <input
                    type="text"
                    value={newBooking.booking_type}
                    onChange={(e) => setNewBooking({ ...newBooking, booking_type: e.target.value })}
                    placeholder="e.g., Consultation, Meeting"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md"
                  />
                  <input
                    type="number"
                    value={newBooking.duration_minutes}
                    onChange={(e) => setNewBooking({ ...newBooking, duration_minutes: parseInt(e.target.value) })}
                    min="15"
                    step="15"
                    className="w-24 px-3 py-2 border border-gray-300 rounded-md"
                  />
                  <button
                    type="submit"
                    disabled={loading}
                    className="bg-blue-600 text-white px-4 py-2 rounded-md disabled:opacity-50"
                  >
                    Add
                  </button>
                </div>
              </form>

              <div className="mt-4 space-y-2">
                {bookingTypes.map((bt) => (
                  <div key={bt.id} className="p-3 bg-gray-100 rounded-md">
                    <p className="font-semibold">{bt.booking_type}</p>
                    <p className="text-sm text-gray-600">{bt.duration_minutes} minutes</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Add Contacts */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold mb-4">👥 Contacts</h2>
              <form onSubmit={handleAddContact} className="space-y-4 mb-4">
                <input
                  type="text"
                  value={newContact.name}
                  onChange={(e) => setNewContact({ ...newContact, name: e.target.value })}
                  placeholder="Contact Name"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  required
                />
                <div className="flex gap-4">
                  <input
                    type="email"
                    value={newContact.email}
                    onChange={(e) => setNewContact({ ...newContact, email: e.target.value })}
                    placeholder="Email"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md"
                  />
                  <input
                    type="tel"
                    value={newContact.phone}
                    onChange={(e) => setNewContact({ ...newContact, phone: e.target.value })}
                    placeholder="Phone"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md"
                  />
                  <button
                    type="submit"
                    disabled={loading}
                    className="bg-blue-600 text-white px-4 py-2 rounded-md disabled:opacity-50"
                  >
                    Add
                  </button>
                </div>
              </form>

              <div className="space-y-2">
                {contacts.map((contact) => (
                  <div key={contact.id} className="p-3 bg-gray-100 rounded-md">
                    <p className="font-semibold">{contact.name}</p>
                    <p className="text-sm text-gray-600">{contact.email} | {contact.phone}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">📊 Workspace Summary</h2>
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div>
                <p className="text-gray-600 text-sm">Name</p>
                <p className="text-lg font-semibold">{currentWorkspace.name}</p>
              </div>
              <div>
                <p className="text-gray-600 text-sm">Address</p>
                <p className="text-lg font-semibold">{currentWorkspace.address}</p>
              </div>
              <div>
                <p className="text-gray-600 text-sm">Timezone</p>
                <p className="text-lg font-semibold">{currentWorkspace.timezone}</p>
              </div>
              <div>
                <p className="text-gray-600 text-sm">Booking Types</p>
                <p className="text-lg font-semibold">{bookingTypes.length}</p>
              </div>
            </div>

            <div className="mb-6">
              <p className="text-gray-600 text-sm mb-2">✅ Setup Progress</p>
              <ul className="space-y-2 text-sm">
                <li className={bookingTypes.length > 0 ? '✅ Booking types configured' : '⏳ Add booking types'}</li>
                <li>{contacts.length > 0 ? '✅ Test contacts created' : '⏳ Add test contacts'}</li>
                <li>⏳ Email integration configured</li>
              </ul>
            </div>

            <button
              onClick={handleActivate}
              disabled={bookingTypes.length === 0}
              className="w-full bg-green-600 text-white py-3 rounded-md font-bold hover:bg-green-700 disabled:opacity-50"
            >
              🚀 Activate Workspace
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
