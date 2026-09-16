module.exports = {
  content: [
    './public/*.html',
    './app/helpers/**/*.rb',
    './app/javascript/**/*.js',
    './app/views/**/*.{erb,haml,html,slim}'
  ],
  theme: {
    extend: {
      colors: {
        // Upstream class names (centaur-*/ink-*) kept working, mapped onto the
        // shadcn neutral scale. Semantic tokens (background, card, primary, …)
        // come from the @theme block in app/assets/tailwind/application.css.
        centaur: {
          50: '#ffffff', 100: '#fafafa', 200: '#f5f5f5', 300: '#e5e5e5',
          400: '#d4d4d4', 500: '#a1a1a1', 600: '#737373', 700: '#525252',
          800: '#404040', 900: '#262626'
        },
        ink: {
          950: '#0a0a0a', 900: '#0a0a0a', 850: '#141414', 800: '#171717',
          700: '#1f1f1f', 600: '#262626', 500: '#343434', 400: '#404040'
        }
      },
      fontFamily: {
        sans: [
          'ui-sans-serif',
          'system-ui',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'sans-serif'
        ],
        mono: [
          'Berkeley Mono',
          'Berkeley Mono Variable',
          'BerkeleyMono',
          'JetBrains Mono',
          'ui-monospace',
          'SFMono-Regular',
          'Menlo',
          'monospace'
        ]
      }
    },
    // Very small radii everywhere for the sharp, terminal-ish look.
    borderRadius: {
      none: '0px',
      sm: 'calc(var(--radius) - 4px)',
      DEFAULT: 'calc(var(--radius) - 4px)',
      md: 'calc(var(--radius) - 2px)',
      lg: 'var(--radius)',
      xl: 'calc(var(--radius) + 4px)',
      '2xl': 'calc(var(--radius) + 8px)',
      '3xl': 'calc(var(--radius) + 12px)',
      full: '9999px'
    }
  },
  plugins: []
}
