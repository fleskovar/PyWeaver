const path = require('path')
console.log();

module.exports = {
    runtimeCompiler: true,
    outputDir: path.resolve(__dirname, "../pkg/PyWeaver/static"),
    pages: {
      index: {
        // entry for the page
        entry: 'src/main.js',
        // the source template
        template: 'public/index.html',
        // output as dist/index.html
        filename: 'index.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'Index Page',
        // chunks to include on this page, by default includes
        // extracted common chunks and vendor chunks.
        chunks: ['chunk-vendors', 'chunk-common', 'index']
      },
      nodeViewer: {
        // entry for the page
        entry: 'src/NodeViewer/NodeViewer_main.js',
        // the source template
        template: 'public/node_viewer.html',
        // output as dist/index.html
        filename: 'node_viewer.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'Node Viewer',
        // chunks to include on this page, by default includes
        // extracted common chunks and vendor chunks.
        chunks: ['chunk-vendors', 'chunk-common', 'nodeViewer']
      },
    }
  };