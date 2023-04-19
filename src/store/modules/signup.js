import Cookies from 'js-cookie'
import {router} from "@/main.js"
import axios from 'axios'
import jwt_decode from "jwt-decode";

export default {
    namespace: true,

    state: {
        username: '',
        email:'',
        email2:'',
        country:'',
        password:'',
        user: null,
        registeredUser: false,
        UID:'',
        emailVerified:null,
        authIsReady:false,
        checkedEmail:null,
        accountURL: window.location.origin, 
        actionCodeSettings:{
            url: null,
            handleCodeInApp: true
        },
        tempUser: {
            test: false,
            statusList:'',
            grade:'',
            level:''
        },
        favoriteQuestion:'',
        logger:{
            exist: false,
            actualErrorName:'',
            actualErrorMessage:'',
            message:'',
            path:''
        },
        userInfo:'',
        exceptUserInfo:'',
        beingException:false,
        reloadForException: false,
        apiError:{
            // this is for connection Error
            django: false,
            firebase: false,
            ipinfo: false,
            any: false
        },
        onSigningup:false,
        myQuestion:'',
        gradeDict:{
            '超初級':0,
            '初級':10,
            '中級':20,
            '上級':30
        },
        thirdPartylogindata:'',
        thirdPartyError:'',
        countryData:'',
        googleLogin:false,
        tokenError:false,
        accessToken:'',
        refreshToken:'',
        loginError:'',
        quizTakerId:'',
        quizTakerObj:'',
        mounted: false,
        userFavoriteQuestions:{},
        notificationList:'',
        notificationDetail:'',
        userCannotCreateError:false,
        asyncActionEndObj: {
            end: false,
            success: false
        }
    },
    getters:{
        getUser(state){
            return state.user
        },
        getQuizTakerId(state){
            return state.quizTakerId
        },
        getEmailVerified(state){
            return state.emailVerified
        },
        getTempUser(state){
            return state.tempUser
        },
        logger(state){
            return state.logger
        },
        onSigningup(state){
            return state.onSigningup
        },
        quizNameIdInSignup(state, getters, rootState){
            return rootState.quiz.quizNameId
        },
        getUserInfo(state){
            return state.userInfo
        },
        getThirdPartyError(state){
            return state.thirdPartyError
        },
        getTokenError(state) {
            return state.tokenError
        },
        getLoginError(state) {
            return state.loginError
        },
        getMounted(state) {
            return state.mounted
        },
        quizTakerObj(state) {
            return state.quizTakerObj
        },
        getNotificationList(state) {
            return state.notificationList
        },
        notificationDetail(state) {
            return state.notificationDetail
        },
        getGoogleLogin(state) {
            return state.googleLogin
        },
        getUserCannotCreateError(state){
            return state.userCannotCreateError
        },
        getAsyncActionEndObj(state) {
            return state.asyncActionEndObj
        },
        getUID(state) {
            return state.UID
        },
        favoriteQuestion(state) {
            return state.favoriteQuestion
        }
    },
    mutations:{
        getUsername(state,item){
            state.username = item
        },
        getEmail(state,item){
            state.email = item
        },
        getEmail2(state,item){
            state.email2 = item
        },
        getCountry(state,item){
            state.country = item
        },
        getPassword(state,item){
            state.password = item
        },
        setUser(state,payload){
            state.user = payload
            if(state.user){
                state.registeredUser = true
                state.UID = state.user.UID
            }
            console.log('set_user', state.user)
        },
        setQuizTakerId(state, payload) {
            state.quizTakerId = payload
            console.log('set QTID',state.quizTakerId)
        },
        setAuthIsReady(state,payload){
            state.authIsReady = payload
        },
        emailVerifiedHandler(state,payload){
            state.emailVerified = payload
        },
        checkEmailHandler(state,payload){
            state.checkedEmail = payload
        },
        setTempUser(state,payload){
            state.tempUser.test = true
            state.tempUser.statusList = payload.status
            state.tempUser.grade = payload.grade
            state.tempUser.level = payload.level
        },
        setTempUserReset(state){
            state.tempUser.test = false
            state.tempUser.statusList = '',
            state.tempUser.grade = '',
            state.tempUser.level = ''
            Cookies.remove('tempKey')
        },
        tempUserTestTrue(state){
            state.tempUser.test = true
        },
        resetQuizKeyStorage(state){
            // this is for log out
            state.UID = null
            state.user = null
            state.emailVerified = null
            state.beingException = false,
            state.reloadForException = false
            state.apiError.django = false
            state.apiError.firebase = false
            state.apiError.ipinfo = false
            state.apiError.any = false
            state.registeredUser = false
        },
        setLogger(state,payload){
            state.logger.actualErrorName = payload.actualErrorName
            state.logger.actualErrorMessage = payload.actualErrorMessage
            state.logger.path = 'vue' + payload.path
            state.logger.message = payload.message
            state.logger.exist = true
        },
        resetLogger(state){
            state.logger.actualErrorName = ''
            state.logger.actualErrorMessage = ''
            state.logger.path = ''
            state.logger.message = ''
            state.logger.exist = false
        },
        setUserInfo(state,payload){
            state.userInfo = payload
        },
        checkBeingException(state,payload){
            if(state.user&&!state.user){
                state.beingException = true
            }
        },
        reloadForExceptionTrueForGeneralApiError(state){
            state.reloadForException = true
        },
        reloadForExceptionTrue(state){
            if(state.user&&!state.user){
                state.reloadForException = true
            }
        },
        reloadForExceptionFalse(state){
            state.reloadForException = false
        },
        handleapiError(state,payload){
            if(payload=='django'){
                state.apiError.django = true
            }
            else if(payload=='firebase'){
                state.apiError.firebase = true
            }
            else if(payload=='ipinfo'){
                state.apiError.ipinfo = true
            }
        },
        checkDjangoError(state,payload){
            if(state.apiError.django){
                router.push({ name: 'ConnectionError' })
            }
            else if(payload=="Network Error"){
                state.apiError.django = true
                state.apiError.any = true
            }else{
                router.push({ name: 'NotFound404' })
            }
        },
        resetDjangoError(state){
            state.apiError.django = false
            state.apiError.any = false
        },
        handleOnSigningup(state){
            state.onSigningup = !state.onSigningup
        },

        updateQuizTaker(state,payload) {
            state.quizTakerObj.grade = payload.grade
            state.quizTakerObj.level = payload.level
        },
        updateQuizTakerMax(state, payload) {
            // this is for session storage only to reduce API hit
            state.quizTakerObj.max_level = state.quizTakerObj.level
            state.quizTakerObj.max_grade = payload
        },
        setTirdPartyloginData(state, payload){
            if(state.tempUser.test){
                state.userInfo={
                    UID: payload.uid,
                    name: payload.displayName,
                    email: payload.email,
                    quiz_taker: [
                        {grade: state.tempUser.grade},
                        {level: state.tempUser.level},
                    ],
                }
            }else{
                state.userInfo={
                    UID: payload.uid,
                    name: payload.displayName,
                    email: payload.email,
                }
            }
        },
        setIpData(state, payload){
            state.userInfo['ip_data'] = [{
                city: payload.city,
                ip: payload.ip,
                loc: payload.loc,
                org: payload.org,
                postal: payload.postal,
                region: payload.region,
                timezone: payload.timezone,
                country: payload.country
            }]
        },
        setTokens(state, payload) {
            state.accessToken =  payload.access_token
            state.refreshToken =  payload.refresh_token
        },
        cookieDelete(state) {
            state.accessToken = ''
            state.refreshToken = ''
        },
        handleGoogleLogin(state) {
            state.googleLogin = !state.googleLogin
        },
        handleTokenError(state) {
            state.tokenError = !state.tokenError
        },
        setLoginError(state,payload) {
            state.loginError = payload
        },
        setMounted(state, payload) {
            state.mounted = payload
            const top = window.scrollY
            if(payload) {
                document.body.style.top = `-${window.scrollY}px`;
                document.body.style.position = 'fixed'
            } else {
                document.body.style.position = ''
                window.scrollTo(0, top)
            }
            
        },
        setQuizTakerObj(state,payload) {
            state.quizTakerObj = payload
            console.log("SET_QTOBJ",state.quizTakerObj)
        },
        testTakenTrue(state) {
            state.user.test_taken = true
        },
        setFavoriteQuestions(state, payload) {
            state.favoriteQuestion= payload
        },
        setUserFavoriteQuestions(state, payload) {
            state.userFavoriteQuestions = payload
            state.userFavoriteQuestions.results = payload.results.map((e) => {
                console.log(typeof e, Object.values(e))
                return Object.values(e)[0]
            })
            console.log("SET_FAVORITE",state.userFavoriteQuestions )
        },
        handleFavoriteQuestion(state, payload) {
            console.log("IN_HABDLE", payload)
            let isDeleted = false
            if(Object.keys(state.userFavoriteQuestions).length) {
                state.userFavoriteQuestions.results.forEach((e, index) => {
                    console.log("LOOP",e.id,payload.id)
                    if(e.id === payload.id) {
                        state.userFavoriteQuestions.results.splice(index,1)
                        isDeleted = true
                        console.log("delete")
                    }
                })
                if(!isDeleted) {
                    state.userFavoriteQuestions.results.unshift(payload)
                    console.log("UNSHIFT", state.userFavoriteQuestions.results)
                }
                // const isExist = state.userFavoriteQuestions.results.find(e => e.id === payload.id )
                // if(isExist) {
                //     state.userFavoriteQuestions.results.splice()
                // }
                // state.userFavoriteQuestions.results.unshift(payload)
                console.log("HANDL",state.userFavoriteQuestions, payload.id)
            }
        },
        setNotificationList(state, payload) {
            state.notificationList = payload
            console.log("set_notification",state.notificationList )
        },
        filterNotificationDetail(state, payload) {
            if(state.notificationList) {
                state.notificationDetail = state.notificationList.find((each) => {
                    return each.slug === payload
                })
            } else {
                console.log("else")
                return ''
            }
        },
        setNotificationDetail(state, payload) {
            state.notificationDetail = payload
        },
        handleUserCannotCreateError(state, payload) {
            state.userCannotCreateError = payload
        },
        setAsyncActionEndObj(state, payload) {
            state.asyncActionEndObj.end = true
            state.asyncActionEndObj.success = payload
            console.log("set", state.asyncActionEndObj)
        },
        resetetAsyncActionEndObj(state) {
            state.asyncActionEndObj.end = false
            state.asyncActionEndObj.success = false
            console.log("reset")
        },
        setUID(state, payload) {
            state.UID = payload
        },
        updateTestTaken(state) {
            state.user.test_taken = true
        }
    },
    actions:{
        async googleLogin(context,payload ){
            const googleloginConf =
            google.accounts.oauth2.initTokenClient({
                client_id: process.env.VUE_APP_GOOGLE_CLIENT_ID,
                scope: 'https://www.googleapis.com/auth/userinfo.email',
                callback: (response) => {context.dispatch("googleloginCallback", response)},
            })
            try{
                googleloginConf.requestAccessToken()
            }
            catch(e){
                console.log("error", e)
                const logger = {
                    message: "in store/signup.googleLogin. couldn't login google user",
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,
                }
                context.commit('setLogger',logger)
                router.push({ name: 'ConnectionError' })
            }
        },
        async googleloginCallback(context, response){
            context.commit('handleGoogleLogin')
            context.commit('setMounted', false)
            const googleAccessToken = response.access_token
            await axios({
                method: 'post',
                url: '/api/user-google/',
                withCredentials: true,
                data: {
                    access_token: googleAccessToken,
                },
                
            })
            .then(async (res) => {
                console.log("then")
                context.commit("setTokens", res.data)     
                await context.dispatch("getUserData")
                if(context.state.tempUser.test) {
                    const quizTaker = {
                        user_UID: context.state.user.UID,
                        quiz_taker: {
                            grade: context.state.tempUser.grade,
                            level: context.state.tempUser.level,
                            statusList: context.state.tempUser.statusList
                        }
                    }
                    context.dispatch('quizTakerUpdateForInitialization', quizTaker)
                }
            })
            .catch((e) => {
                const logger = {
                    message: "in store/signup.googleLoginCallback. couldn't execute google callback",
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,

                }
                commit('setLogger',logger)
                router.push({ name: 'ConnectionError' })
            })
        },
        async getUserData(context) {
            // context.commit('setIsLoading', true, {root:true})
            const accessToken = context.state.accessToken
            if(accessToken) {
                try{
                    const UID = jwt_decode(accessToken).user_id
                    if(UID) {
                        await axios.get( `/api/user/${UID}`,{
                            // withCredentials: true,
                            headers: {
                                "Authorization": 'JWT ' + `${accessToken}`,
                                "Content-Type":"aplication/json"
                            }
                        })
                        .then((res) => {

                            context.commit('setUser',res.data)
                            context.commit('emailVerifiedHandler',res.data.is_active)
                            context.commit('setAuthIsReady',true)
                            // context.commit('setIsLoading', false, {root:true})
                            if(context.state.googleLogin){
                                context.commit('setIsLoading', true, {root:true})
                                console.log("PUSH")
                                router.push({ name: 'Account' })
                                context.commit('handleGoogleLogin')
                            }
                            context.commit('setMounted',true)
                        })
                        .catch(async (e) => {
                            
                            if(context.dispatch('handleTokenError',e.response.data)) {
                                const newPayload = {
                                    fun: 'getUserData',
                                    args: UID
                                }
                                await context.dispatch('retryFetch',newPayload)
                            } else {
                                return
                            }
                        })
                    }
                } catch {
                    context.commit('setAuthIsReady',true)
                    context.commit('setMounted', true)
                }
            } else {
                context.commit('resetQuizKeyStorage')
                context.commit('setAuthIsReady',true)
                context.commit('setMounted', true)
            }
        },
        async login(context, payload) {

            const email = payload.email
            const password = payload.password
            await axios({
                method: 'post',
                url: '/api/auth/login/',
                withCredentials: true,
                data: {
                    email: email,
                    password: password
                },
            })
            .then((res) => {
                const UID = res.data.user.pk
                context.commit('handleGoogleLogin')
                context.commit("setTokens", res.data)                
                context.dispatch("getUserData", UID)

            })
            .catch((e) =>{
                context.commit('setLoginError',e.response.data)
            })       
        },
        async logout(context){
            try{
                await axios({
                    method: 'post',
                    url: '/api/auth/logout/',
                    withCredentials: true,
                })
                context.commit('setUser',null)
                context.commit('resetQuizKeyStorage')
                context.commit('cookieDelete')
                router.push({ name: 'Home' })
            } catch(e) {
                let logger = {
                    message: "in store/signup.logout. couldn't logout",
                    name: window.location.pathname,
                    actualErrorName: e.code,
                    actualErrorMessage: e.message,
                }
                context.commit('setLogger',logger)
                router.push({ name: 'ConnectionError' })
            }
        },
        async GetAccessTokenFromRefreshToken(context) {

            if(context.state.refreshToken) {
                try{
                    await axios({
                        method: 'post',
                        url: '/api/auth/token/refresh/',
                        data: {
                            'refresh':context.state.refreshToken
                        }
                    })
                    .then((res) => {
                        const token = {
                            access_token:res.data.access,
                            refresh_token:res.data.refresh
                        }
                        context.commit("setTokens", token)   
                    })
                }
                catch(e){
                    context.commit('setAuthIsReady',true)
                    context.commit("cookieDelete")
                    throw("no valid token")        
                }
            } else {
                context.commit('setAuthIsReady',true)
                throw("no valid token")       
            }       
        },
        getAccessTokenFromCookies(state) {
            return state.accessToken
        },
        async retryFetch(context, payload) {
            // when get returned invalid token error with access_token, 
            // try to get accesss_token with refresh_token, and try again.
            // the payload must include a function as func you want to retry 
            // and arguments as args for it.
            await context.dispatch("GetAccessTokenFromRefreshToken")
            .then(async () => {
                const fun = payload.fun
                const args = payload.args
                await context.dispatch(fun,args)
            })
        },
        async quizTakenChange({state}) {
            if(state.user.quiz_taken) {
                
            }
        },
        async emailVerify(context,payload) {
            await axios.post( '/api/email-verify/',{
                withCredentials: true,
                data:payload,
                headers: {
                    "Content-Type":"aplication/json"
                }
            })
            .then(async (res) => {
                if(res.data.verification) {
                    context.commit("setTokens",res.data.tokens)
                    context.dispatch("getUserData")
                    .then(() => {
                      router.push({ name: 'Account' })
                    })
                }  else if(!res.data.verification) {
                    return
                }
            })
            .catch((e) => {
                let logger = {
                    message: "in store/signup.emailVerify. couldn't verify user",
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,

                }
                commit('setLogger',logger)
                commit("checkDjangoError", e.message)
            })
        },
        async userCreate(context, payload) {
            // "payload includes username, email. password"
            await axios({
                method:"post",
                url: "api/user-create/",
                data: payload
            })
            .then(res => {
                console.log("RESS",res.data,res.data.quiz_taker_id)
                context.commit('setQuizTakerId',res.data.quiz_taker_id)
                context.commit('setUID', res.data.UID)
            })
            .catch((e) =>{
                context.commit('setIsLoading', false, {root:true})
                context.commit('handleUserCannotCreateError', true)
                let logger = {
                    message: "in store/signup.userCreate. couldn't create user",
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,
                }
                context.commit('setLogger',logger)
                router.push({ name: 'ConnectionError' })
            })            
        },
        async quizTakerUpdateForInitialization(context, payload){
            
            await axios({
                method: 'post',
                url: '/api/quiz-taker-update/',
                withCredentials: true,
                data: {
                    user_UID: payload.user_UID,
                    quiz_taker: payload.quiz_taker

                },
                
            })
            .then((res) => {
                console.log("INIQR", res.data)
                context.commit('setTempUserReset')
                context.commit('setQuizTakerObj', res.data)
            })
            .catch((e) => {
                let logger = {
                    message: "in store/signup.quizTakerUpdateForInitialization. couldn't create quiz taker",
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,
                }
                context.commit('setLogger',logger)
                context.commit("checkDjangoError", e.message)
            })
        },
        async SendChangePassword(context, payload) {
            console.log("SEND", payload)
            await axios.post( '/api/user-send-password-change/',{
                withCredentials: true,
                data: payload,
                headers: {
                    "Content-Type":"aplication/json"
                }
            })
            .catch((e) => {
                let logger = {
                    message: "in store/signup.password_reset. couldn't change password",
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,

                }
                commit('setLogger',logger)
                commit("checkDjangoError", e.message)
            })
        },
        async sendEmailVerify(context, payload) {
            console.log("SEND", payload)
            await axios.post( '/api/send-email-verify/',{
                UID:payload,
                headers: {
                    "Content-Type":"aplication/json"
                }
            })
            .then((res) => {
                context.commit('setAsyncActionEndObj', res.data.sent)
                console.log("RES", res.data)
            })
            .catch((e) => {
                let logger = {
                    message: "in store/signup.password_reset. couldn't change password",
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,

                }
                commit('setLogger',logger)
                commit("checkDjangoError", e.message)
            })
        },
        async testTakenUpdate(context, payload) {
            // this set user.quiz_taken = true, date_offset and quiz_taken_at
            
            await axios.patch( '/api/set-test-taken/',{
                data: payload,
                headers: {
                    "Content-Type":"aplication/json"
                }
            })
            .catch(async(e) => {
                if(context.dispatch('handleTokenError',e.response.data)) {
                    const newPayload = {
                        fun: 'testTakenUpdate',
                        args: payload
                    }
                    await context.dispatch('retryFetch',newPayload)
                } else {
                    let logger = {
                        message: "in store/signup.password_reset. couldn't update quiz_taken",
                        path: window.location.pathname,
                        actualErrorName: e.name,
                        actualErrorMessage: e.message,
                    }
                    commit('setLogger',logger)
                    commit("checkDjangoError", e.message)
                }
            })
        },
        handleTokenError(context, payload) {
            if(payload.message==="Your token is expired") {
                return true
            } else {
                return false
            }
        },
        async getUserFavoriteQuestions({state, commit}) {
            const url = `api/board/favorite-question-list?UID=${state.user.UID}`
            await axios.get(url)
            .then((res) => {
                commit('setUserFavoriteQuestions', res.data)
            })
            .catch((e) => {
                console.log("ERROE", e)
            })
        },
        async getFavoriteQuestion({ state, commit }){
            state.favoriteQuestion = null
            console.log("GET",'question' in state.userFavoriteQuestions)
            const questionId = state.userFavoriteQuestions
            if(state.user&&'question' in state.userFavoriteQuestions){
                await axios
                .get(`/api/board/question-favorite?question_id=${questionId.question}`)
                .then(response => {
                    commit('setFavoriteQuestions', response.data)
                    })
                .catch(e => {
                    let logger = {
                        message: "in store/signup.getFavoriteQuestion. couldn't get favoriteQuestion ",
                        path: window.location.pathname,
                        actualErrorName: e.name,
                        actualErrorMessage: e.message,
                    }
                    commit('setLogger',logger)
                    commit("checkDjangoError", e.message)
                
                })
                
            } else {
                console.log("ELSE")
            }
        },

        async checkEmail(context,email){
            try {
                const result = await axios({
                    method: 'post',
                    url: '/api/user-exists/',
                    data: {
                        "email": email,

                    },
                })
                .then(res => {return res.data})
                if (result.exists){
                    context.commit('checkEmailHandler',false)
                }else{
                    context.commit('checkEmailHandler',true)
                }
            }catch(e){
                let logger = {
                    message: "in store/signup.checkEmail. couldn't check Email",
                    name: window.location.pathname,
                    actualErrorName: e.code,
                    actualErrorMessage: e.message,
                }
                // context.commit('setLogger',logger)
                // router.push({ name: 'ConnectionError' })
            }
        },
        
        updateQuizTakerAction({state, commit, getters},payload){
            commit('updateQuizTaker',payload);
            for(let i of getters.quizNameIdInSignup){
                if(i.id == payload.grade){
                    if(state.gradeDict[state.quizTakerObj.max_grade] < state.gradeDict[i.name]){
                        commit('updateQuizTakerMax',i.name);
                        break
                    }
                    else if(state.gradeDict[state.quizTakerObj.max_grade] == state.gradeDict[i.name]){
                        if(state.quizTakerObj.max_level < payload.level){
                            commit('updateQuizTakerMax',i.name);
                            break
                        }
                    }
                }
            }
        },

        async createLog(context,payload){
            if(context.state.logger.exist) {
                await axios
                .post('/api/loggers-create',{
                    message: payload.message,
                    path: payload.path,
                    actualErrorName: payload.actualErrorName,
                    actualErrorMessage: payload.actualErrorMessage,
                })
                .catch((e) => {
                    let logger = {
                        message: "in store/signup.createLog. couldn't create log",
                        name: window.location.pathname,
                        actualErrorName: e.code,
                        actualErrorMessage: e.message,
                    }
                    context.commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
                });
                context.commit('resetLogger')
            }
        },
        async getQuizTaker({ state , commit }, payload){
            await axios({
                method: 'get',
                url: `/api/quiz-taker-detail/${state.user.UID}`,
            })
            .then((res) => {
                commit('setQuizTakerObj', res.data)
                commit('setQuizTakerId', res.data.id)
            })
            .catch((e) => {
                let logger = {
                    message: "in store/quiz.createAndDeleteMyQuiz. couldn't create And Delete MyQuiz",
                    name: window.location.pathname,
                    actualErrorName: e.code,
                    actualErrorMessage: e.message,
                }
                context.commit('setLogger',logger)
                router.push({ name: 'ConnectionError' })
            });
        },
        
        aurhStatusChange(context) {
            context.commit('setAuthIsReady',true)
        },

        async getNotificationList({commit}) {
            await axios.get( '/api/notification/list')
            .then((res) => {
                commit('setNotificationList',res.data)
            })
            .catch((e) => {
                let logger = {
                    message: "in store/signup.getNotificationList. couldn't get notification -list",
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,

                }
                commit('setLogger',logger)
                commit("checkDjangoError", e.message)
            })
        },
        async getNotificationDetail({state,commit},payload) {
            if(state.notificationList) {
                commit('filterNotificationDetail',payload)
            } else {
                await axios.get(`/api/notification/detail/${payload}`)
                .then((res) => {
                    commit('setNotificationDetail',res.data)
                })
                .catch((e) => {
                    let logger = {
                        message: "in store/signup.getNotificationDetail. couldn't get notification - detail",
                        path: window.location.pathname,
                        actualErrorName: e.name,
                        actualErrorMessage: e.message,

                    }
                    commit('setLogger',logger)
                    commit("checkDjangoError", e.message)
                })
            }
        },
    }
}