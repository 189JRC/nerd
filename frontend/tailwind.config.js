  // tailwind.config.js
  module.exports = {

    purge: [],
 
    purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
     darkMode: false, // or 'media' or 'class'
     theme: {
       extend: {},
     },
     variants: {
       extend: {},
     },
     plugins: [],
   }

   //TODO: LOOK TO OPTIMISE TREE SHAKING FOR PRODUCTION: https://v2.tailwindcss.com/docs/optimizing-for-production
   
   // /** @type {import('tailwindcss').Config} */
// export default {
//   content: [],
//   theme: {
//     extend: {},
//   },
//   plugins: [],
// }

