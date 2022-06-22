<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js App" />
    <t-button :click="onClick()"> 按钮</t-button>
  </div>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";

// import './custom.scss'

export default {
  name: "App",
  components: {
    HelloWorld,
  },
  methods: {
    onClick() {
      console.log("click");
      this.$router
        .resolve({
          name: "HelloWorld",
          path: "/queryPage",
          params: {
            msg: "Hello World",
          },
        })
        .then(({ component }) => {
          console.log(component);
        });
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
