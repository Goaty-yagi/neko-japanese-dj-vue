<template>
    <div class="quiz-wrapper" :class="{'laoding-center':$store.state.isLoading}">
        <div class="main-wrapper">
            <QuizP
                 v-if="!finishTest"
                @nextQuestionFunForTest='checkConsecutiveResult'
                dispatchFunctionName='getTestQuestions'
                quizType='init'
                ref='quiz'
            />
            <TestResult
            v-if="finishTest"
            :finalResult="finalResult"
            :init="init"
            />
        </div>
    </div>
</template>

<script>
import {mapGetters,mapActions} from 'vuex'
import QuizP from "@/components/quiz_components/QuizP.vue";
import TestResult from '@/components/initial/TestResult.vue'

export default {
    components: {
    TestResult,
    QuizP
  },  
    data(){
        return{
            SelectedAnswerInfo:{},
            selectedAnswer: {},
            answerIDAndOrder:{},
            showResult: false,
            showNextOrFinishButton:false,
            result: false,
            countupDict:{
                answerID:'',
                questionID:'',
                questionType:''
            },
            pagination:{
                a: 0,
                b: 1,
            },
            resultHandleDict:{
                isCorrect: false,
                IsNotCorrect: false,
                answerIDType3: '',
                questionType4: false,
                answerAllTrueType4: false,
                answerIDType4: '',
                answerIDType5: '',
            },
            
            maxSelectReach: false,
            selectedIndexNum: null,
            showSelectNum: true,
            selectedOrderAnswer:{},
            selectAnswerCounter:0,
            NumOfIscorrect:0,
            // here for status attribute
            userStatusDict:{
                status:'',
                isCorrect:0,
                isFalse:0
            },
            // from here for test attributes
            quizTestInfo:{
                level:'',
                quizId:4
            },
            LevelCounters:{
                handleLevelUp:0,
                handleLevelDown:0
            },
            finalResult:{
                grade:'',
                level:''
            },
            finishTest:false,
            currentLevel:1,
            currentGrade:"超初級",
            correctAnswer:{},
            tempStatusDict:{
                'status':[],
                'grade':'',
                'level':''
            },
            init: true,
        }
    },
    created(){
        this.getTestQuestions()
    },
    mounted(){
        this.$store.commit('onQuizTrue')
        this.SelectedAnswerInfo = {}
    },
    beforeUnmount(){
        this.$store.commit('onQuizFalse')
    },
    computed: mapGetters(['questions','quiz']),
    methods:{
        ...mapActions(['getTestQuestions']),

        
        // from here for test function
        checkConsecutiveResult(){
            const selectedAnswerInfo = this.$refs.quiz.SelectedAnswerInfo
            const testAnswerFunction = this.$refs.quiz.testAnswerFunction
            console.log("from TEST",selectedAnswerInfo)
            var correctCounter = 0
            if(Object.keys(selectedAnswerInfo).length >= 4){
                console.log("more than 4")
                if(Object.keys(selectedAnswerInfo).length == 10){
                    let isTrue = 0
                    let isFalse = 0
                    for (let i = 1; i <= 10; i++){
                        if(selectedAnswerInfo[i].isCorrect){
                            isTrue += 1
                        }else{
                            isFalse += 1
                        }
                    }
                    if(isTrue >= 7){
                        this.LevelCounters.handleLevelUp += 1
                        this.currentLevel += 1
                        // this.quizTestInfoHandler()
                        if(this.LevelCounters.handleLevelUp+this.LevelCounters.handleLevelDown == 3){
                            this.finishTest = true
                            this.getFinalResult()
                            this.LevelCounters.handleLevelUp = 0
                            this.LevelCounters.handleLevelDown = 0
                        }
                        else{
                            this.quizTestInfo.level = this.currentLevel
                            // this.$store.commit('getTestQuizInfo',this.quizTestInfo)
                            this.getTestQuestions()
                            correctCounter = 0
                            testAnswerFunction()
                        }
                    }
                    else if(isTrue > 4 && isTrue < 7){
                        this.finishTest = true
                        this.getFinalResult()
                        this.LevelCounters.handleLevelUp = 0
                        this.LevelCounters.handleLevelDown = 0
                    }
                    else{
                        this.LevelCounters.handleLevelDown += 1
                        this.$store.commit('convertGradeFromIntToID',this.gradeList[0])
                        if(this.currentGrade !=this.gradeForConvert){
                            this.currentLevel -= 1
                            // this.quizTestInfoHandler()
                            if(this.LevelCounters.handleLevelUp+this.LevelCounters.handleLevelDown == 3){
                                this.finishTest = true
                                this.getFinalResult()
                                this.LevelCounters.handleLevelUp = 0
                                this.LevelCounters.handleLevelDown = 0
                            }
                            else{
                                this.quizTestInfo.level = this.currentLevel
                                // this.$store.commit('getTestQuizInfo',this.quizTestInfo)
                                this.getTestQuestions()
                                correctCounter = 0
                                testAnswerFunction()
                            }
                        }
                        else{
                        }
                    }
                    if(this.LevelCounters.handleLevelUp+this.LevelCounters.handleLevelDown == 3){
                        this.finishTest = true
                        this.getFinalResult()
                        this.LevelCounters.handleLevelUp = 0
                        this.LevelCounters.handleLevelDown = 0
                    }
                }else{
                    console.log("less than 10")
                    let num4 = 0
                    num4 = Object.keys(selectedAnswerInfo).length - 4
                    // check correct answer 4 times in a row
                    for (let i = 1; i <= 4; i++){
                        if(selectedAnswerInfo[i + num4].isCorrect){
                            correctCounter += 1
                        }
                    }
                    if(correctCounter == 4){
                        this.LevelCounters.handleLevelUp += 1
                        if(this.LevelCounters.handleLevelUp>=3&&this.LevelCounters.handleLevelDown==0){
                            this.finishTest = true
                            this.getFinalResult()
                            this.LevelCounters.handleLevelUp = 0
                        }else if(this.LevelCounters.handleLevelUp+this.LevelCounters.handleLevelDown==3){
                            this.finishTest = true
                            this.getFinalResult()
                            this.LevelCounters.handleLevelUp = 0
                            this.LevelCounters.handleLevelDown = 0
                        }else{
                            this.currentLevel += 1
                            // this.quizTestInfoHandler()
                            this.quizTestInfo.level = this.currentLevel
                            // this.$store.commit('getTestQuizInfo',this.quizTestInfo)
                            this.getTestQuestions()
                            testAnswerFunction()
                            correctCounter = 0
                        }                
                    }else if(correctCounter == 0){
                        this.$store.commit('convertGradeFromIntToID',this.gradeList[0])
                        if(this.currentLevel==1&&this.currentGrade==this.gradeForConvert){
                            this.finishTest = true
                            this.getFinalResult()
                            this.LevelCounters.handleLevelUp = 0
                            this.LevelCounters.handleLevelDown = 0
                        }
                        else{
                            this.LevelCounters.handleLevelDown += 1
                            if(this.LevelCounters.handleLevelDown>=3&&this.LevelCounters.handleLevelUp==0){
                                this.finishTest = true
                                this.getFinalResult()
                                this.LevelCounters.handleLevelDown = 0
                            }
                            else if(this.LevelCounters.handleLevelUp+this.LevelCounters.handleLevelDown==3){
                                this.finishTest = true
                                this.getFinalResult()
                                this.LevelCounters.handleLevelUp = 0
                                this.LevelCounters.handleLevelDown = 0
                            }else{
                                this.currentLevel -= 1
                                // this.quizTestInfoHandler()
                                this.quizTestInfo.level = this.currentLevel
                                // this.$store.commit('getTestQuizInfo',this.quizTestInfo)
                                this.getTestQuestions()
                                correctCounter = 0
                                testAnswerFunction()
                            }
                        }
                    }
                }
            }
        },
        getFinalResult(){
            this.finalResult.grade = this.currentGrade
            this.finalResult.level = this.currentLevel
            this.tempStatusDict.level = this.currentLevel
            this.$store.dispatch('convertGradeFromIntToIDForNewUser',this.currentGrade)
            this.tempStatusDict.grade = this.$store.getters.gradeForConvert
            this.tempStatusDict.grade = this.$store.state.quiz.gradeForConvert
            if(!this.tempStatusDict.grade){
                // 4 is 超初級. it might be chainge
                this.tempStatusDict.grade = '超初級'
            }
            this.$store.commit('setTempUser',this.tempStatusDict)
            this.$store.commit('tempUserTestTrue')
        }
    }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.quiz-wrapper{
    width: 100%;
    display: flex;
    justify-content: center;
    margin-top: 0.5rem;
    padding-bottom: 2rem;
}
</style>