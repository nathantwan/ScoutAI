import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'
import { copyFileSync, mkdirSync } from 'fs'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    {
      name: 'copy-extension-files',
      writeBundle() {
        // Copy manifest and other files to dist
        copyFileSync('manifest.json', 'dist/manifest.json')
        copyFileSync('popup.html', 'dist/popup.html')
        copyFileSync('popup.js', 'dist/popup.js')
        
        // Create icons directory and copy placeholder icons
        mkdirSync('dist/icons', { recursive: true })
        
        // Create placeholder icons (you would replace these with actual icons)
        const iconSizes = [16, 32, 48, 128]
        iconSizes.forEach(size => {
          // Create a simple SVG icon as placeholder
          const svgIcon = `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
            <rect width="${size}" height="${size}" fill="#3b82f6"/>
            <text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="white" font-family="Arial" font-size="${size * 0.4}">S</text>
          </svg>`
          
          // For now, we'll create a simple text file as placeholder
          // In production, you'd convert this to PNG
          copyFileSync('manifest.json', `dist/icons/icon${size}.png`)
        })
      }
    }
  ],
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        sidebar: resolve(__dirname, 'src/content/sidebar.tsx'),
        background: resolve(__dirname, 'src/background/background.ts'),
        content: resolve(__dirname, 'src/content/content.ts')
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]'
      }
    }
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  }
}) 