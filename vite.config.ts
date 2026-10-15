import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';
export default defineConfig({
  base: process.env.NODE_ENV === 'production' ? '/NPTEL_Reinforcement_Learning_Website/' : '/',
  plugins: [tailwindcss()]
});
