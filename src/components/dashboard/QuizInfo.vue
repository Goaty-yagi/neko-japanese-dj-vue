<template>
    <section class='quiz-info-section'>
        <div class="main-wrapper">
            <div class="bar-wrapper">
                <bar
                class="bar-chart"
                :chart-data='barChartData'
                :detail="detail"
                @barChartDetail="barChartDetail"/>
            </div>
            <div class="chart-footer">
                <div @click="setBarChartData()" class='all-quizzes' :class="{'selected':!currentTitle}">
                    <p class="all">ALL</p>
                </div>
                <p class="total">Total:{{sumOfAllQuestions}} questions</p>
                <div class="each-title-container">
                    <div class="title-loop"
                        v-for="(quiz,index) in quizNameId"
                        v-bind:key="index">
                        <p class="each-title" 
                            :class="{'selected-title':currentTitle==quiz.name}"
                            @click="barChartDetail(quiz.id-1)">{{ quiz.name }}</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import ConfettiExplosion from "vue-confetti-explosion";
import TestConf from '@/components/initial/TestConf.vue'
import Notification from '@/components/initial/Notification.vue'
import NotLogin from '@/components/login/NotLogin.vue'
import  Bar from '@/components/charts/Bar.vue'
import  Chart from '@/components/account/Chart.vue'
import {router} from "@/main.js"
import axios from 'axios';

export default {
    name: 'Home',
    components: {
        TestConf,
        Notification,
        NotLogin,
        Bar,
        Chart,
        ConfettiExplosion
    },
    data(){
        return{
            numOfQuestions:'',
            detail: false,
            fixedTitleArray:[],
            currentTitle:'',
            errorMessage:'components/dashboard/QuizInfo',
            
            field:'並び替え',
            showCompo: false,
            showNotLogin: false,
            item:{status: 1,num:5,test:true},
            test1:"",
            slideIn:true,
            slideOut:false,
            backgroundColorList:[
                'rgba(255, 153, 51, 0.2)',
                'rgba(81, 255, 0, 0.2)',
                'rgba(191, 0, 255, 0.2)',
                'rgba(255, 6, 6, 0.2)',
            ],
            sumOfAllQuestions:'',
            barChartData:{
                labels: [],
                datasets: [{ 
                    label: "",
                    data: [],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(255, 205, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(201, 203, 207, 0.2)'
                        ],
                    borderColor: [
                    'rgb(255, 99, 132)',
                    'rgb(255, 159, 64)',
                    'rgb(255, 205, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(54, 162, 235)',
                    'rgb(153, 102, 255)',
                    'rgb(201, 203, 207)'
                    ],
                }]
            },
            chartData: {
                labels: ["形容詞","文法","動詞","語彙","数字"],
                datasets: [{ 
                    label: "",
                    data: [7,3,8,1,9],
                    borderWidth:1,
                    backgroundColor:'rgba(81, 255, 0, 0.2)',
                    borderColor: ' #ff9933',
                    pointBackgroundColor: 'rgb(255, 99, 132)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'red'
                }],
            },
        }
    },
    created() {
        
    },
    mounted(){
        this.getNumOfQuestions()
    },
    computed:{
        user(){
            return this.$store.state.signup.djangoUser
        },
        tempUser(){
            return this.$store.state.signup.tempUser
        },
        reccomendedQuestion(){
            return this.$store.getters.gettersReccomendedQuestion
        },
        emailVerified(){
            return this.$store.getters.getEmailVerified
        },
        tempUserTest(){
            try{
                return this.$store.state.signup.tempUser.test
            }
            catch{
                return false
            }
        },
        questions(){
            return this.$store.getters.questions
        },
        quizNameId(){
                    return this.$store.getters.quizNameId
        },
    },
    methods:{
        async getNumOfQuestions() {
            const response = await axios
            .get('/api/questions-dashboard/')
            .catch(e => {
                let logger = {
                    message: this.errorMessage + " getNumOfQuestions",
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,
                }
                this.$store.commit('setLogger',logger)
                this.$store.commit('setIsLoading', false)
                router.push({ name: 'ConnectionError' })
            })
            this.numOfQuestions = response.data[0]
            this.setBarChartData()
        },
        setBarChartData() {
            this.detailFalse()
            this.currentTitle=''
            const tempList = []
            const tempLadelList = []
            for(let i of this.numOfQuestions.get_num_of_question.slice(0,this.numOfQuestions.get_num_of_question.length-1)) {
                let title = Object.keys(i)[0]
                tempLadelList.push(title)
                this.fixedTitleArray = tempLadelList
                this.barChartData.labels = tempLadelList
                tempList.push(i[title].sum)
                this.barChartData.datasets[0].data = tempList
            }
            this.sumOfAllQuestions = this.numOfQuestions.get_num_of_question[this.numOfQuestions.get_num_of_question.length-1].all_questions_num
        },
        barChartDetail(index) {
            for(let i of this.numOfQuestions.get_num_of_question.slice(0,this.numOfQuestions.get_num_of_question.length-1)) {
                if(Object.keys(i)[0]==this.fixedTitleArray[index]){
                    this.currentTitle = this.fixedTitleArray[index]
                    this.barChartData.datasets[0].data= Object.values(i[this.fixedTitleArray[index]])
                    this.barChartData.labels = Object.keys(i[this.fixedTitleArray[index]])
                    this.detail = true
                    
                }
            }
        },
        detailFalse() {
            this.detail = false
        },
        componentHandler(){
            if(this.tempUserTest){
                this.handleShowNotLogin()
            }
            else{
                this.showCompoHandler()
            }
        },
        showCompoHandler(){
        this.showCompo = !this.showCompo
        },
        handleShowNotLogin(){
            this.showNotLogin = !this.showNotLogin
        },
        scrollTop(){
            window.scrollTo({
            top: 0,
            // behavior: "smooth"
            });
        },
        async setInitUserStatus(){
            if(this.emailVerified){
                if(this.$store.getters.getTempUser.test){
                    this.$store.commit('setQuizTakerID',this.user.quiz_taker.id)
                    this.$store.commit('setQuizID',this.$store.getters.getTempUser.grade)
                    for(let i of this.$store.getters.getTempUser.statusList){
                        await this.$store.dispatch('userStatusPost',i)
                    }
                }
                this.$store.commit('setTempUserReset')
            }
        },
        testClick(){
            this.slideIn = !this.slideIn
            this.slideOut = !this.slideOut
        },
    }
}       
</script>
<style scoped lang="scss">
@import "style/_variables.scss";

.quiz-info-section{
    width:100%;
    display: flex;
    align-items: center;
    flex-direction: column;
    .main-wrapper{
        .bar-wrapper{
            position: relative;
            .bar-chart{
                width: 90%;
                left: 0;
                right: 0;
                margin: 0 auto;
            }
        }
        .chart-footer{
            display: flex;
            flex-direction: column;
            align-items: center;
            .all-quizzes{
                color: white;
                padding: 0 1rem;
                margin: 0.5rem 0;
                font-size: 1.2rem;
                font-weight: bold;
                border: solid $base-color;
                border-radius: 50vh;
                transition: .5s;
                .all{

                }                
            }
            .selected{
                color: $dark-blue;
                background: $base-color-tr;
                border: solid white;
            }
            .total{
            color: white;
            font-weight: bold;
            margin-bottom: 0.5rem;
            }
            .each-title-container{
                display: flex;
                justify-content: center;
                width: 100%;
                .title-loop{
                    .each-title{
                        color: white;
                        margin-left: 0.5rem;
                        margin-right: 0.5rem;
                        padding: 0 0.4rem;
                        font-weight: bold;
                        border: solid $base-color;
                        transition: .5s;
                    }.selected-title{
                        color: $dark-blue;
                        background: $base-color-tr;
                        border: solid white;
                    }
                }

            }
        }
    }
}
.hero-title{
    border-top: 6px solid $base-color;
    border-right: 1px solid $base-color;
    border-left: 1px solid $base-color;
    border-bottom: 1px solid $base-color;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    padding-right: 0.1rem;
    padding-left: 0.1rem;
    font-weight: bold;
    font-size: 1.1rem;
    color: white;

}




.slide-in{
	text-align: center;
	opacity: 0;
	animation: slide-in-anim 1.5s ease-out forwards;
}
.slide-out{
    text-align: center;
	opacity: 1;
	animation: slide-out-anim 1.5s ease-out forwards;
}

@keyframes slide-in-anim {
	20% {
		opacity: 0;
        transform: translateX(-20%);
	}
	100% {
		opacity: 1;
		transform: translateX(0);
	}
}
@keyframes slide-out-anim {
	20% {
		opacity: 1;
        transform: translateX(0);
	}
	100% {
		opacity: 0;
		transform: translateX(-20%);
        display: none;
	}
}
</style>
