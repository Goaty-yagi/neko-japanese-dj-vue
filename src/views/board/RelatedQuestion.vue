<template>
  <div class="related-wrapper scroll_area">
    <div class="main-wrapper">
      <h1 class="title-white">質問板</h1>
      <div class="related-title">関連した質問</div>
      <AbstractQuestionList :questions="$store.state.board.relatedQuestion" />
    </div>
  </div>
</template>

<script>
import { router } from "/src/main.js";
import AbstractQuestionList from "@/components/board/AbstractQuestionList.vue";
export default {
  components: {
    AbstractQuestionList,
  },
  data() {
    return {};
  },
  beforeMount() {
      this.$store.commit('setIsLoading', false)
  },
  mounted() {
    this.scrollTop();
    console.log("MOUNTED", this.relatedQuestions);
  },
  computed: {
    relatedQuestions() {
      return this.$store.state.board.relatedQuestion;
    },
  },
  methods: {
    scrollTop() {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";

.related-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.main-wrapper {
  .related-title {
    font-size: 1.2rem;
    font-weight: bold;
    margin: 2rem 0;
    color: $dark-blue;
  }
}
</style>