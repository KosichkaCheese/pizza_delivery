// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true
// })
const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  chainWebpack: (config) => {
    // Удаляем существующий загрузчик для SVG
    const svgRule = config.module.rule('svg');
    svgRule.uses.clear();

    // Добавляем новый загрузчик для обработки SVG
    svgRule
      .use('vue-svg-loader')
      .loader('vue-svg-loader')
      .options({
        // Опции для vue-svg-loader
        // Например, вы можете настроить, чтобы SVG были инлайн
      });
  },
});

module.exports = {
  chainWebpack: config => {
    config.module.rules.delete("svg");
  },
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.svg$/, 
          loader: 'vue-svg-loader', 
        },
      ],
    }      
  }
};
