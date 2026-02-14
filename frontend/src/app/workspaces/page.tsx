'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { workspaceApi } from '@/services/api';
import { useAuthStore, useWorkspaceStore } from '@/services/store';

export default function WorkspacesPage() {
  const { token } = useAuthStore();
  const { setWorkspace } = useWorkspaceStore();
  const [workspaces, setWorkspaces] = useState<any[]>([]);
  const [newWorkspace, setNewWorkspace] = useState({ name: '', address: '', timezone: 'UTC', contact_email: '' });
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const router = useRouter();

  useEffect(() => {
    if (!token) {
      router.push('/login');
      return;
    }
    fetchWorkspaces();
  }, [token, router]);

  const fetchWorkspaces = async () => {
    try {
      const response = await workspaceApi.list(token!);
      setWorkspaces(response.data);
    } catch (error) {
      console.error('Failed to fetch workspaces:', error);
    }
  };

  const handleCreateWorkspace = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await workspaceApi.create(token!, newWorkspace);
      setWorkspaces([...workspaces, response.data]);
      setNewWorkspace({ name: '', address: '', timezone: 'UTC', contact_email: '' });
      setShowForm(false);
    } catch (error) {
      console.error('Failed to create workspace:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectWorkspace = (workspace: any) => {
    setWorkspace(workspace);
    router.push('/workspace-setup');
  };

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">🎯 My Workspaces</h1>

        {/* Workspace List */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          {workspaces.map((ws) => (
            <div
              key={ws.id}
              onClick={() => handleSelectWorkspace(ws)}
              className="bg-white p-6 rounded-lg shadow cursor-pointer hover:shadow-lg hover:bg-blue-50 transition"
            >
              <h3 className="text-xl font-bold mb-2">{ws.name}</h3>
              <p className="text-gray-600 text-sm mb-2">{ws.address}</p>
              <p className="text-gray-500 text-xs">Zone: {ws.timezone}</p>
              <div className="mt-4">
                <span className={`px-3 py-1 rounded text-sm font-semibold ${
                  ws.is_active ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {ws.is_active ? 'Active' : 'Setup Pending'}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Create New Workspace */}
        <div className="bg-white rounded-lg shadow p-6">
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-blue-600 text-white px-4 py-2 rounded-md font-medium hover:bg-blue-700"
          >
            {showForm ? 'Cancel' : '+ New Workspace'}
          </button>

          {showForm && (
            <form onSubmit={handleCreateWorkspace} className="mt-6 space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Business Name</label>
                <input
                  type="text"
                  value={newWorkspace.name}
                  onChange={(e) => setNewWorkspace({ ...newWorkspace, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Address</label>
                <input
                  type="text"
                  value={newWorkspace.address}
                  onChange={(e) => setNewWorkspace({ ...newWorkspace, address: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Timezone</label>
                <select
                  value={newWorkspace.timezone}
                  onChange={(e) => setNewWorkspace({ ...newWorkspace, timezone: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option>UTC</option>
                  <option>EST</option>
                  <option>PST</option>
                  <option>IST</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Contact Email</label>
                <input
                  type="email"
                  value={newWorkspace.contact_email}
                  onChange={(e) => setNewWorkspace({ ...newWorkspace, contact_email: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-green-600 text-white py-2 rounded-md font-medium hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? 'Creating...' : 'Create Workspace'}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
