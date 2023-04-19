import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Contents from '../views/footer-contents/Contents.vue'
import Faq from '../views/footer-contents/Faq.vue'
import Quiz from '../views/Quiz.vue'
import QuizTest from '../views/quiz/QuizTest.vue'
import QuizTestInit from '../views/quiz/QuizTestInit.vue'
// import QuizPractice from '../views/quiz/QuizPractice.vue'
import QuizHome from '../views/quiz/QuizHome.vue'
import MyQuiz from '../views/quiz/MyQuiz.vue' 
import NotFound from '../views/not-found/NotFound.vue'
import NotFound404 from '../views/not-found/NotFound404.vue'
import ConnectionError from '../views/not-found/ConnectionError.vue'
import Signup from '../views/Signup.vue'
import Account from '../views/Account.vue'
import Dboard from '../views/Dboard.vue'
import Login from '../views/Login.vue'
import Policy from '../views/Policy.vue'
import Community from '../views/Community.vue'
import BoardDetail from '../views/BoardDetail.vue'
import RelatedQuestion from '../views/board/RelatedQuestion.vue'
import BoardAccount from '../views/board/BoardAccount.vue'
import TermsAndConditions from '../views/footer-contents/TermsAndConditions.vue'
import Privacy from '../views/footer-contents/Privacy.vue'
import Enquire from '../views/footer-contents/Enquire.vue'
import EmailVerification from '../views/EmailVerification.vue'
import PasswordReset from '../views/authentications/PasswordReset.vue'
import NotificationDetail from '../views/NotificationDetail.vue'
import NotificationList from '../views/NotificationList.vue'

import store from '../store'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/about',
    name: 'About',
    component: About,
  },
  {
    path: '/contents/:key',
    name: 'Contents',
    component: Contents,
  },
  {
    path: '/faq',
    name: 'Faq',
    component: Faq,
  },
  {
    path: '/quiz-home',
    name: 'QuizHome',
    component: QuizHome,
    meta:{login:true,beingException:true}
    
  },
  {
    path: '/quiz-test',
    name: 'QuizTest',
    component: QuizTest,
    meta:{login:true}
  },
  {
    path: '/quiz-test-init',
    name: 'QuizTestInit',
    component: QuizTestInit,
    meta:{quizTook:true,emailVerified:true,compUser:true,beingException:true}
  },
  // {
  //   path: '/quiz-practice',
  //   name: 'QuizPractice',
  //   component: QuizPractice,
  //   meta:{login:true,beingException:true}
  // },
  {
    path: '/my-quiz',
    name: 'MyQuiz',
    component: MyQuiz,
    meta:{login:true,beingException:true}
  },
  {
    path: '/dboard',
    name: 'Dboard',
    component: Dboard,
    meta:{isStaff:true}
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
    meta:{emailVerified:true,compUser:true,beingException:true}
  },
  {
    path: '/account',
    name: 'Account',
    component: Account,
    meta:{login:true,beingException:true}
  },
  {
    path: '/board',
    name: 'Community',
    component: Community,
  },
  {
    path: '/board/related',
    name: 'RelatedQuestion',
    component: RelatedQuestion,
  },
  {
    path: '/board/account',
    name: 'BoardAccount',
    component: BoardAccount,
    meta:{login:true,emailVerified:true,beingException:true}
  },
  {
    path: '/board-detail/:slug',
    name: 'BoardDetail',
    component: BoardDetail,
  },
  {
    path: '/note-detail/:slug',
    name: 'NotificationDetail',
    component: NotificationDetail,
  },
  {
    path: '/note-list/',
    name: 'NotificationList',
    component: NotificationList,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta:{emailVerified:true,compUser:true,beingException:true}
  },
  {
    path: '/policy',
    name: 'Policy',
    component: Policy,
  },
  {
    path: '/terms-and-conditions',
    name: 'terms-and-conditions',
    component: TermsAndConditions,
  },
  {
    path: '/privacy',
    name: 'Privacy',
    component: Privacy,
  },
  {
    path: '/enquire',
    name: 'Enquire',
    component: Enquire,
  },
  {
    path: '/verification/:token',
    name: 'EmailVerification',
    component: EmailVerification,
  },
  {
    path: '/password-change/:token',
    name: 'PasswordReset',
    component: PasswordReset,
  },
  { 
    path: '/notfound',
    name: 'NotFound',
    component: NotFound,
  },
  { 
    path: '/notfound404',
    name: 'NotFound404',
    component: NotFound404,
  },
  { 
    path: '/connection-error',
    name: 'ConnectionError',
    component: ConnectionError,
  },
  { 
    path: '/:catchAll(.*)',
    name: 'catchAll',
    component: NotFound,
    // meta:{emailVerified:true}
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
const scrollTop = (() => {  
    window.scrollTo({
        top: 0,
    });
})

function isEmpty(obj){
  console.log("OBJ",Object.keys(obj))
  return !Object.keys(obj).length;
}


function setIsLoading(){
  store.commit('setIsLoading', true)
}

async function initialization() {
  console.log("START_USER_GET")
  await store.dispatch("getUserData")
}

async function getQuizTaker() {
  console.log("GQTO",store.state.signup.quizTakerObj)
  if(!store.state.signup.quizTakerObj) {
    console.log("GQTO2")
    await store.dispatch("getQuizTaker")
  }
}
async function getMyQuiz(user) {
  console.log("MY_QUIZ",store.state.quiz.myQuiz)
  if(!store.state.quiz.myQuiz) {
    await store.dispatch("getMyQuiz",user)
  }
}
async function getUserFavoriteQuestions(user) {

  if(isEmpty(store.state.signup.userFavoriteQuestions)&&user) {
    await store.dispatch("getUserFavoriteQuestions")
  }
}
async function getAnsweredQuestions() {
  console.log("GET_ANSWEREd")
  await store.dispatch("getAnsweredQuestion")
}
async function getUserTag(user) {
  console.log("GET_TAG")
  if(!store.state.board.userTags||store.state.board.userTags.length < 3) {
    await store.dispatch("getUserTag",user)
  }
}
async function getDetail(slug) {
  console.log('GD')
  await store.dispatch('getDetail', slug)
}


// state
const mountedComponentsList = ['Account','BoardAccount','BoardDetail']


// there are 6 types of way, 
// 1 is not non registered user 
// => can go community except Aaccount and some error or login
// 2 is not registered but took init tes
// => the same as avobe but not include quiz-init
// 3 is registerd firebase but not djangoUser(comes from error)
// => can only go to connection error
// 4 is registered complitely but not emailVerified
// => can't go signup, login, Caccount, quiz-init
// 5 registered user
// => can't go signup,login quiz-init
// 6 can't go quiz-test if took already
  router.beforeEach(async(to, from, next) => {
    // scrollTop()
    // initial setting
    setIsLoading()
    if(!store.state.signup.user) {
      await initialization()
    }
    // this is for 1
    if (to.matched.some(record => record.meta.login) && !store.state.signup.user) {
      next({ name: 'Login' });

    }
    // this is for 2
    else if(to.matched.some(record => record.meta.quizTook)&&store.state.signup.tempUser.test){
        next({ name: 'Login' });
      }
    //  this is for 3 ** no longer need.
    else if(to.matched.some(record => record.meta.apiException==false)&&store.state.signup.apiError.any){
      next({ name: 'ConnectionError' });
      }
    //   this is for 4 next will be change to new not found im gonna make later
    else if(to.matched.some(record => record.meta.emailVerified)&&!store.state.signup.emailVerified&&store.state.signup.registeredUser){
    next({ name: 'NotFound' });
    }
    // this is for 5 next will be chainge to new not found im gonna male later
    else if(to.matched.some(record => record.meta.compUser)&&store.state.signup.emailVerified){
        next({ name: 'NotFound' });
    }
    else if(to.matched.some(record => record.meta.isStaff)){
      if(!store.state.signup.user) {
        next({ name: 'NotFound' });
      } else if(store.state.signup.user.is_staff==false) {
        next({ name: 'NotFound' });
      } else {
        next()
      }

  } else if(to.name=='BoardDetail') {
    console.log("DETAIL", to)
    const slug = to.params.slug
    await getUserFavoriteQuestions(store.state.signup.user)
    await getDetail(slug)
    next()
  }
    else if(store.state.signup.user) {
      if(to.name=='Account'||to.name=='QuizTest'){
        await getQuizTaker()
      } else if(to.name=='MyQuiz') {
        console.log("MY_QUIZ_ROUTE")
        await getMyQuiz(store.state.signup.user.UID)
        await getQuizTaker()
      } else if(to.name=='BoardAccount') {
          await getUserTag(store.state.signup.user.UID)
          await getUserFavoriteQuestions()
          await getAnsweredQuestions()
      } 
    console.log("gonna NEXT")
    next()
  } else {
    next()
  }
})

export default router
