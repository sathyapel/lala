

const defaultTheme = require('tailwindcss/defaultTheme');
const colors = require('tailwindcss/colors');

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./static/**/*.{py,html,js}",
      "./dashboard/**/*.{py,html,js}",
      "./dashboard/*.{py,html,js}",
    ],


    important: false,
    theme: {
        colors: {
            transparent: 'transparent',
            current: 'currentColor',
            black: colors.black,
            blue: colors.blue,
            cyan: colors.cyan,
            emerald: colors.emerald,
            fuchsia: colors.fuchsia,
            slate: colors.slate,
            gray: colors.gray,
            neutral: colors.neutral,
            stone: colors.stone,
            green: colors.green,
            indigo: colors.indigo,
            lime: colors.lime,
            orange: colors.orange,
            pink: colors.pink,
            purple: colors.purple,
            red: colors.red,
            rose: colors.rose,
            sky: colors.sky,
            teal: colors.teal,
            violet: colors.violet,
            yellow: colors.amber,
            white: colors.white,
        },
        fontSize: {
            'xs': '0.75rem',
            'sm': '0.8rem',
            'base': '1rem',
            'lg': '1.125rem',
            'xl': '1.25rem',
            '2xl': '1.5rem',
            '3xl': '2rem',
            '4xl': '2.4rem',
            '5xl': '3rem',
        },

        extend: {
            fontFamily: {
                sans: ["Nunito", ...defaultTheme.fontFamily.sans],
            },
            inset: {
                '3px': '3px',
            },
            borderRadius: {
                'md': '12px',
                'xl': '2rem',
                '3xl': '50px'
            },
        },
        minWidth: {
            '1/4': '25%',
        }
    },

    corePlugins: {
        aspectRatio: false,
    },


    safelist: [
        {
            pattern: /bg-(red|green|blue)-(100|200|300|400|500|600|700|800|900)/,
          },
    ],

    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography')
    ],
}

