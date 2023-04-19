<template>
    <div  class="board-account-wrapper scroll_area" >
        <div class="main-wrapper">
            <div v-if="$store.state.isLoading===false&&allReady" class='main-container'>
                <div v-if="onNotification.show" :class="{'notification-blue':onNotification.show}">
                    <div class="notification-text" v-if="onNotification.onAnswer">
                        新しい回答があります。
                    </div>
                    <div class="notification-text" v-if="onNotification.onReply">
                        新しい返信があります。
                    </div>
                    <div class="notification-text" v-if="onNotification.onBest">
                        あなたの回答がベストアンサーに選ばれました。
                    </div>
                </div>
                <h1 class='title-white'>質問板</h1>
                <div class="user-info">
                    <div class="header">
                        <img class='img' v-bind:src="user.sns_thumbnail?user.sns_thumbnail:user.thumbnail"/>
                        <div class="board-account-content">
                            <p class="board-account-user-name">{{ user.username}}</p>
                             <div class="each-container">
                                <div class="each-title">質問数</div>
                                <div class="space">:</div>
                                <div class="num">{{ userQuestion.count }}</div>
                            </div>
                            <div class="each-container">
                                <div class="each-title">回答数</div>
                                <div class="space">:</div>
                                <div class="num">{{ answeredNum }}</div>
                            </div>
                            <div class="each-container">
                                <div class="each-title">ベストアンサー数</div>
                                <div class="space">:</div>
                                <div class="num">{{ bestAnswerNum }}</div>
                            </div>
                            <div class='line'></div>
                            <div class="tag-container">
                                <div class="tag-text">関連するタグ</div>
                                <div class="tag-wrapper">
                                    <div v-if="!getThreeUsertag">
                                        <p>現在表示できるタグはありません。</p>
                                    </div>
                                    <div 
                                        @click="handleTag(questionindex,tag.tag.id,'tag')"
                                        class="tag"
                                        :class="{'animation-tag':active==questionindex}" 
                                        v-for="(tag,questionindex) in getThreeUsertag"
                                        v-bind:key="questionindex"
                                        >
                                        {{ tag.tag.tag }}
                                    </div>
                                    
                                </div>
                            </div>
                        </div>
                    </div>   
                </div>
                
                <div class="nav-ber" v-if="tag==false">
                    <div :class="{'selected': showQuestion.questionType.question}" @click="handleQuestionType('question')">質問</div>
                    <div :class="{'selected': showQuestion.questionType.answered}" @click="handleQuestionType('answered')">回答</div>
                    <div :class="{'selected': showQuestion.questionType.reccomend}" @click="handleQuestionType('reccomend')">おすすめ</div>
                    <div :class="{'selected': showQuestion.questionType.favorite}" @click="handleQuestionType('favorite')">お気に入り</div>
                </div>
                <div class="selecter">
                    <div :class="{'option-selected': showQuestion.questionStatus.all}" @click="handleQuestionStatus('all')" class="select-item">ALL</div>
                    <div :class="{'option-selected': showQuestion.questionStatus.solved}" @click="handleQuestionStatus('solved')" class="select-item">解決</div>
                    <div :class="{'option-selected': showQuestion.questionStatus.unsolved}" @click="handleQuestionStatus('unsolved')" class="select-item">未解決</div>
                    <!-- <div :class="{'option-selected': showQuestion.questionStatus.onVoting}" @click="handleQuestionStatus('onVoting')" class="select-item">投票中</div> -->
                    <div v-if="showQuestion.questionType.answered" :class="{'option-selected': showQuestion.questionStatus.best}" @click="handleQuestionStatus('best')" class="select-item">ベスト</div>
                </div>
                <div v-if="spinner" class="is-loading-bar has-text-centered middle-loading" v-bind:class="{'is-loading': spinner }">
                    <div class="lds-dual-ring"></div>
                </div>
            <div class="no-question" v-if="!handleQuestion[0]&&tag==false&&!spinner">
                <div v-if="showQuestion.questionType.question">
                    <p>表示できる質問はありません。</p>
                    <p v-if="showQuestion.questionStatus.all">質問をするとここに表示されます。</p>
                </div>
                <div v-if="showQuestion.questionType.answered">
                    <p>表示できる質問はありません。</p>
                    <p v-if="showQuestion.questionStatus.all">質問に回答するとここに表示されます。</p>
                </div>
                 <div v-if="showQuestion.questionType.reccomend">
                    <p>表示できる質問はありません。</p>
                </div>
                <div v-if="showQuestion.questionType.favorite">
                    <p>表示できる質問はありません。</p>
                    <p v-if="showQuestion.questionStatus.all">お気に入りに登録するとここに表示されます。</p>
                </div>
            </div>
            <!-- <div class="question-list-wrapper">
                <AbstractQuestionList
                :questions="setQuestionsForAbstractQuestionList"/>
            </div> -->
                <div
                    class='question-container'
                    v-for="(question,questionindex) in handleQuestion"
                    v-bind:key="questionindex">
                    
                    <div class='question-list' v-if="spinner==false" @click="getDetail(question.slug)">
                        <div class="tag-wrapper">
                            <div 
                                class="tag"
                                v-for="(tag,tagindex) in question.tag" 
                                v-bind:key="tagindex">{{ tag.tag }}
                            </div>
                            <div v-if="checkExist(question,'answer')" class="on-answer-wrapper">
                                <div class="on-answer" v-if="handleOnAnswer(question)||handleOnReply2(question)">
                                        <div class="on-answer-container" v-if="handleOnAnswer(question)">
                                            <span class="span1"> NEW</span><span class="span2">ANSWER</span>
                                        </div>
                                        <div class="on-answer-container" v-if="handleOnReply2(question)">
                                            <span class="span1"> NEW</span><span class="span2">Reply</span>
                                        </div>
                                </div>
                                <div class="on-answer" v-if="onReplyCheck(question.answer)||onBestCheck(question.answer)">
                                    <div class="on-answer-container" v-if="onReplyCheck(question.answer)">
                                        <span class="span1"> NEW</span><span class="span2">REPLY</span>
                                    </div>
                                    <div class="on-answer-container" v-if="onBestCheck(question.answer)">
                                        <span class="span1"> NEW</span><span class="span2">BEST</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="question-title">{{ question.title }}</div>
                        <div class="question-description" v-if="question.description">{{ question.description.substr(0,10)+'...' }}</div>
                        <div class='good-like-wrapper'>
                            <i class="far fa-heart"></i>
                            <div class="good" v-if="question">{{ viewedNum(question.liked_num) }}</div>
                            <i class="far fa-comment"></i>
                            <div>{{ question.answer.length }}</div>
                            <div class="date">作成日：{{ dateConvert(question.created_on) }}</div>
                        </div>
                    </div>   
                </div>
                <div v-if="questions.next&&scrollBottom" class="question-list-dammy shine">
                    <div class="tag-wrapper-dammy">
                        <div class="tag-dammy"></div>
                    </div>
                    <div class="question-title-dammy"></div>
                    <div class="questiondescroption-dammy"></div>
                    <div class="footer-dammy"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {router} from "/src/main.js"
import axios from 'axios'
import AbstractQuestionList from "@/components/board/AbstractQuestionList.vue";
export default {
    components:{
        AbstractQuestionList
    },
    data(){
        return{
            allReady:false,
            questions:'',
            reccomendedQuestion:'',
            favoriteQuestion:'',
            answeredQuestion:'',
            bestansweredQuestion:'',
            userQuestion:'',
            bestAnswerNum:0,
            answeredNum:0,
            tagQuestion:'',
            bottomScrollActionHandler: true,
            scrollBottom: false,
            tag:false,
            active: null,
            spinner:false,
            showOnes:false,
            onNotification:{
                onReply:false,
                onAnswer:false,
                onBest:false,
                show: false
            },
            showNotifications: false,
            temporaryStatus:'',
            showQuestion:{
                questionType:{
                    question: true,
                    answered: false,
                    reccomend: false,
                    favorite: false,
                    tag:false,

                },
                questionStatus:{
                    all: true,
                    solved: false,
                    unsolved: false,
                    onVoting: false,
                    best: false,
                }
            },
            tagQuestionStored:[]
        }
    },
    watch:{
        showOnes:function(v) {if (v == true){
            this.setTime()
        }}
    },
    computed:{
        user(){
            return this.$store.state.signup.user
        },
        userTags() {
            return this.$store.state.board.userTags
        },
        // favoriteQuestion() {
        //     return this.$store.state.signup.userFavoriteQuestions
        // },
        getThreeUsertag(){
            const _ = require('lodash');
            const used_num_list = []
            const userTag = _.cloneDeep(this.userTags)
            userTag.forEach((e) => {
                const obj = {
                    'tagName':e.tag.tag,
                    'tagId':e.tag.id,
                    'questions':''
                }
                this.tagQuestionStored.push(obj)
            }) 
            if(userTag){
                if(userTag.length == 1){
                    return userTag
                }
                else if(userTag.length == 2){
                    used_num_list.push(userTag.reduce((a,b)=>a.used_num>b.used_num?a:b))
                    used_num_list.push(userTag.reduce((a,b)=>a.used_num<b.used_num?a:b))
                    if(used_num_list[0].id == used_num_list[1].id){
                        return userTag
                    }
                    else{
                        return used_num_list
                    }
                }
                else if(userTag.length >= 3){
                    while (used_num_list.length < 3){
                        used_num_list.push(userTag.reduce((a,b)=>a.used_num>b.used_num?a:b))
                        Object.values(userTag).forEach(value =>{
                            if(value.id == used_num_list.slice(-1)[0].id)                   
                                delete userTag[userTag.indexOf(value)]
                        })
                    }
                    return used_num_list
                }
            }else{
                
            }
        },
        getAnsweredQuestion(){
            return this.$store.getters.gettersAnsweredQuestions
        },
        handleQuestion(){
            const handledQuestion= []
            if(this.showQuestion.questionType.question){
                try{
                    this.questions = this.userQuestion
                    return this.handleStatus(this.HandleQuestionOnanswerOrder(this.questions.results))
                }catch{
                }
            }
            else if(this.showQuestion.questionType.answered){
                const answeredquiz = []
                this.questions = this.getAnsweredQuestion
                if(this.showQuestion.questionStatus.best){
                    Object.values(this.questions.results).forEach(value =>{
                        for(let answer of value.answer){
                            if(answer.best==true&&answer.user.UID===this.user.UID){
                                answeredquiz.push(value)
                            }
                        }
                    })
                    return answeredquiz
                }
                else{
                    var answeredquiz2 = []
                    Object.values(this.questions.results).forEach(value =>{
                        if(value.answer[0].on_reply==true&&value.answer[0].user.UID==this.user.UID){
                            answeredquiz.push(value)
                        }else{
                            answeredquiz2.push(value)
                        }
                    })
                    if(answeredquiz){
                        for(let i of answeredquiz2){
                            answeredquiz.push(i)
                        }
                        return this.handleStatus(answeredquiz)
                    }
                    return this.handleStatus(this.getAnsweredQuestion.results)   
                }
            }else if(this.showQuestion.questionType.reccomend){
                this.questions = this.reccomendedQuestion
                return this.handleStatus(this.questions.results)
            }else if(this.showQuestion.questionType.favorite){
                if(this.favoriteQuestion){
                     this.questions = this.favoriteQuestion
                    return this.handleStatus(this.questions.results)
                }else{
                    this.questions = ''
                    return this.handleStatus(this.questions)
                }
            }else if(this.showQuestion.questionType.tag){
                this.questions = this.tagQuestion
                return this.handleStatus(this.questions.results)
            }
            
        },
        setQuestionsForAbstractQuestionList() {
            const questionObj = {
                results: this.handleQuestion,
                showOnNote: true,
            };
            return questionObj;
        },
    },
    created(){
        this.getUserQuestion()
    },
    async beforeMount(){
        this.scrollTop()
        this.bestAnswerCalculation()
        this.handleOnReply()
        this.allReady=true
    },
    mounted(){
        window.addEventListener('scroll', this.handleScroll)
        window.addEventListener('scroll', this.getScrollY)
        this.bottomScrollActionHandler = true
        this.scrollBottom = false
    },
    beforeUnmount(){
        window.removeEventListener('scroll', this.handleScroll)
        window.removeEventListener('scroll', this.getScrollY)
    },
    methods:{
        bestAnswerCalculation() {
            const answeredquiz = []
            const questions = this.getAnsweredQuestion.results
            this.answeredNum = this.getAnsweredQuestion.count
            Object.values(questions).forEach(value =>{
                for(let answer of value.answer){
                    if(answer.best==true&&answer.user.UID==this.user.UID){
                        answeredquiz.push(value)
                    }
                }
            })
            this.bestAnswerNum = answeredquiz.length
        },
        getDetail(slug){
            router.push(`/board-detail/${slug}` )
        },
        async getAdditionalQuestion(next){
            if(next!=null){
                await axios
                .get(next)
                .then(response => {
                    for(let i of response.data.results){
                        const eachQuestion = this.showQuestion.questionType.favorite?i.question:i
                        this.questions.results.push(eachQuestion)
                    }
                    console.log(this.questions.results)
                    this.questions.next= response.data.next
                    this.bottomScrollActionHandler = true
                    if(this.questions.next==null){
                        this.bottomScrollActionHandler = false
                        this.scrollBottom = false
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            }
        },
        async getUserQuestion(){
            this.$store.commit('setIsLoading', true)
            await axios
                .get(`/api/board/question-user-question?uid=${this.user.UID}`)
                .then(response => {
                    this.userQuestion = response.data
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        },
        async getTagQuestion(tagID, tag){
            this.spinner = true
            await axios
                .get(`/api/board/tag-question?tag=${tagID}`)
                .then(response => {
                    this.tagQuestionStored.forEach((e) => {
                        if(e.tagId === tagID) {
                            e['questions'] = response.data
                        }
                    })
                    this.tagQuestion = response.data
                    this.handleQuestionType(tag)
                })
                .catch(error => {
                    console.log(error)
                })
            this.spinner = false
        },
        handleStatus(question){
            const handledQuestion= []
            if(this.showQuestion.questionStatus.all||this.showQuestion.questionStatus.best){
                    return question
                }
                else if(this.showQuestion.questionStatus.solved){
                    for(let i of question){
                        if(i.solved){
                            handledQuestion.push(i)
                        }
                    }
                    return handledQuestion
                }else if(this.showQuestion.questionStatus.unsolved){
                    for(let i of question){
                        if(i.solved==false){
                            handledQuestion.push(i)
                        }
                    }
                    return handledQuestion
                }else if(this.showQuestion.questionStatus.onVoting){
                    for(let i of question){
                        if(i.vote_on_going==true){
                            handledQuestion.push(i)
                        }
                    }
                    return handledQuestion
                } 
        },
        HandleQuestionOnanswerOrder(question){
            const questionList = []
            var questionList2 = []
            for(let i of question){
                if(i.on_answer==true){
                    questionList.push(i)
                }else{
                    questionList2.push(i)
                }
            }
            if(questionList){
                for(let o of questionList2){
                    questionList.push(o)
                }
                return questionList
            }
            return question

        },
        handleQuestionStatus(status){
            // handle questionStatus start from here by click.
            // change all status = false then invocation = true
            // then handleQuestion on computed will be triggered
            // which make question from answer to return question to handleStatus
            if(this.showQuestion.questionStatus[status]){
            }
            else{
                Object.keys(this.showQuestion.questionStatus).forEach(key =>{
                    this.showQuestion.questionStatus[key] = false
                })
                this.showQuestion.questionStatus[status] = true
                this.scrollTop()
            }
        },
        async handleQuestionType(type){
            this.bottomScrollActionHandler = true
            if(this.showQuestion.questionType[type]){
                ;
            }
            else{
                Object.keys(this.showQuestion.questionType).forEach(key =>{
                    this.showQuestion.questionType[key] = false
                })
                this.showQuestion.questionType[type] = true
                if(type==='reccomend'&&!this.reccomendedQuestion) {
                    this.spinner = true
                    await this.$store.dispatch('getRelatedQuestion')
                    this.reccomendedQuestion = this.$store.state.board.reccomendedQuestion
                    this.spinner = false
                }
                if(type==='favorite') {
                    if(!this.favoriteQuestion) {
                        this.spinner = true
                        await this.$store.dispatch("getUserFavoriteQuestions")
                        this.favoriteQuestion = this.$store.state.signup.userFavoriteQuestions
                        this.spinner = false
                    }
                }
                this.scrollTop()
                if(this.showQuestion.questionStatus.best==true){
                    this.showQuestion.questionStatus.best==false
                    this.handleQuestionStatus('all')
                }
            }
        },
        resetNotifications(){
            this.onNotification.show = false
        },
        setTime(){
            if(this.onNotification.onReply||this.onNotification.onAnswer||this.onNotification.onBest){
                this.onNotification.show = true
                setTimeout(this.resetNotifications, 4500) 
            }
        },
        handleOnReply(){
            try{
                for(let question of this.getAnsweredQuestion.results){
                    for(let answer of question.answer){
                        if(answer.on_reply==true&&answer.user.UID==this.user.UID){
                            this.onNotification.onReply = true
                            this.showOnes = true
                        }
                        if(answer.on_best==true&&answer.user.UID==this.user.UID){
                            this.onNotification.onBest = true
                            this.showOnes = true
                        }
                    }
                }
            }
            catch{

            }
        },
        handleOnAnswer(question){
            if(question.on_answer&&question.user.UID==this.user.UID){
                this.onNotification.onAnswer = true
                this.showOnes = true
                return true      
            }else{
                return false
            }
        },
        handleOnReply2(question){
            if(question.on_reply&&question.user.UID==this.user.UID){
                this.onNotification.onReply = true
                this.showOnes = true
                return true      
            }else{
                return false
            }
        },
        onReplyCheck(questionAnswer){
            for(let answer of questionAnswer){
                if(answer.on_reply==true){
                    if(answer.user.UID==this.user.UID){
                        this.showOnes = true
                    return true
                    }
                }
            }
            return false
        },
        onBestCheck(questionAnswer){
            for(let answer of questionAnswer){
                if(answer.on_best==true){
                    if(answer.user.UID==this.user.UID){
                        this.showOnes = true
                    return true
                    }
                }
            }
            return false
        },
        scrollTop(){
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        },
        getScrollY(){
            this.scrollY = window.scrollY
        },
        handleScroll(){
            var doch = document.querySelector('.scroll_area').scrollHeight
            var winh = window.innerHeight; //ウィンドウの高さ
            var bottom = doch - winh; //ページ全体の高さ - ウィンドウの高さ = ページの最下部位置
            if (bottom+100 <= this.scrollY&&this.bottomScrollActionHandler) {
                this.bottomScrollActionHandler = false
                this.scrollBottom = true
                this.getAdditionalQuestion(this.questions.next)
            }
        },
        handleTag(indexNum, tagID, tag){
            this.tag = !this.tag
            if(this.showQuestion.questionType.tag == false){
                for(let i of Object.keys(this.showQuestion.questionType)){
                    if(this.showQuestion.questionType[i]==true){
                        this.temporaryStatus = i
                    }
                }
            }
            if(this.active == indexNum){
                this.active = null
                this.tag = false
                this.showQuestion.questionType.tag = false
                this.handleQuestionType(this.temporaryStatus)
            }else{
                this.active = indexNum
                this.tag = true
                if(this.tagQuestionStored.find((e => e.tagId ===tagID&&e.questions))) {
                    this.tagQuestionStored.forEach((e) => {
                        if(e.tagId===tagID) {
                            this.tagQuestion = e.questions
                            this.handleQuestionType(tag)
                        }
                    })
                } else {
                    this.getTagQuestion(tagID, tag)
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
        viewedNum(likedNum){
            try{
                if(likedNum){
                    return likedNum[0].liked_num
                }
                else{
                    return 0
                }
            }
            catch{
                return 0
            }
        },
        countBestanswers(answers) {
            let count = 0
            answers.forEach((answer) => {
                count += answer.best ? 1 : 0  
            })
            return count
        },
        checkExist(obj, key) {
            if(typeof obj[key] !== 'undefined') {
                return true
            } else {
                return false
            }
        }
    }
}
</script>

<style lang='scss' scoped>
@import "style/_variables.scss";
.question-list-wrapper{
    width: 90%;
}
.animation-tag{
    color: white;
    background: $dark-blue;
    animation-name: tag;
    animation-timing-function:linear;
    animation-duration:1s;
    animation-iteration-count:1;
    animation:tag  forwards;
}
@keyframes tag {
  from   { opacity: 1;
        } 
  100% { 
      color:white;
      background: $dark-blue;
      border: 0.1rem solid $base-color;
      
  }
}

.board-account-wrapper{
    display: flex;
    height: auto;
    min-height: 80vh;
    width: 100vw;
    margin-bottom: 1rem;
    flex-direction: column;
    align-items: center;
}
.main-container{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    .notification-blue{
        display: flex;
        display: flex;
        flex-direction: column;
        .notification-text{
            margin-top: 1rem;
        }
    }
    
    .user-info{
        width: 90%;
        height: 350px;
        .header{
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            .img{
                border: solid $dark-blue;
                border-radius: 50%; 
                width:  5rem;   
                height: 5rem;
                margin: 0.5rem;
                z-index: 1;
            }
        }
        .board-account-content{
            position: absolute ;
            width: 100%;
            top: 50%;
            border: solid $base-color;
            border-radius: 0.5rem;
            background: $back-lite-white;
            padding:1rem;
            padding-top: 2.7rem;
            .board-account-user-name {
                font-family: 'Gill Sans', bold;
                font-size: 1.7rem;
            }
        }
    }
    .tag-container{
        .tag-text{
            font-size: 1.2rem;
            font-weight: bold;
            margin: 0.5rem;
        }
        .tag-wrapper{
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
            .tag{
                border: solid $dark-blue;
                border-radius: 50vh;
                background: $base-lite-2;
                margin-top: 0.5rem;
                margin-left: 0.5rem;
                margin-right: 0.5rem;
                margin-bottom: 0.5rem;
                padding: 0.5rem;
                min-width: 5rem;
                font-size: 1rem;
                font-weight: bold;
                color:$dark-blue;
                transition: 0.5s;
            }
            .tag:hover{
                color: gray
            }
        }
        p{
            text-align: right;
        }
    }
    .nav-ber{
        width:100%;
        display: flex;
        justify-content: center;
        margin-top: 1rem;
        div{
            font-size:0.8rem;
            color: white;
            border:0.1rem solid white;
            position:flex;
            flex-direction: column;
            flex-basis:20%;
            padding-left:0.1rem;
            padding-right:0.1rem;
            padding: 0.2rem;
            background: linear-gradient(rgba(91, 117, 159, 0.9),rgba(28, 37, 76, 0.9));
            transition:0.5s;
        }
        div:hover{
            font-weight: bold;
        }
        .selected{
            background: $base-color;
            font-weight: bold;
            color: black;
        }
    }
    .selecter{
        width:100%;
        display: flex;
        justify-content: center;
        margin-top: 1rem;
        transition: 0.5s;
        .select-item{
            font-size:0.8rem;
            color: white;
            border:0.1rem solid $base-color;
            border-radius: 1rem;
            margin:0.3rem;
            min-width: 3rem;
            position:flex;
            padding-left:0.1rem;
            padding-right:0.1rem;
            padding: 0.2rem;
            transition:0.5s;
        }
        .select-item:hover{
            font-weight: bold;
        }
        .option-selected{
            color: black;
            font-weight: bold;
            background: $base-lite;
            border:0.1rem solid $dark-blue;
        }
    }
    .middle-loading{
        margin-top: 2rem;
    }
    .question-container{
        width: 90%;
        .question-list:hover{
            background: $base-lite-3;
        }
        .question-list{
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
                .on-answer-wrapper{
                    position:relative;
                    width:100%;
                    .on-answer{
                        position: absolute;
                        right: 0;
                        flex-direction: column;
                        width:3.7rem;
                        margin-top: 0.5rem;
                        margin-right: 0.3rem;
                        padding-right:0.2rem;
                        padding-left:0.2rem; 
                        .on-answer-container{
                            display: flex;
                            flex-direction: column;
                            color: red;
                            border: solid red;
                            border-radius: 0.5rem;
                            margin-bottom: 0.3rem;     
                        }
                        .span1{
                            font-weight: bold;
                        }
                        .span2{
                            margin-top: -0.5rem;
                            font-size: 0.6rem;
                            font-weight: bold;             
                        }
                    }
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
    .question-list-dammy{
        background: gray;
        display: flex;
        width: 90%;
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
}
.no-question{
    border: solid $dull-red;
    background: $back-gra-white;
    width: 80%;
    padding: 1rem 0;
    font-weight: bold;
}
.each-container {
    // display: inline;
    text-align: left;
    .each-title {
        font-weight: bold;
    }
    .space {
        padding: 0 0.2rem;
        font-weight: bold;
    }
    .num {
        font-weight: bold;
        color: $middle-blue;
    }
    div{
        display: inline
    };
}
.line {
    border: solid $base-white;
    margin: 1rem 0;
}

</style>