module.exports = {
  type: "react-component",
  npm: {
    cjs: false,
    esModules: false,
    umd: {
      global: "CONPReact",
      externals: {
        react: "React"
      }
    }
  }
};
