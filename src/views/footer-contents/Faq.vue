<template>
  <div class="fqa-wrapper">
    <div class="main-wrapper">
      <div class="title-white">
        <p>FAQ</p>
      </div>
      <div class="content-wrapper">
        <img
          @click="innerContainerCalculation"
          src="@/assets/logo-with-logo.png"
        />
        <p class="faq-title">サービスについてよくある質問</p>
        <div class="question-wrapper">
          <div
            class="question-container-wapper"
            ref="outerContainer"
            v-for="(obj, index) in qAndAObjList"
            v-bind:key="index"
          >
            <div class="question-container" ref="innerContainer">
              <i class="fab fa-quora"></i>
              <p>{{ obj.question }}</p>
              <div class="button-container">
                <i
                  @click="clickedNumHandler(index)"
                  class="fas fa-caret-square-down"
                  :class="{'lotate':clickedNum===index + 1}"
                ></i>
              </div>
            </div>
            <div class="answer-container" ref="answer">
              <div>A</div>
              <p>{{ obj.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      clickedNum: "",
      // type musr be 'quiz','community', 'service' or 'others'
      qAndAObjList: [
        {
          question: "ユーザー登録しないと遊べませんか。",
          answer: "ユーザー登録なしでもコミュニティの閲覧やお試し日本語テストを受けることができます。登録することでコミュニティに参加したり、日本語のスキルを管理したりすることができます。ユーザー登録は無料でできます。",
          type: "service",
        },
        {
          question: "無料で遊べますか。",
          answer: "現在、全てのサービスを無料で利用することができます。",
          type: "service",
        },
        {
          question: "クイズの超初級以上はいつアンロックされますか",
          answer: "現在、アンロックに向けて全力を尽くしていますので少々お待ちください。",
          type: "quiz",
        },
        {
          question:
            "質問の時のタグに適切なものがありません。どうすればいいですか。",
          answer:
            "問い合わせページから要望を出してください。もしかすると追加されるかもしれません。",
          type: "community",
        },
        {
          question:
            "もっと新しい機能が欲しいです。どうすればいいですか。",
          answer:
            "問い合わせページから要望を出してください。",
          type: "others",
        },
        {
          question:
            "仕事の依頼がしたいです。どうすればいいですか。",
          answer:
            "問い合わせページから”仕事のの問合せ”選択してを問い合わせてください。",
          type: "others",
        },
      ],
      outerOriginalHeightArray: [],
    };
  },
  created() {},
  beforeMount() {
      this.$store.commit('setIsLoading', false)
  },
  mounted() {
    this.innerContainerCalculation();
  },
  computed: {
  },
  methods: {
    clickedNumHandler(index) {
      const outerRefs = this.$refs.outerContainer;
      const answerRefs = this.$refs.answer
      const open = () => {
        const addHeightNum = parseInt(outerRefs[index].style.height) + answerRefs[index].offsetHeight + 15 + 'px'
        outerRefs[index].style.height = addHeightNum
        this.clickedNum = index + 1;
      };
      if (this.clickedNum === index + 1) {
        outerRefs[index].style.height = this.outerOriginalHeightArray[index];
        this.clickedNum = ""
      } else if (this.clickedNum) {
        for (let i = 0; i < outerRefs.length; i++) {
          outerRefs[i].style.height = this.outerOriginalHeightArray[i];
        }
        open();
      } else {
        open();
      }
    },
    innerContainerCalculation() {
      const innerRefs = this.$refs.innerContainer;
      const outerRefs = this.$refs.outerContainer;
      console.log("OUTHER_REF",outerRefs[0]);
      for (let i = 0; i < outerRefs.length; i++) {
        console.log("INNER",innerRefs[i].offsetHeight)
        outerRefs[i].style.height = innerRefs[i].offsetHeight > 100?innerRefs[i].offsetHeight+'px':'100px'
        innerRefs[i].style.height = 
          outerRefs[i].offsetHeight + "px";
        this.outerOriginalHeightArray.push(outerRefs[i].style.height);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";

.fqa-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .title-white {
    margin: 1rem 0;
  }
  .content-wrapper {
    width: 100%;
    margin: 1rem 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    img {
      width: 200px;
    }
    .faq-title {
      color: whitesmoke;
      font-size: 1.5rem;
      font-weight: bold;
    }
  }
}
.question-wrapper {
  width: 100%;
  margin-top: 1rem;
  .question-container-wapper {
    position: relative;
    margin-bottom: 0.5rem;
    border: solid $dark-blue;
    border-radius: 5px;
    width: 100%;
    min-height: 100px;
    background: $back-gra-white;
    transition: 0.5s;
    overflow:hidden;
  }
  .question-container {
    padding: 0.5rem 0;
    width: 100%;
    display: flex;
    align-items: center;
    height: 100%;
  }
  .fa-quora {
    flex-basis: 10%;
    font-size: 1.8rem;
    color: $dark-blue;
  }
  p {
    flex-basis: 80%;
    text-align: left;
    color: $dark-blue;
  }
  .button-container {
    display: inline-block;
    flex-basis: 10%;
    .fa-caret-square-down {
      font-size: 1.2rem;
      color: $dull-red;
      // color: rgb(255, 162, 177);
      transition: .3s;
    }
    .fa-caret-square-down:hover {
      color: $lite-dull-red;
    }
  }
}
.answer-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 1rem;
  div{
    font-family: 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    color: $base-dark;
    font-size: 1.5rem;
    margin-right: 0.7rem;
    font-weight: bold;
  }
  p {
    color: $base-dark;
  }
}
.lotate{
    transform:rotate(180deg);
    transition: .3s;
}
</style>