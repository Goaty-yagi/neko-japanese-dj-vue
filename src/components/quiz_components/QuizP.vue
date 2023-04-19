<template>
  <div
    v-if="!$store.state.isLoading&&questions"
    class="quiz-wrapper"
    :class="{ 'laoding-center': $store.state.isLoading }"
  >
    <div class="main-wrapper">
      <Start
        v-if="startQuiz && questionLength && $store.state.isLoading == false"
        :questionLength="questionLength"
        :forQuizPageInfo="forQuizPageInfo"
        :testOrInit='testOrInit'
        @closeStart="closeStart"
      />
      <div v-if="startQuiz == false">
        <p class="quiz-description title-white">{{ quiz.description }}</p>
        <ProgressBar
        v-if='!showResult&&!testOrInit||!testOrInit'
        :divisor="questionLengthCounter"
        :numToBeDevided="questions.length"
        :showProgressBar="result"
        ref='progressBarRef'/>

        <div v-if="showResult == false" class="quiz-countainer">
          <div
            class="question-loop"
            v-for="(question, questionindex) in questions.slice(
              pagination.a,
              pagination.b
            )"
            v-bind:key="questionindex"
          >
            <QuestionText
            :counter='questionNumToBeShown'
            :questionLabel='question.label'
            :questionText='question.text'
            />
            <Image
            v-if="question.image"
            :imageUrl='question.get_image'
            />
            <Answers
            :question='question'
            :result='result'
            :selectedIndexNum='selectedIndexNum'
            :selectedOrderAnswer='selectedOrderAnswer'
            :resultHandleDict='resultHandleDict'
            :maxSelectReach='maxSelectReach'
            :selectedAnswer='selectedAnswer'
            @onClick='onClick'
            @type3And5CheckResult='type3And5CheckResult'

            />
            <Footer
            :user='user'
            :result='result'
            :myQuiz='myQuiz'
            :questionLengthCounter='questionLengthCounter'
            :question='question'
            :questions='questions'
            :showNextOrFinishButton='showNextOrFinishButton'
            :testOrInit='testOrInit'
            @finish='finish'
            @nextQuestion='nextQuestion'
            @resultBack="resultBack"
            @resultNext="resultNext"
            @handleShowResult="handleShowResult"
            />
          </div>
        </div>
        <Result
          v-if="showResult"
          :SelectedAnswerInfo="SelectedAnswerInfo"
          :question_length="questions.length"
          @handlePagination="handlePagination"
          @handleShowResult="handleShowResult"
          @resultAnswerHandler="resultAnswerHandler"
          @handleResult="handleResult"
          @playAgain="playAgain"
          @backQuizHome="backQuizHome"
        />
      </div>
    </div>
  </div>
</template>

<script>
// currentry questiontype is these 3
// questionType:[
//         '選択','並び替え','多答'
//       ],
import axios from "axios";
import Result from "@/components/quiz_components/Result.vue";
import Start from "@/components/quiz_components/Start.vue";
import ProgressBar from '@/components/quiz_components/small_parts/ProgressBar.vue'
import QuestionText from '@/components/quiz_components/small_parts/QuestionText.vue'
import Image from '@/components/quiz_components/small_parts/Image.vue'
import Answers from '@/components/quiz_components/small_parts/Answers.vue'
import Footer from '@/components/quiz_components/small_parts/footers/Footer.vue'
import TestResult from '@/components/initial/TestResult.vue'

export default {
  components: {
    Result,
    Start,
    ProgressBar,
    QuestionText,
    Image,
    Footer,
    Answers
  },
  props: [
    "forQuizPageInfo",
    "quizType",
    "dispatchFunctionName",
    
    ],
  data() {
    return {
      quizTypeList:['practice', 'myQuiz', 'init', 'test'], // currentry not in use.
      currentQuizType:this.quizType,
      questionLengthCounter: 1,
      questionCounterForTest:1,
      questionLength: "",
      SelectedAnswerInfo: {},
      selectedAnswer: {},
      answerIDAndOrder: {},
      showResult: false,
      // finishTest:false,
      showNextOrFinishButton: false,
      result: false,
      startQuiz: false,
      pagination: {
        a: 0,
        b: 1,
      },
      resultHandleDict: {
        isCorrect: false,
        IsNotCorrect: false,
        answerIDType3: "",
        questionType4: false,
        answerAllTrueType4: false,
        answerIDType4: "",
        answerIDType5: "",
      },
      countupDict: {
        answerID: "",
        questionID: "",
        questionType: "",
      },
      userStatusDict: {
        status: "",
        isCorrect: 0,
        isFalse: 0,
      },
      maxSelectReach: false,
      selectedIndexNum: null,
      showSelectNum: true,
      selectedOrderAnswer: {},
      selectAnswerCounter: 0,
      NumOfIscorrect: 0,
      buttonDisabled: false,
    };
  },
  async created() {
    if(this.quizType === 'myQuiz'||this.quizType === 'init') {
      this.startQuiz = false
    } else {
      this.startQuiz = true;
    }
  },
  mounted() {
    console.log('MOUNTP',this.forQuizPageInfo)
    this.userStatusDict.status = this
    this.questionLength = this.questions.length;
    this.SelectedAnswerInfo = {};
  },
  beforeUnmount() {
    this.attributeReset()
  },
  watch: {
    questions: function (v) {
      if (this.questions) {
        this.questionLength = this.questions.length;
      }
    },
  },
  computed: {
    questions() {
      return this.$store.getters.questions;
    },
    quiz() {
      return this.$store.getters.quiz;
    },
    myQuiz() {
      return this.$store.getters.myQuiz;
    },
    user() {
      return this.$store.getters.user;
    },
    testOrInit() {
      if(this.quizType==='init'||this.quizType==='test') {
        return true
      } else {
        return false
      }
    },
    questionNumToBeShown() {
      if(this.testOrInit) {
        return this.questionCounterForTest
      } else {
        return this.questionLengthCounter
      }
    }
  },
  methods: {
    // ...mapActions(['getquestions','getMyQuiz']),
    nextQuestion(questionType, questionID, questionStatus) {
      // if(this.quizType==='test') {
      //   console.log("from QUizP")
      //   this.$emit('nextQuestionFunForTest')
      // }
      this.userStatusDict.status = questionStatus
      this.getQuizTaker();
      this.handleCountUpDict(this.selectedAnswer, questionType, questionID);
      this.pagination.a += 1;
      this.pagination.b += 1;
      this.selectedIndexNum = null;
      this.showNextOrFinishButton = false;
      this.selectAnswerHandler(questionType);
      this.NumOfIscorrect = 0;
      this.maxSelectReach = false;
      this.selectedOrderAnswer = {};
      this.selectedAnswer = {};
      this.selectAnswerCounter = 0;
      this.questionLengthCounter += 1;
      this.questionCounterForTest += 1
      this.answerIDAndOrder = {};
       if(this.testOrInit) {
        console.log("from QUizP")
        this.$emit('nextQuestionFunForTest')
      }
      this.scrollTop();
    },
    finish(questionType, questionID, questionStatus) {
      this.userStatusDict.status = questionStatus
      this.handleCountUpDict(this.selectedAnswer, questionType, questionID);
      this.updateQuizTaker();
      // this.resultHandler()
      this.showResult = true;
      this.result = true;
      this.selectedIndexNum = null;
      this.selectAnswerHandler(questionType);
      this.NumOfIscorrect = 0;
      this.maxSelectReach = false;
      this.selectedOrderAnswer = {};
      this.selectedAnswer = {};
      this.selectAnswerCounter = 0;
      this.answerIDAndOrder = {};
      this.resultAnswerHandler();
      this.scrollTop();
    },
    // resultHandler() {
    //   if(this.currentQuizType==='test') {
    //     finishTest = true
    //   } 
    // },
    getQuizTaker() {
      console.log("qto",this.questions.length - this.questionLengthCounter)
      if (this.questions.length - this.questionLengthCounter === 1&&this.user) {
        if (!this.$store.state.quizTakerObj) {
          console.log(this.$store.state.quizTakerObj);
          this.$store.dispatch("getQuizTaker");
        }
      }
    },
    onClick(answerindex, answer, question) {
      // this is for 2 things,
      // first is for controling CSS return selectedIndexNum
      // which used for questionType 選択, and selectedOrderAnswer
      // which used for questionType 並び替え and 多答.
      // second is for selected-answer and is_correct.
      // return selectedAnswer for questionType 選択.
      // for questionType 並び替え, use getAnswerIDAndOrder function.
      // for questionType 多答, use getIDAndIsCorrect function.
      if(!this.testOrInit) {
        this.$refs.progressBarRef.progressBar()
      }
      if (question.question_type.name == '選択') {
        if (this.selectedIndexNum == answerindex) {
          this.selectedIndexNum = null;
          this.selectedAnswer = {};
          this.showNextOrFinishButton = false;
        } else {
          this.selectedIndexNum = answerindex;
          this.selectedAnswer["answerID"] = answer.id;
          this.selectedAnswer["isCorrect"] = answer.is_correct;
          this.handleShowNextOrFinishButton();
        }
      } else if (question.question_type.name == '並び替え') {
        if (
          this.selectedOrderAnswer[answerindex + 1] &&
          this.questions.length >= this.selectAnswerCounter
        ) {
          this.selectedOrderAnswer = this.changeOrder(
            this.selectedOrderAnswer,
            answerindex + 1
          );
          this.getAnswerIDAndOrder(answer.answer_id, this.selectAnswerCounter);
          this.selectAnswerCounter -= 1;
          this.showNextOrFinishButton = false;
        } else {
          this.selectAnswerCounter += 1;
          this.selectedOrderAnswer[answerindex + 1] = this.selectAnswerCounter;
          this.getAnswerIDAndOrder(answer.answer_id, this.selectAnswerCounter);
          if (
            Object.keys(this.selectedOrderAnswer).length ==
            question.answer.length
          ) {
            this.handleShowNextOrFinishButton();
          }
        }
      } else if (question.question_type.name == '多答') {
        this.getNumOfIscorrect(question.answer);
        if (this.selectedOrderAnswer[answerindex + 1]) {
          this.selectedOrderAnswer = this.changeOrder(
            this.selectedOrderAnswer,
            answerindex + 1
          );
          this.getIDAndIsCorrect(answer.id, answer.is_correct);
          this.selectAnswerCounter -= 1;
          if (question.max_select) {
            if (
              Object.keys(this.selectedOrderAnswer).length < question.max_select
            ) {
              this.showNextOrFinishButton = false;
              this.maxSelectReach = false;
            }
          } else if (Object.keys(this.selectedOrderAnswer).length == 0) {
            this.showNextOrFinishButton = false;
          }
        } else {
          this.selectAnswerCounter += 1;
          this.selectedOrderAnswer[answerindex + 1] = this.selectAnswerCounter;
          this.getIDAndIsCorrect(answer.id, answer.is_correct);
          if (question.max_select) {
            if (
              Object.keys(this.selectedOrderAnswer).length ==
              question.max_select
            ) {
              this.handleShowNextOrFinishButton();
              this.maxSelectReach = true;
            }
          } else {
            this.handleShowNextOrFinishButton();
          }
        }
      }
    },
    changeOrder(dict, index) {
      // if deleted, the num or nums before the deleted items order num
      // change
      let orderNum = dict[index];
      delete dict[index];
      if (dict) {
        let changeDict = {};
        Object.keys(dict).forEach((key) => {
          if (dict[key] > orderNum) {
            dict[key] -= 1;
          }
        });
      }
      return dict;
    },
    selectAnswerHandler(questionType) {
      // this is get informations about selected-answer for result component
      // return SelectedAnswerInfo
      if (questionType.name == '選択') {
        this.SelectedAnswerInfo[this.questionLengthCounter] = {};
        this.SelectedAnswerInfo[this.questionLengthCounter]["questionType"] =
          questionType;
        this.SelectedAnswerInfo[this.questionLengthCounter]["isCorrect"] =
          this.selectedAnswer.isCorrect;
        this.handleUserStatus(this.selectedAnswer.isCorrect);
        this.SelectedAnswerInfo[this.questionLengthCounter]["answerID"] =
          this.selectedAnswer.answerID;
      } else if (questionType.name == '並び替え') {
        this.SelectedAnswerInfo[this.questionLengthCounter] = {};
        this.SelectedAnswerInfo[this.questionLengthCounter]["questionType"] =
          questionType;
        let stringKeys = Object.keys(
          this.answerIDAndOrder[this.questionLengthCounter]
        ).map(function (a) {
          return Number(a);
        });
        if (
          JSON.stringify(stringKeys) ==
          JSON.stringify(
            Object.values(this.answerIDAndOrder[this.questionLengthCounter])
          )
        ) {
          this.SelectedAnswerInfo[this.questionLengthCounter][
            "isCorrect"
          ] = true;
          this.handleUserStatus(true);
        } else {
          this.SelectedAnswerInfo[this.questionLengthCounter][
            "isCorrect"
          ] = false;
          this.handleUserStatus(false);
        }
        this.makeOrderBoolean();
        this.SelectedAnswerInfo[this.questionLengthCounter]["orderAnswer"] =
          this.answerIDAndOrder;
      } else if (questionType.name == '多答') {
        this.SelectedAnswerInfo[this.questionLengthCounter] = {};
        this.SelectedAnswerInfo[this.questionLengthCounter]["questionType"] =
          questionType;
        let isCorrectCounter = 0;
        var type5IsCorrect = true;
        Object.values(this.selectedAnswer).forEach((value) => {
          if (value == false) {
            this.SelectedAnswerInfo[this.questionLengthCounter][
              "isCorrect"
            ] = false;
            this.handleUserStatus(false);
            type5IsCorrect = false;
          } else {
            isCorrectCounter += 1;
          }
        });
        if (this.NumOfIscorrect == isCorrectCounter && type5IsCorrect) {
          this.SelectedAnswerInfo[this.questionLengthCounter][
            "isCorrect"
          ] = true;
          this.handleUserStatus(true);
        } else if (type5IsCorrect == false && isCorrectCounter > 0) {
          this.SelectedAnswerInfo[this.questionLengthCounter]["isCorrect"] =
            null;
          this.handleUserStatus(false);
        }
        this.SelectedAnswerInfo[this.questionLengthCounter]["selectedAnswer"] =
          this.selectedAnswer;
      }
    },
    getAnswerIDAndOrder(answerID, orderNum) {
      // this is for collecting answer from questionType 4
      if (this.questionLengthCounter in this.answerIDAndOrder) {
        if (orderNum in this.answerIDAndOrder[this.questionLengthCounter]) {
          this.answerIDAndOrder[this.questionLengthCounter] = this.changeOrder(
            this.answerIDAndOrder[this.questionLengthCounter],
            orderNum
          );
        } else {
          this.answerIDAndOrder[this.questionLengthCounter][orderNum] =
            answerID;
        }
      } else {
        this.answerIDAndOrder[this.questionLengthCounter] = {};
        this.answerIDAndOrder[this.questionLengthCounter][orderNum] = answerID;
      }
    },
    makeOrderBoolean() {
      // this is for AnswerIDAndOrder{1:1} to be {1:true}
      let newDict = {};
      let IntegerKeys = Object.keys(
        this.answerIDAndOrder[this.questionLengthCounter]
      ).map(function (a) {
        return Number(a);
      });
      for (let i = 0; i < IntegerKeys.length; i++) {
        if (
          IntegerKeys[i] ==
          Object.values(this.answerIDAndOrder[this.questionLengthCounter])[i]
        ) {
          newDict[i + 1] = true;
        } else {
          newDict[i + 1] = false;
        }
      }
      this.answerIDAndOrder = newDict;
    },
    getIDAndIsCorrect(id, isCorrect) {
      // this is for questionType 5
      if (id in this.selectedAnswer) {
        delete this.selectedAnswer[id];
      } else {
        this.selectedAnswer[id] = isCorrect;
      }
    },
    getNumOfIscorrect(answers) {
      // this is for questionType 5
      if (this.NumOfIscorrect == false) {
        Object.values(answers).forEach((value) => {
          if (value.is_correct) {
            this.NumOfIscorrect += 1;
          }
        });
      }
    },
    handleShowNextOrFinishButton() {
      this.showNextOrFinishButton = true;
    },
    resultAnswerHandler() {
      if (this.result) {
        this.resultHandleDict.isCorrect = false;
        this.resultHandleDict.isNotCorrect = false;
        this.resultHandleDict.answerAllTrueType4 = false;
        this.resultHandleDict.questionType4 = false;
        this.resultHandleDict.answerIDType3 = "";
        this.resultHandleDict.answerIDType4 = "";
        this.resultHandleDict.answerIDType5 = "";
        Object.keys(this.SelectedAnswerInfo).forEach((key) => {
          if (key == this.questionLengthCounter) {
            if (this.SelectedAnswerInfo[key].isCorrect) {
              if (this.SelectedAnswerInfo[key].questionType.name == '並び替え') {
                this.resultHandleDict.answerAllTrueType4 = true;
              } else if (this.SelectedAnswerInfo[key].questionType.name == '多答') {
                this.resultHandleDict.answerIDType5 =
                  this.SelectedAnswerInfo[key].selectedAnswer;
              }
              this.resultHandleDict.isCorrect = true;
            } else if (
              this.SelectedAnswerInfo[key].isCorrect == false &&
              this.SelectedAnswerInfo[key].questionType.name == '選択'
            ) {
              this.resultHandleDict.isCorrect = true;
              this.resultHandleDict.isNotCorrect = true;
              this.resultHandleDict.answerIDType3 =
                this.SelectedAnswerInfo[key].answerID;
            } else if (this.SelectedAnswerInfo[key].questionType.name == '多答') {
              this.resultHandleDict.isCorrect = true;
              this.resultHandleDict.isNotCorrect = true;
              this.resultHandleDict.answerIDType5 =
                this.SelectedAnswerInfo[key].selectedAnswer;
            } else if (
              this.SelectedAnswerInfo[key].isCorrect == false &&
              this.SelectedAnswerInfo[key].questionType.name == '並び替え'
            ) {
              this.resultHandleDict.questionType4 = true;
              this.resultHandleDict.isCorrect = true;
              this.resultHandleDict.isNotCorrect = true;
              this.resultHandleDict.answerIDType4 =
                this.SelectedAnswerInfo[key].orderAnswer;
            }
          }
        });
      }
    },
    type3And5CheckResult(selectedAnswer5, selectedAnswer3, answerID) {
      if (this.result) {
        if (
          this.SelectedAnswerInfo[this.questionLengthCounter].questionType.name == '多答'
        ) {
          if (answerID in selectedAnswer5) {
            return true;
          } else {
            return false;
          }
        } else if (
          this.SelectedAnswerInfo[this.questionLengthCounter].questionType.name == '選択'
        ) {
          if (answerID == selectedAnswer3) {
            return true;
          } else {
            return false;
          }
        }
      }
    },
    handleCountUpDict(selectedAnswer, questionType, questionID) {
      this.countupDict.questionType = questionType;
      this.countupDict.questionID = questionID;
      if (questionType.name === '多答') {
        this.countupDict.answerID = Object.keys(selectedAnswer);
      } else if (questionType.name === '選択') {
        Object.keys(selectedAnswer).forEach((key) => {
          if ((key = "answerID")) {
            this.countupDict.answerID = selectedAnswer[key];
          }
        });
      }
      this.$store.dispatch("countUpAnswerAndQuestion", this.countupDict);
    },
    handlePagination(a, b) {
      // this is for result component
      this.pagination.a = a;
      this.pagination.b = b;
      this.questionLengthCounter = b;
    },
    handleShowResult() {
      console.log("RESU")
      this.showResult = !this.showResult;
    },
    handleResult() {
      this.result = !this.result;
    },
    handleUserStatus(selectedAnswer) {
      console.log("UUSS",selectedAnswer)
      // this is for only is_true and is_false
      this.userStatusDict.isCorrect = 0;
      this.userStatusDict.isFalse = 0;
      if (selectedAnswer) {
        this.userStatusDict.isCorrect = 1;
      } else {
        this.userStatusDict.isFalse = 1;
      }
      if(this.user) {
        this.$store.dispatch("userStatusPost", this.userStatusDict);
      }
    },
    getQuestionStatus(lavel, status) {
      this.userStatusDict.status = status;
      return lavel;
    },
    async updateQuizTaker() {
      const quizTakerid = this.$store.getters.quizTakerObject.id;
      await axios
        .patch(`api/quiz-taker-practice/?quiz_taker=${quizTakerid}`)
        .then((res) => {
          console.log("QTU", res.data, res);
          this.$store.commit("setQuizTakerObj", res.data);
        })
        .catch((e) => {
          let logger = {
            message:
              "in components/quiz_components/QuizP/updateQuizTaker. couldn't update QuizTaker",
            path: window.location.pathname,
            actualErrorName: e.name,
            actualErrorMessage: e.message,
          };
          this.$store.commit("setLogger", logger);
          this.$store.commit("setIsLoading", false);
          router.push({ name: "ConnectionError" });
        });
    },
    resultNext() {
      console.log("result-next")
      this.pagination.a += 1;
      this.pagination.b += 1;
      this.questionLengthCounter += 1;
      this.resultAnswerHandler();
      this.scrollTop();
    },
    resultBack() {
      console.log("result-back")
      this.pagination.a -= 1;
      this.pagination.b -= 1;
      this.questionLengthCounter -= 1;
      this.resultAnswerHandler();
      this.scrollTop();
    },
    scrollTop() {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    },
    closeStart() {
      this.startQuiz = false;
      this.$emit('startFunction') 
    },
    playAgain() {
      console.log("playagain",this.dispatchFunctionName )
      if(this.quizType === 'myQuiz') {
          this.$store.commit('questionsShuffle')
           this.startQuiz = false
      } else {
         this.startQuiz = true
      }
      this.attributeReset();
      if(this.dispatchFunctionName) {
        console.log("dipatch",this.dispatchFunctionName)
        this.$store.dispatch(this.dispatchFunctionName);
      }
    },
    attributeReset() {
      this.result = false;
      this.showResult = false;
      this.pagination.a = 0;
      this.pagination.b = 1;
      this.selectedIndexNum = null;
      this.showNextOrFinishButton = false;
      this.SelectedAnswerInfo = {};
      this.NumOfIscorrect = 0;
      this.maxSelectReach = false;
      this.selectedOrderAnswer = {};
      this.selectedAnswer = {};
      this.selectAnswerCounter = 0;
      this.questionLengthCounter = 1;
      this.questionCounterForTest= 1;
      (this.resultHandleDict.isCorrect = false),
        (this.resultHandleDict.IsNotCorrect = false),
        (this.resultHandleDict.answerIDType3 = ""),
        (this.resultHandleDict.questionType4 = false),
        (this.resultHandleDict.answerAllTrueType4 = false),
        (this.resultHandleDict.answerIDType4 = ""),
        (this.resultHandleDict.answerIDType5 = "");
      this.answerIDAndOrder = {};
    },
    backQuizHome() {
      // this.$emit("backQuizHome");
      this.attributeReset();
    },
    testAnswerFunction() {
      this.pagination.a = 0
      this.pagination.b = 1
      this.SelectedAnswerInfo = {}
      this.questionLengthCounter = 1
    }
  },
};
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.quiz-wrapper {
  width: 100%;
  min-height: 80vh;
  padding-bottom: 1rem;
  display: flex;
  justify-content: center;
  .quiz-countainer {
    width: 100%;
    display: flex;
    justify-content: center;
    .question-loop {
      width: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
  }
}
</style>