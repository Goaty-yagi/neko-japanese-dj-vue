<template>
    <section class='home-section' :class="{'scroll-fixed':fixedScroll}">

        <div class="main-wrapper" v-if="!$store.state.isLoading">
            <div v-if="!showCompo" class='home-main-wrapper'>
                <div class="home-hero">
                    <p class="hero-title">楽しく学ぶ最高峰の日本語ラーニングコミュニティ</p>
                    <img src="@/assets/logo-with-logo.png">
                    <div class="hero-paragraph-wrapper">
                        <div class="paragraph-container">
                            <p class="hero-paragraph">自分のレベルに合った問題をクイズ形式で
                            解き、実力の確認ができるプラットフォーム。</p>
                            <chart
                            class="hero-image"
                            :chart-data="chartData"
                            />
                            <!-- <img @click="testClick" class='hero-image' src="@/assets/status.png"> -->
                        </div>
                        <div class="paragraph-container">
                            <i class="fas fa-comments hero-image"></i>
                            <p class="hero-paragraph">
                            分からないことはコミュニティで質問し、
                            世界中のユーザー同士が助け合い学び合う場。
                            </p>
                        </div>
                        <div v-if="!user" class="test-button-wrapper">
                            <div class='test-button' @click='componentHandler()'>実力テストを始める</div>
                        </div>
                        <div v-if="user" class=registered-user>
                            <div class="hero-title">
                                <p>１日１回実力テストに挑戦できるよ！</p>
                            </div>
                            <div class="paragraph-container">
                                <div v-if="!user.test_taken" class="test-button-wrapper2">
                                    <div class='test-button' @click='goTest'>実力テストに挑戦する</div>
                                </div>
                                <div v-if="user.test_taken" class="done-test">
                                    本日の実力テストは終了しました
                                </div>
                                <i class="fas fa-gamepad  hero-image"></i>
                            </div>
                            <div class="hero-title">
                                <p>運営からのお知らせ</p>
                            </div>
                            <div class="paragraph-container-note">
                                <div class="note-wrapper">
                                    <div class="note-container" v-for="(note, index) in noticeFromTeam.slice(0,2)"
                                        :key="index">
                                        <div class="note-header">
                                            <div class="note-type">{{ note.type }}</div>
                                            <DateToLocal
                                            class="note-date"
                                            :UTCDate='note.issued_date'/>
                                            <!-- <div class="note-date">{{ note.issued_date }}</div> -->
                                        </div>
                                        <div class="note-title">{{ note.title.substr(0,17) }}</div>
                                        <div class="note-body">{{ note.body.substr(0,20)+'...' }}</div>
                                        <div class="note-next-container">
                                            <div class="note-next" @click='goToNoteDetail(note.slug)'>
                                                続きを見る>>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            <div class="more-read" @click="goToNoteList" v-if="noticeFromTeam.length > 2">
                                もっと見る >>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>   
            <!-- <div class='home-conf' v-if='showCompo'> -->
                <TestConf 
                @close='showCompoHandler'
                v-if='showCompo'/>   
            <!-- </div> -->
            <transition name="notice">
                <NotLogin
                    v-if="tempUserTest&&showNotLogin"
                    @handleShowNotLogin="handleShowNotLogin"
                    />
            </transition>
        </div>
    </section>
</template>

<script>
import ConfettiExplosion from "vue-confetti-explosion";
import TestConf from '@/components/initial/TestConf.vue'
import Notification from '@/components/initial/Notification.vue'
import NotLogin from '@/components/login/NotLogin.vue'
import  Chart from '@/components/account/Chart.vue'
import axios from 'axios'
import { router } from "../main.js"
import FormSelect from "@/components/parts/FormSelect.vue";
import Animation from "@/components/parts/Animation.vue";
import DateToLocal from "@/components/parts/DateToLocal.vue";
// import jwt_decode from "jwt-decode";

// import Cookies from 'js-cookie'
// import { uuid } from 'vue-uuid';
export default {
    name: 'Home',
    components: {
        TestConf,
        Notification,
        NotLogin,
        Chart,
        ConfettiExplosion,
        FormSelect,
        Animation,
        DateToLocal
    },
    data(){
        return{
            open:false,
            field:'並び替え',
            showCompo: false,
            showNotLogin: false,
            item:{status: 1,num:5,test:true},
            test1:"",
            slideIn:true,
            slideOut:false,
            googleInstance:'',
            uid:"",
            token:"",
            backgroundColorList:[
                'rgba(255, 153, 51, 0.2)',
                'rgba(81, 255, 0, 0.2)',
                'rgba(191, 0, 255, 0.2)',
                'rgba(255, 6, 6, 0.2)',
            ],
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
    created(){
        this.$store.dispatch('getNotificationList')
    },
    beforeMount() {
        this.$store.commit('setIsLoading', false)
    },
    mounted(){
        this.$store.commit('setIsLoading', false)
        console.log("mount",this.$refs.animation)
        this.scrollTop()
    },
    computed:{
        user(){
            return this.$store.state.signup.user
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
            console.log("TUT",this.$store.state.signup.tempUser.test)
            try{
                return this.$store.state.signup.tempUser.test
            }
            catch{
                return false
            }
        },
        fixedScroll(){
            return this.$store.getters.fixedScroll
        },
        noticeFromTeam(){
            return this.$store.getters.getNotificationList
        }
    },
    methods:{
        componentHandler(){
            if(this.tempUserTest){
                this.handleShowNotLogin()
            }
            else{
                this.showCompoHandler()
            }
        },
        goTest() {
            this.$store.commit('setIsLoading', true)
            router.push({ name: 'QuizTest' })
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
        goToNoteDetail(slug) {
            router.push(`/note-detail/${slug}`)
        },
        goToNoteList() {
            router.push({name:'NotificationList'})
        }
    }
}       
</script>
<style scoped lang="scss">
@import "style/_variables.scss";

.home-section{
    width:100%;
    display: flex;
    align-items: center;
    flex-direction: column;
    .main-wrapper{
        .home-main-wrapper{
            display: flex;
            .home-hero{
                width: 100%;
                margin: 1rem;
                .hero-title{
                    border-top: 6px solid $base-color;
                    border-right: 1px solid $base-color;
                    border-left: 1px solid $base-color;
                    border-bottom: 1px solid $base-color;
                    box-shadow:  1px 1px 18px #888888;
                    padding-top: 0.5rem;
                    padding-bottom: 0.5rem;
                    padding-right: 0.1rem;
                    padding-left: 0.1rem;
                    margin-top: 1rem;margin-bottom: 1rem;
                    font-weight: bold;
                    font-size: 1.1rem;
                    color: white;

                }
                // img{
                //     width: 100px;
                // }
                
                .hero-paragraph-wrapper{
                    color: $back-white;
                    .paragraph-container{
                        display: flex;
                        align-items: center;
                        background: rgba($color: $back-white, $alpha: 0.1);
                        padding: 0.6rem;
                        margin-bottom: 0.5rem;
                        .hero-paragraph{
                            flex-basis: 50%;
                            font-weight: bold;
                        }
                        .hero-image{
                            flex-basis: 60%;
                            width: 10%;
                        }
                        .fa-comments{
                            font-size: 6rem;
                            color: rgba($color: #a6a6a6, $alpha: 0.6);
                        }
                        .fa-gamepad{
                            font-size: 6rem;
                            color: rgba($color: #a6a6a6, $alpha: 0.6);
                        }
                        .done-test{
                            border: solid $dull-red;
                            padding: 0.1rem 0.5rem 0.1rem 0.5rem;

                        }
                    }
                    .test-button-wrapper{
                        margin: 1rem;
                        display: flex;
                        justify-content: center;
                        .test-button{
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            border: solid $lite-gray;
                            border-radius: 50vh;
                            padding: 1rem 1.8rem;
                            width: 250px;
                            height: 50px;
                            color: $back-white;
                            font-size: 1.1rem;
                            font-weight: bold;
                            transition: .5s;
                            margin: 2rem;
                        }
                        .test-button:hover{
                            background: rgba($color: $back-white, $alpha: 0.1);
                        }
                    }
                    // .test-button-wrapper{
                    //     margin: 1rem;
                    //     .test-button{
                    //         display: inline-block;
                    //         border: solid $lite-gray;
                    //         border-radius: 50vh;
                    //         padding: 0.1rem 0.8rem 0.1rem 0.8rem;
                    //         color: $back-white;
                    //         transition: .5s;
                    //     }
                    //     .test-button:hover{
                    //         background: rgba($color: $back-white, $alpha: 0.1);
                    //     }
                    // }
                }
            }
        }
        .home-conf{
            // margin-bottom: 200px;
        }
    }
}
.hero-title{
    border-top: 6px solid $base-color;
    border-right: 1px solid $base-color;
    border-left: 1px solid $base-color;
    border-bottom: 1px solid $base-color;
    // background: rgb(254, 254, 221);
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    padding-right: 0.1rem;
    padding-left: 0.1rem;
    font-weight: bold;
    font-size: 1.1rem;
    color: white;

}
.test-button-wrapper2{
    margin: 1rem;
    display: flex;
    justify-content: center;
    cursor: pointer;
    .test-button{
        display: flex;
        justify-content: center;
        align-items: center;
        border: solid $lite-gray;
        border-radius: 50vh;
        padding: 1rem 1.8rem;
        width: 100%;
        height: 60px;
        color: $back-white;
        font-size: 1.1rem;
        font-weight: bold;
        transition: .5s;
    }
    .test-button:hover{
        background: rgba($color: $back-white, $alpha: 0.1);
    }
}
.paragraph-container-note{
    display: flex;
    align-items: center;
    flex-direction: column;
    background: rgba($color: $back-white, $alpha: 0.1);

    margin-bottom: 0.5rem;
}
.note-wrapper {
    width: 100%;
    display: flex;
    flex-direction: column;
    // .note-container:hover{
    //     background: $base-white; 
    // }
    // .note-container:hover .note-body{
    //    color: $dark-blue; 
    // }
    // .note-container:hover .note-date{
    //    color: $dark-blue; 
    // }
    .note-container {
        transition: .3s;
        display: flex;
        flex-direction: column;
        min-height: 130px;
        justify-content: space-between;
        border-bottom: solid $dark-blue;
        .note-header{
            display: flex;
            padding: 0.5rem;
            // justify-content: center;
            align-items: center;
            .note-type {
                border: solid $dull-red;
                font-weight: bold;
                padding: 0 0.5rem;
                margin-right: 0.5rem;
                color: $dull-red;
                width: 120px;
            }
            .note-date{
                transition: .3s;
            }
        }
        .note-title {
            font-weight: bold;
            font-size:1.3rem;
            text-decoration: underline;
            color: darkgray;
        }
        .note-body {
            margin-bottom: 0.4rem;
            transition: .3s;
        }
        .note-next-container {
            width: 100%;
            .note-next {
                text-align: right;
                margin-right: 1rem;
                margin-top: 1rem;
                margin-bottom: 0.5rem;
                color: rgb(47, 218, 152);
                cursor: pointer;
                transition: .3s;
            }
            .note-next:hover {
                color: rgb(53, 242, 169);
            }
        }
    }
}
.more-read{
    margin-right: 0.5rem;
    margin-top: 0.8rem;
    margin-bottom: 0.8rem;
    border: solid $base-white;
    padding: 0.5rem;
    border-radius: 2rem;
    display: inline-block;
    cursor: pointer;
    transition: .3s;
}
.more-read:hover {
    // color: darkgray;
    // border: solid darkgray;
    background: rgba($color: $back-white, $alpha: 0.1)
}

@media(max-width: 520px){
    .hero-image{
        width: auto;
        height: auto;
    }
    .fa-comments{
        font-size: 16rem;
        color: rgba($color: #a6a6a6, $alpha: 0.6);
    }
    .fa-gamepad{
        font-size: 6rem;
        color: rgba($color: #a6a6a6, $alpha: 0.6);
    }
    img{
        width: 60%;
    }

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
	// 60% {
	// 	transform: translateX(-10%);
	// }
	// 75% {
	// 	transform: translateX(2%);
	// }
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
	// 60% {
	// 	transform: translateX(-10%);
	// }
	// 75% {
	// 	transform: translateX(2%);
	// }
	100% {
		opacity: 0;
		transform: translateX(-20%);
        display: none;
	}
}
</style>
