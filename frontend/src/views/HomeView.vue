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
        <div>Time: {{ this.time.toFixed(6) }}s</div>
                <div>
          Search Advice:
          <ul v-for="(advice, index) in query_advice" :key="index">
            {{
              advice
            }}
          </ul>
        </div>
        <div>
          Search History:
          <ul v-for="(h, index) in history" :key="index">
            {{
              h
            }}
          </ul>
        </div>
      </div>
    </b-container>
    <b-container v-if="prod_info != []">
      <b-card
        class="query_card mb-3"
        v-for="(info,i) in prod_info"
        :key="info.asin"
        :title="`${info.title}`"
        :sub-title="`corr:${info.corr}`"
        :img-src="info.img ? info.img[0] : ''"
        img-left
      >
        <b-card-text
          ><b>Feature: </b>
          <li v-for="(f, index1) in info.feature" :key="index1">
            {{ f }}
          </li></b-card-text
        >
        <b-card-text
          ><b>Description: </b>
          <li v-for="(f, index2) in info.description" :key="index2">
            {{ f }}
          </li></b-card-text
        >
        <b-card-text
          ><p><b>Hot Review: </b>{{ info.review.text }}</p>
          <p><b>Review Summary: </b>{{ info.review.summary }}</p>
          <p><b>Reviews Count: </b>{{ info.review.cnt }}</p>
          <p><b>Hot Review Vote: </b>{{ info.review.vote }}</p>
          <p><b>Avg Score: </b>{{ info.review.score }}</p>
          <p v-if="i == 0">
          <b>You Maybe Like:</b>
          <ul v-for="(advice,j) in shop_advice" :key="j">
          {{ advice }}
          </ul>
          </p>
        </b-card-text>

        <b-card-text><b>Price :</b>{{ info.price }}</b-card-text>
        <a href="#" class="card-link">Go to Detail</a>
      </b-card>
    </b-container>
    <b-container id="warning" v-if="prod_info == []">
      <b-alert show>There is no result!</b-alert>
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
      time: 0,
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
      query_advice: [],
      shop_advice: [],
      history: [],
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
          this.prod_info = response.data.result;
          this.time = response.data.time;
          this.query_advice = response.data.query_advice;
          this.shop_advice = response.data.shop_advice;
          this.history.push(this.query);
          console.log(response.data);
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
  max-width: 200px;
  max-height: 200px;
}
.query_box {
  display: flex;
  flex-direction: row;
  align-items: baseline;
  justify-content: center;
  width: 75%;
  margin: 0 auto;
  // margin-top: 20px;
}
.query_box div{
  // display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  margin: 0 10px;
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
