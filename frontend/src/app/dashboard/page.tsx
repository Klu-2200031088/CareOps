'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { dashboardApi } from '@/services/api';
import { useAuthStore, useWorkspaceStore } from '@/services/store';

export default function DashboardPage() {
  const { token } = useAuthStore();
  const { currentWorkspace } = useWorkspaceStore();
  const [dashboard, setDashboard] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    if (!token || !currentWorkspace) {
      router.push('/workspaces');
      return;
    }

    const fetchDashboard = async () => {
      try {
        const response = await dashboardApi.get(token, currentWorkspace.id);
        setDashboard(response.data);
      } catch (error) {
        console.error('Failed to fetch dashboard:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, [token, currentWorkspace, router]);

  if (loading) return <div className="p-8">Loading...</div>;

  if (!dashboard) return <div className="p-8">No data</div>;

  const { stats, alerts, recent_bookings } = dashboard;

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-8">Dashboard - {currentWorkspace?.name}</h1>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-600 text-sm">Today's Bookings</h3>
          <p className="text-3xl font-bold text-blue-600">{stats.today_bookings}</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-600 text-sm">Upcoming</h3>
          <p className="text-3xl font-bold text-green-600">{stats.upcoming_bookings}</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-600 text-sm">New Inquiries</h3>
          <p className="text-3xl font-bold text-orange-600">{stats.new_inquiries}</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-600 text-sm">Pending Forms</h3>
          <p className="text-3xl font-bold text-red-600">{stats.pending_forms}</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-600 text-sm">Low Inventory</h3>
          <p className="text-3xl font-bold text-yellow-600">{stats.low_inventory_count}</p>
        </div>
      </div>

      {/* Alerts */}
      {alerts.length > 0 && (
        <div className="mb-8">
          <h2 className="text-xl font-bold mb-4">Alerts</h2>
          {alerts.map((alert: any, idx: number) => (
            <div key={idx} className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-2">
              <p className="text-yellow-700">{alert.message}</p>
            </div>
          ))}
        </div>
      )}

      {/* Recent Bookings */}
      <div>
        <h2 className="text-xl font-bold mb-4">Recent Bookings</h2>
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold">Contact</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Type</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Date & Time</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Status</th>
              </tr>
            </thead>
            <tbody>
              {recent_bookings?.map((booking: any) => (
                <tr key={booking.id} className="border-t">
                  <td className="px-6 py-4">{booking.contact?.name}</td>
                  <td className="px-6 py-4">{booking.booking_type}</td>
                  <td className="px-6 py-4">{new Date(booking.scheduled_at).toLocaleString()}</td>
                  <td className="px-6 py-4">
                    <span className={`px-3 py-1 rounded text-sm font-semibold ${
                      booking.status === 'confirmed' ? 'bg-green-100 text-green-800' :
                      booking.status === 'completed' ? 'bg-blue-100 text-blue-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {booking.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
