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
        // Upstream class names map onto the shadcn tokens (not fixed hexes) so
        // every surface follows the light/dark theme. Tailwind v4 renders
        // /alpha modifiers with color-mix(), so `bg-ink-800/80` still works.
        centaur: {
          50: 'var(--foreground)', 100: 'var(--foreground)', 200: 'var(--foreground)',
          300: 'var(--foreground)', 400: 'var(--primary)', 500: 'var(--primary)',
          600: 'var(--muted-foreground)', 700: 'var(--muted-foreground)',
          800: 'var(--border)', 900: 'var(--border)'
        },
        ink: {
          950: 'var(--background)', 900: 'var(--background)', 850: 'var(--card)',
          800: 'var(--card)', 700: 'var(--muted)', 600: 'var(--border)',
          500: 'var(--input)', 400: 'var(--ring)'
        },
        // The console writes body/secondary text as zinc; these are all light
        // values meant for dark chrome, so they resolve to foreground/muted.
        zinc: {
          50: 'var(--foreground)', 100: 'var(--foreground)', 200: 'var(--foreground)',
          300: 'var(--muted-foreground)', 400: 'var(--muted-foreground)',
          500: 'var(--muted-foreground)', 600: 'var(--muted-foreground)',
          700: 'var(--border)', 800: 'var(--card)', 900: 'var(--background)',
          950: 'var(--background)'
        }
      },
      fontFamily: {
        sans: [
          'Inter Variable',
          'Inter',
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
