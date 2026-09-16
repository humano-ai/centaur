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
        // Fyndry is monochrome: one neutral ramp, no brand hue. `accent`
        // (aliased as `centaur` so upstream class names keep working) is the
        // light end used for emphasis on the dark chrome; `ink` is the surface
        // ramp from page black to raised borders.
        accent: {
          50: '#ffffff', 100: '#fafafa', 200: '#f4f4f5', 300: '#e4e4e7',
          400: '#d4d4d8', 500: '#c4c4c8', 600: '#a1a1aa', 700: '#71717a',
          800: '#52525b', 900: '#3f3f46'
        },
        centaur: {
          50: '#ffffff', 100: '#fafafa', 200: '#f4f4f5', 300: '#e4e4e7',
          400: '#d4d4d8', 500: '#c4c4c8', 600: '#a1a1aa', 700: '#71717a',
          800: '#52525b', 900: '#3f3f46'
        },
        ink: {
          950: '#000000', 900: '#050506', 850: '#09090b', 800: '#101012',
          700: '#18181b', 600: '#1f1f22', 500: '#27272a', 400: '#3f3f46'
        }
      },
      fontFamily: {
        sans: [
          'Inter',
          'ui-sans-serif',
          'system-ui',
          '-apple-system',
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
      none: '0px', sm: '1px', DEFAULT: '2px', md: '2px',
      lg: '2px', xl: '2px', '2xl': '3px', '3xl': '3px', full: '2px'
    }
  },
  plugins: []
}
