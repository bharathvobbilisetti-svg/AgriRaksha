import React, { useEffect, useState } from 'react';
import { Navbar } from './components/Navbar';
import { FarmerPortal } from './pages/FarmerPortal';
import { ExpertPortal } from './pages/ExpertPortal';
import { OfficialDashboard } from './pages/OfficialDashboard';
import { AuthPage } from './pages/AuthPage';
import { Language } from './i18n/translations';
import { api } from './services/api';

export const App: React.FC = () => {
  const [currentRole, setCurrentRole] = useState<'farmer' | 'expert' | 'official'>('farmer');
  const [currentLanguage, setCurrentLanguage] = useState<Language>('en');
  const [isLoadingDemo, setIsLoadingDemo] = useState(false);
  const [demoLoaded, setDemoLoaded] = useState(true); // Pre-seeded by default
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [theme, setTheme] = useState<'light' | 'dark'>(() => (
    localStorage.getItem('agriraksha-theme') === 'dark' ? 'dark' : 'light'
  ));

  useEffect(() => {
    localStorage.setItem('agriraksha-theme', theme);
  }, [theme]);

  const handleLoadDemo = async () => {
    setIsLoadingDemo(true);
    try {
      await api.seedDemo();
      setDemoLoaded(true);
    } catch (err) {
      console.error("Demo seeding failed:", err);
    } finally {
      setIsLoadingDemo(false);
    }
  };

  const handleAuthenticated = (authData: any) => {
    const role = authData.user?.role;
    setCurrentRole(role === 'official' ? 'official' : role === 'expert' || role === 'extension_worker' ? 'expert' : 'farmer');
    if (authData.user?.preferred_language === 'hi' || authData.user?.preferred_language === 'te') {
      setCurrentLanguage(authData.user.preferred_language);
    }
    setIsAuthenticated(true);
  };

  return (
    <div className={`${theme === 'dark' ? 'dark' : ''} min-h-screen bg-slate-50 flex flex-col font-sans`}>
      {isAuthenticated && (
        <Navbar
          currentRole={currentRole}
          onRoleChange={setCurrentRole}
          currentLanguage={currentLanguage}
          onLanguageChange={setCurrentLanguage}
          onLoadDemo={handleLoadDemo}
          isLoadingDemo={isLoadingDemo}
          demoLoaded={demoLoaded}
          theme={theme}
          onToggleTheme={() => setTheme((currentTheme) => currentTheme === 'light' ? 'dark' : 'light')}
        />
      )}

      <main className="flex-1">
        {!isAuthenticated && (
          <AuthPage
            language={currentLanguage}
            onAuthenticated={handleAuthenticated}
            onContinueAsGuest={() => setIsAuthenticated(true)}
          />
        )}
        {isAuthenticated && currentRole === 'farmer' && (
          <FarmerPortal
            language={currentLanguage}
            onNavigateToExpert={() => setCurrentRole('expert')}
            onNavigateToGIS={() => setCurrentRole('official')}
          />
        )}
        {isAuthenticated && currentRole === 'expert' && (
          <ExpertPortal language={currentLanguage} />
        )}
        {isAuthenticated && currentRole === 'official' && (
          <OfficialDashboard language={currentLanguage} />
        )}
      </main>

      {/* Footer */}
      {isAuthenticated && <footer className="bg-white border-t border-slate-200/80 py-4 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>AgriRaksha • Smart India Hackathon (SIH) 2026 Prototype</span>
          <span className="text-[11px] text-slate-400">
            Multimodal Crop Health Early Warning & Decision Support System • Ministry of Agriculture & Farmers Welfare
          </span>
        </div>
      </footer>}
    </div>
  );
};

export default App;
