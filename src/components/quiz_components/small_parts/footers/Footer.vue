<template>
    <div v-if='myQuestionIsReady' class="quiz-footer" :class="{ 'quiz-footer-result': result }">
        <div v-if="showError" class="error-form">
            <i class="fas fa-exclamation-triangle"></i>
            <div>これ以上登録できません</div>
            <div>現在、最大で{{ myQuiz.max_num }}まで登録できます</div>
        </div>
        <div
        v-if="!testOrInit"
        class="register-container"
        :class="{ 'register-container-result': result }"
        >
        <button
            @click="deleteMyQuestion(question)"
            :disabled="showError"
            class="register-border-red"
            v-if="myQuestionIdList.includes(question.id) == false"
        >
            この問題を<br />登録する
        </button>
        <button
            @click="deleteMyQuestion(question)"
            class="register-border-blue"
            v-if="myQuestionIdList.includes(question.id)"
        >
            この問題を<br />登録解除する
        </button>
        </div>
        <div
        v-if="showNextOrFinishButton && result == false"
        class="button-quiz-container"
        >
        <div
            v-if="questionLengthHandler('finish',questionLengthCounter)"
            @click="finishQuiz(question.question_type, question.id,question.status[0])"
            class="btn-tr-white-base-sq"
        >
            FINSH
        </div>
        <div
            v-if="questionLengthHandler('',questionLengthCounter)"
            @click="nextQuestion(question.question_type, question.id, question.status[0])"
            class="btn-tr-white-base-sq"
        >
            NEXT ＞
        </div>
        </div>

        <!-- here for buttun in result -->
        <div v-if="result" class="buttun-in-result">
        <button
            :style="{
            visibility:
                questionLengthCounter != 1 ? 'visible' : 'hidden',
            transition:
                    questionLengthCounter != 1 ? '.3s' : 'none',
            }"
            @click="resultBack()"
            class="btn-tr-white-base-sq back"
        >
            ＜BACK
        </button>
        <div
            @click="handleShowResult()"
            class="btn-base-black-db-ov result"
        >
            結果画面
        </div>
        <button
            :style="{
            visibility:
                questions.length != questionLengthCounter ? 'visible' : 'hidden',
            transition:
                    questions.length != questionLengthCounter ? '.3s' : 'none',
            }"
            @click="resultNext()"
            class="btn-tr-white-base-sq next"
        >
            NEXT＞
        </button>
        </div>
    </div>
</template>

<script>
export default {
    props: [
        'user',
        'result',
        'myQuiz',
        'questionLengthCounter',
        'questions',
        'question',
        'showNextOrFinishButton',
        'testOrInit'
    ],
    data(){
        return {
            myQuestionIdList:[],
            showError: false,
            myQuestionIsReady: false

        }
    },
    async created() {
        if(this.user) {
            await this.$store.dispatch("getMyQuiz", this.user.UID)
            .then(() => {
                 this.getMyQuestionIds(this.myQuestion);
                 this.myQuestionIsReady = true
            })
        }
    },
    mounted() {
    },
    computed:{
        myQuestion() {
            return this.$store.getters.myQuestion;
        },
        // user(){
        //     return this.$store.state.signup.user
        // },
    },
    methods:{
        deleteMyQuestion(question) {
            const payload = {
                question: question.id,
                myQuiz: this.myQuiz.id,
            };
            if (!this.myQuestionIdList.includes(question.id)) {
                if (this.myQuestionIdList.length >= this.myQuiz.max_num) {
                    this.showErrorTrue()
                    setTimeout(this.showErrorFalse, 3000);
                    } else {
                    this.myQuestionIdList.push(question.id);
                    this.$store.commit("addMyQuestion", { question: question });
                    this.$store.dispatch("createAndDeleteMyQuiz", payload);
                    }
            } else {
                console.log("INCLUDE", this.myQuestionIdList);
                this.myQuestionIdList = this.myQuestionIdList.filter(
                (item) => item != question.id
                );
                console.log('before commit',this.myQuestionIdList,question )
                this.$store.commit("deleteMyQuestion", question.id);
                this.$store.dispatch("createAndDeleteMyQuiz", payload);
            }
        },
        getMyQuestionIds(myQuestion) {
            for (let i of myQuestion) {
                this.myQuestionIdList.push(i.question.id);
            }
            console.log("QIDLIST", this.myQuestionIdList);
        },
        showErrorFalse() {
            this.showError = false;
        },
        showErrorTrue() {
            this.showError = true;
        },
        nextQuestion(questionType, questionID, questionStatus) {
            this.$emit('nextQuestion', questionType, questionID, questionStatus)
        },
        finishQuiz(questionType, questionID, questionStatus) {
            this.$emit('finish', questionType, questionID, questionStatus)
        },
        resultBack() {
            console.log("BSCK")
            this.$emit('resultBack')
        },
        resultNext() {
            console.log("next")
            this.$emit('resultNext')
        },
        handleShowResult() {
            console.log("result")
            this.$emit('handleShowResult')
        },
        questionLengthHandler(type,questionLengthCounter) {
            if(type==='finish') {
                if(this.testOrInit) {
                    return false
                } else {
                    if(this.questions.length === questionLengthCounter) {
                        return true
                    } else {
                        return false
                    }
                }

            } else {
                console.log("not_FINISH")
                if(this.testOrInit) {
                    return true
                } else {
                    if(this.questions.length !== questionLengthCounter) {
                        return true
                    }  else {
                        return false
                    }
                }
            }
        }
    }

}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.quiz-footer {
    width: 100%;
    display: flex;
    justify-content: center;
    position: relative;
    margin-bottom: 1rem;
    height: 3rem;
    .error-form {
        animation: notification 3s;
        animation-fill-mode: forwards;
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        padding-bottom: 0.7rem;
        margin: auto;
        width: 80%;
        background: rgba(252, 252, 252, 0.85);
        z-index: 2;
        }
    .register-container {
        position: absolute;
        margin-top: 0.5rem;
        margin-right: 1rem;
        right: 0;
        .register-border-red {
        border: 0.3rem solid $dull-red;
        border-radius: 5px;
        padding: 0.2rem;
        font-size: 0.8rem;
        background: $back-white;
        color: $dark-blue;
        font-weight: bold;
        transition: 0.5s;
        }
        .register-border-red:hover {
        background: white;
        border: 0.3rem solid $lite-dull-red;
        }
        .register-border-blue {
        border: 0.3rem solid $dull-blue;
        border-radius: 5px;
        padding: 0.2rem;
        font-size: 0.8rem;
        background: $back-white;
        color: $dark-blue;
        font-weight: bold;
        transition: 0.5s;
        }
        .register-border-blue:hover {
        background: white;
        border: 0.3rem solid $lite-dull-blue;
        }
    }
    .button-quiz-container {
        display: flex;
        margin-top: 1rem;
        z-index: 1;
        div {
        padding-right: 0.3rem;
        padding-left: 0.3rem;
        }
    }
    .buttun-in-result {
        display: inherit;
        margin-top: 1rem;
        .back {
        display: inline-block;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        padding-top: 0.2rem;
        padding-bottom: 0.2rem;
        }
        .result {
        display: inline-block;
        min-width: 100px;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        padding-top: 0.2rem;
        padding-bottom: 0.2rem;
        margin-right: 0.5rem;
        margin-left: 0.5rem;
        font-weight: bold;
        }
        .next {
        display: inline-block;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        padding-top: 0.2rem;
        padding-bottom: 0.2rem;
        }
    }
}
@media (max-width: 480px) {
  .result {
    flex-basis: 33% !important;
  }
  .register-container-result {
    margin-top: 4rem !important;
  }
}
@media (max-height: 960px) {
  .quiz-footer-result {
    margin-bottom: 5rem !important;
  }
}

</style>