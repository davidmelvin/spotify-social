const fs = require("fs");

exports.readFiles = function readFiles(dirname, onFileContent) {
  // fs.readdir(dirname, function (err, filenames) {
  //   if (err) {
  //     onError(err);
  //     return;
  //   }
  //   for (const filename of filenames) {
  //     if (!filename.endsWith(".json")) {
  //       console.log("Skipping ", filename);
  //       continue;
  //     }

  //     content = fs.readFileSync(dirname + filename, "utf-8");
  //     onFileContent(filename, content);
  //   }
  // });

  filenames = fs.readdirSync(dirname);

  for (const filename of filenames) {
    if (!filename.endsWith(".json")) {
      console.log("Skipping ", filename);
      continue;
    }

    content = fs.readFileSync(dirname + filename, "utf-8");
    onFileContent(filename, content);
  }
};
