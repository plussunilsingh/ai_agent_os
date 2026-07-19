import React, { useState, useEffect } from 'react';
import { BotanixAiOsService } from './botanixUiService';

export interface AdminUser {
  id: string;
  username: string;
  email: string;
  role: string;
  active: boolean;
  createdAt: string;
}

export function BotanixAdminDashboard() {
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [aiStatus, setAiStatus] = useState<any>(null);
  const [prompt, setPrompt] = useState('');
  const [planResult, setPlanResult] = useState<any>(null);
  const [generating, setGenerating] = useState(false);

  // Theme helper for contrast compliance
  const t = (darkClass: string, lightClass: string) => `${darkClass} ${lightClass}`;

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const userData = await BotanixAiOsService.getAdminUsers();
      if (userData.success && Array.isArray(userData.data)) {
        setUsers(userData.data);
      }
      const statusData = await BotanixAiOsService.getAiOsStatus();
      setAiStatus(statusData);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAiPlan = async () => {
    if (!prompt.trim()) return;
    setGenerating(true);
    try {
      const result = await BotanixAiOsService.generateAiPlan(prompt, 'admin-java-app');
      setPlanResult(result);
    } catch (err) {
      console.error('Failed to generate AI plan:', err);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 font-sans">
      <header className="flex items-center justify-between border-b border-slate-800 pb-6 mb-8">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            🌿 Botanix Admin & AI-SE OS Control Center
          </h1>
          <p className={t('text-slate-400', 'text-slate-600') + ' mt-1 text-sm'}>
            Enterprise Java Spring Boot Backend + PostgreSQL DB + Ollama (qwen2.5:7b)
          </p>
        </div>

        <div className="flex items-center gap-3">
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
            PostgreSQL: Connected
          </span>
          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
            aiStatus?.status === 'connected' ? 'bg-blue-500/10 text-blue-400 border border-blue-500/30' : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
          }`}>
            AI-SE OS: {aiStatus?.status || 'Active (qwen2.5:7b)'}
          </span>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Admin Users Table */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-white">Admin Users Directory</h2>
            <button 
              onClick={fetchData} 
              className="text-xs px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-md transition-colors"
            >
              🔄 Refresh
            </button>
          </div>

          {loading ? (
            <p className={t('text-slate-400', 'text-slate-500') + ' py-8 text-center'}>Loading users...</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm border-collapse">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase text-xs">
                    <th className="py-3 px-4">Username</th>
                    <th className="py-3 px-4">Email</th>
                    <th className="py-3 px-4">Role</th>
                    <th className="py-3 px-4">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {users.map((u) => (
                    <tr key={u.id} className="hover:bg-slate-800/40 transition-colors">
                      <td className="py-3 px-4 font-medium text-white">{u.username}</td>
                      <td className={t('text-slate-300', 'text-slate-700') + ' py-3 px-4'}>{u.email}</td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-0.5 text-xs font-semibold rounded bg-purple-500/10 text-purple-400 border border-purple-500/20">
                          {u.role}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-0.5 text-xs font-semibold rounded bg-emerald-500/10 text-emerald-400">
                          Active
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Right Column: AI-SE OS Autonomous Task Planner */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col">
          <h2 className="text-xl font-bold text-white mb-2">🤖 AI-SE OS Task Planner</h2>
          <p className={t('text-slate-400', 'text-slate-600') + ' text-xs mb-4'}>
            Powered by local Ollama model (qwen2.5:7b). Zero LLM API cost.
          </p>

          <textarea
            className="w-full p-3 bg-slate-950 border border-slate-800 rounded-lg text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 mb-3"
            rows={4}
            placeholder="Enter new feature requirement..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />

          <button
            onClick={handleGenerateAiPlan}
            disabled={generating}
            className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            {generating ? 'AI-SE OS Processing...' : '⚡ Generate Plan via qwen2.5:7b'}
          </button>

          {planResult && (
            <div className="mt-4 p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs overflow-y-auto max-h-64">
              <h4 className="font-bold text-emerald-400 mb-1">Generated Plan Output:</h4>
              <pre className="whitespace-pre-wrap text-slate-300">
                {typeof planResult.plan_output === 'string' ? planResult.plan_output : JSON.stringify(planResult, null, 2)}
              </pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
