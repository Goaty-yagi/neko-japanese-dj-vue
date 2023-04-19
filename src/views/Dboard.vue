<template>
    <div class="dashboard-wrapper" :class="{'scroll-fixed':$store.state.fixedScroll,}">
        <div class="">
            <div class="dashboard-container" v-if="$store.state.isLoading==false">
                <div class="header-flex">
                    <h1 class='title-white'>ダッシュボード
                        <i @click="handleShowSideBar()" 
                        class="fas fa-align-justify" :class="{'less-bar':showSideBar==false}"></i>
                    </h1>
                    <h2 class="current-option">
                        {{ currentOption }}
                    </h2>
                </div>
                <div class="side-bar" :class="{'less-side-bar':showSideBar==false}">
                    <div class='space'></div>
                    <div class="option-loop" v-for="(val, key, index) in options"
                        :key="index">
                        <div v-if="showSideBar" class="each-option" :class="{'select-option':selectOption(key)}" @click="handleEachPage(key)">
                            {{ key }}   
                        </div>       
                    </div>
                </div>
            </div>
        </div>
        <CreateQuizQuestion
        v-if="options.createQuiz"/>
        <CreateNotification
        v-if="options.notification"/>
        <QuizInfo
        v-if="options.quizInfo"/>
        <Logger
        v-if="options.logger"/>
        <Enquire
        v-if="options.enquire"/>
    </div>
</template>

<script>
import CreateQuizQuestion from '@/components/dashboard/CreateQuizQuestion.vue'
import CreateNotification from '@/components/dashboard/CreateNotification.vue'
import QuizInfo from '@/components/dashboard/QuizInfo.vue'
import Logger from '@/components/dashboard/Logger.vue'
import Enquire from '@/components/dashboard/Enquire.vue'

export default {
    components: {
        CreateQuizQuestion,
        CreateNotification,
        QuizInfo,
        Logger,
        Enquire 
    },
    data(){
        return{
            showSideBar: true,
            currentOption:'quizInfo',
            // fixedScroll: this.$store.state.fixedScroll,
            options:{
                'quizInfo':true,
                'notification': false,
                'createQuiz':false,
                'logger': false,
                'enquire': false
                }
                
        }
    },
    beforeMount() {
        this.$store.commit('setIsLoading', false)
    },
    mounted(){
    },
    conoputed:{
    },
    methods:{
        handleShowSideBar(){
            this.showSideBar = !this.showSideBar 
        },
        handleEachPage(key) {
            if(this.options[key] == false){
                this.options[key] = true
                this.options[this.currentOption] = false
                this.currentOption = key
            }
        },
        selectOption(key){
            if(this.currentOption == key){
                return true
            } else {
                return false
            }
        },
        
    }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.dashboard-wrapper{
    
    width: 100%;
    margin: 0;
    .side-bar{
        position: fixed;
        left: 0;
        bottom: 0;
        margin-top: 1rem;
        background: $dark-tr-blue;
        width: 200px;
        height: 100%;
        transition: .5s;
        z-index: 1;
        .space {
            height: 150px;
        }
        .option-loop{
            color: white;
            .each-option{
                padding: 1.3rem 0;
                transition: .5s;
                font-weight: bold;
            }
            .each-option:hover {
                background: $lite-gray;
                color: $lite-blue;
            }
            .select-option{
                background: $lite-gray;
                transition: .5s;
                color: $dark-blue;
            }
        }
    }
    .less-side-bar{
        width: 0px;
    }
    .dashboard-container{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0;
        width: 100%;
        .header-flex{
            width: 60%;
            display: flex;
            flex-direction: column;
            align-items: center;
            .title-white{
                position: relative;
                .fa-align-justify{
                    position: absolute;
                    left:-3rem;
                    top: 0;
                    display: inline-block;
                    color: $lite-gray;
                    margin-top: 0.7rem;
                    margin-right: 0.5rem;
                    transition: .5s;
                    z-index: 2;
                }
                .fa-align-justify.less-bar{
                    transition: .5s;

                    transform: rotate(180deg);
                }
            }
            .current-option{
                margin-top: 0.5rem;
                font-size: 1.2rem;
                font-weight: bold;
                color: white;
                border: solid $lite-gray;
                padding: 0 1rem;
            }
        }
    }
} 
</style>