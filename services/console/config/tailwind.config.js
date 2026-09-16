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
        // Monochrome accent: the UI is black and white, so the former brand
        // ramp resolves to neutrals (light values read as accents on the dark
        // chrome, dark values sit under light text).
        centaur: {
          50: '#ffffff', 100: '#fafafa', 200: '#f4f4f5',
          300: '#e4e4e7', 400: '#d4d4d8', 500: '#e8e8ea',
          600: '#a1a1aa', 700: '#71717a', 800: '#52525b', 900: '#3f3f46'
        },
        // Near-black neutral surfaces matching centaur.run (#050506 page,
        // #101012 / #111114 surfaces, #17171a sunk).
        ink: {
          950: '#050506', 900: '#070708', 850: '#0b0b0d', 800: '#101012',
          700: '#17171a', 600: '#242427', 500: '#33333a'
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
