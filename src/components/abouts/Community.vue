<template>

    <AbstractAbout 
    :mainText='mainText'
    :dataObjArray="dataObjArray"
    :note='note'
    :buttonText='buttonText'
    @func='goCommunity'/>

</template>

<script>
import AbstractAbout from "@/components/abouts/AbstractAbout.vue";
import { router } from "@/main.js"

export default {
  components: {
    AbstractAbout,
  },
  data() {
    return {
      note: "※ 一部のサービスはアカウントがないと利用できません。アカウントは無料で作成できます。",
      buttonText:'コミュニティへ行く >>',
      mainText:
        "世界中の日本語学習者が集い学び合える場をコンセプトに作られたコミュニティ。分からないことは質問し、分かっていることは回答し助け合うことができます。",
      dataObjArray: [
        {
          title: "関心があるカテゴリが自動で表示",
          image: "community/categorize.jpg",
          text: "ユーザーが関心のあるカテゴリを自動で計算し、コミュニティアカウントページに表示されます。簡単に自分に合った質問を探すことができます。",
        },
        {
          title: "質問や回答を管理できる",
          image: "community/manage.jpg",
          text: "質問や回答、ベストアンサーなどコミュニティに関することを簡単に管理することができます。",
        },
        {
          title: "お気に入りの質問を登録できる。",
          image: "quiz/good.jpg",
          text: "後でまた見たい質問をお気に入りに登録することで、いつでも確認できます。",
        },
      ],
    };
  },
  computed: {
    user() {
      return this.$store.state.signup.user;
    },
  },
  methods:{
    goCommunity() {
        router.push({name:'Community'})
    },
  }
};
</script>

<style>
</style>