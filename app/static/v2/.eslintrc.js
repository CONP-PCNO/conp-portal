const path = require('path');

/** @type {import("eslint").Linter.Config} */
module.exports = {
  root: true,
  ignorePatterns: '*.js',
  env: {
    browser: true,
    es2021: true
  },
  extends: ['eslint:recommended', 'plugin:react/recommended', 'plugin:storybook/recommended'],
  plugins: ['@typescript-eslint'],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true
    }
  },
  overrides: [
    {
      files: ['*.ts', '*.tsx'],
      extends: [
        'plugin:@typescript-eslint/recommended',
        'plugin:@typescript-eslint/recommended-requiring-type-checking'
      ],
      parser: '@typescript-eslint/parser',
      parserOptions: {
        ecmaFeatures: {
          tsx: true
        },
        project: [path.resolve(__dirname, 'tsconfig.json')]
      }
    }
  ],
  settings: {
    react: {
      version: 'detect'
    }
  }
};
