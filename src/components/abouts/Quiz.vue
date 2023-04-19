<template>

  <AbstractAbout 
    :mainText='mainText'
    :dataObjArray="dataObjArray"
    :note='note'
    :buttonText='buttonText'
    @func='goQuiz'/>

</template>

<script>
import { router } from "@/main.js"
import AbstractAbout from "@/components/abouts/AbstractAbout.vue";

export default {
  components:{
    AbstractAbout
  },
  data() {
    return {
      note: "※ 一部のサービスはアカウントがないと利用できません。アカウントは無料で作成できます。",
      buttonText:'クイズへ行く >>',
      mainText:
        "『楽しく学ぶ』をコンセプトに作られた日本語学習クイズプラットフォームです。自分のレベルに合った問題をクイズ形式で 解き、実力の確認ができます。",
      dataObjArray: [
        {
          title: "多様な形式やジャンル",
          image: "quiz/question.jpg",
          text: "細かく分類された日本語のカテゴリを超初級から上級までの四つのレベルに分けられています。加えて、複数の答えから正しいものを一つだけ選ぶオーソドックスなクイズや複数選択、並び替え問題も収録されているので多面的にスキルを確認することができます。",
        },
        {
          title: "グラフで得意・不得意の確認",
          image: "quiz/pie_chart.jpg",
          text: "実力を各級に応じた日本語カテゴリを元にグラフ化し確認することができます。得意・不得意が一目瞭然になり、苦手な項目を強化するといった使い方ができます。グラフは実力テストや練習することで変動します。",
        },
        {
          title: "実力テストをスキルを評価",
          image: "quiz/exam.jpg",
          text: "１日１回受けられる日本語試験で現在の実力を試すことができます。超初級から上級までの級測定に加え、そこから10段階評価することで実力を細かく評価します。（レベルや級は実力テストを受けることでのみ変動します。アカウント画面から確認できます。）",
        },
        {
          title: "お気に入りのクイズを保存",
          image: "quiz/good.jpg",
          text: "苦手な問題や後で確認したい問題などを保存することができます。保存した問題だけを練習することができるので重点的に苦手の克服ができます。",
        },
      ],
    };
  },
  methods: {
    goQuiz() {
        router.push({name:'QuizHome'})
    },
  },
};
</script>

<style>

</style>