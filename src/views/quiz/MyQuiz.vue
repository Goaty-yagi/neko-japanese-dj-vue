<template>
    <div class="my-quiz-wrapper" >
        <div v-if="$store.state.board.notifications.reply" :class="{'notification-blue':$store.state.board.notifications.reply}">
            <div class="notification-text">
                削除しました。
            </div>
        </div>
        <div class="main-wrapper">
            <QuizP
            v-if="quizOpen"
            quizType='myQuiz'
            :myQuestion='myQuestion'
            />
            <div class="main-container" v-if="!quizOpen&&!$store.state.isLoading">
                <div class="my-quiz-header">
                    <p class="title-white">My-Quiz</p>
                    <p class="register">登録数{{ length }} / {{myQuiz.max_num}}</p>
                    <p class="max">(最大 {{myQuiz.max_num}} 個まで登録できます)</p>
                </div>
                <div class="my-quiz-container" v-if="$store.state.isLoading==false">
                    <div class="no-my-quiz" v-if="!showButtonAndNoQuiz">
                        <div class="no-quiz">
                            登録したクイズはありません。<br>
                            クイズ画面から登録できます。<br><br>
                            クイズを登録すると、<br>そのクイズだけ練習できます。
                        </div>
                        <router-link :to="{ name: 'QuizHome'}" class="btn-basegra-white-db-sq">
                            クイズへ行く
                        </router-link>
                    </div>
                    <div class=my-quiz-loop @click="getQuestionDetailInfo(question)" v-for="(question,questionindex) in myQuestion"
                        v-bind:key="questionindex">
                        <div class="each-quiz-container">
                            <div class="question-index-container">
                                <div class="question-index">{{ questionindex+1 }}</div>
                            </div>
                            <div class="question-field">{{ convertFieldIdToInt(question.question.field[0]) }}</div>
                            <div class="question-grade">{{ convertQuizIdToInt(question.question.quiz) }}</div>
                            <div class="question-label">{{ question.question.label.substr(0,15)+'...' }}</div>
                            <div class="close-container">
                            </div>
                        </div>
                    </div>
                    <QuizDetail
                    v-if="quizDetail"
                    :questionDetailInfo="questionDetailInfo"
                    :myQuestion="myQuestion"
                    :showButtonAndNoQuiz="showButtonAndNoQuiz"
                    :myQuiz="myQuiz"
                    @handleQuizDetail='handleQuizDetail'
                    @deleteQuestionFunForDetailPage="deleteQuestionFunForDetailPage"                    
                    />
                </div>
                <div @click="handleQuizOpen()" v-if="showButtonAndNoQuiz" class="btn-basegra-white-db-sq">
                    練習
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import NotVerified from '@/components/login/NotVerified.vue'
import MyQuizPractice from '@/components/quiz_components/MyQuizPractice.vue'
import QuizP from '@/components/quiz_components/QuizP.vue'
import QuizDetail from '@/components/quiz_components/QuizDetail.vue'

export default {
    components: {
        MyQuizPractice,
        NotVerified,
        QuizDetail,
        QuizP
    },
    data(){
        return{
            myQuestion:'',
            showButtonAndNoQuiz:false,
            quizOpen: false,
            quizDetail: false,
            questionDetailInfo:{
                id:'',
                grade:'',
                field:'',
                status:'',
                label:'',
                image:'',
            }
        }
    },
    beforeMount() {
        this.$store.commit('setIsLoading', false)
    },
    mounted(){
        this.getMyQuestion()
        console.log("M", this.myQuiz, this.myQuestion)
    },
    computed:{
        user(){
            return this.$store.state.signup.user
        },
        myQuiz(){
            return this.$store.state.quiz.myQuiz
        },
        length(){
            return this.myQuestion.length
        },
        fieldNameId(){
            return this.$store.getters.fieldNameId
        },
        quizNameId(){
            return this.$store.getters.quizNameId
        },
        statusNameId(){
            this.$store.dispatch("getStatusNameId")
            return this.$store.getters.statusNameId
        }

    },
    methods:{
        convertFieldIdToInt(fieldId){
            for(let i of this.fieldNameId){
                if(i.id==fieldId){
                    return i.name
                }
            }
        },
        convertQuizIdToInt(quizId){
            for(let i of this.quizNameId){
                if(i.id==quizId){
                    return i.name
                }
            }
        },
        convertStatusIdToInt(statusId){
            for(let i of this.statusNameId){
                if(i.id==statusId){
                    return i.name
                }
            }
        },
        getQuestionDetailInfo(question){
            this.questionDetailInfo.id = question.question.id
            this.questionDetailInfo.grade = this.convertQuizIdToInt(question.question.quiz)
            this.questionDetailInfo.field = this.convertFieldIdToInt(question.question.field[0])
            this.questionDetailInfo.status = this.convertStatusIdToInt(question.question.status[0])
            this.questionDetailInfo.label = question.question.label
            this.questionDetailInfo.image = question.question.image
            this.handleQuizDetail()

        },
        getMyQuestion(){
            this.myQuestion = this.$store.getters.myQuestion
            if(this.myQuestion.length){
                this.showButtonAndNoQuiz = true
            }
        },
        deleteMyQuestion(question){
            let payload = {
                "question":question,
                "myQuiz":this.myQuiz.id
            }
            this.myQuestion = this.myQuestion.filter(item =>{
                return (item.question.id !=question)
            })
            if(this.myQuestion.length==0){
                this.myQuestion = ''
                this.showButtonAndNoQuiz = false
            }
            this.$store.commit("deleteMyQuestion",question)
            this.$store.dispatch("createAndDeleteMyQuiz",payload)
        },
        deleteQuestionFunForDetailPage(question){
            this.myQuestion = this.myQuestion.filter(item =>{
                return (item.question.id !=question)
            })
            if(this.myQuestion.length==0){
                this.myQuestion = ''
                this.showButtonAndNoQuiz = false
            }
        },
        async handleQuizOpen(again){
            const payload = this.myQuestion.map(item =>{
                return item.question.id
            })
            console.log("PAY", payload)
            this.$store.commit('setIsLoading', true)
            await this.$store.dispatch("getQuestionFromMyQuestion",payload)
            this.$store.commit('setIsLoading', false)
            this.quizOpen = !this.quizOpen
        },
        handleQuizDetail(){
            this.quizDetail = !this.quizDetail
        },
    }

}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.main-container{
        display: flex;
        flex-direction: column;
        align-items: center;
        }

.my-quiz-wrapper{
    display: flex;
    justify-content: center;
    .main-wrapper{
        .my-quiz-header{
            margin-bottom: 1rem;
            .register{
                font-size: 1.3rem;
                color: $lite-gray;
                font-weight: bold;
            }
            .max{
                font-size: 0.8rem;
                color: $lite-gray;
            }
        }
        .my-quiz-container{
            width: 95%;
            min-height: 300px;
            max-height: 350px;
            border: solid $base-color;
            border-radius: 5px;
            background: $back-white;
            padding-top: 1rem;
            padding-bottom: 1rem;
            overflow: scroll;
            .no-my-quiz{
                margin:2rem;
                .no-quiz{
                    color: $dark-blue;
                    font-weight: bold;
                    margin-bottom: 2rem;
                }
            
            }
            .my-quiz-loop:hover{
                background: $back-lite-white;
                border-bottom: solid $lite-gray;
            }
            .my-quiz-loop{
                position: relative;
                display: flex;
                align-items: center;
                border-bottom: solid $lite-gray;
                transition: .5s;
                .each-quiz-container{
                    position: relative;
                    display: flex;
                    width: 100%;
                    margin-bottom: 1rem;
                    margin-top: 1rem;
                    // padding-bottom: 0.5rem;
                    align-items: center;
                    // justify-content: center;
                    .question-index-container{
                        flex-basis: 10%;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        .question-index{
                            border: solid $base-color;
                            border-radius: 50vh;
                            width: 1.7rem;
                            height: 1.7rem;
                            margin-left: 0.4rem;
                            font-weight: bold;
                            background: $dark-blue;
                            color: white;
                        }
                    }
                    .question-field{
                        flex-basis: 20%;

                    }
                    .question-grade{
                        flex-basis: 20%;
                    }
                    .question-label{
                        flex-basis: 50%;
                        font-size: 0.8rem;
                    }
                }
            }
           
        }
        .btn-basegra-white-db-sq{
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
            padding-top: 0.2rem;
            padding-bottom: 0.2rem;
            padding-left: 1.2rem;
            padding-right: 1.2rem;
            font-weight: bold;
            font-size: 1.2rem;

        }

    }

}
</style>