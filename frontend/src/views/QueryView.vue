<template>
  <div>
    <b-container class="query_container">
      <t-row>
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
export default {
  name: "QueryView",
};
</script>
<style scoped>
.query_container {
  text-align: center; /*让div内部文字居中*/
  height: 350px;
  margin: 0 auto;
  padding-top: 20%;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
</style>
