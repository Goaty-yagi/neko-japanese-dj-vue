<template>
  <div>
    <div :class="[styleType==='simple'?'simple-wrapper':'default-wrapper']"
    v-for="(question,questionindex) in questions.results"
    v-bind:key="questionindex"
    >
        <div class='question-list' @click="getDetailHandler(question.slug)">
            
            <div 
            class="tag-wrapper">
                <div 
                class="tag"
                v-for="(tag,tagindex) in question.tag" 
                v-bind:key="tagindex">{{ tag.tag }}
                </div>
            </div>
            <div v-if="!notShowSolved" class="solved-container">
                <div v-if="question.solved">
                    解決済み
                </div>
                <div v-if="!question.solved">
                    回答受付中
                </div>
            </div>
            <div class="question-title">{{ question.title }}</div>
            <div class="question-description">{{ question.description.substr(0,10)+'...' }}</div>
            <div class='good-like-wrapper'>
                <i class="far fa-heart"></i>
                <div class="good" v-if="question.liked_num[0]">{{ question.liked_num[0].liked_num }}</div>
                <i class="far fa-comment"></i>
                <div>{{ question.answer.length }}</div>
                <div class="date">作成日：{{ dateConvert(question.created_on) }}</div>
            </div>
        </div>        
    </div>
    <div v-if="scrollBottom&&questions.next" class="question-list-dammy shine">
        <div class="tag-wrapper-dammy">
            <div class="tag-dammy"></div>
        </div>
        <div class="question-title-dammy"></div>
        <div class="questiondescroption-dammy"></div>
        <div class="footer-dammy"></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import {router} from "@/main.js"
export default {
    props:[
        'questions',
    ],
    data() {
        return {
            scrollY: 0,
            scrollHeight:'',
            scrollBottom: false, 
            bottomScrollActionHandler:true,
        }
    },
    mounted() {
        this.$emit("parent", this.bottomScrollActionHandlerTrue);
        window.addEventListener('scroll', this.getScrollY)
        window.addEventListener('scroll', this.handleScroll)
        this.bottomScrollActionHandler = true
        this.scrollBottom = false

    },
    beforeUnmount(){
        window.removeEventListener('scroll', this.handleScroll)
        window.removeEventListener('scroll', this.getScrollY)
    },
    computed:{
        styleType() {
            return this.questions.styleType==='simple'?'simple':''
        },
        notShowSolved() {
            return this.questions.notShowSolved?true:false
        }
     },
    methods:{
        async getAdditionalQuestion(next){
            console.log("ADD", next)
            if(next!=null) {
                await axios
                .get(next)
                .then(response => {
                    console.log("res",response.data)
                    for(let i of response.data.results){
                        this.questions.results.push(i)
                    }
                    this.questions.next = response.data.next
                    this.bottomScrollActionHandler = true
                    console.log("NEXT",this.questions.next)
                    if(this.questions.next==null){
                         console.log("NEXT_NULL",this.questions.next)
                        this.bottomScrollActionHandler = false
                        this.scrollBottom = false
                    }
                })
                .catch(e => {
                    let logger = {
                    message: "in Community/getAdditionalQuestion. couldn't get EdditionalQuestion",
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,
                    }
                    this.$store.commit('setLogger',logger)
                    this.$store.commit('setIsLoading', false)
                    router.push({ name: 'ConnectionError' })
                })
            }
        },
        getDetail(slug){
            router.push(`/board-detail/${slug}` )
        },
        getDetailHandler(slug) {
            'getDetail' in this.questions?this.questions.getDetail(slug):this.getDetail(slug)
        },
        getScrollY(){
            this.scrollY = window.scrollY
        },
        handleScroll(){
            if(document.querySelector('.scroll_area')){
                const doch = document.querySelector('.scroll_area').scrollHeight // .scroll_area is from parent the most out class name
                const winh = window.innerHeight; //ウィンドウの高さ
                const bottom = doch - winh; //ページ全体の高さ - ウィンドウの高さ = ページの最下部位置
                if (bottom+150 <= this.scrollY&&this.bottomScrollActionHandler) {
                    this.bottomScrollActionHandler = false
                    this.scrollBottom = true
                    this.getAdditionalQuestion(this.questions.next)
                    if(!this.questions.next){
                        this.scrollBottom = false
                    }
                }
            }
        },
        dateConvert(date){
            const dateObj = new Date()
            const offset = dateObj.getTimezoneOffset()
            let dt = new Date(date)
            const localTime = dt.setMinutes(offset*-1 + dt.getMinutes())
            
            dt = new Date(localTime)
            const stringDT = dt.toLocaleString([], {year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit'})
            return stringDT.replace(/\//g,'-')
        },
        bottomScrollActionHandlerTrue() {
            // this is for parent
            this.bottomScrollActionHandler = true
        }
    }
}
</script>

<style lang='scss' scoped>
@import "style/_variables.scss";
.default-wrapper {
    .question-list:hover{
        background: $base-lite-3;
    }
    .question-list{
        position: relative;
        border: solid $base-color;
        margin-bottom: 0.5rem;
        width:100%;
        background: rgb(252, 252, 252);
        display: flex;
        flex-direction: column;
        .tag-wrapper{
            display: flex;
            width: 100%;
            .tag{
                border: solid black;
                border-radius: 50vh;
                background: rgb(230, 230, 230);
                margin-top: 0.5rem;
                margin-left: 0.3rem;
                margin-bottom: 0.5rem;
                padding: 0.5rem;
                min-width: 3rem;
            }
        }
        .good-like-wrapper{
            display: flex;
            .fa-heart{
                color: rgb(221, 36, 221);
                margin-left: 0.5rem;
                margin-right: 0.3rem;
                margin-top: 0.2rem;
            }
            .fa-comment {
                color: $lite-blue;
                margin-left: 0.5rem;
                margin-right: 0.3rem;
                margin-top: 0.2rem;
            }
            .date{
                margin-left: 0.5rem;
            }
        }
    }
}
.solved-container {
    position: absolute;
    right: 0.5rem;
    top: 0.5rem;
    border: solid $dull-red;
    color: $dull-red;
    padding: 0 0.2rem;
}
.question-list-dammy{
    background: gray;
    display: flex;
    width: 100%;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    .tag-wrapper-dammy{
        display: flex;
        width: 100%;
        .tag-dammy{
            border-radius: 50vh;
            background: rgb(92, 92, 92);
            margin-top: 0.5rem;
            margin-left: 0.3rem;
            margin-bottom: 0.5rem;
            padding: 0.5rem;
            min-width: 3rem;
            min-height: 1.5rem;
        }
    }
    .question-title-dammy{
        background: rgb(92, 92, 92);
        padding: 0.5rem;
        width: 80%;
    }
    .questiondescroption-dammy{
        background: rgb(92, 92, 92);
        padding: 0.5rem;
        width: 80%;
        margin-top: 0.5rem;
    }
    .footer-dammy{
        background: rgb(92, 92, 92);
        padding: 0.5rem;
        width: 80%;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
}
.simple-wrapper {
    .question-list{
        position: relative;
        border-bottom: solid rgb(236, 234, 234);
        margin-bottom: 0.5rem;
        width:100%;
        padding: 0.2rem;
        display: flex;
        flex-direction: column;
        .tag-wrapper{
            display: flex;
            width: 100%;
            .tag{
                border: solid rgb(230, 230, 230);
                margin-left: 0.3rem;
                min-width: 2rem;
            }
        }
        .good-like-wrapper{
            display: flex;
            font-size: 0.7rem;
            .fa-heart{
                margin-left: 0.5rem;
                margin-right: 0.3rem;
                margin-top: 0.2rem;
            }
            .fa-comment {
                color: $lite-blue;
                margin-left: 0.5rem;
                margin-right: 0.3rem;
                margin-top: 0.2rem;
            }
            .date{
                margin-left: 0.5rem;
            }
        }
    }
}
</style>