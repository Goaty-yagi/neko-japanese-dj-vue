import store from '..'
import {router} from "@/main.js"
import axios from 'axios'


let getDefaultState = () => {
    return {
        isLoading: false,
        quizID: 1,
        countUpDict:{
            questionID: '',
            answerID: '',
            questionType:''
        },
        userStatusDict:{
            status:'',
            grade:'',
            quizTaker:'',
            isCorrect:0,
            isFalse:0
        },
        currentQuizMode:{
            myQuiz: false,
            practice: false,
            test: false
        },
        gradeForConvert:'',
        numOfQuiz: 3,
        questionField: [1,2],
        level: 1,
        questions:[],
        quiz:[],
        quizNameId:'',
        fieldNameId:'',
        questionTypeId:'',
        statusNameId:'',
        randomURL:'',
        test:null,
        notice:false,
        step:1,
        // onQuiz is for footer view 
        onQuiz: false,
        myQuiz: '',
        myQuestion: ''
    }
}

export default {
    namespace: true,
    state: getDefaultState(),
    getters:{
        questions:(state) => state.questions,
        quiz:(state) => state.quiz,
        quizNameId:(state) => state.quizNameId,
        fieldNameId:(state) => state.fieldNameId,
        statusNameId:(state) => state.statusNameId,
        gradeForConvert:(state) => state.gradeForConvert,
        currentQuizMode:(state) => state.currentQuizMode,
        questionTypeId:(state) => state.questionTypeId,
        myQuiz:(state) => state.myQuiz,
        myQuestion:(state) => state.myQuestion,
        quizTaker(state, getters, rootState){
            try{
                return rootState.signup.quizTakerObj.id
            }catch{
                return null
            }
        },
        quizTakerObject(state, getters, rootState){
            try{
                return rootState.signup.quizTakerObj
            }catch{
                return null
            }
        },
        quizID(state, getters, rootState){
            try{
                return rootState.signup.quizTakerObj.grade
            }catch{
                return null
            }
        },
    },
    mutations:{
        getRandomQuestion(state,array){
            for ( let k =0; k < array.length; k++){
                for (let i = array[k].answer.length - 1; i >= 0; i--) {
                    let r = Math.floor(Math.random() * (i + 1))
                    let tmp = array[k].answer[i]
                    array[k].answer[i] = array[k].answer[r]
                    array[k].answer[r] = tmp
                }
            }
            return array
        },
        questionsShuffle(state){
            for ( let k =0; k < state.questions.length; k++){
                for (let i = state.questions[k].answer.length - 1; i >= 0; i--) {
                    let r = Math.floor(Math.random() * (i + 1))
                    let tmp2 = state.questions[k].answer[i]
                    state.questions[k].answer[i] = state.questions[k].answer[r]
                    state.questions[k].answer[r] = tmp2
                }
            }
            for ( let k =0; k < state.questions.length; k++){
                let random = Math.floor(Math.random() * (k + 1))
                let tmp1 = state.questions[k]
                state.questions[k] = state.questions[random]
                state.questions[random] = tmp1
            }
        },
        setQuestions:(state,questions) => (state.questions = questions),
        setTestQuestions:(state,questions) => (state.questions = questions, console.log('set_QUESTIONS', state.questions)),
        getQuiz(state, payload){
            state.quiz = payload
        },
        setAnswerAndQuestionID(state,IDs){
            state.countUpDict.questionID = IDs.questionID
            state.countUpDict.answerID = IDs.answerID
            state.countUpDict.questionType = IDs.questionType
        },
        getQuizInfo(state, quizInfo){
            state.questionField = []
            state.quizID = quizInfo.quizID
            state.numOfQuiz = quizInfo.quizNum
            state.quizID = quizInfo.quizId
            if(quizInfo.fieldId){
                state.questionField = quizInfo.fieldId
            }
            state.numOfQuiz = quizInfo.quizNum
            console.log("GET_QUIZ_INFO", quizInfo)
        },
        getTestQuizInfo(state, quizInfo){
            state.quizID = quizInfo.quizId
            state.level = quizInfo.level
        },
        setQuizNameId(state, payload){
            state.quizNameId = payload
        },
        setFieldNameId(state, payload){
            state.fieldNameId = payload
        },
        setStatusNameId(state, payload){
            state.statusNameId = payload
        },
        setQuestionTypeId(state, payload){
            state.questionTypeId = payload
        },
        getUserStatusInfo(state, payload){
            state.userStatusDict.status = payload.status
            state.userStatusDict.isCorrect = payload.isCorrect
            state.userStatusDict.isFalse = payload.isFalse
        },
        setQuizID(state, payload){
            state.userStatusDict.grade = payload
            console.log("SET_QUIZ_ID", state.userStatusDict.grade)
        },
        setQuizTakerID(state, payload){
            state.userStatusDict.quizTaker = payload
            console.log("SET_QUIZ_TAKER", state.userStatusDict.quizTaker)
        },
        convertGradeFromIntToID(state, payload){
            for(let i of state.quizNameId){
                if(i.name == payload){
                    state.gradeForConvert = i.id
                }
            }
        },
        convertGradeFromIDToInt(state, payload){
            for(let i of state.quizNameId){
                if(i.id == payload){
                    state.gradeForConvert = i.name
                }
            }
        },
        onQuizTrue(state){
            state.onQuiz = true
        },
        onQuizFalse(state){
            state.onQuiz = false
        },
        handleCurrentQuizMode(state,payload){
            for (let i of state.currentQuizMode){
                if(i == payload){
                    state.currentQuizMode[i] = true
                }
            }
        },
        setQuizIdAndlevel(state, getters){
            state.quizID = getters.grade
            state.level = getters.level
        },
        setMyQuiz(state,payload) {
            state.myQuiz = payload
            state.myQuestion = payload.my_question
            console.log("MY_QUIZ_SET", state.myQuiz)
        },
        deleteMyQuestion(state,payload){
            state.myQuestion = state.myQuestion.filter(item =>{
                return (item.question.id !=payload)
            })
            console.log("deleted",state.myQuestion)
        },
        addMyQuestion(state,payload){
            state.myQuestion.push(payload)
        },
    },
    actions:{
        async getQuestions({ state, commit,getters }){
            console.log("GQL1")
            try{
                state.questions = []
                state.quiz = []
                if(state.questionField[0]){
                    var response = await axios.get(`/api/quizzes-questions/?quiz=${state.quizID}&num=${state.numOfQuiz}&field=${state.questionField}`)
                }else{
                    var response = await axios.get(`/api/quizzes-questions/?quiz=${state.quizID}&num=${state.numOfQuiz}`)
                }
                commit('setQuizTakerID',getters.quizTaker)
                commit('getQuiz',response.data[0])
                commit('setQuizID',response.data[0].name)
                response.data.shift()
                commit('getRandomQuestion',response.data)
                commit('setQuestions',response.data);
            } catch(e) {
                let logger = {
                    message: "in store/quiz.getquestions. couldn't get questions",
                    name: window.location.pathname,
                    actualErrorName: e.code,
                    actualErrorMessage: e.message,
                }
                commit('setLogger',logger)
                router.push({ name: 'ConnectionError' })
            }
        },
        async getQuestionFromMyQuestion({ state, commit,getters }, payload) {
            const response = await axios
              .get(`/api/my-question-list?ids=${payload}`)
              .catch((e) => {
                let logger = {
                  message:
                    "in components/quiz_components/MyQuiz/MyQuizPracticet/getQuestionFromMyQuestion. couldn't get QuestionFromMyQuestion",
                  path: window.location.pathname,
                  actualErrorName: e.name,
                  actualErrorMessage: e.message,
                };
                commit("setLogger", logger);
                commit("setIsLoading", false);
                router.push({ name: "ConnectionError" });
              });
              console.log("MQL",response.data)
              commit('getRandomQuestion',response.data)
              commit('setQuestions',response.data);
              commit('setQuizTakerID',getters.quizTaker)
              commit('setQuizID',response.data[0].quiz)
          },
        async getQuizNameId({ state, commit }){
            if(state.quizNameId==false){
                let response = await axios
                .get("/api/quizzes-name-id/")
                .catch((e) => {
                    let logger = {
                        message: "in store/quiz.getQuizNameId. couldn't get QuizNameId",
                        name: window.location.pathname,
                        actualErrorName: e.code,
                        actualErrorMessage: e.message,
                    }
                    context.commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
                });
                commit('setQuizNameId',response.data)
            }
        },
        async getFieldNameId({ state, commit }){
                let response = await axios
                .get("/api/field-list/")
                .catch((e) => {
                    let logger = {
                        message: "in store/quiz.getFieldNameId. couldn't get FieldNameId",
                        name: window.location.pathname,
                        actualErrorName: e.code,
                        actualErrorMessage: e.message,
                    }
                    context.commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
                });
                commit('setFieldNameId',response.data)
                commit('setIsLoading', false,{root:true})
            // }
        },
        async getStatusNameId({ state, commit }){
            if(state.statusNameId==false){
                commit('setIsLoading', true, {root:true})
                let response = await axios
                .get("/api/status-list/")
                .catch((e) => {
                    let logger = {
                        message: "in store/quiz.getStatusNameId. couldn't get StatusNameId",
                        name: window.location.pathname,
                        actualErrorName: e.code,
                        actualErrorMessage: e.message,
                    }
                    context.commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
                });
                commit('setStatusNameId',response.data)
                commit('setIsLoading', false,{root:true})
            }
        },
        async getQuestionTypeId({ state, commit }){
            if(state.questionTypeId==false){
                commit('setIsLoading', true, {root:true})
                let response = await axios
                .get("/api/question-types")
                .catch((e) => {
                    let logger = {
                        message: "in store/quiz.getQuestionTypeId. couldn't get QuestionTypeId",
                        name: window.location.pathname,
                        actualErrorName: e.code,
                        actualErrorMessage: e.message,
                    }
                    context.commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
                });
                commit('setQuestionTypeId',response.data)
                commit('setIsLoading', false,{root:true})
            }
        },
        async getTestQuestions({ state, commit, getters }){
            // need things for non login

            if(getters.quizID!=null){
                // quiz_taker exist
                commit('setIsLoading', true, {root:true})
                let response = await axios
                .get(`/api/quizzes-tests/?quiz=${state.quizID}&level=${state.level}`)
                .catch((e) => {
                    let logger = {
                        message: "in store/quiz.getTestQuestions-first. couldn't get TestQuestions",
                        name: window.location.pathname,
                        actualErrorName: e.code,
                        actualErrorMessage: e.message,
                    }
                    context.commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
                });
                console.log("get_tsest_quiz", response.data)
                commit('getQuiz',response.data[0])
                commit('setQuizTakerID',getters.quizTaker)
                commit('setQuizID',response.data[0].name)
                response.data.shift()
                commit('getRandomQuestion',response.data)
                commit('setTestQuestions',response.data);
                commit('setIsLoading', false,{root:true})
            }else{
                // first questions in init
                commit('setIsLoading', true, {root:true})
                const superEasyGradeId = '1' //this depends on when the grade created. if first, should be 1
                const easiestLevel = '1'// it is starting point for init quiz
                let response = await axios
                .get(`/api/quizzes-tests/?quiz=${superEasyGradeId}&level=${easiestLevel}`)
                .catch((e) => {
                    let logger = {
                        message: "in store/quiz.getTestQuestions-second. couldn't get TestQuestions",
                        name: window.location.pathname,
                        actualErrorName: e.code,
                        actualErrorMessage: e.message,
                    }
                    commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
                });
                commit('getQuiz',response.data[0])
                response.data.shift()
                commit('getRandomQuestion',response.data)
                commit('setTestQuestions',response.data);
                commit('setIsLoading', false,{root:true})
            }
        },
        async countUpAnswerAndQuestion({ state , commit }, payload){
            commit('setAnswerAndQuestionID',payload)
            if(state.countUpDict.questionType!=4){
                await axios
                .patch(`/api/answers-count/?answer=${state.countUpDict.answerID}&question=${state.countUpDict.questionID}`)
                .catch((e) => {
                    let logger = {
                        message: "in store/quiz.countUpAnswerAndQuestion. couldn't countUp AnswerAndQuestion",
                        name: window.location.pathname,
                        actualErrorName: e.code,
                        actualErrorMessage: e.message,
                    }
                    context.commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
                });
            }
            
        },
        async userStatusPost({ state , commit }, payload){
            console.log("USP",state.userStatusDict,payload)
            commit('getUserStatusInfo',payload)
            await axios({
                method: 'post',
                url: '/api/user-status/',
                data: {
                    status: state.userStatusDict.status,
                    grade: state.userStatusDict.grade,
                    quiz_taker: state.userStatusDict.quizTaker,
                    is_correct: state.userStatusDict.isCorrect,
                    is_false: state.userStatusDict.isFalse,
                }
            })
            .catch((e) => {
                let logger = {
                    message: "in store/quiz.userStatusPost. couldn't post userStatus",
                    name: window.location.pathname,
                    actualErrorName: e.code,
                    actualErrorMessage: e.message,
                }
                context.commit('setLogger',logger)
                router.push({ name: 'ConnectionError' })
            });
        },
        async createAndDeleteMyQuiz({ state , commit }, payload){
            console.log("in_DELETE",payload)
            await axios({
                method: 'post',
                url: '/api/my-question/',
                data: {
                    my_quiz: payload.myQuiz,
                    question: payload.question
                }
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
        async convertGradeFromIntToIDForNewUser({ state , dispatch, commit }, payload){
            if(!state.quizNameId){
                await dispatch('getQuizNameId')
            }
            commit('convertGradeFromIntToID', payload)
        },
        async getMyQuiz({ state ,dispatch, commit }, payload) {
            //respons no include answer. this is just for listing purpose
            await axios({
                method: 'get',
                url: `/api/my-quiz-detail/${payload}`,
            })
            .then((res) => {
                commit('setMyQuiz', res.data)
                console.log("CHECK_MY_QUESTUONB", res.data)
            })
            .catch((e) => {
                let logger = {
                    message: "in store/quiz.getMyQuiz. couldn't get MyQuiz",
                    name: window.location.pathname,
                    actualErrorName: e.code,
                    actualErrorMessage: e.message,
                }
                commit('setLogger',logger)
                router.push({ name: 'ConnectionError' })
            });
        },
        setQuizIdAndlevelAction({ state , commit, getters }){
            commit('setQuizIdAndlevel', getters.quizTakerObject)
        },
    }
}