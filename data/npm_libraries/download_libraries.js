// download all npm library names

const fs = require('fs');
const allThePackageNames = require('all-the-package-names');

// get all package names and normalize to lowercase
const normalised = allThePackageNames.map((name) => name.toLowerCase());

// prepare data in required format
const data = {
  datetime: new Date().toISOString(),
  data: normalised.sort(),
};

// write to json file
const outputPath = '../data/npm_libraries/npm_data.json';
fs.writeFileSync(outputPath, JSON.stringify(data, null, 2));

console.log(`Downloaded ${normalised.length.toLocaleString()} package names to ${outputPath}`);
