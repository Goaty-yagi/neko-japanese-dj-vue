<template>
  <AbstractCreateAndConfirm :obj="objForModal" />
</template>

<script>
// answerConfig: {
//     clickFun:this.answerClickFun,
//     showHandler:this.handleShowAnswerPage,
//     questionTitle:this.questionTitle,
//     questionDescription:this.questionDescription,
//     questionId:this.questionId
// },

import axios from "axios";
import AbstractCreateAndConfirm from "@/components/board/AbstractCreateAndConfirm.vue";
export default {
  components: {
    AbstractCreateAndConfirm,
  },
  data() {
    return {
      errorMessage: "components/board/Answer",
      description: "",
      alert: false,
      objForModal: {
        mainTitle: "質問文",
        title: this.config.questionTitle,
        text: this.config.questionDescription,
        userMainText: "回答文",
        placeholder: "回答",
        buttonText: "回答する",
        cancelFunc: this.handlePage,
        buttonFunc: this.addAnswer,
      },
    };
  },
  props: [
    "config",
  ],
  mounted() {
  },
  beforeUnmount() {
    
  },
  methods: {
    async answerPost(description) {
      await axios({
        method: "post",
        url: "/api/board/answer/create",
        data: {
          description: description,
          user: this.$store.state.signup.user.UID,
          question: this.config.questionId,
        },
      })
      .then((res) => {
        this.$store.commit("setAnswerToQuestion", res.data);
      })
      .catch((e) => {
        this.$store.commit("setApiError");
      });
    },
    async addAnswer(description) {
      this.$store.commit('setIsLoading', true)
      await this.answerPost(description);
      this.config.clickFun()
      this.$store.dispatch("handleNotifications", "answer");
      this.$store.commit('setIsLoading', false)
    },
    handlePage() {
      this.config.showHandler()
    },
  },
};
</script>

<style>
</style>