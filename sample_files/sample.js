const fs = require('fs');
const path = require('path');

function readFileSync(path) {
  return fs.readFileSync(path, 'utf8');
}

function writeFileSync(path, data) {
  fs.writeFileSync(path, data, 'utf8');
}

function appendFileSync(path, data) {
  fs.appendFileSync(path, data, 'utf8');
}

function deleteFileSync(path) {
  fs.unlinkSync(path);
}

function doesFileExistSync(path) {
  return fs.existsSync(path);
}

function getFilesInDirectorySync(dir) {
  return fs.readdirSync(dir).filter(file => {
    return fs.statSync(path.join(dir, file)).isFile();
  });
}

console.log('Sample JS file');
console.log('Another line');
console.log('Yet another line');
console.log('This is line 5');
console.log('This is line 6');
console.log('More content');
console.log('Additional lines');
console.log('Keep adding lines');
console.log('Line 10');
console.log('Line 11');
console.log('Line 12');