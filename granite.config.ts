import { defineConfig } from '@apps-in-toss/web-framework/config';

export default defineConfig({
  appName: 'dubai-cookie',
  web: {
    host: '0.0.0.0',
    port: 3014,
    commands: {
      dev: 'rsbuild dev --host',
      build: 'rsbuild build',
    },
  },
  permissions: [],
  outdir: 'dist',
  brand: {
    displayName: '내가 두쫀쿠?',
    icon: 'https://raw.githubusercontent.com/jino123413/app-logos/master/dubai-cookie.png',
    primaryColor: '#8B6914',
    bridgeColorMode: 'basic',
  },
  webViewProps: {
    type: 'partner',
  },
});
