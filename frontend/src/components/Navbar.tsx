import React, { useState } from 'react';
import { Sprout, ShieldCheck, MapPin, Database, RefreshCw, Globe2, Moon, Sun } from 'lucide-react';
import { Language, translations } from '../i18n/translations';

interface NavbarProps {
  currentRole: 'farmer' | 'expert' | 'official';
  onRoleChange: (role: 'farmer' | 'expert' | 'official') => void;
  currentLanguage: Language;
  onLanguageChange: (lang: Language) => void;
  onLoadDemo: () => Promise<void>;
  isLoadingDemo: boolean;
  demoLoaded: boolean;
  theme: 'light' | 'dark';
  onToggleTheme: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentRole,
  onRoleChange,
  currentLanguage,
  onLanguageChange,
  onLoadDemo,
  isLoadingDemo,
  demoLoaded,
  theme,
  onToggleTheme
}) => {
  const t = translations[currentLanguage];

  return (
    <header className="bg-slate-900 text-white sticky top-0 z-50 shadow-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
        <div className="flex flex-col gap-2 py-2.5 sm:h-16 sm:flex-row sm:items-center sm:justify-between sm:py-0">
          
          {/* Logo & Tagline */}
          <div className="flex items-center space-x-2.5 sm:space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-green-400 flex items-center justify-center shadow-lg shadow-green-900/30 shrink-0">
              <Sprout className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-lg sm:text-xl tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-green-200 truncate">
                  {t.appTitle}
                </span>
                <span className="hidden sm:inline text-[10px] font-semibold tracking-wider uppercase px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800">
                  SIH 2026
                </span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">
                {t.tagline}
              </p>
            </div>
          </div>

          {/* Mobile: a dedicated full-width role switcher keeps navigation readable. */}
          <nav className="order-3 grid w-full grid-cols-3 items-center bg-slate-800/80 p-1 rounded-xl border border-slate-700/60 sm:order-2 sm:flex sm:w-auto sm:shrink-0 gap-1">
            <button
              onClick={() => onRoleChange('farmer')}
              className={`flex min-w-0 items-center justify-center space-x-1 px-1.5 py-2 rounded-lg text-xs font-semibold transition-all sm:flex-none sm:space-x-2 sm:px-3 sm:py-1.5 ${
                currentRole === 'farmer'
                  ? 'bg-emerald-600 text-white shadow'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Sprout className="w-3.5 h-3.5 sm:w-4 sm:h-4 shrink-0" />
              <span className="inline xl:hidden text-[11px] sm:text-xs">Farmer</span>
              <span className="hidden xl:inline">{t.farmerPortal}</span>
            </button>
            <button
              onClick={() => onRoleChange('expert')}
              className={`flex min-w-0 items-center justify-center space-x-1 px-1.5 py-2 rounded-lg text-xs font-semibold transition-all sm:flex-none sm:space-x-2 sm:px-3 sm:py-1.5 ${
                currentRole === 'expert'
                  ? 'bg-indigo-600 text-white shadow'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <ShieldCheck className="w-3.5 h-3.5 sm:w-4 sm:h-4 shrink-0" />
              <span className="inline xl:hidden text-[11px] sm:text-xs">Expert</span>
              <span className="hidden xl:inline">{t.expertPortal}</span>
            </button>
            <button
              onClick={() => onRoleChange('official')}
              className={`flex min-w-0 items-center justify-center space-x-1 px-1.5 py-2 rounded-lg text-xs font-semibold transition-all sm:flex-none sm:space-x-2 sm:px-3 sm:py-1.5 ${
                currentRole === 'official'
                  ? 'bg-amber-600 text-white shadow'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <MapPin className="w-3.5 h-3.5 sm:w-4 sm:h-4 shrink-0" />
              <span className="inline xl:hidden text-[11px] sm:text-xs">GIS Map</span>
              <span className="hidden xl:inline">{t.officialPortal}</span>
            </button>
          </nav>

          {/* Right Side: Demo Seeder & Language Dropdown */}
          <div className="order-2 absolute right-3 top-3 flex items-center space-x-2 sm:static sm:space-x-3">
            
            {/* One-Click SIH Demo Seeder Button */}
            <button
              onClick={onLoadDemo}
              disabled={isLoadingDemo}
              className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-bold transition-all border shadow-sm ${
                demoLoaded
                  ? 'bg-emerald-950/80 text-emerald-300 border-emerald-700 hover:bg-emerald-900/60'
                  : 'bg-emerald-500 hover:bg-emerald-600 text-slate-950 border-emerald-400 font-extrabold'
              }`}
              title="Seeds 105 farms, pest traps, and weather stations"
            >
              <Database className={`w-3.5 h-3.5 ${isLoadingDemo ? 'animate-spin' : ''}`} />
              <span className="hidden xl:inline">
                {isLoadingDemo ? t.loadingDemo : demoLoaded ? t.demoLoaded : t.loadDemo}
              </span>
            </button>

            {/* Language Selector */}
            <div className="flex items-center space-x-1 bg-slate-800 px-1.5 py-1 rounded-lg border border-slate-700 text-xs sm:space-x-1.5 sm:px-2">
              <Globe2 className="w-3.5 h-3.5 text-slate-400" />
              <select
                value={currentLanguage}
                onChange={(e) => onLanguageChange(e.target.value as Language)}
                className="w-14 bg-transparent text-slate-200 focus:outline-none cursor-pointer font-medium sm:w-auto"
              >
                <option value="en" className="bg-slate-900 text-white">English (EN)</option>
                <option value="hi" className="bg-slate-900 text-white">हिंदी (HI)</option>
                <option value="te" className="bg-slate-900 text-white">తెలుగు (TE)</option>
              </select>
            </div>

            <button
              type="button"
              onClick={onToggleTheme}
              className="flex h-8 w-8 items-center justify-center rounded-lg border border-slate-700 bg-slate-800 text-slate-200 transition-colors hover:bg-slate-700"
              aria-label={theme === 'light' ? 'Switch to dark theme' : 'Switch to light theme'}
              title={theme === 'light' ? 'Switch to dark theme' : 'Switch to light theme'}
            >
              {theme === 'light' ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4 text-amber-300" />}
            </button>

          </div>

        </div>
      </div>
    </header>
  );
};
