# **npm libraries downloader**

Downloads all `npm` library names using the [`all-the-package-names`](https://www.npmjs.com/package/all-the-package-names) package.

## *installation*

First make sure you have [`npm` installed](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).
Then switch directory and install the dependencies.

```bash
npm --version

cd npm_libraries/

npm install
```

## *usage*

Use node to run the download script.
This will download all `npm` library names to `../data/libraries/npm_data.json`.

```bash
node download_libraries.js
```
