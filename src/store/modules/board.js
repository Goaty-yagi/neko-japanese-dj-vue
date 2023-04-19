import axios from 'axios'

export default {
    namespace: true,
    state: {
        title:'',
        description:'',
        selectedTagList:'',
        relatedQuestion:'',
        searchedQuestions:'',
        reccomendedQuestion:'',
        answeredQuestion:'',
        notificationApi:'',
        userTags:'',
        detailQuestion:'',
        showNoticeOnAcount:{
            answer:false,
            reply:false,
        },
        notifications:{
            error:false,
            reply: false,
            answer: false,
            post: false,
            others: false,
        },
    },
    getters:{
        user(state, getters, rootState){
            return rootState.signup.user
        },
        gettersAnsweredQuestions(state){
            return state.answeredQuestion
        },
        gettersReccomendedQuestion(state){
            return state.reccomendedQuestion
        },
        gettersAnswer(state){
            return state.showNoticeOnAcount.answer
        },
        gettersReply(state){
            return state.showNoticeOnAcount.reply
        },
        getDetailQuestion(state) {
            return state.detailQuestion
        },
        getUserTags(state, getters){
            if(getters.user){
                let checkDict = {}  
                let checkedList = []
                let checkedlist2 = []
                for(let i of state.userTags){
                    checkDict[i.tag.id] = i.total_num
                    checkedList.push(i.tag)
                }
                if(Object.keys(checkDict).length <= 3){
                    let checkedIdList = []
                    for (let i of checkedList){
                        checkedIdList.push(i.id)
                    }
                    return checkedIdList
                }
                if(Object.keys(checkDict).length > 3){
                    for(let m=0; m < 3; m++){
                        const aryMax = function (a, b) {return Math.max(a, b);}
                        let max = Object.values(checkDict).reduce(aryMax);
                        const result = Object.keys(checkDict).reduce( (r, key) => {
                            return checkDict[key] === max ? key : r 
                            }, null);
                        delete checkDict[result]
                        checkedlist2.push(result)
                    }
                    return checkedlist2
                }
            }
        },
        notificationApi(state){
            var noty = state.notificationApi
            if(noty.length==0){
                return false
            }
            else {
                for (let i=0; i < noty.length; i ++) {
                    if(noty[i].length){
                        for (let j=0; j <= noty[i].length; j ++) {
                            if('on_reply' in noty[i][j] || 'on_answer' in noty[i][j] || 'on_best' in noty[i][j]) {
                                return true
                            }
                        }
                    }
                }
            }
        },        
    },
    mutations:{
        resetNotifications(state){
            state.notifications.error = false
            state.notifications.answer = false
            state.notifications.reply = false
            state.notifications.post = false
            state.notifications.others = false
        },
        getTitle(state,payload){
            state.title = payload
        },
        getDescription(state, payload){
            state.description = payload
        },
        setReccomendedQuestion(state, payload){
            state.reccomendedQuestion = payload
            console.log("SET_RECCO", state.reccomendedQuestion)
        },
        setRelatedQuestion(state, payload){
            state.relatedQuestion = payload
        },
        getTagList(state, payload){
                state.selectedTagList = payload
        },
        setUserTags(state, payload) {
            state.userTags = payload
            console.log("SET_UT", state.userTags)
        },
        setApiError(state) {
            state.notifications.error = true
        },
        setAnsweredQuestion(state, payload) {
            state.answeredQuestion = payload
            console.log("set_AnsweredQ", state.answeredQuestion)
        },
        setDetailQuestion(state, payload) {
            state.detailQuestion = payload
            console.log("question is set", state.detailQuestion)
        },
        setAnswerToQuestion(state, payload) {
            state.detailQuestion.answer.push(payload)
            console.log('ANSWER IS SET', state.detailQuestion)
        },
        setReplayToAnswer(state, payload) {
            const answerId = payload.answerId
            const reply = payload.reply
            state.detailQuestion.answer.forEach((e) => {
                if(e.id === answerId) {
                    e.reply.push(reply)
                }
            })
        }
    },
    
    actions:{
        commitHandleOnReplyAndOnAnswer({commit,getters}){
            commit('handleOnReplyAndOnAnswer', getters.user)
        },
        handleNotifications(context, payload){
            console.log("error-check",context.state.notifications.error)
            if(payload == "reply"){
                context.state.notifications.reply = true
                setTimeout(context.commit, 4500,"resetNotifications")      
            }
            if(payload == "answer"){
                context.state.notifications.answer = true
                setTimeout(context.commit, 4500,"resetNotifications")
            }
            if(payload == "post"){
                context.state.notifications.post = true
                setTimeout(context.commit, 4500,"resetNotifications")
            }
            if(payload == "others"){
                context.state.notifications.others = true
                setTimeout(context.commit, 4500,"resetNotifications")
            }
        },
        async getSearchQuestion(state,payload){            
            await axios
                .get(`/api/board/question/search/?keyword=${payload}`)
                .then(response => {
                    state.searchedQuestions = response.data
                })
                .catch((e) => {
                    let logger = {
                        message: "in store/board.getSearchQuestion. couldn't get SearchQuestion",
                        name: window.location.pathname,
                        actualErrorName: e.code,
                        actualErrorMessage: e.message,
                    }
                    context.commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
                });
        },
        async getRelatedQuestion({ state , getters, commit }, payload) {
            // for reccomended-question, if user and user.user_tag exist, get reccomended-question.
            // else, get question-viewed-order.
            if(getters.user){
                try{
                    if(getters.getUserTags.length == 1){
                        var url = `/api/board/question/filter-list?tag=${getters.getUserTags[0]}&uid=${getters.user.UID}`
                    }
                    if(getters.getUserTags.length == 2){
                        var url = `/api/board/question/filter-list?tag=${getters.getUserTags[0]}&tag=${getters.getUserTags[1]}&uid=${getters.user.UID}`
                    }
                    if(getters.getUserTags.length == 3){
                        var url = `/api/board/question/filter-list?tag=${getters.getUserTags[0]}&tag=${getters.getUserTags[1]}&tag=${getters.getUserTags[2]}&uid=${getters.user.UID}`
                    }
                    else{
                        var url = '/api/board/question-viewed-order'
                    }
                }
                catch{
                    var url = '/api/board/question-viewed-order'  
                }
            }else{
                var url = '/api/board/question-viewed-order'
            }
            console.log("URL",url)
            await axios
            .get(url)
            .then(response => {
                console.log("GET_RELA+TEDS", response.data)
                commit('setReccomendedQuestion', response.data)
            })
            .catch((e) => {
                let logger = {
                    message: "in store/board.getRelatedQuestion. couldn't get RelatedQuestion",
                    name: window.location.pathname,
                    actualErrorName: e.code,
                    actualErrorMessage: e.message,
                }
                context.commit('setLogger',logger)
                router.push({ name: 'ConnectionError' })
            });
                
        },
        async getAnsweredQuestion({ state ,commit, getters,rootState,rootGetters}, payload) {
            var url = `/api/board/question-answered?user=${rootGetters.user.UID}`
            await axios.get(url)
                .then(response => {
                    commit('setAnsweredQuestion', response.data)

                })
                .catch((e) => {
                    let logger = {
                        message: "in store/board.getAnsweredQuestion. couldn't get AnsweredQuestion",
                        name: window.location.pathname,
                        actualErrorName: e.code,
                        actualErrorMessage: e.message,
                    }
                    context.commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
                });           
        },
        async getNotificationApi({ state , getters,rootState,rootGetters}, payload) {
            if(rootGetters.user) {
                var url = `/api/board/user-question-answer-notification?user=${rootGetters.user.UID}`
                await axios.get(url)
                    .then(response => {
                    state.notificationApi = response.data
                    })
                    .catch((e) => {
                        let logger = {
                            message: "in store/board.getNotificationApi. couldn't get NotificationApi",
                            name: window.location.pathname,
                            actualErrorName: e.code,
                            actualErrorMessage: e.message,
                        }
                        context.commit('setLogger',logger)
                        router.push({ name: 'ConnectionError' })
                    });          
            }       
        },
        async getUserTag({ state , commit }, payload){
            console.log("IN_GUT")
            await axios({
                method: 'get',
                url: `/api/board/get-user-tag/?user=${payload}`,
            })
            .then((res) => {
                commit('setUserTags', res.data)
            })
            .catch((e) => {
                let logger = {
                    message: "in store/board.getUsertag. couldn't get UserTag",
                    name: window.location.pathname,
                    actualErrorName: e.code,
                    actualErrorMessage: e.message,
                }
                context.commit('setLogger',logger)
                router.push({ name: 'ConnectionError' })
            });
        },
        async getDetail({ state , commit }, payload) {
            const url = `/api/board/question/${payload}`
            await axios
                .get(url)
                .then(async (res) =>  {
                    commit('setDetailQuestion', res.data)
                })
                .catch(e => {
                    console.log("ERROR",e)
                    let logger = {
                    message:  "in store/board/getDetail. couldn't get Detail-question",
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,
                }
                    this.$store.commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
            })
            console.log("GRT_DETAIL_END")
            // this.$store.commit('setIsLoading', false)
        },
    }
}