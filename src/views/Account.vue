<template>
    <div v-if="!isLoading" class="account-wrapper" >
        <div class="main-wrapper">
            <div v-if="imageCreated" class='notification-blue'>
                <div class="notification-text">
                    サムネイルを変更しました。
                </div>
            </div>
            <div class="content-wrapper" >
                <h1 class='title-white'>アカウント</h1>
                <div class="cropper-wrapper">
                    <img v-bind:src="user.sns_thumbnail?user.sns_thumbnail:user.thumbnail"/>
                    <p class="change-img" @click='handleShowThumbnail'>画像を<br>変更する</p>
                </div>
                <div class="my-quiz-wrapper">
                    <router-link :to="{ name: 'MyQuiz'}" class="my-quiz">My Quiz</router-link>
                </div>

                <div v-if="showNotification" class="notification-container">
                    <div class="alert-position-container">
                        <div class="notification-text">
                            お知らせ
                        </div>
                        <div class="notification-alert">
                            Notifications
                        </div>
                    </div>
                </div>
                <div class="user-info-wrapper">
                    <div class="user-name user-container">
                        <div class="left-side">
                            User<br>Name
                        </div>
                        <div class="right-side">
                            {{ user.username}}
                        </div>
                    </div>
                    <div class="current-level user-container">
                        <div class="left-side">
                            Current<br>Grade
                        </div>
                        <div class="right-side grade-right-side">
                            <div classs="current-level-text">
                                {{ getCurrentGradeNameFromIds(quizTaker.grade)}}
                                Lv,{{ quizTaker.level }}
                            </div>
                        </div>       
                    </div>
                    <div class="current-level user-container">
                        <div class="left-side">
                            Max<br>Grade
                        </div>
                        <div class="right-side grade-right-side">
                            <div classs="current-level-text">
                                {{ quizTaker.max_grade }}
                                Lv,{{ quizTaker.max_level }}
                            </div>
                        </div>       
                    </div>
                    <div @click="stopFlash()" :class="(gradeUp)?'next-grade-up':'next-level'">
                        <span v-if="!gradeUp" class="next-title">Next-Level</span>
                        <span v-if="gradeUp" class="next-title grade-up">Grade-Up</span>
                        <p :class="{'stop':stop}">{{ nextGrade(getCurrentGradeNameFromIds(quizTaker.grade),quizTaker.level) }}</p>
                    </div>
                </div>
                <div class="status-wrapper">
                    <div class=chart-loop 
                    v-for="(g,key,index) in grade"
                    v-bind:key="index">
                        <div @click="handleStatusParameter(convertGradeIntToGradeId(key))" 
                            v-if="showChartHeaderGrade(key)" 
                            class="chart-header"
                            :class="{'current-status-grade':getCurrentStatusGrade(convertGradeIntToGradeId(key))}">
                            <div>{{key}}</div>
                        </div>
                    </div>
                    <chart
                    
                    :chart-data="chartData"
                    />
                </div>
                <div @click="goCommunityAccount()" class="comunity-account">
                    コミュニティアカウントへ移動
                </div>
            </div>
        </div>
        <NotVerified
        v-if="!emailVerified&&$store.state.isLoading==false"
        :currentPageName="currentPageName"
        />
        <Sent v-if='showSent'/>
        <Thumbnail v-if="showThumbnail"
        @showThumbnailFalse="showThumbnailFalse"
        @imageCreatedHandler="imageCreatedHandler"
        :getUser="getUser"
        :minContainerHeight="minContainerHeight"
        :imageType="imageType"
        :minContainerWidth="minContainerWidth"/>
    </div>
</template>

<script>
import {router} from "../main.js"
import 'cropperjs/dist/cropper.css';
import  Thumbnail from '@/components/account/Thumbnail.vue'
import  Chart from '@/components/account/Chart.vue'
import Sent from '@/components/signin/Sent.vue'
import NotVerified from '@/components/login/NotVerified.vue'
import { computed } from 'vue'
import { useStore } from 'vuex'
import {mapGetters,mapActions} from 'vuex'

export default{
    setup(){
        const store = useStore()
        return{
            user: computed(() => store.state.signup.user),
            quizTaker: computed(() => store.state.signup.quizTakerObj),
            email: computed(() => store.state.signup.email),
            password: computed(() => store.state.signup.password),
            emailVerified: computed(() => store.state.signup.emailVerified),
            mounted: computed(() => store.state.signup.mounted),
            isLoading: computed(() => store.state.isLoading) 
        }
    },
    data(){
        return{
            showSent:false,
            error:'',
            userData:'',
            showThumbnail:false,
            currentPageName:'',
            gotInfo:false,
            showNotification:false,
            stop: false,
            gradeUp: false,
            currentStatusGrade:'',
            widthForCropper:'',
            minContainerHeight:'',
            minContainerWidth:'',
            imageType: 'thumbnail',
            imageCreated: false,
            backgroundColorList:{
                '超初級':'rgba(255, 153, 51, 0.2)',
                '初級':'rgba(81, 255, 0, 0.2)',
                '中級':'rgba(191, 0, 255, 0.2)',
                '上級':'rgba(255, 6, 6, 0.2)',
            },
            grade:{
                '超初級':0,
                '初級':1,
                '中級':2,
                '上級':3,
            },
            chartAllData:{
                '超初級':{
                    labels:[
                        'ひらがな', 
                        'カタカナ', 
                        'ボキャブラリー', 
                        'すうじ'
                        ],
                },
                '初級':{
                    labels:[
                        '漢字',
                        '動詞',
                        'い形容詞',
                        'ボキャブラリー',
                        '文法',
                        'な形容詞',
                    ],
                },
                '中級':{
                    labels:[],
                },
                '上級':{
                    labels:[],
                }
            },
            chartData: {
                labels: [],
                datasets: [{ 
                    label: "",
                    data: [],
                    borderWidth:1,
                    backgroundColor: 'rgba(255, 153, 51, 0.2)',
                    borderColor: ' #ff9933',
                    pointBackgroundColor: 'rgb(255, 99, 132)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'red'
                }],
            },
        }
    },
    components: {
        Sent,
        Thumbnail,
        Chart,
        NotVerified
    },
    async created(){
        // this.$store.commit('setIsLoading', true)
        await this.getQuizNameId()
        this.$store.commit('setIsLoading', false)
    },
    computed: mapGetters(['quizNameId','getUser','getEmailVerified', 'quizTakerObject','fixedScroll']),
        
    mounted(){

        window.addEventListener('resize', this.getWidth)
        this.currentPageName = ''
        this.getCurrentPageName()
        this.handleStatusParameter(this.quizTaker.grade)
    },
    beforeUnmount(){
    },
    methods:{
        ...mapActions(['getQuizNameId']),
        async resent(){
            try{
                await this.$store.dispatch('sendEmailVerify')
                this.handleShowSent()

            }catch(err){
                this.error = err
            }
        },
        handleShowSent(){
            this.showSent = true
        },
        handleShowThumbnail(){
            this.showThumbnail = true
        },
        showThumbnailFalse(){
            console.log("FALSE")
            this.showThumbnail = false
        },
        getCurrentGradeNameFromIds(gradeID){
            for (let i of this.quizNameId){
                if(i.id == gradeID){
                    return i.name
                }
            }
        },
        convertGradeIntToGradeId(gradeInt){
            for (let i of this.quizNameId){
                if(i.name==gradeInt){
                    return i.id
                }
            }
        },
        handleStatusParameter(grade){
            // this is handling chart view.
            // 1, get quiz_taker from userinfo
            // 2, get current grade from the quizTaker.
            // 3, get chart labels which is locally set.
            // 4, get percentage for each status from user_status from quiz_taker
            // 5, set the labels and the percentages to chartData to invoke data for chart component
            
            let tempDict = {}
            let tempChartAllData = this.chartAllData[this.getCurrentGradeNameFromIds(grade)].labels
            let tempArray = []
            this.currentStatusGrade = grade
            for(let i of this.quizTaker.user_status){
                if(i.grade==grade){
                    tempDict[i.status[0]]={"percentage":i.percentage,
                    'order':i.status[1],
                    }
                }
            // var sort = Object.keys(tempDict).map((k)=>({ key: k, value: tempDict[k] }));
            }
            for(let i of tempChartAllData){
                if(i in tempDict){
                    tempArray.push(tempDict[i].percentage / 10)
                }else{
                    tempArray.push(0)
                }
            }
            this.chartData.labels = tempChartAllData
            this.chartData.datasets[0].data = tempArray
            this.chartData.datasets[0].backgroundColor = this.backgroundColorList[this.getCurrentGradeNameFromIds(grade)]
            this.gotInfo = true
        },
        getCurrentStatusGrade(grade){
            if(this.currentStatusGrade==grade){
                return true
            }
            else{
                return false
            }
        },
        getCurrentPageName(){
            let i = this.$route.path
            i = i.split("/")
            this.currentPageName = i[1]
        },
        nextGrade(grade,level){
            if(level==10){
                var max = Math.max(...Object.values(this.grade))
                var g = this.grade[grade]+ 1
                if(max == this.grade[grade]){
                    return `最大レベルだよ！`
                }
                else{
                    for(let i in this.grade){
                        if(this.grade[i] == g){
                            this.gradeUp = true
                            return `次は${i}レベル${1}だよ！`
                        }
                    }
                }
            }
            else{
                return `次は${grade}レベル${level + 1}だよ！`
            }
        },
        stopFlash(){
            this.stop = !this.stop
        },
        showChartHeaderGrade(grade){
            if(this.grade[grade] <= this.grade[this.quizTaker.max_grade]){
                return true   
            }
            else{
                return false
            }
        },
        mountReset(){
            this.gradeUp = false
        },
        goCommunityAccount(){
            router.push("/board/account")
        },
        getWidth(){
            this.widthForCropper = window.innerWidth
            if(this.widthForCropper > 820 < 1200){
                this.minContainerHeight = 800
                this.minContainerWidth = 800
            }
        },
        imageCreatedHandler() {
            this.imageCreated = !this.imageCreated
            setTimeout(() => {
                this.imageCreated = !this.imageCreated
            },3000)
        }
    }
}
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";

.account-wrapper{
    display: flex;
    justify-content: center;
    .main-wrapper{
        position: relative;
        .content-wrapper{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
            .my-quiz-wrapper{
                position: relative;
                height: 30px;
                width: 100%;
                margin-top: 1rem;
                margin-bottom: 0.5rem;
                .my-quiz{
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    margin: auto;
                    padding-right: 0.6rem;
                    padding-left: 0.6rem;
                    border: solid $base-color;
                    font-weight: bold;
                    color: $lite-gray;
                    border-radius: 5px;
                    width: 90px;
                    transition: .5s;

                }
                .my-quiz:hover{
                    color: $dark-blue;
                    border: solid $dark-blue;
                    background: $buttongradient;
                }
            }
            .cropper-wrapper{
                display: flex;
                position:relative;
                justify-content: center;
                margin-top: 0.5rem;
                width: 15rem;
                img{
                    border-radius: 50%; 
                    border: solid $dark-blue;
                    width:  5rem;   
                    height: 5rem;       
                }
                .change-img{
                    position: absolute;
                    right: 0;
                    color: white;
                    font-size: 0.8rem;
                    border: solid $lite-gray;
                    border-radius: 5px;
                    padding-left: 0.3rem;
                    padding-right: 0.3rem;
                    margin-left: 1rem;
                    transition: .5s;
                }
                .change-img:hover{
                    background:rgba(252, 252, 252, 0.25);
                    border: solid $dark-blue;

                }
            }
            .notification-container{
                position: relative;
                display: flex;
                justify-content: center;
                width: 100%;
                .alert-position-container{
                    width:70%;
                    border: solid $base-color;
                    min-height: 3rem;
                    background: $back-white;
                    margin-top: 1rem;
                    margin-bottom: 1rem;
                    .notification-alert{
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
                    background:rgba(252, 75, 175, 0.961); 
                    }
                }
            }
            .user-info-wrapper{
                margin-top: 1rem;
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 100%;
                .user-container{
                    display: flex;
                    border: 0.1rem solid $dark-blue;
                    background: $back-white;
                    border-radius: 0.5rem;
                    width: 80%;
                    min-height: 3rem;
                    margin-bottom: 0.5rem;
                    overflow: hidden;
                    .left-side{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        flex-basis: 30%;
                        background: $base-color;
                        border-right: 0.1rem solid $dark-blue;
                        line-height: 0.8rem;
                        color: white;
                        font-weight: bold;
                        font-size: 1.1rem;                      
                    }
                    .right-side{
                        position: relative;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        flex-basis: 70%;
                        width:70%;
                        font-size: 1.2rem;
                        font-weight: bold;                       
                    }
                    .grade-right-side{
                        position: relative;
                        display: flex;
                        justify-content: center;
                        .current-level-text{
                            display: flex;
                            justify-content: center;
                            align-items: flex-end;
                        }
                    }
                }
                .next-level{
                    position: relative;
                    margin: 2em 0;
                    padding: 0.5em 1em;
                    width: 70%;
                    border: solid 3px #62c1ce;
                    background: $base-white;
                    .next-title{
                        position: absolute;
                        display: inline-block;
                        top: -27px;
                        left: -3px;
                        padding: 0 9px;
                        height: 25px;
                        line-height: 25px;
                        font-size: 17px;
                        background: #62c1ce;
                        color: #ffffff;
                        font-weight: bold;
                        border-radius: 5px 5px 0 0;
                    }
                    p{
                        color: $dark-blue;
                        font-weight: bold;
                        margin: 0; 
                        padding: 0;
                    }
                }
                .next-grade-up{
                    position: relative;
                    margin: 2em 0;
                    padding: 0.5em 1em;
                    width: 70%;
                    background: $base-white;
                    border: solid 3px rgb(236, 113, 181);
                    .grade-up{
                        position: absolute;
                        display: inline-block;
                        top: -27px;
                        left: -3px;
                        padding: 0 9px;
                        height: 25px;
                        line-height: 25px;
                        font-size: 17px;
                        color: #ffffff;
                        font-weight: bold;
                        border-radius: 5px 5px 0 0;
                        background: rgb(236, 113, 181);
                    }
                    p{
                        animation: flash 2.5s linear infinite;
                        color: $dull-red;
                        font-weight: bold;
                        margin: 0; 
                        padding: 0;
                    }
                    .stop{
                        animation: none;
                    }
                }
            }
            .status-wrapper{
                .chart-loop{
                    display: inline-block;
                    .chart-header:hover{
                        background:rgba(255, 6, 6, 0.2);
                        font-weight: bold;
                    }
                    .chart-header{
                        border: solid $base-color;
                        border-radius: 5px;
                        margin-right: 0.3rem;
                        margin-left: 0.3rem;
                        padding-right: 0.7rem;
                        padding-left: 0.7rem;
                        padding-top: 0.1rem;
                        padding-bottom: 0.1rem;
                        color: white;
                        transition: .5s;
                    }
                    .current-status-grade{
                        background:$base-color-tr;
                        font-weight: bold;
                        border: solid $dull-red;
                    }
                }
            }
            .comunity-account{
                color: white;
                cursor : pointer;
                border: solid rgba(0, 0, 0, 0);
                border: solid gray;
                border-radius: 5px;
                padding: 1rem;
                transition: 0.5s;
                margin-bottom: 1rem;
            }
            .comunity-account:hover{
                border: solid $dark-blue;
                background:rgba(252, 252, 252, 0.25);
                padding: 1rem;
            }
        }
    }
}
.notification-blue {
    position: absolute;
    height: 80px;
    bottom: 0;
    right: 0;
    left: 0;
    margin: 0 auto;
}
@keyframes flash {
  0%,100% {
    opacity: 1;
  }

  50% {
    opacity: 0;
  }
}



    .main-image{
        width:15%;
        height:auto;
        margin-left: auto;
        margin-right: auto;
    }
    .main-text1{
        font-size:1rem;
        font-weight: bold;
        margin:2rem;
    }
    img {
        border-radius: 50%; 
        width:  5rem;   
        height: 5rem;       
    }
    .cropper-view-box,
    .cropper-face {
      border-radius: 50%;
      cursor: grab;
      outline: initial;
    }
    .cropper-face:active {
      cursor: grabbing;
    }
</style>