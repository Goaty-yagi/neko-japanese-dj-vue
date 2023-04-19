import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import SecureLS from "secure-ls";
import Cookies from 'js-cookie'
import  signup  from './modules/signup'
import  board  from './modules/board'
import  quiz  from './modules/quiz'

const ls = new SecureLS({ isCompression: false,useSessionStore: true });

let getDefaultState = () => {
  return {
    isLoading: false,
    smallIsLoading: false,
    id: 1,
    field:'',
    num:3,
    questions:[],
    quizzes:[],
    randomURL:'',
    test:null,
    notice:false,
    step:1,
    showModal: false,
    fixedScroll: false,
  }}


export default createStore({
  modules: {
    signup,
    board,
    quiz
  },
  state: getDefaultState(),
  plugins: [
    createPersistedState({
      key: 'quizkey',  // 設定しなければ'vuex'
      paths: [
        "signup.emailVerified",
        "signup.registeredUser",
        "signup.myQuestion",
        "signup.myQuizInfo",
      ],  // 保存するモジュール：設定しなければ全部。
      storage: {
          getItem: key => ls.get(key),
          setItem: (key, value) => ls.set(key, value),
          removeItem: key => ls.remove(key),
      }
    }),
    createPersistedState({
      key: 'quiz-session',
      paths:[
        "board.centerTag",
        "quiz.quizNameId",
        "quiz.fieldNameId",
        ],
        storage:
        {
          getItem: key => ls.get(key),
          setItem: (key, value) => ls.set(key, value),
          removeItem: key => ls.remove(key),
        },
    }),
    createPersistedState({
        key: 'tempKey',
        paths: [
          "signup.tempUser",
          "signup.userInfo",
          "signup.beingException",
          "signup.reloadForException",
        ],
        storage:{
          getItem:(key) => Cookies.get(key),
          setItem:(key,value) =>
            Cookies.set(key,value, {expires: 3, secure: true}),
          removeItem:(key) => Cookies.remove(key),
        }
      }),
      createPersistedState({
        key: 'tokens',
        paths: [
          "signup.accessToken",
          "signup.refreshToken",
        ],
        storage:{
          getItem:(key) => Cookies.get(key),
          setItem:(key,value) =>
            Cookies.set(key,value, {secure: false}),
          removeItem:(key) => Cookies.remove(key),
        }
      })
  ],
  getters:{
    questions2:(state) => state.questions,
    quizzes2:(state) => state.quizzes,
    showModal:(state) => state.showModal,
    fixedScroll:(state) => state.fixedScroll,
    smallIsLoading:(state) => state.smallIsLoading
  },
  mutations: {
    setIsLoading(state, status) {
      state.isLoading = status
      const top = window.scrollY
      if(status) {
        document.body.style.top = `-${window.scrollY}px`;
        document.body.style.position = 'fixed'
      } else {
        document.body.style.position = ''
        window.scrollTo(0, top)
        }
    },
    setSmallIsLoading(state, status) {
      state.smallIsLoading = status
    },
    reset(state) {
      Object.assign(state, getDefaultState())
    },
    getURLs(state,item){
      state.num = item.num
      state.id = item.status
      state.test = item.test
      state.randomURL = `/quiz/${state.id}`
    },
    
    testHandler(state){
      state.test = false
    },
    noticeHandler(state){
      state.notice = true
    },
    noticeOff(state){
      state.notice = false  
    },
    addStep(state){
      state.step += 1
    },
    stepClear(state){
      state.step = 1
    },
    showModalTrue(state){
      state.showModal = true
    },
    showModalFalse(state){
      state.showModal = false
    },
    fixedScrollTrue(state){
      state.fixedScroll = true
      console.log("scroll-status-changed",state.fixedScroll)
    },
    fixedScrollFalse(state){
      state.fixedScroll = false
    },
    handleFixedScroll(state){
      state.fixedScroll = !state.fixedScroll
    }
  },
})
