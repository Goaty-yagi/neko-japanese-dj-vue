<template>
  <div class="quiz-wrapper">
    <div class="main-text">
      {{ mainText }}
    </div>
    <div class="note">
      {{ note }}
    </div>
    <div
      class="main-quiz-wrapper"
      v-for="(data, index) in dataObjArray"
      v-bind:key="index"
    >
      <div class="title">
        {{ data.title }}
      </div>
      <div class="image">
        <img :src="getImage(data.image)" :alt="data.title" />
      </div>
      <div class="text">
        {{ data.text }}
      </div>
    </div>
    <div v-if="!user" class="signup_login">
        <button @click="goLogin" class='btn-tr-white-base-sq'>ログインしますか？</button>
        <button @click="goSignup" class='btn-tr-white-base-sq'>ユーザー登録しますか？</button>
    </div>
    <div v-if="user" @click="dynamicFunc" class="go-dynamic">
        {{ buttonText }}
    </div>
  </div>
</template>

<script>
import { router } from "@/main.js"

export default {
    props:[
        'dataObjArray',
        'mainText',
        'note',
        'buttonText',
    ],
  data() {
    return {

    };
  },
  computed: {
    user() {
      return this.$store.state.signup.user
    },
  },
  methods: {
    getImage(path) {
      // path = 'vue_front/src'+ path
      return require("@/assets/" + path);
    },
    goQuiz() {
        router.push({name:'QuizHome'})
    },
    dynamicFunc() {
        this.$emit('func')
    },
    goLogin() {
        router.push({name:'Login'})
    },
    goSignup() {
        router.push({name:'Signup'})
    }
  },
};
</script>

<style scoped lang="scss">
@import "style/_variables.scss";
.main-text {
  color: whitesmoke;
  font-size: 1.3rem;
  font-weight: bold;
  margin-top: 2rem;
  margin-bottom: 1.5rem;
  padding: 0 0.2rem;
}
.note {
  color: whitesmoke;
  font-size: 0.8rem;
  padding: 0 0.2rem;
}
.main-quiz-wrapper {
  border: solid $base-lite-2;
  border-radius: 20px;
  padding: 0.2rem;
  margin: 2rem 0;
  .title {
    display: inline-block;
    padding: 1rem;
    margin-top: 1rem;
    color: whitesmoke;
    border-left: 0.5rem solid $base-color;
    border-bottom: solid gray;
  }
  .text {
    margin: 1rem;
    padding: 2rem;
    background: $back-gra-orange;
    border-radius: 20px;
    border: solid $lite-blue;
    font-size: 1.2rem;
    font-weight: bold;
  }
}
.image {
  img {
    object-fit: cover;
  }
}
.go-dynamic {
    border: solid whitesmoke;
    width: auto;
    display: inline-block;
    padding: 0.3rem 1rem;
    font-size: 1.1rem;
    font-weight: bold;
    color: whitesmoke;
    margin: 3rem 0;
    transition: .3s;
}
.go-dynamic:hover {
    background: rgba($color: $back-white, $alpha: 0.1)
}
.signup_login {
    margin: 3rem 0;
    button{
        background: none;
        padding: 0.3rem 0.5rem;
        margin:  1rem;
        font-size: 1rem;
        font-weight: bold;
        width: 200px;

    }
}

@media(max-width: 600px){
  .title {
    font-size: 1.3rem;
  }
}
@media(max-width: 500px){
  .image {
    img {
      height: auto;
      width: 100%;
      object-fit: cover;
    }
  }
}
</style>