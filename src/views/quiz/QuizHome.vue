<template>
  <div class="quiz-home-wrapper">
    <div class="main-wrapper">
      <QuizP
        v-if="componentHandleDict.quiz"
        :forQuizPageInfo="forQuizPageInfo"
        dispatchFunctionName='getQuestions'
        quizType='practice'
        @backQuizHome="backQuizHome"
      />
      <div v-if="!componentHandleDict.quiz && !$store.state.isLoading">
        <div v-if="componentHandleDict.quiz == false" class="title-white">
          クイズ
        </div>
        <div
          v-if="this.componentHandleDict.quizStart == false"
          class="quiz-home-container"
        >
          <div class="select-container">
            <div
              class="select-loop"
              v-for="(select, key, selectindex) in quizSelectDict"
              v-bind:key="selectindex"
            >
              <div
                class="unlock-false"
                :class="{ unlock: lockHandler(select.grade) }"
              >
                <div
                  v-if="lockHandler(select.grade)"
                  :class="{ 'lock-container': lockHandler(select.grade) }"
                >
                  <i class="fas fa-lock"></i>
                  <div>LOCKED</div>
                </div>
              </div>
              <div
                @click="
                  (e) =>
                    lockHandler(select.grade) == false &&
                    showGrade(select.grade, key)
                "
                class="loop-wrapper"
              >
                <div
                  class="english-title"
                  :class="{ 'lock-english-title': lockHandler(select.grade) }"
                >
                  {{ key }}
                </div>
                <div v-if="selectindex == 0" class="font">
                  <i class="fas fa-dice-one"></i>
                </div>
                <div v-if="selectindex == 1" class="font">
                  <i class="fas fa-dice-two"></i>
                </div>
                <div v-if="selectindex == 2" class="font">
                  <i class="fas fa-dice-three"></i>
                </div>
                <div v-if="selectindex == 3" class="font">
                  <i class="fas fa-dice-four"></i>
                </div>
                <div v-if="selectindex == 4" class="font">
                  <i class="fas fa-dice-five"></i>
                </div>
                <div class="grade">{{ select.grade }}</div>
                <div class="description">{{ select.description }}</div>
              </div>
            </div>
          </div>
          <div v-if="showEachGrade" class="l-wrapper">
            <div class="l-container">
              <div class="close-container">
                <div @click="closeGrade()" class="close">
                  <i class="fas fa-times"></i>
                </div>
              </div>
              <div>
                <img class="is-image" src="@/assets/logo.png" />
              </div>
              <div class="animation-in-quiz-home">
                <div class="title-blue">{{ gradeTitle }}</div>
                <div
                  class="category-outer-loop"
                  v-for="(selects, key, selectsindex) in quizCategories"
                  v-bind:key="selectsindex"
                >
                  <div v-if="key == receivedKey">
                    <div
                      class="category-inner-loop"
                      v-for="(titles, titlesindex) in selects"
                      v-bind:key="titlesindex"
                    >
                      <!-- @click="e => result==false && onClick(answerindex,answer,question)" -->
                      <div
                        class="category-container"
                        v-for="(options, title, titleindex) in titles"
                        v-bind:key="titleindex"
                      >
                        <!-- <div @click="e => options &&options != 'all' && showOptions(titleindex,title)" class="category-title-container" :class="{'animation-move':this.optionDict.showOption}"> -->
                        <div class="category-title-container"
                          @click="
                                (e) => options == 'all' && getAllCategoryQuiz()
                            ">
                          <FormSelect
                            v-if="options !== 'all'"
                            :choicesArray="options !== 'all'?options:''"
                            :clickTypeConfig="clickTypeConfig"
                            optionAlign="center-on-left"
                            :bulletObj="titleindex === 2 ? bulletObj : {}"
                          >
                          </FormSelect>
                          <div
                            class="for-all"
                          >
                            <div class="category-title">
                              {{ title }}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <NotVerified
        v-if="!getEmailVerified && $store.state.isLoading == false"
        :currentPageName="currentPageName"
      />
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import NotVerified from "@/components/login/NotVerified.vue";
import QuizP from "@/components/quiz_components/QuizP.vue";
import FormSelect from "@/components/parts/FormSelect.vue";

export default {
  components: {
    QuizP,
    NotVerified,
    FormSelect,
  },
  data() {
    return {
      clickTypeConfig: {
        showArrow: true,
        arrowPlace:'right',
        arrowColor:'white',
        showChosenItem: false,
        clickMovePage:true,
        function: this.goStart,
      },
      bulletObj: {
        type: "array",
        isFont: true, //default is false
        bullet: ":",
        array: [
          "fas fa-apple-alt",
          "fas fa-carrot",
          "fas fa-cat",
          "fas fa-car-side",
          "fas fa-utensils",
          "fas fa-mug-hot",
        ],
      },
      quizSelectDict: {
        beginner: {
          grade: "超初級",
          description: "ひらがなやカタカナなど簡単なボキャブラリー",
        },
        basic1: {
          grade: "初級１",
          description: "簡単な文法や一般的な語彙などN５相当",
        },
        basic2: {
          grade: "初級２",
          description: "少し複雑な文法や状況に応じた表現などN４相当",
        },
        intermediate: {
          grade: "中級",
          description: "日常的な場面で使われる表現などN３相当",
        },
        Advanced: {
          grade: "上級",
          description: "難しいです",
        },
      },
      quizCategories: {
        beginner: {
          title: {
            ひらがな: ["50音"],
            カタカナ: ["50音"],
            ボキャブラリー: [
              "くだもの",
              "やさい",
              "どうぶつ",
              "のりもの",
              "たべもの",
              "のみもの",
            ],
            すうじ: ["記号"],
            超初級道場: "all",
          },
        },
        basic: {
          title: {
            初級道場: "all",
          },
        },
      },
      optionDict: {
        currentCategory: "",
        showOption: false,
      },
      forQuizPageInfo: {
        grade: "",
        field: "",
        option: "",
        description: [
          "・クイズはランダムに作成されるので毎回問題が異なります。",
        ],
        all: false,
      },
      // quizStart manage after start
      componentHandleDict: {
        quiz: false,
        quizStart: false,
      },
      configQuizIdAndFieldId: {
        quizId: "",
        fieldId: [],
        quizNum: "",
      },
      quizNum: {
        general: 10,
        all: 20,
      },
      showEachGrade: false,
      receivedKey: "",
      gradeTitle: "",
      currentPageName: "",
      lockedOptions: {
        unlock: true,
        future_content: false,
      },
      selectedItem: "",
      top:0
    };
  },
  computed: mapGetters([
    "quizNameId",
    "fieldNameId",
    "getEmailVerified",
    "fixedScroll",
  ]),

  created() {
    this.getQuizNameId();
    this.getFieldNameId();
  },
  mounted() {
    console.log("MOUN", this.fieldNameId);
    // this.scrollFixedForUnmailverified()
    this.scrollTop();
    this.getCurrentPageName();
    this.optionDict.currentCategory = "";
  },
  beforeUnmount() {
    document.body.style.position = ''
    window.scrollTo(0, this.top)
  },
  methods: {
    ...mapActions(["getQuizNameId", "getFieldNameId"]),
    showGrade(grade, key) {
      this.top = window.scrollY
      document.body.style.top = `-${window.scrollY}px`;
      document.body.style.position = 'fixed'
      this.showEachGrade = true;
      this.gradeTitle = grade;
      this.receivedKey = key;
      this.getQuizPageInfo((grade = grade));
    },
    closeGrade() {
      document.body.style.position = ''
      window.scrollTo(0, this.top)
      this.showEachGrade = false;
      this.optionDict.currentCategory = "";
      this.optionDict.showOption = false;
    },
    closeoption() {
      this.optionDict.showOption = false;
      this.optionDict.currentCategory = "";
    },
    showOptions(index, field) {
      if (this.optionDict.currentCategory == index) {
        this.optionDict.showOption = !this.optionDict.showOption;
        this.optionDict.currentCategory = "";
      } else {
        this.optionDict.currentCategory = index;
        this.optionDict.showOption = true;
        this.forQuizPageInfo.field = field;
      }
    },
    allReset() {
      this.optionDict.showOption = false;
      this.showEachGrade = false;
      this.optionDict.currentCategory = "";
      this.configQuizIdAndFieldId.quizId = "";
      this.configQuizIdAndFieldId.fieldId = [];
    },
    async goStart(option) {
      // specific field questions must be more than quizNum
      console.log("GO_ATART", option)
      await this.$store.dispatch("getQuizTaker");
      this.getQuizPageInfo(0, option);
      this.getQuizId();
      this.getFieldIds();
      this.getQuizInfo();
      await this.$store.dispatch("getQuestions");
      this.forQuizPageInfo.all = false;
      this.componentHandleDict.quiz = true;
      this.componentHandleDict.quizStart = true;
      this.allReset();
    },
    backQuizHome() {
      this.componentHandleDict.quizStart = false;
      this.componentHandleDict.quiz = false;
      this.scrollTop();
      this.allReset();
    },
    getQuizPageInfo(grade = "", option = "") {
      if (grade) {
        this.forQuizPageInfo.grade = grade;
      } else if (option) {
        this.forQuizPageInfo.option = option;
      }
    },
    getQuizId() {
      // this is for matching quiz name to quiz id.
      // quiz name set in front must be the same as a quiz name in DB
      for (let i of this.quizNameId) {
        if (i.name == this.forQuizPageInfo.grade) {
          this.configQuizIdAndFieldId.quizId = i.id;
          break;
        }
      }
    },
    getFieldIds() {
      // this is for matching field name to field id.
      // field name set in front must be the same as a field name in DB
      for (let i of this.fieldNameId) {
        console.log('option',this.forQuizPageInfo.option)
        if (i.name == this.forQuizPageInfo.option) {
          this.configQuizIdAndFieldId.fieldId.push(i.id);
          break;
        }
      }
    },
    getQuizInfo() {
      this.configQuizIdAndFieldId.quizNum = this.quizNum.general;
      this.$store.commit("getQuizInfo", this.configQuizIdAndFieldId);
    },
    async getAllCategoryQuiz(title) {
      for (let i of this.quizNameId) {
        if (i.name == this.forQuizPageInfo.grade) {
          this.configQuizIdAndFieldId.quizId = i.id;
          break;
        }
      }
      this.configQuizIdAndFieldId.quizNum = this.quizNum.all;
      this.$store.commit("getQuizInfo", this.configQuizIdAndFieldId);
       await this.$store.dispatch("getQuizTaker");
      await this.$store.dispatch("getQuestions");
      this.forQuizPageInfo.all = true;
      this.componentHandleDict.quiz = true;
      this.componentHandleDict.quizStart = true;
      this.allReset();
    },
    getCurrentPageName() {
      let i = this.$route.path;
      i = i.split("/");
      this.currentPageName = i[1];
    },
    scrollTop() {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    },
    lockHandler(val) {
      if (val == "超初級") {
        return false;
      } else {
        return true;
      }
    },
    scrollFixedForUnmailverified() {
      if (!this.getEmailVerified && this.$store.state.isLoading == false) {
        this.$store.commit("fixedScrollTrue");
        this.$store.commit("showModalTrue");
      }
    },
    getSelectedItem(item) {
      this.forQuizPageInfo.option = item;
    },
  },
};
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.quiz-home-wrapper {
  display: flex;
  justify-content: center;
  min-height: 80vh;
  width: 100vw;
  .quiz-home-container {
    display: flex;
    flex-direction: column;
    .select-container {
      width: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      .select-loop {
        width: 90%;
        display: flex;
        justify-content: center;
        position: relative;
        padding: 0.7rem;
        max-height: 110px;
        .unlock {
          position: absolute;
          background: rgba(0, 0, 0, 0.7);
          width: 97%;
          height: 80px;
          display: flex;
          align-items: center;
          .lock-container {
            position: absolute;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
            opacity: 0.8;
            color: rgb(182, 76, 196);
            i {
              font-size: 2.5rem;
            }
            div {
              font-size: 0.7rem;
            }
          }
        }
        .loop-wrapper:hover {
          background: $back-lite-white;
        }
        .loop-wrapper {
          display: flex;
          align-items: center;
          width: 100%;
          border: solid $base-color;
          border-radius: 0.5rem;
          margin-top: 0.5rem;
          margin-bottom: 0.5rem;
          background: $back-white;
          padding: 1rem;
          transition: 0.5s;
          .english-title {
            position: absolute;
            right: 0;
            top: 0;
            margin-right: 0.9rem;
            padding-right: 0.5rem;
            padding-left: 0.5rem;
            color: $back-white;
            font-weight: bold;
            border: solid $dark-blue;
            border-radius: 50vh;
            background: rgba(252, 75, 175, 0.961);
          }
          .lock-english-title {
            background: $dark-blue;
            color: $lite-blue;
          }
          .font {
            font-size: 1.5rem;
            flex-basis: 10%;
          }
          .grade {
            flex-basis: 30%;
            font-size: 1.5rem;
            font-weight: bold;
          }
          .description {
            flex-basis: 60%;
            font-size: 0.9rem;
          }
        }
      }
    }
    .l-wrapper {
      .l-container {
        display: flex;
        flex-direction: column;
        // justify-content: center;
        // nim-height: 75%;
        min-height: 60%;
        padding-bottom: 2rem;
        .close-grade {
          // width: inherit;
          // left:auto;
          display: flex;
          justify-content: flex-end;
          .close {
            position: fixed;
            display: flex;
            justify-content: center;
            align-items: center;
            border: 0.2rem solid rgb(180, 179, 179);
            border-radius: 50vh;
            width: 1.5rem;
            height: 1.5rem;
            margin-top: 0.2rem;
            margin-right: 0.2rem;
            color: rgb(172, 172, 172);
          }
        }
        .is-image {
          width: 8rem;
          height: auto;
        }
        .animation-in-quiz-home {
          position: relative;
          .space-off {
            height: 0px;
          }
          // .animations-apace{
          //     height: 30px;
          // }

          .category-outer-loop {
            width: 100%;
            .category-inner-loop {
              // position: relative;
              width: 100%;
              display: flex;
              align-items: center;
              flex-direction: column;
              .category-container {
                position: relative;
                display: flex;
                justify-content: center;
                width: 100%;
                // transition: 1s;
                .animation-move {
                  position: absolute;
                }
                .category-title-container:hover {
                  background: $lite-blue;
                }
                .category-title-container {
                  height: 100%;
                  width: 100%;
                  display: flex;
                  position: relative;
                  flex-direction: column;
                  justify-content: center;
                  align-items: center;
                  width: 80%;
                  border: solid $base-color;
                  border-radius: 0.5rem;
                  margin-top: 0.5rem;
                  margin-bottom: 0.5rem;
                  min-height: 3rem;
                  background: $background-bottom-right;
                  // transition: .3s;
                  .category-title {
                    color: white;
                    font-weight: bold;
                    transition: 0.5s;
                    .fa-caret-down {
                      position: absolute;
                      right: 0;
                      margin-top: 0.3rem;
                      margin-right: 1rem;
                      transition: 0.5s;
                    }
                    .lotate {
                      transform: rotate(180deg);
                    }
                  }
                }
                .option-container {
                  position: absolute;
                  width: 80%;
                  border: solid grey;
                  border-top: 0.3rem solid grey;
                  border-bottom: 0.3rem solid grey;
                  top: 2rem;
                  margin-top: 0.1rem;
                  margin-bottom: 0.5rem;
                  // padding-top: 1rem;
                  min-height: 5rem;
                  background: $back-tr-white;
                  transition: 0.5s;
                  z-index: 1;
                  .close-container {
                    height: 1.7rem;
                    .close {
                      font-size: 0.8rem;
                      width: 1rem;
                      height: 1rem;
                      margin-top: 0.3rem;
                      margin-right: 0.3rem;
                      border: solid;
                    }
                  }
                  .option-loop {
                    width: 100%;
                    .each-option:hover {
                      background: $lite-gray;
                    }
                    .each-option {
                      display: flex;
                      position: relative;
                      justify-content: center;
                      margin-bottom: 0.5rem;
                      padding: 0.5rem;
                      transition: 0.5s;
                      .option-font {
                        position: absolute;
                        // flex-basis: 35%;
                        display: flex;
                        margin-right: 6rem;
                        justify-content: flex-end;
                        .fa-apple-alt {
                          color: $dull-red;
                        }
                        .fa-carrot {
                          color: rgb(255, 188, 63);
                        }
                        .fa-cat {
                          color: brown;
                        }
                        .fa-car-side {
                          color: rgb(68, 70, 220);
                        }
                        .fa-utensils {
                          color: gray;
                        }
                        .fa-mug-hot {
                          color: rgb(223, 221, 221);
                        }
                      }
                      .option-title {
                        // flex-basis: 65%;
                        display: flex;
                        // margin-left: 1rem;
                        p {
                          color: $dark-blue;
                          font-weight: bold;
                          width: 100%;
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
.for-all {
  width: 100%;
}
</style>