import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import { useTheme } from "./hooks/useTheme";
import Translator from "./pages/Translator";
import Sentiment from "./pages/Sentiment";
import Combined from "./pages/Combined";
import About from "./pages/About";

function Layout({ children }: { children: React.ReactNode }) {
  const { dark, toggle } = useTheme();

  const navItems = [
    { path: "/", label: "Translator" },
    { path: "/sentiment", label: "Sentiment" },
    { path: "/combined", label: "Combined" },
    { path: "/about", label: "About" },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-700">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          <h1 className="text-lg font-semibold text-brand-700 dark:text-brand-300">
            Translator &amp; Sentiment Analyser
          </h1>
          <nav className="flex items-center gap-1" aria-label="Main navigation">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-brand-100 text-brand-800 dark:bg-brand-900 dark:text-brand-200"
                      : "text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
            <button
              onClick={toggle}
              aria-label={dark ? "Switch to light theme" : "Switch to dark theme"}
              className="ml-2 px-2 py-1 rounded-md text-sm border border-slate-300 dark:border-slate-600"
            >
              {dark ? "Light" : "Dark"}
            </button>
          </nav>
        </div>
      </header>
      <main className="flex-1 max-w-5xl mx-auto w-full px-4 py-8">
        {children}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Translator />} />
          <Route path="/sentiment" element={<Sentiment />} />
          <Route path="/combined" element={<Combined />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
