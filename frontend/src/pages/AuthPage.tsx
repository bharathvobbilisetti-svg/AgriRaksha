import React, { FormEvent, useState } from 'react';
import { ArrowRight, Eye, EyeOff, Leaf, LockKeyhole, Mail, MapPin, UserRound } from 'lucide-react';
import { Language } from '../i18n/translations';
import { api } from '../services/api';

interface AuthPageProps {
  language: Language;
  onAuthenticated: (authData: any) => void;
  onContinueAsGuest: () => void;
}

export const AuthPage: React.FC<AuthPageProps> = ({ language, onAuthenticated, onContinueAsGuest }) => {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    full_name: '',
    email: '',
    password: '',
    role: 'farmer',
    village: '',
    preferred_language: language
  });

  const updateField = (field: string, value: string) => {
    setForm((current) => ({ ...current, [field]: value }));
    setError('');
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setIsSubmitting(true);
    setError('');
    try {
      const response = mode === 'login'
        ? await api.login(form.email, form.password)
        : await api.register(form);
      localStorage.setItem('agriraksha_token', response.access_token);
      onAuthenticated(response);
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : 'Something went wrong. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="min-h-[calc(100vh-4rem)] bg-[radial-gradient(circle_at_top_left,_rgba(16,185,129,0.22),_transparent_35%),linear-gradient(135deg,#ecfdf5,#f8fafc_48%,#e0f2fe)] px-4 py-10 sm:px-6">
      <div className="mx-auto grid max-w-5xl overflow-hidden rounded-3xl border border-white/70 bg-white/90 shadow-2xl shadow-emerald-900/10 backdrop-blur lg:grid-cols-[0.9fr_1.1fr]">
        <section className="relative hidden overflow-hidden bg-emerald-950 p-10 text-white lg:block">
          <div className="absolute -right-20 -top-20 h-64 w-64 rounded-full bg-emerald-500/20 blur-3xl" />
          <div className="relative flex h-full flex-col justify-between">
            <div>
              <div className="mb-8 flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-400 text-emerald-950">
                  <Leaf className="h-7 w-7" />
                </div>
                <span className="text-2xl font-black tracking-tight">AgriRaksha</span>
              </div>
              <p className="mb-3 text-sm font-bold uppercase tracking-[0.2em] text-emerald-300">Crop health intelligence</p>
              <h1 className="max-w-md text-4xl font-black leading-tight">Better decisions for every field.</h1>
              <p className="mt-5 max-w-md text-sm leading-7 text-emerald-100/75">
                Connect your farm to disease detection, weather risk, pest surveillance, and expert guidance.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-3 text-xs text-emerald-100/80">
              <div className="rounded-xl border border-emerald-800 bg-emerald-900/60 p-4">AI crop diagnosis</div>
              <div className="rounded-xl border border-emerald-800 bg-emerald-900/60 p-4">Local risk alerts</div>
            </div>
          </div>
        </section>

        <section className="p-6 sm:p-10">
          <div className="mb-8 flex items-center justify-between gap-4">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.18em] text-emerald-700">Welcome to AgriRaksha</p>
              <h2 className="mt-2 text-3xl font-black text-slate-900">{mode === 'login' ? 'Sign in' : 'Create account'}</h2>
              <p className="mt-2 text-sm text-slate-500">{mode === 'login' ? 'Access your crop health workspace.' : 'Set up your farmer or field team profile.'}</p>
            </div>
            <div className="flex rounded-lg bg-slate-100 p-1 text-xs font-bold">
              <button type="button" onClick={() => setMode('login')} className={`rounded-md px-3 py-2 ${mode === 'login' ? 'bg-white text-emerald-700 shadow-sm' : 'text-slate-500'}`}>Login</button>
              <button type="button" onClick={() => setMode('register')} className={`rounded-md px-3 py-2 ${mode === 'register' ? 'bg-white text-emerald-700 shadow-sm' : 'text-slate-500'}`}>Register</button>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {mode === 'register' && (
              <label className="block text-sm font-semibold text-slate-700">
                Full name
                <span className="relative mt-1.5 block"><UserRound className="absolute left-3 top-3 h-4 w-4 text-slate-400" /><input required value={form.full_name} onChange={(event) => updateField('full_name', event.target.value)} className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-3 text-sm outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100" placeholder="Your name" /></span>
              </label>
            )}

            <label className="block text-sm font-semibold text-slate-700">
              Email address
              <span className="relative mt-1.5 block"><Mail className="absolute left-3 top-3 h-4 w-4 text-slate-400" /><input required type="email" value={form.email} onChange={(event) => updateField('email', event.target.value)} className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-3 text-sm outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100" placeholder="you@example.com" /></span>
            </label>

            <label className="block text-sm font-semibold text-slate-700">
              Password
              <span className="relative mt-1.5 block"><LockKeyhole className="absolute left-3 top-3 h-4 w-4 text-slate-400" /><input required minLength={6} type={showPassword ? 'text' : 'password'} value={form.password} onChange={(event) => updateField('password', event.target.value)} className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-10 text-sm outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100" placeholder="At least 6 characters" /><button type="button" onClick={() => setShowPassword((visible) => !visible)} className="absolute right-3 top-2.5 text-slate-400" aria-label="Show password">{showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}</button></span>
            </label>

            {mode === 'register' && (
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <label className="block text-sm font-semibold text-slate-700">Role<select value={form.role} onChange={(event) => updateField('role', event.target.value)} className="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm outline-none focus:border-emerald-500"><option value="farmer">Farmer</option><option value="expert">Agronomist / Expert</option><option value="official">Agriculture Official</option></select></label>
                <label className="block text-sm font-semibold text-slate-700">Village<span className="relative mt-1.5 block"><MapPin className="absolute left-3 top-3 h-4 w-4 text-slate-400" /><input value={form.village} onChange={(event) => updateField('village', event.target.value)} className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-3 text-sm outline-none focus:border-emerald-500" placeholder="Village name" /></span></label>
              </div>
            )}

            {error && <p className="rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-sm font-medium text-rose-700">{error}</p>}
            <button disabled={isSubmitting} className="flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-600 py-3 text-sm font-extrabold text-white shadow-lg shadow-emerald-900/15 transition hover:bg-emerald-700 disabled:cursor-wait disabled:opacity-60">{isSubmitting ? 'Connecting...' : mode === 'login' ? 'Sign in to workspace' : 'Create my account'}<ArrowRight className="h-4 w-4" /></button>
          </form>

          <button type="button" onClick={onContinueAsGuest} className="mt-4 w-full rounded-xl border border-slate-200 py-2.5 text-sm font-bold text-slate-600 transition hover:border-emerald-300 hover:text-emerald-700">Continue as demo guest</button>
        </section>
      </div>
    </main>
  );
};
