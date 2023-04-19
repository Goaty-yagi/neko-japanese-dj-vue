<template>
  <div class="about-wrapper">
    <div class="main-about-wrapper">
      <div class="about-container">
        <h1 class="title-white">About</h1>
      </div>
      <div class="about-description-container">
        <img src="@/assets/logo-with-logo.png" alt="logo" />
        <div class="about-description">
          {{ description }}
        </div>
      </div>
      <div class="button-container">
        <button :class="{ clicked: show.quiz }" @click="showHandler('quiz')">
          クイズ
        </button>
        <button
          :class="{ clicked: show.community }"
          @click="showHandler('community')"
        >
          コミュニティ
        </button>
      </div>
      <Quiz width="800" v-if="show.quiz" />
      <Community width="800" v-if="show.community" />
    </div>
  </div>
</template>

<script>
import Community from "@/components/abouts/Community.vue";
import Quiz from "@/components/abouts/Quiz.vue";

export default {
  components: {
    Community,
    Quiz,
  },
  data() {
    return {
      description:
        "本サービス”ねこJAPANESE”は以下の三つの理念『楽しく学ぶ』『学び合い』『継続は力なり』を体現することを目的として構築されています。世界中にいるたくさんの日本語学習者が集い、学び、助け合い、各々の目的に合った日本語学習のサポートになれば、それが”ねこJAPANESE”の存在意義になります。",
      show: {
        quiz: true,
        community: false,
      },
    };
  },
  beforeMount() {
      this.$store.commit('setIsLoading', false)
  },
  methods: {
    showHandler(val) {
      this.show.quiz = false;
      this.show.community = false;
      switch (val) {
        case "quiz":
          this.show.quiz = true;
          break;
        case "community":
          this.show.community = true;
          break;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";
.about-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.main-about-wrapper {
  width: 800px;
}
.about-description-container {
  display: flex;
  align-items: center;
  border-top: 0.5rem solid gray;
  border-bottom: 0.5rem solid gray;
  margin-top: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  font-size: 1.4rem;
  img {
    height: 230px;
    width: 100%;
    margin-bottom: 3rem;
    object-fit: cover;
  }
  .about-description {
    margin-top: 1.5rem;
    padding: 1.5rem;
    color: whitesmoke;
    font-weight: bold;
  }
}
.button-container {
  margin: 1rem 0;
  button {
    background: transparent;
    margin: 0.5rem;
    padding: 0 0.8rem;
    font-weight: bold;
    font-size: 1.2rem;
    color: whitesmoke;
    width: 150px;
  }
  .clicked {
    border-left: solid $base-gray;
    border-top: solid $base-gray;
    border-right: solid $base-dark;
    border-bottom: solid $base-dark;
    background: rgba($color: $back-white, $alpha: 0.1);
  }
}
@media (max-width: 800px) {
  .main-about-wrapper {
    width: auto;
  }
  .about-description-container {
    flex-direction: column;
    img {
      height: 150px;
      width: 150px;
      object-fit: cover;
      margin-bottom: 0;
    }
    .about-description {
      margin-top: 0;
    }
  }
}
</style>