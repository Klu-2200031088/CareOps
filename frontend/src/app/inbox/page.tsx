'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore, useWorkspaceStore } from '@/services/store';
import { inboxApi } from '@/services/api';
import { format } from 'date-fns';

export default function InboxPage() {
  const { token } = useAuthStore();
  const { currentWorkspace } = useWorkspaceStore();
  const [conversations, setConversations] = useState<any[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<any>(null);
  const [messageText, setMessageText] = useState('');
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    if (!token || !currentWorkspace) {
      router.push('/workspaces');
      return;
    }

    loadConversations();
  }, [token, currentWorkspace, router]);

  const loadConversations = async () => {
    try {
      const response = await inboxApi.getConversations(token!, currentWorkspace.id);
      setConversations(response.data);
      if (response.data.length > 0) {
        setSelectedConversation(response.data[0]);
      }
    } catch (error) {
      console.error('Failed to load conversations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!messageText.trim() || !selectedConversation) return;

    setLoading(true);
    try {
      await inboxApi.sendMessage(token!, currentWorkspace.id, selectedConversation.id, {
        content: messageText,
        sender_type: 'staff',
        channel: 'system'
      });

      setMessageText('');
      await loadConversations();
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8">Loading...</div>;

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Conversations List */}
      <div className="w-80 bg-white border-r border-gray-200">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-xl font-bold">💬 Inbox</h2>
          <p className="text-sm text-gray-600">{conversations.length} conversations</p>
        </div>

        <div className="overflow-y-auto h-[calc(100vh-80px)]">
          {conversations.map((conv) => (
            <div
              key={conv.id}
              onClick={() => setSelectedConversation(conv)}
              className={`p-4 border-b cursor-pointer hover:bg-gray-50 ${
                selectedConversation?.id === conv.id ? 'bg-blue-50' : ''
              }`}
            >
              <p className="font-semibold">{conv.contact.name}</p>
              <p className="text-sm text-gray-600">{conv.contact.email}</p>
              <p className="text-xs text-gray-500 mt-1">
                {format(new Date(conv.updated_at), 'MMM d, HH:mm')}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Chat View */}
      <div className="flex-1 flex flex-col">
        {selectedConversation ? (
          <>
            {/* Header */}
            <div className="bg-white border-b border-gray-200 p-4">
              <h3 className="text-lg font-bold">{selectedConversation.contact.name}</h3>
              <p className="text-sm text-gray-600">{selectedConversation.contact.email}</p>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {selectedConversation.messages?.map((msg: any) => (
                <div
                  key={msg.id}
                  className={`flex ${msg.sender_type === 'staff' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                      msg.sender_type === 'staff'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 text-gray-900'
                    }`}
                  >
                    <p className="text-sm">{msg.content}</p>
                    <p className="text-xs mt-1 opacity-70">
                      {format(new Date(msg.created_at), 'HH:mm')}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {/* Input */}
            <form onSubmit={handleSendMessage} className="border-t border-gray-200 p-4 bg-white">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={messageText}
                  onChange={(e) => setMessageText(e.target.value)}
                  placeholder="Type a message..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  Send
                </button>
              </div>
            </form>
          </>
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500">Select a conversation to start</p>
          </div>
        )}
      </div>
    </div>
  );
}
