#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const glob = require('glob');

// List of directories to process
const TEMPLATE_DIR = './templates/img/';
const NON_PLAYER_DIR = './campaign/characters/non-player/img/';
const NON_PLAYER_DIRS = './campaign/characters/non-player/*/img/';
const PLAYER_DIR = './campaign/characters/player/img/';

// Use glob to get all matching directories
const directories = [TEMPLATE_DIR, NON_PLAYER_DIR, ...glob.sync(NON_PLAYER_DIRS), PLAYER_DIR];

const README_FILENAME = 'README.md';
const NB_IMAGES_PER_LINE = 3;

// Loop through each directory
directories.forEach((ROOT_DIR) => {
  let nbImages = 0;
  let mdContent = '<table><tr>';

  fs.readdirSync(ROOT_DIR).forEach((image) => {
    if (image !== README_FILENAME) {
      if (!(nbImages % NB_IMAGES_PER_LINE)) {
        if (nbImages > 0) {
          mdContent += `
</tr>`;
        }
        mdContent += `
<tr>`;
      }
      nbImages++;
      mdContent += `
<td valign="bottom">
<img src="./${image}" width="250"><br>
${image}
</td>
`;
    }
  });
  mdContent += `
</tr></table>`;

  fs.writeFileSync(path.join(ROOT_DIR, README_FILENAME), mdContent);
});
