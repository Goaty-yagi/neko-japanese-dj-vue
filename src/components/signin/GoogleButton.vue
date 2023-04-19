<template>
  <div>
    <i v-if="whileGoogleLogin" class="fas fa-spinner fa-pulse"></i>
    <img
      v-if="!whileGoogleLogin"
      class="google"
      @click="googleLogin"
      src="@/assets/google/btn_google.png"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  computed: {
    whileGoogleLogin() {
      return this.$store.getters.getGoogleLogin;
    },
  },
  created() {},
  mounted() {},
  methods: {
    googleLogin() {
      console.log("GOOGLE_LOGIN")
      this.$store.dispatch("googleLogin");
    },
  },
};
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
.google {
  width: auto;
  transition: 0.3s;
}
.google:hover {
  filter: brightness(110%);
}
.fa-pulse {
  margin-top: 2rem;
  font-size: 3rem;
  color: rgb(190, 190, 190);
}
</style>