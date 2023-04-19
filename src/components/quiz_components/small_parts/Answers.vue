<template>
<div class="answer-wrapper">
    <button
    class="answer-loop"
    :class="{
        'selected-answer':
        selectedIndexNum == answerindex ||
        answerindex + 1 in selectedOrderAnswer,
        'is-correct-answer':
        (resultHandleDict.isCorrect && answer.is_correct) ||
        resultHandleDict.answerAllTrueType4 ||
        resultHandleDict.answerIDType4[answer.answer_id],
        'isnot-correct-answer':
        (resultHandleDict.isNotCorrect &&
            resultHandleDict.answerIDType3 == answer.id) ||
        resultHandleDict.answerIDType5[answer.id] == false ||
        resultHandleDict.answerIDType4[answer.answer_id] == false,
        'answer-hover': !result && !maxSelectReach,
    }"
    @click="
        (e) =>
        result == false && onClick(answerindex, answer, question)
    "
    :disabled="
        maxSelectReach && answer.id in selectedAnswer == false
    "
    v-for="(answer, answerindex) in question.answer"
    v-bind:key="answerindex"
    >
    <div class="answer-select-bases">
        <div class="answer-select">
        <div class="selecter">
            {{ String.fromCharCode(answerindex + 65) }}
        </div>
        </div>
    </div>
    <div class="answer-label-bases">
        <div class="answer-label">
        {{ answer.label  }}
        </div>
    </div>
    <div class="selected-answer-bases">
        <div
        v-if="
            selectedOrderAnswer[answerindex + 1] &&
            question.question_type.name == '並び替え'
        "
        class="selected-answer-order"
        >
        {{ selectedOrderAnswer[answerindex + 1] }}
        </div>
        <div class="result-answer-order">
        <div class="order" v-if="resultHandleDict.questionType4">
            {{ answer.answer_id }}
        </div>
        <div
            v-if="
            type3And5CheckResult(
                resultHandleDict.answerIDType5,
                resultHandleDict.answerIDType3,
                answer.id
            ) && question.question_type.name != '並び替え'
            "
        >
            <i class="fas fa-check"></i>
        </div>
        </div>
        <i
        v-if="
            selectedOrderAnswer[answerindex + 1] &&
            question.question_type.name == '多答'
        "
        class="fas fa-check"
        ></i>
        <!-- for result -->
        <i
        v-if="
            (resultHandleDict.isCorrect && answer.is_correct) ||
            resultHandleDict.answerAllTrueType4 ||
            resultHandleDict.answerIDType4[answer.answer_id]
        "
        class="far fa-circle"
        ></i>
        <i
        v-if="
            (resultHandleDict.isNotCorrect &&
            resultHandleDict.answerIDType3 == answer.id) ||
            resultHandleDict.answerIDType5[answer.id] == false ||
            resultHandleDict.answerIDType4[answer.answer_id] == false
        "
        class="fas fa-times"
        ></i>
    </div>
    </button>

</div>

</template>

<script>
export default {
    props: [
        'question',
        'result',
        'selectedIndexNum',
        'selectedOrderAnswer',
        'resultHandleDict',
        'maxSelectReach',
        'selectedAnswer'
    ],
    data(){
        return {

        }
    },
    mounted() {
        console.log('answers mounted')
       
    },
    computed:{
        
    },
    methods:{
       type3And5CheckResult(selectedAnswer5, selectedAnswer3, answerID) {
        this.$emit('type3And5CheckResult', selectedAnswer5, selectedAnswer3, answerID)
       },
       onClick(answerindex, answer, question) {
        this.$emit('onClick', answerindex, answer, question)
       }
    }

}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.answer-wrapper {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 1rem;
        .is-correct-answer {
          background: rgb(148, 255, 235);
        }
        .answer-hover:hover {
          border: solid $base-color;
          .answer-select {
            background: $base-lite-2;
          }
        }
        .answer-loop {
          width: 95%;
          height: 3rem;
          border: solid black;
          border-radius: 0.5rem;
          background: white;
          display: flex;
          align-items: center;
          margin-bottom: 0.5rem;
          transition: 0.3s;
          .answer-select-bases {
            flex-basis: 15%;
            .answer-select {
              border: solid black;
              border-radius: 50vh;
              width: 2.5rem;
              height: 2.5rem;
              margin-left: 0.5rem;
              display: flex;
              align-items: center;
              justify-content: center;
              transition: 0.3s;
              .selecter {
                font-weight: bold;
                font-size: 1.5rem;
              }
            }
          }
          .answer-label-bases {
            flex-basis: 70%;
            .answer-label {
            }
          }
          .selected-answer-bases {
            flex-basis: 15%;
            display: flex;
            align-items: center;
            justify-content: center;
            .selected-answer-order {
              font-size: 1.5rem;
              font-weight: bold;
              color: gray;
              flex-basis: 50%;
            }
            .result-answer-order {
              flex-basis: 50%;
              .order {
                font-size: 1.5rem;
                font-weight: bold;
                color: gray;
                margin-right: 0.5rem;
              }
            }
            .fa-check {
              color: gray;
              flex-basis: 50%;
            }
            .fa-circle {
              color: rgba(0, 84, 75, 0.839);
              font-size: 1.5rem;
              flex-basis: 50%;
              margin-right: 0.1rem;
            }
            .fa-times {
              color: rgba(244, 10, 10, 0.839);
              font-size: 1.5rem;
              margin-right: 0.1rem;
              flex-basis: 50%;
            }
          }
        }
        .is-correct-answer {
          background: rgb(177, 243, 231);
        }
        .isnot-correct-answer {
          background: rgb(255, 147, 147);
        }
        .selected-answer {
          background: $base-lite-3;
          .answer-select {
            background: $base-color;
            color: white;
          }
        }
      }


</style>