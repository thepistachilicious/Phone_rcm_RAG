module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        lato: ['Roboto', 'sans-serif'],
      },
      screens: {
        xs: { max: '600px' },
      },
    },
  },
  plugins: [],
  prefix: 'tw-',
}
