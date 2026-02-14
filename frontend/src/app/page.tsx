'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/services/store';

export default function Home() {
  const { token } = useAuthStore();
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return;
    
    if (token) {
      router.push('/workspaces');
    } else {
      router.push('/login');
    }
  }, [token, mounted, router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-600 to-indigo-600">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-white mb-4">🎯 CareOps</h1>
        <p className="text-xl text-blue-100">Unified Operations Platform</p>
        <p className="text-blue-200 mt-4">Loading...</p>
      </div>
    </div>
  );
}
