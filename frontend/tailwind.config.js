/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cloud: {
          primary: "#4A4466",   // main brand
          secondary: "#6EADBC",
          accent: "#9FCBAD",
          light: "#F1F7D4"
        }
      }
    }
  },
  plugins: [],
};