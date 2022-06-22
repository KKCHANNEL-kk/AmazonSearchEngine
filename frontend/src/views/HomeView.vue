<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <b-container>
      <t-row>
        <t-col flex="100px">
          <t-select
            v-model="field"
            :options="options"
            placeholder="请选择云解决方案"
          />
        </t-col>
        <t-col flex="auto">
          <t-input></t-input>
        </t-col>
        <t-col flex="100px">
          <t-button>搜索</t-button>
        </t-col>
      </t-row>
    </b-container>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "HomeView",
  components: {},
  data() {
    return {
      options: [
        {
          label: "title",
          value: "1",
        },
        {
          label: "选项2",
          value: "2",
        },
        {
          label: "选项3",
          value: "3",
        },
      ],
      field: "title",
    };
  },
};
</script>
<style scoped lang="css">
.home {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
