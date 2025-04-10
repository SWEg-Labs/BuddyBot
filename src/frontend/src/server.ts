import { APP_BASE_HREF } from '@angular/common';
import { CommonEngine, isMainModule } from '@angular/ssr/node';
import express from 'express';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import bootstrap from './main.server';

const serverDistFolder = dirname(fileURLToPath(import.meta.url));
const browserDistFolder = resolve(serverDistFolder, '../browser');
const indexHtml = join(serverDistFolder, 'index.server.html');

const app = express();
const commonEngine = new CommonEngine();

console.log('Initializing server...');
console.log('Server dist folder:', serverDistFolder);
console.log('Browser dist folder:', browserDistFolder);
console.log('Index HTML:', indexHtml);

app.get(
  '**',
  express.static(browserDistFolder, {
    maxAge: '1y',
    index: 'index.html',
  }),
);

app.get('**', (req, res, next) => {
  const { protocol, originalUrl, baseUrl, headers } = req;

  console.log('Incoming request:', req.url);

  commonEngine
    .render({
      bootstrap,
      documentFilePath: indexHtml,
      url: `${protocol}://${headers.host}${originalUrl}`,
      publicPath: browserDistFolder,
      providers: [{ provide: APP_BASE_HREF, useValue: baseUrl }],
    })
    .then((html) => res.send(html))
    .catch((err) => {
      console.error('SSR rendering error:', err);
      next(err);
    });
});

if (isMainModule(import.meta.url)) {
  const port = process.env['PORT'] || 4000;
  console.log(`Server will start on port ${port}...`);

  app.listen(port, () => {
    console.log(`Node Express server listening on http://localhost:${port}`);
  });
} else {
  console.log('Server is not running as main module');
}
