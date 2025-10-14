// Dark mode toggle logic
(function() {
	const STORAGE_KEY = 'portfolio-theme';
	const CLASS_DARK = 'theme-dark';
	const toggleBtn = document.getElementById('theme-toggle');
	// We no longer update icon text; icons are controlled with CSS via theme class
	const metaTheme = document.getElementById('meta-theme-color');

	function systemPrefersDark() {
		return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
	}

	function applyTheme(dark) {
		const root = document.documentElement; // <html>
		if (dark) {
			root.classList.add(CLASS_DARK);
			if (metaTheme) metaTheme.setAttribute('content', '#0f1419');
		} else {
			root.classList.remove(CLASS_DARK);
			if (metaTheme) metaTheme.setAttribute('content', '#ffffff');
		}
		if (toggleBtn) {
			toggleBtn.setAttribute('aria-pressed', dark ? 'true' : 'false');
			toggleBtn.setAttribute('aria-label', dark ? 'Activate light theme' : 'Activate dark theme');
		}
	}

	function getStoredPreference() {
		try { return localStorage.getItem(STORAGE_KEY); } catch (_) { return null; }
	}

	function storePreference(val) {
		try { localStorage.setItem(STORAGE_KEY, val); } catch (_) { /* ignore */ }
	}

	// Initial load
	const stored = getStoredPreference();
	const initialDark = stored === 'dark' || (stored === null && systemPrefersDark());
	applyTheme(initialDark);

	// Listen for system changes if user hasn't explicitly chosen
	if (stored === null && window.matchMedia) {
		window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
			applyTheme(e.matches);
		});
	}

	if (toggleBtn) {
		toggleBtn.addEventListener('click', () => {
			const willBeDark = !document.documentElement.classList.contains(CLASS_DARK);
			applyTheme(willBeDark);
			storePreference(willBeDark ? 'dark' : 'light');
		});
	}
})();
