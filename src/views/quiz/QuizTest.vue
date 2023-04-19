<template>
    <div class="quiz-wrapper" :class="{'laoding-center':$store.state.isLoading}">
        <div class="main-wrapper">
             <QuizP
                v-if="!finishTest"
                :forQuizPageInfo="forQuizPageInfo"
                @nextQuestionFunForTest='checkConsecutiveResult'
                @startFunction='closeStart'
                dispatchFunctionName='getTestQuestions'
                quizType='test'
                ref='quiz'
            />

            <TestResult
            v-if="finishTest"
            :forQuizPageInfo="forQuizPageInfo"
            :finalResult="finalResult"
            :startGradeAndLevel="startGradeAndLevel"
            :gradeList="gradeList"
            />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {mapGetters,mapActions} from 'vuex'
import QuizP from "@/components/quiz_components/QuizP.vue";
import TestResult from '@/components/initial/TestResult.vue'

export default {
    beforeRouteLeave (to, from, next) {
        if(this.start&&!this.finishTest){
            let answer = window.confirm("本当に離れますか？　本日のテストは終了になります。")
            if (answer) {
                next()
            } else {
                next(false)
            }
        }else{
            next(true)
        }
    },
    components: {
    TestResult,
    QuizP
  },  
    data(){
        return{
            answerIDAndOrder:{},
            showResult: false,
            showNextOrFinishButton:false,
            result: false,
            start: false,
            date:'',
            forQuizPageInfo:{
                grade:'',
                field:'',
                option:'テスト',
                description:['・1日1回受けることができます。','・途中でやめた場合は1回にカウントされます。','・質問数は決まっていません。'],
                all: false,
            },
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
            currentGrade:"",
            correctAnswer:{},
            startGradeAndLevel:{
                grade:'',
                level:''
            },
            tempStatusDict:{
                'status':[],
                'grade':'',
                'level':''
            },
            setQuizAndLevel:{
                'quizId':'',
                'level':''
            },
            gradeList:[
                '超初級',
                '初級',
                '中級',
                '上級'
            ]
        }
    },
    created(){
        this.$store.commit('setIsLoading', false)
        this.$store.dispatch('setQuizIdAndlevelAction')
        this.getTestQuestions()
    },
    mounted(){
        console.log('test_moin', this.$refs.quiz.SelectedAnswerInfo,this.SelectedAnswerInfo)
        if(location.pathname==="/quiz-test") {
            window.addEventListener('beforeunload',this.handleBeforeUnload)
        }
        this.startGradeAndLevel.grade = this.quizTakerObject.grade
        this.startGradeAndLevel.level = this.quizTakerObject.level
        this.quizTestInfo.quizId = this.quizTakerObject.grade
        this.currentGrade = this.quizTakerObject.grade
        this.$store.commit('convertGradeFromIDToInt',this.currentGrade)
        this.currentLevel = this.quizTakerObject.level
        this.$store.commit('onQuizTrue')
        this.forQuizPageInfo.grade = this.gradeForConvert
    },
    beforeUnmount(){
        this.$store.commit('onQuizFalse')
        window.removeEventListener('beforeunload',this.handleBeforeUnload)
    },
    computed: mapGetters(['questions','quiz', 'quizTakerObject', 'gradeForConvert', 'getUser']),
    SelectedAnswerInfo() {
        debugger
        return this.$refs.quiz.SelectedAnswerInfo
    }
    ,
    methods:{
        ...mapActions(['getTestQuestions']),
        
        
        // from here for test function
        quizTestInfoHandler(){
            if(this.currentLevel >= 11) {
                this.currentLevel = 1;
                for(let [index,i] of this.gradeList.entries()){
                    this.$store.commit('convertGradeFromIntToID',i)
                    if(this.gradeForConvert == this.currentGrade) {
                        this.$store.commit('convertGradeFromIntToID',this.gradeList[index +1])
                        this.quizTestInfo.quizId = this.gradeForConvert
                        this.currentGrade = this.gradeForConvert
                        break
                    }
                }
            }
            else if(this.currentLevel == 0){
                this.currentLevel = 10;
                for(let [index,i] of this.gradeList.entries()){
                    this.$store.commit('convertGradeFromIntToID',i)
                    if(this.gradeForConvert == this.currentGrade) {
                        this.$store.commit('convertGradeFromIntToID',this.gradeList[index -1])
                        this.quizTestInfo.quizId = this.gradeForConvert 
                        this.currentGrade = this.gradeForConvert
                        break
                    }
                }
            }
        },
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
                        this.quizTestInfoHandler()
                        if(this.LevelCounters.handleLevelUp+this.LevelCounters.handleLevelDown == 3){
                            this.finishTest = true
                            this.getFinalResult()
                            this.LevelCounters.handleLevelUp = 0
                            this.LevelCounters.handleLevelDown = 0
                        }
                        else{
                            this.quizTestInfo.level = this.currentLevel
                            this.$store.commit('getTestQuizInfo',this.quizTestInfo)
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
                            this.quizTestInfoHandler()
                            if(this.LevelCounters.handleLevelUp+this.LevelCounters.handleLevelDown == 3){
                                this.finishTest = true
                                this.getFinalResult()
                                this.LevelCounters.handleLevelUp = 0
                                this.LevelCounters.handleLevelDown = 0
                            }
                            else{
                                this.quizTestInfo.level = this.currentLevel
                                this.$store.commit('getTestQuizInfo',this.quizTestInfo)
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
                            this.quizTestInfoHandler()
                            this.quizTestInfo.level = this.currentLevel
                            this.$store.commit('getTestQuizInfo',this.quizTestInfo)
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
                                this.quizTestInfoHandler()
                                this.quizTestInfo.level = this.currentLevel
                                this.$store.commit('getTestQuizInfo',this.quizTestInfo)
                                this.getTestQuestions()
                                correctCounter = 0
                                testAnswerFunction()
                            }
                        }
                    }
                }
            }
        },
        async updateQuizTaker(){
            const quiztakerId = this.$store.state.signup.quizTakerObj.id
            this.$store.commit("convertGradeFromIntToID",this.finalResult.grade)
            await axios
            .patch(`api/quiz-taker-test/?quiz_taker=${quiztakerId}&grade=${this.currentGrade}&level=${this.finalResult.level}`)
            .catch(e => {
                    let logger = {
                        message: "in QuizTestInit/updateQuizTaker. couldn't update QuizTaker",
                        path: window.location.pathname,
                        actualErrorName: e.name,
                        actualErrorMessage: e.message,
                    }
                    this.$store.commit('setLogger',logger)
                    this.$store.commit('setIsLoading', false)
                    router.push({ name: 'ConnectionError' })
                })
        },
        getFinalResult(){
            this.$store.commit('convertGradeFromIDToInt',this.currentGrade)
            this.finalResult.grade = this.gradeForConvert
            this.finalResult.level = this.currentLevel
            // this.tempStatusDict.level = this.currentLevel
            this.$store.dispatch('convertGradeFromIntToIDForNewUser',this.currentGrade)
            // this.tempStatusDict.grade = this.$store.getters.gradeForConvert
            // this.tempStatusDict.grade = this.$store.state.quiz.gradeForConvert
            // console.log("CHECK_TEMP+DICT_GRADE", this.tempStatusDict.grade)
            // if(!this.tempStatusDict.grade){
            //     // 4 is 超初級. it might be chainge
            //     this.tempStatusDict.grade = 4
            // }
            let payload = {grade:this.currentGrade,level:this.currentLevel}
            this.$store.dispatch('updateQuizTakerAction',payload)
            this.updateQuizTaker()
            this.$store.commit('convertGradeFromIDToInt',this.startGradeAndLevel.grade)
        },
        async closeStart(){
            this.$store.commit('updateTestTaken')
            this.start = true
            this.date = new Date()
            const testTakenObj = {
                UID:this.getUser.UID,
                test_taken:true,
                date_offset: this.date.getTimezoneOffset()

            }
            await this.$store.dispatch('testTakenUpdate', testTakenObj)
        },
        handleBeforeUnload(e){
            e.preventDefault()
            const message =
                "Are you sure you want to leave? All provided data will be lost.";
            e.returnValue = message;
            return e.returnValue;
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