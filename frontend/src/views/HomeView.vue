<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <b-container style="margin-top: 20px">
      <div class="query_box">
        <b-form-select v-model="field" :options="options"></b-form-select>
        <b-form-input
          v-model="query"
          placeholder="Enter info you need"
        ></b-form-input>
        <b-button variant="outline-primary" @click="get_query()"
          >Query</b-button
        >
      </div>
    </b-container>
    <b-container>
      <b-card
        class="query_card mb-3"
        v-for="info in prod_info"
        :key="info.asin"
        :title="`${info.title}`"
        :sub-title="`corr:${info.corr}`"
        :img-src="info.img"
        img-left
      >
        <b-card-text
          ><b>Feature: </b>
          <li v-for="(f, index) in info.feature" :key="index">
            {{ f }}
          </li></b-card-text
        >
        <b-card-text
          ><b>Description: </b>
          <li v-for="(f, index) in info.description" :key="index">
            {{ f }}
          </li></b-card-text
        >
        <b-card-text
          ><p><b>Hot Review: </b>{{ info.review.text }}</p>
          <p><b>Vote: </b>{{ info.review.vote }}</p>
          <p><b>Avg Score: </b>{{ info.review.score }}</p></b-card-text
        >

        <b-card-text><b>Price :</b>{{ info.price }}</b-card-text>
        <a href="#" class="card-link">Go to Detail</a>
      </b-card>
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
          text: "title",
          value: "title",
        },
        {
          text: "review",
          value: "reviewText",
        },
        {
          text: "feature",
          value: "feature",
        },
        {
          text: "summary",
          value: "summary",
        },
        {
          text: "description",
          value: "description",
        },
      ],
      field: "title",
      query: "",
      prod_info: [
        {
          asin: "B07XQQQQQQ",
          corr: "0.99",
          title: "Test-The Great Gatsby",
          feature: [
            "The Great Gatsby is a novel written by American author F. Scott Fitzgerald that chronicles the adventures of the fabulously wealthy Jay Gatsby and his friends Nick and Jay.",
          ],
          description: [
            "The Great Gatsby is a novel written by American author F. Scott Fitzgerald that chronicles the adventures of the fabulously wealthy Jay Gatsby and his friends Nick and Jay.",
          ],
          review: {
            text: "good",
            vote: 5,
            score: 4.9,
          },
          price: "99$",
        },
        {
          asin: "B07XQQBQQQ",
          title: "Test2-The Great Gatsby",
          feature: [
            "The Great Gatsby is a novel written by American author F. Scott Fitzgerald that chronicles the adventures of the fabulously wealthy Jay Gatsby and his friends Nick and Jay.",
          ],
          description: [
            "The Great Gatsby is a novel written by American author F. Scott Fitzgerald that chronicles the adventures of the fabulously wealthy Jay Gatsby and his friends Nick and Jay.",
          ],
          review: {
            top_review: "good",
            vote: 5,
            score: 4.9,
          },
          price: "99$",
        },
      ],
    };
  },
  methods: {
    get_query: function () {
      let params = {
        field: this.field,
        query: this.query,
      };
      this.$http
        .get("http://127.0.0.1:5000/query", {
          params: params,
        })
        .then((response) => {
          console.log(response);
          this.prod_info = response.data;
          console.log(this.prod_info);
        });
    },
  },
};
</script>
<style lang="less" scoped>
* {
  // margin: 0;
  // padding: 0;
  box-sizing: border-box;
}

.home {
  // display: flex;
  /* justify-content: center; */
  // align-items: center;
  margin: 0 auto;
  width: 100%;
  height: 100%;
}
p {
  text-align: left;
}
img {
  width: 50%;
  height: 50%;
}
.query_box {
  display: flex;
  flex-direction: row;
  // align-items: center;
  justify-content: center;
  width: 75%;
  margin: 0 auto;
  // margin-top: 20px;
}
.query_card {
  width: 100%;
  height: auto;
  margin-top: 2rem;
  margin-bottom: 2rem;
}
.container {
  width: 90%;
  margin: 0 auto;
}
</style>
