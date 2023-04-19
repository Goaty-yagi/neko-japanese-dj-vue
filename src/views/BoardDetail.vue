<template>
<!-- this scroll fixed should be change -->
    <div ref='test' class="board-detail-wrapper" v-if="renderingCheck&&!$store.state.isLoading">
        <div class="main-wrapper">
            <div class="question-wrapper">
                <p class='title-white'>質問板</p>
                    <div v-if="notifications.reply||notifications.answer||notifications.post||notifications.others" :class="[!$store.state.board.notifications.error?'notification-blue':'notification-red']">
                        <div v-if="notifications.reply" class="notification-text">
                            {{ !$store.state.board.notifications.error?'返信しました。':'返信できませんでした。しばらく経ってからもう一度お試しください。' }}
                        </div>
                        <div v-if="notifications.answer" class="notification-text">
                            {{ !$store.state.board.notifications.error?'回答しました。':'回答できませんでした。しばらく経ってからもう一度お試しください。' }}
                        </div>
                        <div v-if="notifications.post" class="notification-text">
                            {{ !$store.state.board.notifications.error?'投稿しました。':'投稿できませんでした。しばらく経ってからもう一度お試しください。' }}
                        </div>
                        <div v-if="notifications.others" class="notification-text">
                            {{ otherNotification }}
                        </div>
                    </div>
                <div class='question-box'> 
                    <div class="question-box-header">
                        <div class="image">
                            <img @click='test' class='img' v-bind:src="question.user.get_thumbnail"/>
                        </div>
                        <div class="username-date">
                            <p> {{ question.user.username}}さん </p>
                            <p> {{ dateConvert(question.created_on) }} </p>
                        </div>
                        <div class="question-status-container">
                            <p class="question-status"> {{ handleQuestionStatus(question.solved) }} </p>
                        </div>
                    </div>
                    <div
                     class="tag-container">
                        <div
                         class="tag"
                         v-for="(tag,questionindex) in question.tag"
                         v-bind:key="questionindex">
                            {{ tag.tag }}
                        </div>
                    </div>
                    <div class="title-question">
                        <p class="question-title">  {{ question.title }} </p>        
                        <p class='question-description'> {{ question.description}} </p>
                    </div>
                    <div class="question-box-footer">
                        <div class="like-wrapper">
                            <AbstractIcon
                            :config='questionLikeIconConfig'
                            :clicked='addedLiked'/>
                        </div>
                        <p class="good" v-if="question.liked_num[0]">{{ liked_num }} </p>
                        <div class="viewed-wrapper">
                            <p class="viewed"> viewed {{ question.viewed}} </p>
                        </div>
                        <div class="favorite-container">
                            <AbstractIcon
                            :config='favoriteIconConfig'
                            :clicked='addedFavorite'/>
                        </div>
                    </div>
                    <div v-if="user">
                        <div class="comment-to-respondents" v-if="question.user.UID==user.UID&&question.solved">
                            <p class='comment-text'>回答者にコメント</p>
                            <div v-if="!question.comment_to_respondents" class="textarea-container">
                                <textarea class="textarea" maxlength="100" placeholder="100字以内" v-model="commentToRespondents"></textarea>
                                <button class="btn-base-white-db-sq" :disabled="smallIsLoading" @click="addComment">
                                    <p v-if="!smallIsLoading">コメント</p>
                                    <i v-if="smallIsLoading" class="fas fa-spinner fa-pulse"></i>
                                </button>
                            </div>
                            <div class="question-comment" v-if="question.comment_to_respondents">
                                {{ question.comment_to_respondents }}
                            </div>
                        </div>
                        <button v-if="question.user.UID != UID&&!question.solved" class="btn-base-white-db-sq" @click='handleShowAnswerPage'>回答する</button>
                    </div>
                </div>
                <div class="relative-box" v-if='slicedRelatedQuestion'>
                    <p>関連した質問</p>
                    <div
                        class="related-question-wrapper"
                        >
                        <AbstractQuestionList
                        :questions='setQuestionsForAbstractQuestionList'
                        />
                    </div>
                    <div class="see-more">
                        <div  @click="goToRelatedQuestion">もっと見る></div>
                    </div>
                </div>
                <div class="answer-box" >
                    <div class="answer-box-title">
                        <p> 回答</p>
                        ({{ question.answer.length }}件)
                    </div>
                    <div class='no-answer' v-if="!question.answer.length">
                        <p>表示できる回答はありません。</p>
                    </div>
                    <div v-if='question.answer[0]' class="answer-exist-wrapper " >
                        <div
                     class="under-line"
                     v-for="(answer,answerindex) in answerOrderBestTop(question.answer)"
                     v-bind:key="answerindex">
                     <div class="best-answer" v-if="answer.best"><i class="fas fa-crown"></i>ベストアンサー</div>
                        <div class="answer-box-header">
                            <img class='img' v-bind:src="answer.user.get_thumbnail"/>
                            <div class="username-date">
                                <p> {{ answer.user.username}}さん </p>
                                <p> {{ dateConvert(answer.created_on) }} </p>
                            </div>
                        </div>
                        <p class="answer-description-container">{{ answer.description }} </p>
                        <div class="answer-box-footer">
                            <AbstractIcon
                            :config='answerLikeIconConfig'
                            :clicked='answerDict[answer.id].addedAnswerLiked'
                            :eventArguments='iconCompoArguments(answer.id)'/>
                            <p class="good"> {{ answerDict[answer.id].liked_num }} </p>
                        </div>
                        <div v-if="user">
                            <button v-if="question.user.UID == $store.state.signup.user.UID && answer.reply.length == 0 && !question.solved"
                            class='btn-base-white-db-sq' 
                            @click='handleReplyPage(answer.id, answer.description)'>
                            返信する
                            </button>
                        </div>
                        <!-- reply should be appir if post user or replyer -->
                        <div class='reply-wrapper' v-if='answer.reply[0]'>
                            <div class="replay-length">コメント<span class="replay-length">({{answer.reply.length}}件)</span></div>
                            <div class='reply-flex' 
                            v-for="(reply,replyindex) in answer.reply.length > 2&&!answerIndexList.includes(answerindex)?answer.reply.slice(0,2):answer.reply"
                            v-bind:key="replyindex">
                                <div class="reply-wrapper-header">
                                     <div class="img-container">
                                        <img class='img' v-bind:src="reply.user.get_thumbnail"/>
                                     </div>
                                    <div class="username-date">
                                         <!-- <p class="mobile-questioner" v-if="reply.user.UID==question.user.UID">
                                                質問者
                                            </p> -->
                                        <div :class="[reply.user.UID==question.user.UID?'with-questioner':'without-questioner']" attr="質問者"> {{ reply.user.username}}さん
                                            <!-- <p class="questioner" v-if="reply.user.UID==question.user.UID">
                                                質問者
                                            </p> -->
                                        </div>
                                        <p> {{ reply.created_on }} </p>
                                    </div>
                                </div>
                                <p class="replay-description" ref="replayDescriptionRef">{{ reply.description }}</p>
                                <div v-if="user">
                                    <button v-if='$store.state.signup.user.UID==question.user.UID && answer.reply.slice(-1)[0].id==reply.id &&!question.solved || $store.state.signup.user.UID==answer.user.UID && answer.reply.slice(-1)[0].id==reply.id &&!question.solved'
                                    class='btn-base-white-db-sq' 
                                    @click='handleReplyPage(answer.id, reply.description)'>
                                    返信する
                                    </button>
                                </div>

                            </div>
                        </div>
                        <div class="show-more-comment-container" @click="answerIndexList.push(answerindex)" v-if="answer.reply.length > 2&&!answerIndexList.includes(answerindex)">
                            <div class='show-more-comment'>
                                <span>さらにコメントを表示しますか ({{answer.reply.length-2}}件) </span>
                            </div>
                        </div>
                        <div v-if='user'>
                            <button  v-if='$store.state.signup.user.UID==question.user.UID&&!question.solved' class="best-answer-button">
                                <div class="text-container"  @click="showPopoverHandler(index=answerindex, answer.id)">
                                     <p>ベストアンサーに選びますか？</p>
                                </div>
                            <Popover
                            :popoverConfig='popoverConfig'
                            />
                            </button>
                        </div>
                        <div class='line-flex'>
                            <div class="line"></div>
                        </div>
                    </div>

                    </div>
                </div>
            </div>
            <transition name="notice">
                <NotVerified
                    class="components"
                    v-if="showEmailVerified"
                    @handleShowEmailVerified="handleShowEmailVerified"
                />
            </transition>
            <transition name="notice">
                <NotLogin
                    class="components"
                    v-if="showNotLogin"
                    @handleShowNotLogin="handleShowNotLogin"
                />
            </transition>
            <Answer v-if='showAnswerPage'
            class="components"
            :config='answerConfig'
            />
            <Reply v-if='showReplyPage'
            class="components"
            @handleShowReplyPage='handleShowReplyPage'
            @getDetail="answerClickFun"
            :answerId='answerId'
            :reply="reply"
            />
         </div>
    </div>
</template>

<script>
import axios from 'axios'
import {router} from "../main.js"
import NotVerified from '@/components/login/NotVerified.vue'
import NotLogin from '@/components/login/NotLogin.vue'
import  Answer from '@/components/board/Answer.vue'
import  Reply from '@/components/board/Reply.vue'
import  Popover from '@/components/parts/Popover.vue'
import  AbstractIcon from '@/components/board/AbstractIcon.vue'
import AbstractQuestionList from "@/components/board/AbstractQuestionList.vue";
export default {
    components: {
        Answer,
        Reply,
        NotVerified,
        Popover,
        NotLogin,
        AbstractIcon,
        AbstractQuestionList
  },
    data(){
        return{
            currentUserId:'',
            question:'',
            showAnswerPage: false,
            showReplyPage: false,
            answerIndexList:[],
            questionTitle:'',
            questionDescription:'',
            questionSlug:'',
            questionId:'',
            answerId:'',
            allAnswer:'',
            answerDict:{},
            addedAnswerLiked:{},
            viewed:0,
            questionStatus:['回答受付中','解決済み'],
            reply:'',
            questionUser: '',
            questionUserBoolean: false,
            liked_num: '',
            addedLiked: false,
            addedFavorite: false,
            likedUserIdList:'',
            checkedLikedUserList:[],
            relatedQuestion:'',
            slicedRelatedQuestion:'',
            questionTags:[],
            showEmailVerified:false,
            showNotLogin: false,
            commentToRespondents:'',
            showPopover:{
                show:false,
                index:''
            },
            bestanswerId:'',
            bestAnswerUser:false,
            otherNotification:'',
            // answerConfig: {
            //     clickFun:this.answerClickFun,
            //     showHandler:this.handleShowAnswerPage,
            //     questionTitle:this.questionTitle,
            //     questionDescription:this.questionDescription,
            //     questionId:this.questionId
            // },
            popoverConfig:{
                mainText:'よろしいですか。',
                cancelFun: this.showPopoverHandler,
                confirmFun: this.patchQuestionSolved,
                cancelText:'戻る',
                confirmText:'選ぶ'
            },
            favoriteIconConfig: {
                clickEventEnabled: this.$store.getters.user?true:false,
                clickEvent: this.handleAddedFavorite,
                icons:{
                    clicked:{
                        icon:'fas fa-star',
                        color:'yellow'
                    },
                    unclicked:{
                        icon:'far fa-star',
                        color:'',
                        borderColor:''
                    },
                    asBorder:true
                }
            },
            questionLikeIconConfig: {
                enableUnclickEvent:false,
                clickEventEnabled: this.$store.getters.user?true:false,
                clickEvent: this.addLikedNum,
                icons:{
                    clicked:{
                        icon:'fas fa-heart',
                        color:'rgb(221, 36, 221)'
                    },
                    unclicked:{
                        icon:'far fa-heart',
                        color:'rgb(221, 36, 221)',
                        borderColor:'rgb(255 150 218'
                    },
                    asBorder:true
                }
            },
            answerLikeIconConfig: {
                enableUnclickEvent:false,
                clickEventEnabled: this.$store.getters.user?true:false,
                clickEvent: this.addAnsweerLikedNum,
                icons:{
                    clicked:{
                        icon:'fas fa-heart',
                        color:'rgb(221, 36, 221)'
                    },
                    unclicked:{
                        icon:'far fa-heart',
                        color:'rgb(221, 36, 221)',
                        borderColor:'rgb(255 150 218'
                    },
                    asBorder:true
                }
            }
        }
    },
    created() {
        this.favoriteCheck()
        this.getDetail()
    },
    beforeMount() {
    },
    mounted() {
    },
    beforeUnmount(){
    },
    computed:{
        user(){
            return this.$store.state.signup.user
        },
        UID(){
            try{
                return this.$store.state.signup.user.UID
            }catch{
                return ''
            }
        },
        emailVerified(){
            return this.$store.getters.getEmailVerified
        },
        fixedScroll(){
            return this.$store.getters.fixedScroll
        },
        smallIsLoading() {
            return this.$store.getters.smallIsLoading
        },
        favoriteQuestions() {
            return this.$store.state.signup.userFavoriteQuestions
        },
        notifications() {
            return this.$store.state.board.notifications
        },
        detailQuestion() {
            return this.$store.getters.getDetailQuestion
        },
        setQuestionsForAbstractQuestionList() {
             const questionObj = {
                results:this.slicedRelatedQuestion,
                getDetail:this.getRelatedSlug,
                styleType:'simple',
                notShowSolved:true
            }
            return questionObj 
        },
        renderingCheck() {
            if(this.question&&this.relatedQuestion.results&&this.slicedRelatedQuestion) {
                this.$store.commit('setIsLoading', false)
                return true
            } else {
                false
            }

        },
        answerConfig() {
            return {
                clickFun:this.answerClickFun,
                showHandler:this.handleShowAnswerPage,
                questionTitle:this.questionTitle,
                questionDescription:this.questionDescription,
                questionId:this.questionId
            }
        },
    },
    watch:{
        $route(to, from) {
            if(from.name === to.name) {
                this.question = ''
                this.relatedQuestion = ''
                this.slicedRelatedQuestion = ''
                this.addedFavorite = ''
                this.addedLiked = ''
                this.answerIndexList = []
                this.getDetail()
                
            }
        }
    },
    methods: {
        dateConvert(date){
            const dateObj = new Date()
            const offset = dateObj.getTimezoneOffset()
            let dt = new Date(date)
            const localTime = dt.setMinutes(offset*-1 + dt.getMinutes())
            
            dt = new Date(localTime)
            const stringDT = dt.toLocaleString([], {year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit'})
            return stringDT.replace(/\//g,'-')
        },
        async answerClickFun() {
            this.question = this.detailQuestion
            this.allAnswer = this.question.answer
            this.makeAnswerDict()
        },
        async getDetail() {
            this.question = this.detailQuestion
            this.questionTitle = this.question.title
            this.questionDescription = this.question.description
            this.questionSlug = this.question.slug
            this.questionId = this.question.id
            console.log('NUMMM', this.question.liked_num)
            this.liked_num = this.question.liked_num.length?this.question.liked_num[0].liked_num:0
            this.likedUserIdList = this.question.liked_num.length?this.question.liked_num[0].user:[]
            this.questionUser = this.question.user.UID
            this.allAnswer = this.question.answer
            this.viewed = this.question.viewed
            await this.patchOnReply()
            await this.questionPatch()
            this.makeAnswerDict()
            this.getQuestionTagList(this.question.tag)
            await this.getRelatedQuestion()
            await this.countViewedNumUp()
                
        },
        setShowReplyConfig() {
            const obj = {
                index:'',

            }
        },
        showPopoverHandler(index="", answerId) {
            this.bestanswerId = answerId ? answerId:''
            this.showPopover.show = !this.showPopover.show
            this.showPopover.index = index ? index:''
        },
        answerOrderBestTop(answers) {
            const likedNumOrder = () => {
                return answers.sort((a,b) =>{
                        return (b.liked_answer[0].liked_num - a.liked_answer[0].liked_num)
                    })
            }
            const best = answers.find((answer) => {
                return answer.best
            })
            if(best) {
                const orderedAnswers = [best]
                answers = likedNumOrder()
                answers.forEach((each) => {
                    if(each!==best) {
                        orderedAnswers.push(each)
                    }
                })
                return orderedAnswers
            }
            return answers
        },
        async patchQuestionSolved(){
            this.$store.commit("setSmallIsLoading", true)
            const url = `/api/board/best-answer`
            await axios(url, {
                method: 'patch',
                data:{
                    question:this.question.id,
                    answer:this.bestanswerId
                }
            }).then((res) => {
                this.question = res.data
                this.otherNotification = "ベストアンサーを決定しました。"
                this.$store.dispatch("handleNotifications", 'others')
                this.$store.commit("setSmallIsLoading", false)
                this.scrollTop()
            })
        },
        async addComment() {
            if(this.commentToRespondents) {
                this.$store.commit("setSmallIsLoading", true)
                const url = `/api/board/question/${this.$route.params.slug}`
                await axios({
                    method: 'patch',
                    url: url,
                    data: {
                        comment_to_respondents: this.commentToRespondents,
                    },
                })
                .then((res) => {
                    this.question = res.data
                    this.$store.commit("setSmallIsLoading", false)
                    this.scrollTop()
                    this.otherNotification = "回答者にコメントしました。"
                    this.$store.dispatch("handleNotifications", 'others')
                })
            }
        },
        async patchOnReply(){
            for(let answer of this.allAnswer){
                const onReply = answer.on_reply
                const onBest = answer.on_best
                if((onReply || onBest)&&answer.user.UID==this.$store.getters.user.UID){
                    const url = `/api/board/answer-detail/${answer.id}`
                    await axios({
                        method: 'patch',
                        url: url,
                        data: {
                            on_reply: false,
                            on_best: false
                        },
                    })
                    // if error happenes, delete catch part
                    .catch(e =>{
                        let logger = {
                            message: "in Community/PatchOnReplay. couldn't patch onReplay",
                            path: window.location.pathname,
                            actualErrorName: e.name,
                            actualErrorMessage: e.message,
                        }
                        this.$store.commit('setLogger',logger)
                        router.push({ name: 'ConnectionError' })
                    })
                    this.$store.dispatch('getUserData')
                    this.$store.dispatch('getAnsweredQuestion')
                }
            }
        },
        async getRelatedQuestion() {
            // relatedQuestion.results Start from here.
            // => deleteSameQuestion to delete the same question in RQ as detail Q.
            // => makeRandomSlicedArray to make random sliced RQ array
            if(this.user){
                if(this.questionTags.length == 1){
                    var url = `/api/board/question/filter-list?tag=${this.questionTags[0]}&uid=${this.user.UID}`
                }
                if(this.questionTags.length == 2){
                    var url = `/api/board/question/filter-list?tag=${this.questionTags[0]}&tag=${this.questionTags[1]}&uid=${this.user.UID}`
                }
                if(this.questionTags.length == 3){
                    var url = `/api/board/question/filter-list?tag=${this.questionTags[0]}&tag=${this.questionTags[1]}&tag=${this.questionTags[2]}&uid=${this.user.UID}`
                }
            }
            else{
                if(this.questionTags.length == 1){
                    var url = `/api/board/question/filter-list?tag=${this.questionTags[0]}`
                }
                if(this.questionTags.length == 2){
                    var url = `/api/board/question/filter-list?tag=${this.questionTags[0]}&tag=${this.questionTags[1]}`
                }
                if(this.questionTags.length == 3){
                    var url = `/api/board/question/filter-list?tag=${this.questionTags[0]}&tag=${this.questionTags[1]}&tag=${this.questionTags[2]}`
                }
            }
            await axios
                .get(url)
                .then(response => {
                this.relatedQuestion = response.data
                })
                .catch(e => {
                    let logger = {
                        message: "in Community/getRelatedQuestion. couldn't get RelatedQuestion",
                        path: window.location.pathname,
                        actualErrorName: e.name,
                        actualErrorMessage: e.message,
                    }
                    this.$store.commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
                })
            this.$store.commit('setRelatedQuestion', this.relatedQuestion)
            this.deleteSameQuestion()
            this.makeRandomSlicedArray()
        },
        async createFavorite(){
            await axios({
                method: 'post',
                url: '/api/board/each-favorite-question/',
                data: {
                    UID: this.user.UID,
                    question: this.question.id
                },
            })
            .then((res) => {
                console.log("RES FAVORITE",res.data.question.id)
                let question = ''
                if(typeof res.data.question.id !== 'undefined'){
                    console.log("NOT_UNDEFINED")
                    question = res.data.question
                } else {
                    console.log("UNDEFINED")
                    question = this.question
                }
                console.log(question,this.question)
                this.$store.commit('handleFavoriteQuestion',question)
                this.$store.commit('setFavoriteQuestions','')
                console.log(res.data)
            })
            .catch(e => {
                let logger = {
                    message: "in Community/createFavorite. couldn't create Favorite",
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,
                }
                this.$store.commit('setLogger',logger)
                router.push({ name: 'ConnectionError' })
            })
        },
        handleAddedFavorite(){
            if(this.user){
                this.addedFavorite=!this.addedFavorite
                this.createFavorite()
            }else{
                this.handleShowNotLogin()
            }
        },
        async countViewedNumUp(){
            if(this.user){
                for (let i =0; i < this.question.tag.length; i++){
                    await axios({
                    method: 'post',
                    url: '/api/board/user-tag/create/',
                    data: {
                        user: this.user.UID,
                        tag: this.question.tag[i].id
                        },  
                    })
                    .then((res) => {
                    }) 
                    .catch(e => {
                        let logger = {
                            message: "in Community/countViewedNumUp. couldn't increase ViewedNum",
                            path: window.location.pathname,
                            actualErrorName: e.name,
                            actualErrorMessage: e.message,
                        }
                        this.$store.commit('setLogger',logger)
                        // in local environment, database locked error occur frequently
                        // router.push({ name: 'ConnectionError' })
                    })
                }
            }
        },
        handleShowAnswerPage(){
            if(this.user){
                if(this.emailVerified){
                this.showAnswerPage = !this.showAnswerPage
                }else{
                    this.handleShowEmailVerified()
                }
            }else{
                this.handleShowNotLogin()
            }
        },
        getReply(reply){
            this.reply = reply
        },
        handleShowReplyPage(){
            this.showReplyPage = !this.showReplyPage
        },
        handleReplyPage(id, reply=''){
            this.getAnswerId(id)
            this.showReplyPage = !this.showReplyPage
            this.getReply(reply)
        },
        getAnswerId(id){
            this.answerId = id
        },
        getReplyUserAndQuestionUser(reply, question){
            this.questionAnswerUser.push(reply)
            this.questionAnswerUser.push(question)
        },
        handleQuestionStatus(status){
            if(status==true){
                return this.questionStatus[1]
            }
            else{
                return this.questionStatus[0]
            }
        },
        getQuestionTagList(questionTags){
            this.questionTags = []
            for(let tag of questionTags){
                this.questionTags.push(tag.id)
            }
        },
        makeRandomSlicedArray(){
            let num = 3
            if (this.relatedQuestion.results.lendth < 3){
                num = this.relatedQuestion.results.lendth
            }
            this.getRandomQuestion(this.relatedQuestion.results)
            this.slicedRelatedQuestion = this.relatedQuestion.results.slice(0,num)
        },
        deleteSameQuestion(){
            if(this.user){
                for(let q of this.relatedQuestion.results){
                    if (q.id == this.question.id){
                        this.relatedQuestion.results.splice(this.relatedQuestion.results.indexOf(q),1)
                        break
                    }
                }
            }
        },
        getRandomQuestion(array){
            for (let i = array.length - 1; i >= 0; i--) {
                let r = Math.floor(Math.random() * (i + 1))
                let tmp = array[i]
                array[i] = array[r]
                array[r] = tmp
                }
            for ( let k =0; k < array.length; k++){
                for (let i = array[k].answer.length - 1; i >= 0; i--) {
                let r = Math.floor(Math.random() * (i + 1))
                let tmp = array[k].answer[i]
                array[k].answer[i] = array[k].answer[r]
                array[k].answer[r] = tmp
                }}
            return array
            },
        async getRelatedSlug(slug){
            this.question = ''
            this.relatedQuestion = ''
            this.slicedRelatedQuestion = ''
            await router.push(slug)
            },
        addLikedNum(){
            if(this.user){
                this.liked_num += 1
                this.addedLiked = true
                for(let i=0; i<this.likedUserIdList.length; i++){
                    this.checkedLikedUserList.push(this.likedUserIdList[i])
                }
                this.checkedLikedUserList.push(this.$store.state.signup.user.UID)
                this.countUpLiked()
            }else{
                this.handleShowNotLogin()
            }
        },
        clearAllLiked(){
            this.addedLiked = false
            for(let i in this.answerDict){
                this.answerDict[i].addedAnswerLiked = false
            }
        },
        checkUserLiked(){
            // this is for question like
            if(this.user){
                this.clearAllLiked()
                for(let i of this.likedUserIdList){
                    if(i == this.$store.state.signup.user.UID){
                    this.addedLiked = true
                    }
                }
                // this is for answer like
                for(let answerId in this.answerDict){
                    for( let user of this.answerDict[answerId].likedUsers[0]){
                        if(user == this.$store.state.signup.user.UID){
                            this.answerDict[answerId].addedAnswerLiked = true
                        }
                    }
                }   
            }
        },
        favoriteCheck(){
            try{
                if(this.favoriteQuestions){
                    this.addedFavorite = false
                    console.log("FC",this.detailQuestion)
                    for(let i of this.favoriteQuestions.results){
                        if(this.detailQuestion.id==i.id){
                            this.addedFavorite = true
                            break
                        }
                    }
                }
            }
            catch{
                
            }
        },
        countUpLiked(){
            if(this.addedLiked){
                axios.patch(`/api/board/question-liked/${this.question.liked_num[0].id}/`,
                {
                    user: this.checkedLikedUserList,
                    liked_num: this.liked_num
                })
                .catch(e => {
                    let logger = {
                        message: "in Community/countUpLiked. couldn't countUp Liked",
                        path: window.location.pathname,
                        actualErrorName: e.name,
                        actualErrorMessage: e.message,
                    }
                    this.$store.commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
                })
            }
        },
        async questionPatch(){
            // patch view count_up and on_answer
            if(this.user){
                try{
                    const url = `/api/board/question/${this.questionSlug}`
                    if(this.questionUserBoolean == false&&this.question.on_answer==true&&this.question.on_reply==true&&this.question.user.UID==this.user.UID){
                        await axios.patch(url,{
                            viewed: this.viewed + 1,
                            on_answer: false,
                            on_reply: false
                        })
                        this.$store.dispatch('getUserData')
                        this.$store.dispatch('getAnsweredQuestion')
                    }
                    else if(this.questionUserBoolean == false&&this.question.on_answer==true&&this.question.user.UID==this.user.UID){
                        await axios.patch(url,{
                            viewed: this.viewed + 1,
                            on_answer: false
                        })
                        this.$store.dispatch('getUserData')
                        this.$store.dispatch('getAnsweredQuestion')
                    }
                    else if(!this.questionUserBoolean&&this.question.on_reply&&this.question.user.UID==this.user.UID){
                        await axios.patch(url,{
                            viewed: this.viewed + 1,
                            on_reply: false
                        })
                        this.$store.dispatch('getUserData')
                        this.$store.dispatch('getAnsweredQuestion')
                    }
                    else if(this.questionUserBoolean == false){
                        axios.patch(url,{
                            viewed: this.viewed + 1
                        })
                    }
                } catch (e){
                    let logger = {
                        message: "in Community/questionPatch. couldn't patch question",
                        path: window.location.pathname,
                        actualErrorName: e.name,
                        actualErrorMessage: e.message,
                    }
                    this.$store.commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
                }
            }
        },
        makeAnswerDict(){
            // liked_answer start from here to make each answer dict
            // to hold information
            for(let answer of this.allAnswer){
                this.answerDict[answer.id] = {
                    "liked_id":answer.liked_answer[0].id,
                    "liked_num":answer.liked_answer[0].liked_num,
                    "addedAnswerLiked":false,
                    "likedUsers":[answer.liked_answer[0].user]
                }
            }
            this.checkUserLiked()
        },
        addAnsweerLikedNum(answerId){
            // add answer id start from here. answerDict has each answers liked num.
            // invoke answerId to att liked num, then addedAnswerLiked = true 
            if(this.user){
                this.answerDict[answerId].liked_num += 1
                this.answerDict[answerId].addedAnswerLiked = true
                this.answerDict[answerId].likedUsers[0].push(this.$store.state.signup.user.UID)
                this.countUpLikedAnswer(answerId)
            }else{
                this.handleShowNotLogin()
            }
        },
        countUpLikedAnswer(answerId){
            axios.patch(`/api/board/answer-liked/${this.answerDict[answerId].liked_id}/`,
            {
                user: this.answerDict[answerId].likedUsers[0],
                liked_num: this.answerDict[answerId].liked_num
            })
            .catch(e => {
                let logger = {
                    message: "in Community/countUpLikedAnswer. couldn't countUp LikedAnswer",
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,
                }
                this.$store.commit('setLogger',logger)
                router.push({ name: 'ConnectionError' })
            })
        },
        iconCompoArguments(answerId) {
            return {
                clickEvent: answerId
            }
        },
        handleShowEmailVerified(){
            this.showEmailVerified = !this.showEmailVerified
        },
        handleShowNotLogin(){
            this.showNotLogin = !this.showNotLogin
        },
        goToRelatedQuestion() {
            router.push({name:'RelatedQuestion'})
        },
        scrollTop(){
            window.scrollTo({
                top: 0,
            });
        },

    }
}
</script>

<style lang='scss' scoped>
@import "style/_variables.scss";
@import "style/_board.scss";
.scroll{
    position:fixed;
}
.components{
    z-index: 3;
}

.board-detail-wrapper{
    display: flex;
    justify-content: center;
    width: 100vw;
    min-height: 80vh;
    margin-bottom: 1rem;
}
.question-wrapper{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    .question-box{
        border: solid $base-color;
        border-radius: 0.5rem;
        background: $back-lite-white;
        width: 95%;
        padding-bottom: 1rem;
        .question-box-header{
            display: flex;
            .image{
                .img{
                border-radius: 50%; 
                border: solid $dark-blue;
                width:  3rem;   
                height: 3rem;
                margin: 0.5rem; 
                }
            }
            .username-date{
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                margin-top: 0.5rem;
                width:40%;
            }
            .question-status-container{
                display: flex;
                justify-content: flex-end;
                width: 50%;
                position: relative;
                .question-status{
                    position: absolute;
                    right:0;
                    top: 0.5rem;
                    color: rgb(255, 43, 209);
                    margin-right: 1rem;
                    padding: 0 0.2rem;
                    border: solid rgb(255, 43, 209);
                }
            }
        }
        .tag-container{
            display: flex;
            width: 100%;
            padding-left: 1rem;
            .tag{
                margin-right: 0.5rem;
                border: solid gray;
                border-radius: 1rem;
                padding:0.5rem; 
            }
        }
        .title-question{
            padding:1rem;
            .question-title{
                text-align: center;
                margin-bottom: 1rem;
                border-bottom: solid $dark-blue;
                display: inline-block;
                padding-bottom: 1rem;
            }
            .question-description{
                text-align: left;
                padding: 1rem; 
                background: rgb(236, 236, 236);
                white-space: pre-wrap;
            }
        }
        .question-box-footer{
            position: relative;
            display: flex;
            align-items: center;
            margin-bottom: 0.5rem;
            width:100%;
            .like-wrapper{
                width: 1rem;
                height: 1rem;
                margin: 0 0.5rem;
                display: flex;
            }
            .viewed-wrapper{
                display: flex;
                .viewed{
                margin-left: 1rem;
                margin-right: 0.5rem;
                }
            }
            .favorite-container {
                position: absolute;
                right: 1rem;
                height: 1rem;
            }
        }
        .btn-base-white-db-sq{
            margin: 1rem;
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
            font-size: 1rem;
            font-weight: bold;
        }
    }
    .relative-box{
        border: solid $base-color;
        border-radius: 0.5rem;
        background: $back-lite-white;
        width: 95%;
        margin-top: 1rem;
        margin-bottom: 1rem;
        padding: 0.5rem;
        display: flex;
        flex-direction: column;
        P{
            margin: 0.5rem 0;
            font-weight: bold;
        }
        .question-wrapper{
            width: 100%;
            display: flex;
            .question-list{
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
                    .date{
                        margin-left: 0.5rem;
                    }
                }
            }
        }
        .see-more{
            display: flex;
            justify-content: flex-end;
            margin-right: 0.5rem;
            margin-top: 0.5rem;
            div{
                cursor: pointer;
                transition: .3s;
            }
            div:hover{
                color: $middle-blue;
            }
        }
    }
    .answer-exist-wrapper{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .answer-box{
        border: solid $base-color;
        border-radius: 0.5rem;
        background: $back-lite-white;
        width: 95%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        .answer-box-title{
            display: flex;
            justify-content: center;
            margin-top: 1rem;
            font-weight: bold;
        }
        .no-answer {
            margin: 1rem 0;
        }
        .under-line{
            width: 90%;
            border-bottom: 0.2rem solid rgb(236, 236, 236);
            margin-top: 2rem;
            margin-bottom: 1rem;
            &:last-child{
                border-bottom: none;
            }
        }
        .answer-box-header{
            display: flex;
            .img{
                border-radius: 50%;
                border: solid $dark-blue;
                width:  3rem;   
                height: 3rem;
                margin: 0.5rem; 
            }
            .username-date{
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                margin-top: 0.5rem;
            }
        }
        .answer-description-container{
            margin: 1rem;
            background: rgb(236, 236, 236);
            padding: 1rem;
            text-align: left;
        }
        .answer-box-footer{
            display: flex;
            align-items: center;
            height: 1rem;
            .good{
                margin-left: 0.5rem;
            }
        }
        .btn-base-white-db-sq{
            margin: 1rem;
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
            font-size: 1rem;
            font-weight: bold;
        }
        .reply-wrapper{
            .replay-length {
                font-weight: bold;
            }
            .reply-flex{
                width: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                margin-bottom: 1rem;
                .reply-wrapper-header{
                    width: 95%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    .img{
                        border-radius: 50%;
                        border: solid $dark-blue;
                        width:  2.5rem;   
                        height: 2.5rem;
                        margin: 0.5rem; 
                    }
                    .img-container {
                        position: relative;
                        .connect-line {
                            border-left: solid gray;
                            position: absolute;
                            left: 50%;
                        }
                    }          
                    .username-date{
                        display: flex;
                        flex-direction: column;
                        align-items: flex-start;
                    }
                
                }
                .replay-description{
                    width: 80%;
                    background: rgb(236, 236, 236);
                    text-align: left;
                    padding: 0.5rem;
                    white-space: pre-wrap;
                }
            }
        }
        .line-flex{
            display: flex;
            width: 100%;
            justify-content: center;
            align-items: center;
            margin-top: 0.5rem;
            &.line{
                width: 90%;
                border-bottom: 0.2rem solid rgb(236, 236, 236);
                margin-top: 2rem;
                margin-bottom: 1rem;
                &:last-child{
                    border-bottom: none;
                }
            }
        }
    }
}
.icon{
    animation: icon 0.5s ;

}
.questioner{
    color: $dull-red;
    margin-left: 0.5rem;
    border: solid $dull-red;
    padding: 0 0.4rem;
}
.best-answer-button {
    position: relative;
    width: 100%;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: solid rgb(56, 208, 251);
    background: none;
    margin: 1rem 0;
    padding: 0.5rem 0;
    font-weight: bold;
    transition: .3s;
    .text-container {
        height: 40px;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
}
.best-answer-button:hover {
    background: $lite-dull-blue;
    
}
.best-answer-button:checked {
    background: $lite-dull-blue;
    
}
.best-answer {
    font-weight: bold;
    color: #c0a700;
    .fa-crown {
        font-size: 1.5rem;
    }
}
.show-more-comment-container {
    display: flex;
    justify-content: center;
    width: 100%;
    .show-more-comment {
        border: solid gray;
        border-radius: 5px;
        width: 80%;
        text-align: center;
        font-weight: bold;
        padding: 0.3rem 0;
        transition: .3s;

    }
    .show-more-comment:hover {
        background: gray;
        color: white;
    }
}
.comment-to-respondents {
    margin-top: 0.5rem;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    .comment-text {
        font-weight: bold;
    }
    .textarea-container{
        width: 85%;
        white-space: pre-wrap;
        .textarea {
            resize: none;
            padding: 0.5rem;
        }
    }
    .question-comment {
        width: 85%;
        background: $lite-gray;
        padding: 0.5rem;
        white-space: pre-wrap;
        // min-height: 20px;
    }
}
.with-questioner::after {
    content: attr(attr);
    border: solid red;
    margin-left: 1rem;
    padding: 0 0.3rem;
    color: red;
}

</style>