module.exports = {
    env: {
      node: true,
      browser: true,
      es2021: true,
    },
    extends: [
      'eslint:recommended',
      'plugin:vue/essential', // Если вы используете Vue
    ],
    parserOptions: {
      ecmaVersion: 12,
      sourceType: 'module',
    },
    // rules: {
    //   // Здесь вы можете добавить свои правила
    // },
  };
