module.exports = {
  type: "react-component",
  npm: {
    esModules: true,
    umd: {
      global: "CONPReact",
      externals: {
        react: "React"
      }
    }
  }
};
